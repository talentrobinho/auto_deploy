#-*- coding: UTF-8 -*-

import time
import os
import subprocess
import yaml
import json
from flask import Blueprint, render_template, session, Flask
from flask import jsonify, abort, make_response, request
from .util import *
from .. import app
'''
    lizhansheng add
'''
from .cgi.make_server_info import *
from flask_cache import Cache
from flask_wtf.csrf import CsrfProtect
import redis
'''
    redis
'''

config = {
  'CACHE_TYPE': app.config['CACHE_TYPE'],
  'CACHE_REDIS_HOST': app.config['CACHE_REDIS_HOST'],
  'CACHE_REDIS_PORT': app.config['CACHE_REDIS_PORT'],
  'CACHE_REDIS_DB': app.config['CACHE_REDIS_DB'],
  'CACHE_REDIS_PASSWORD': app.config['CACHE_REDIS_PASSWORD']
}
cache = Cache()
cache = cache.init_app(app, config=config)

'''
    lizhansheng add end
'''




#from flask_sse import sse

lau = Blueprint('lau', __name__, template_folder='templates', static_folder='static')
japi = Serjenkins(app)
sapi = SersaltAPI(app)
#db = Mongodb(app)

'''
    lizhansheng 
'''

@lau.route('/online/index', methods=['GET'])
#@cache(timeout = 300)
def index_online():
    """ 主页面 """
    return render_template('online/index.html')

@lau.route('/admini/index', methods=['GET'])
def admini_index():
    """ 主页面 """
    return render_template('admini/index.html')

'''
    lizhansheng  end
'''

@lau.route('/backup/back', methods=['POST'])
def backup_back():
    """ 用于页面备份按钮调用 """
    data = request.form.get("module_path", "None")
    tgt = data + '*'
    param = {
            'client':'local',
            'tgt':tgt,
            'fun':'network.ipaddrs',
            'arg':'eth0',
            'expr_form':'glob'
            }
    if param['tgt'] == '*':
        rv = 'PAEAM: tgt is *.'
    else:
        #r = sapi.salt_cmd(param)
        #result = yaml.load(r.text)['return']
        #for key,value in result[0].iteritems():
        #    data = {'message':str({key:value})}
        #    #sse.publish(data, type='backup_output', channel='backup')    # 执行信息输出
        rv = 0
    return jsonify({'result':rv})

@lau.route('/deploy/build', methods=['POST'])
def deploy_build():
    """ jenkins job 远程构建，用于页面触发job构建按钮调用 """
    data = request.form.get("module_path", "None")
    job = data
    try:
        next_build_number = japi.get_job_info(job)['nextBuildNumber']
    except:
        rv = "ERROR: job is not existed."
    else:
        session['build_number'] = next_build_number
        try:
            japi.build_job(job)
        except:
            rv = "ERROR: job builded error."
        else:
            flag = True
            while flag:
                time.sleep(5)
                try:
                    japi.get_build_info(job, next_build_number)
                except:
                    flag = True
                else:
                    flag = japi.get_build_info(job, next_build_number)['building']
            result = japi.get_build_info(job, next_build_number)
            rv = result['result']
    finally:
        return jsonify(rv)

@lau.route('/deploy/launch', methods=['POST'])
def deploy_launch():
    """ salt 文件分发部署，用于页面触发上线按钮调用 """
    data = request.form.get("module_path", "None")
    print "--------****************---------"
    print data
    tgt = data + '*'
    arg = None
    #TODO arg = session['module_path']    # 有没有路标A
    param = {
            'client':'local',
            'tgt':tgt,
            #TODO 'fun':'pkg.install',
            'fun':'test.ping',
            #TODO 'arg':arg
            }
    if param['tgt'] == '*':
        rv = 'PAEAM: tgt is *.'
    else:
        r = sapi.salt_cmd(param)
        rv = yaml.load(r.text)['return']
    return jsonify(rv)

@lau.route('/rollback/roll', methods=['POST'])
def rollback_roll():
    """ 用于页面回滚按钮调用 """
    data = request.form.get("module_path", "None")
    tgt = data + '*'
    param = {
            'client':'local',
            'tgt':tgt,
            'fun':'network.ipaddrs',
            'arg':'eth0',
            'expr_form':'glob'
            }
    if param['tgt'] == '*':
        rv = 'PAEAM: tgt is *.'
    else:
        r = sapi.salt_cmd(param)
        result = yaml.load(r.text)['return']
        for key,value in result[0].iteritems():
            data = {'message':str({key:value})}
            #sse.publish(data, type='rollback_output', channel='rollback')
        rv = 'rollback ok'
    return jsonify({'result':rv})


@lau.route('/log', methods=['GET'])
def log():
    """ 日志记录及审计 """
    t_list = []
    module = session['module_path']
    info = db.build_info.find({"Name" : module})
    for item in info.sort('BuildNo',pymongo.DESCENDING):
        t_list.append(item)
        if len(t_list) > 10:
            #TODO display to next html
            break
    return render_template('log.html', list=t_list)


############################################    api    ###########################################

@lau.route('/api/ip/<module>', methods=['GET'])
def get_module_ip(module):
    tgt = module + '*'
    param = {
            'client':'local',
            'tgt':tgt,
            'fun':'network.ipaddrs',
            'arg':'eth0',
            'expr_form':'glob'
            }
    r = sapi.salt_cmd(param)
    result = yaml.load(r.text)['return']
    t_list = []
    for ip in result[0].itervalues():
        t_list.append(ip)
    rv = t_list
    return jsonify(rv)

@lau.route('/api/salt/cmd', methods=['GET', 'POST'])
def exe_cmd():
    if request.method == 'POST':
        param = {
                'client':'local',
                'tgt': request.form['tgt'],
                'fun': request.form['cmd'],
                'arg': request.form['arg'],
                'expr_form': request.form['expr_form']
                }
        if param['arg'] == 'None':
            del param['arg']
        r = sapi.salt_cmd(param)
        rv = yaml.load(r.text)['return']
        return jsonify(rv)
    return render_template('cmd.html')

@lau.route('/api/job/info/<module_path>', methods=['GET'])
def get_job_info(module_path):
    module = module_path
    job_info = japi.get_job_info(module)
    return jsonify(job_info)

@lau.route('/api/build/info/<module_path>', methods=['GET'])
def get_build_info(module_path):
    module = module_path
    build_number = 20
    #TODO build_number = session['build_number']
    build_info = japi.get_build_info(module, build_number)
    return jsonify(build_info)

##################################################################

@lau.route('/deploy/machine')
def machine():
    return render_template('machine.html')

@lau.route('/deploy/ip')
def ip():
    ip = [
            "10.142.82.202",
            "10.142.93.223",
            "10.134.108.152"
         ]
    return render_template('ip.html', ip_list=ip)



'''
    ##########################################################################
                            lizhansheng add
    ##########################################################################
'''
csrf = CsrfProtect()
@csrf.exempt
@lau.route('/tree/getsidebar', methods=['GET'])
def sidebar_content():
    root=[]
    tmp_root=[]
    fa=[]
    tmp={}
    deal_list=[]
    sidebar_list=get_service_info()
    ##print type(sidebar_list)
    for line in sidebar_list:
        if line:
            line_tmp = line.strip('/').split('/')
            line_list = line_tmp[:-2]
            if line_list in deal_list:
                continue
            deal_list.append(line_list)
            tmp_root = Make_Tree_Json(tmp_root, line_list)
    ##return HttpResponse(json.dumps(tmp_root), content_type='application/json')
    return jsonify(tmp_root)

################################################################
###         make select of route and ring json data          ###
################################################################
@lau.route('/tree/getrr', methods=['GET'])
def rr_list():
    service_info=get_service_info()
    rr_info = route_map_ring(service_info)
    return jsonify(rr_info)

@lau.route('/api/getip', methods=['GET'])
def get_ip():
    """
        Explain:
            靠request.POST['server']靠� IP 靠
        Render:
            靠 IP 縅SON 靠
            {'ip': '1.1.1.1 2.2.2.2'}
    """
    tmp_dict = {}
    if request.method == "GET":
        server = request.args.get('server')
    return jsonify(get_service_ip(server))

class RedisOp(object):
    def __init__(self, host, port=6739):
        self.redis_host = host
        self.redis_port = port

    def redis_conn(self):
        try:
            redis_obj = redis.Redis(host = self.redis_host, port = self.redis_port)
        except:
            pass

        return redis_obj


redis_inst = RedisOp(host = app.config['CACHE_REDIS_HOST'], port = app.config['CACHE_REDIS_PORT'])
redis_cache = redis_inst.redis_conn()

def is_book(user, server, check_type='user'):
    #redis_cache = redis.Redis(host = app.config['CACHE_REDIS_HOST'], port = app.config['CACHE_REDIS_PORT'])
    check_status = {}
    if check_type == 'user':
        lock_info_list=redis_cache.get("xx%s"%user)
        if not lock_info_list:
            lock_info_list = []
            lock_info_list.append(server)
            redis_cache.set("%s"%user, lock_info_list, ex=app.config['CACHE_REDIS_TIMEOUT'])
            redis_cache.set("%s"%server, user, ex=app.config['CACHE_REDIS_TIMEOUT'])
            check_status['status'] = 0
        else:
            lock_info_list = eval(lock_info_list)
            if server in lock_info_list:
                #status = 1
                check_status['status'] = 1
            else:
                lock_info_list.append(server)
                redis_cache.set("%s"%user, lock_info_list, ex=app.config['CACHE_REDIS_TIMEOUT'])
                check_status['status'] = 0

    elif check_type == 'server':
        lock_info_list=redis_cache.get("%s"%server)
        if not lock_info_list:
            #redis_cache.set("xx%s"%user, lock_info_list, ex=app.config['CACHE_REDIS_TIMEOUT'])
            check_status['status'] = 0
        else:
            #lock_info_list = eval(lock_info_list)
            check_status['status'] = 2
            check_status['info'] = lock_info_list

    
    return check_status



@lau.route('/online/lock', methods=['POST'])
def lock_online():
    '''
        靠靠靠
    '''
    #response.set_cookie('Name','Hyman')
    op_user = request.cookies.get('_adtech_user') 
    op_server = request.form.get('module_path', 'None') 
    server_status = is_book(op_user, op_server, check_type="server")
    print "=============== check server ================="
    print server_status
    if server_status['status'] == 2:
        result = {'result': server_status['status'], 'result_info':server_status['info']}
    else:
        user_status = is_book(op_user, op_server, check_type="user")
        print "=============== check user ================="
        print user_status
        result = {'result': user_status['status']}

    print "*"*50
    return jsonify(result)
    
    
'''
    ##########################################################################
                            lizhansheng add end
    ##########################################################################
'''
