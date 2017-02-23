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
from ..logger import *
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

logger = Logger(file="/search/odin/flasky/log.out",name='lau').getlog()

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
    """ 上线的主页面 """
    return render_template('online/index.html')

@lau.route('/admini/index', methods=['GET'])
def admini_index():
    """ 权限管理的主页面 """
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
            #TODO 'fun':'cmd.script',
            'fun':'network.ipaddrs',
            #TODO 'arg':'salt://scripts/backup.sh',
            'arg':'eth0',
            'expr_form':'glob'
            }
    if param['tgt'] == 'None*':
        logger.error("request get module_path error.")
        rv = 1
    else:
<<<<<<< HEAD
        r = sapi.salt_cmd(param)
        result = yaml.load(r.text)['return']
        for key,value in result[0].iteritems():
            data = {'message':str({key:value})}
            #sse.publish(data, type='backup_output', channel='backup')    # ִ����Ϣ���
        logger.info("backup %s OK." % data)
=======
        #r = sapi.salt_cmd(param)
        #result = yaml.load(r.text)['return']
        #for key,value in result[0].iteritems():
        #    data = {'message':str({key:value})}
        #    #sse.publish(data, type='backup_output', channel='backup')    # Ö´ÐÐÐÅÏ¢Êä³ö
>>>>>>> e5c6a0587ca65075e0149b993b70be12717ed99d
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
        logger.warn("job is not existed.")
        rv = 1
    else:
        session['build_number'] = next_build_number
        try:
            japi.build_job(job)
        except:
            logger.error("job builded error.")
            rv = 1
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
            logger.info("job has been builded and result is %s" % result['result'])
            if result['result'] == 'SUCCESS':
                rv = 0
            else:
                rv = 1
    finally:
        return jsonify({'result':rv})

@lau.route('/deploy/launch', methods=['POST'])
def deploy_launch():
    """ salt 文件分发部署，用于页面触发上线按钮调用 """
    data = request.form.get("module_path", "None")
    tgt = data + '*'
    arg = None
    #TODO arg = session['module_path']    # ÓÐÃ»ÓÐÂ·±êA
    param = {
            'client':'local',
            'tgt':tgt,
            #TODO 'fun':'pkg.install',
            'fun':'test.ping',
            #TODO 'arg':arg
            }
    if param['tgt'] == 'None*':
        logger.error("request get module_path error.")
        rv = 1
    else:
        r = sapi.salt_cmd(param)
        result = yaml.load(r.text)['return']
        logger.info("launch %s OK." % data)
        rv = 0
    return jsonify({'result':rv})

@lau.route('/rollback/roll', methods=['POST'])
def rollback_roll():
    """ 用于页面回滚按钮调用 """
    data = request.form.get("module_path", "None")
    tgt = data + '*'
    param = {
            'client':'local',
            'tgt':tgt,
            #TODO 'fun':'cmd.script',
            'fun':'network.ipaddrs',
            #TODO 'arg':'salt://scripts/rollback.sh',
            'arg':'eth0',
            'expr_form':'glob'
            }
    if param['tgt'] == 'None*':
        logger.error("request get module_path error.")
        rv = 1
    else:
        r = sapi.salt_cmd(param)
        result = yaml.load(r.text)['return']
        for key,value in result[0].iteritems():
            data = {'message':str({key:value})}
            #sse.publish(data, type='backup_output', channel='backup')    # ִ����Ϣ���
        logger.info("backup %s OK." % data)
        rv = 0
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
    '''
        生成服务树形列表
        Returns：
            返回树形列表json数据
    '''
    root=[]
    tmp_root=[]
    fa=[]
    tmp={}
    deal_list=[]
    sidebar_list=get_service_info()
<<<<<<< HEAD
    ##logger.info( type(sidebar_list)
=======
>>>>>>> e5c6a0587ca65075e0149b993b70be12717ed99d
    for line in sidebar_list:
        if line:
            line_tmp = line.strip('/').split('/')
            line_list = line_tmp[:-2]
            if line_list in deal_list:
                continue
            deal_list.append(line_list)
            tmp_root = Make_Tree_Json(tmp_root, line_list)
    return jsonify(tmp_root)

@lau.route('/tree/getrr', methods=['GET'])
def rr_list():
    '''
        生成路和环下拉列表的json数据

        Args:
            Null
        Returns:
            返回数据格式如下：
                [
                  {
                    "children": [
                      {
                        "children": [
                          "ring0", 
                          "ring1"
                        ], 
                        "content": "A"
                      }, 
                      {
                        "children": [
                          "ring0", 
                          "ring1"
                        ], 
                        "content": "B"
                      }]
                  }
                ]
        Raises:
            Null
    '''
    service_info=get_service_info()
    rr_info = route_map_ring(service_info)
    return jsonify(rr_info)

@lau.route('/api/getip', methods=['GET'])
def get_ip():
    """
        从凯撒接口获取用户选中的服务的IP列表
        Returns:
            返回用户选中服务的IP列表json数据，格式如下：
            {'ip': '1.1.1.1 2.2.2.2'}
    """
    tmp_dict = {}
    if request.method == "GET":
        server = request.args.get('server')
<<<<<<< HEAD
    #logger.info( server
    #tmp_dict['ip'] = get_service_ip(server)
    #logger.info( tmp_dict
    #return HttpResponse(json.dumps(get_service_ip(server)), content_type='application/json')
=======
>>>>>>> e5c6a0587ca65075e0149b993b70be12717ed99d
    return jsonify(get_service_ip(server))

class RedisOp(object):
    '''
         创建Redis链接类
    '''
    def __init__(self, host, port=6739):
        self.redis_host = host
        self.redis_port = port

    def redis_conn(self):
        '''
            创建Redis链接对象

            Args:
                Null

            Returns:
                返回redis链接对象

            Raises:
                Null
        '''
        try:
            redis_obj = redis.Redis(host = self.redis_host, port = self.redis_port)
        except:
            pass

        return redis_obj


redis_inst = RedisOp(host = app.config['CACHE_REDIS_HOST'], port = app.config['CACHE_REDIS_PORT'])
redis_cache = redis_inst.redis_conn()

def is_book(user, server):
    '''
        判断用户要上线的服务模块是否已经预订
    
        Args:
            user: 要上线的用户的用户名
            server: 用户选中的要上线的服务模块名
    
        Returns:
            check_book['status'] = value (value列表如下)                                                                                                                                                        
        Returns:
            check_book['status'] = value (value列表如下)
            0: 表示该用户没有任何预订信息
            1: 表示该用户已经预订这个服务
            2: 表示该用户有预订的上线服务，但没有预订这个服务
               当状态值为2时，会同时返回已预订服务列表，格式如下
               check_book['info'] = book_server_list
    
        Raises:
            Null
    '''
    check_book = {}
    lock_info_list=redis_cache.get("%s"%user)
    if not lock_info_list:
        check_book['status'] = 0
    else:
        lock_info_list = eval(lock_info_list)
        if server in lock_info_list:
            check_book['status'] = 1
        else:
            check_book['status'] = 2
        check_book['info'] = lock_info_list
    return check_book


def book(user, server, check_type='user'):
   
    '''
        Args:
            user: 要上线的用户的用户名
            server: 用户选中的要上线的服务模块名
            check_type: 指定是通过用户，还是服务进行预订的判断
                        只接受2个参数，user(默认值)和server
    
        Returns:
            当check_type == user时，返回值如下
                check_status = {'status': 状态码}
                0: 表示该用户没有预订此服务，并且增加用户预订信息
                1: 表示该用户已经预订
            当check_type == server时，返回值如下
                check_status = {'status': 状态码, 'info': 用户名}
                0: 表示此服务没有用户预订
                1: 表示该用户已经预订
                2：表示此服务已有用户预订，并返回已预订此服务的用户名
    
        Raises:
            Null
    '''
    
    check_status = {}
    book_list = []
    if check_type == 'user':
        check_book = is_book(user, server)
        if check_book['status'] == 1:
            check_status['status'] = 1
        elif check_book['status'] == 0:
            book_list.append(server)
            redis_cache.set("%s"%user, book_list, ex=app.config['CACHE_REDIS_TIMEOUT'])
            redis_cache.set("%s"%server, user, ex=app.config['CACHE_REDIS_TIMEOUT'])
            check_status['status'] = 0
        elif check_book['status'] == 2:
            check_book['info'].append(server)
            redis_cache.set("%s"%user, check_book['info'], ex=app.config['CACHE_REDIS_TIMEOUT'])
            check_status['status'] = 0
            

    elif check_type == 'server':
        lock_info_list=redis_cache.get("%s"%server)
        if not lock_info_list:
            check_status['status'] = 0
        else:
            if lock_info_list == user:
                check_status['status'] = 1
            else:
                check_status['status'] = 2
                check_status['info'] = lock_info_list

    
    return check_status



@lau.route('/online/lock', methods=['POST'])
def lock_online():
    '''
        预订上线接口

        Args:
            user: 登陆的用户名
            module_path: 前端网页选中的服务
    
        Returns:
            result = {'result': 预订状态码, 'result_info': 预订信息}
            0: 表示当前用户预订服务成功
            1: 表示当前用户已经预订了服务
            2: 表示当前用户要预订的服务已经有人预订

        Raises:
            Null
    '''
    op_user = request.cookies.get('_adtech_user') 
    op_server = request.form.get('module_path', 'None') 
    server_status = book(op_user, op_server, check_type="server")
    if server_status['status'] == 2:
        result = {'result': server_status['status'], 'result_info':server_status['info']}
    else:
        user_status = book(op_user, op_server, check_type="user")
        result = {'result': user_status['status']}

    return jsonify(result)
    
@lau.route('/online/checklock', methods=['POST'])
def check_lock():
    '''
        检查用户选定的服务是否已被预订

        Args:
            user: 登陆的用户名
            module_path: 前端网页选中的服务

        Returns:
            0: 表示已经预订
            1: 表示未预订

        Raises:
            Null
    '''
    check_user = request.form.get('user', 'None')
    check_server = request.form.get('module_path', 'None')
    check_status = is_book(check_user, check_server)
    if check_status['status'] == 1:
        result = {'result': 0}
    else:
        result = {'result': 1}
    return jsonify(result)
    
'''
    ##########################################################################
                            lizhansheng add end
    ##########################################################################
'''

