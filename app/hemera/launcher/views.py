#-*- coding: UTF-8 -*-

import time
import os
import subprocess
import yaml
import json
from flask import Blueprint, render_template, session
from flask import jsonify, abort, make_response, request
from .util import *
from .. import app
<<<<<<< HEAD
'''
    lizhansheng add
'''
=======
from ..logger import *
>>>>>>> upstream/master
from .cgi.make_server_info import *
#from flask.ext.cache import Cache




#from flask_sse import sse

lau = Blueprint('lau', __name__, template_folder='templates', static_folder='static')
japi = Serjenkins(app)
sapi = SersaltAPI(app)
#db = Mongodb(app)


#@lau.route('/admini/getrole', methods=['POST'])
def get_user_role(user):
    '''
        获取用户角色属性

        Args:
            登陆的用户名

        Returns:
            返回所传用户名的权限列表
            {'role': 用户角色}
            0: 表示普通用户
            1: 表示管理员用户

        Raises:
            Null
    '''
    #get_user = request.form.get('user', 'None')
    #user_info = find_privilege(get_user)
    user_info = find_privilege(user)
    return user_info['role']
    


@lau.route('/online/index', methods=['GET'])
def index_online():
    return render_template('online/index.html')

@lau.route('/admini/index', methods=['GET'])
def admini_index():
<<<<<<< HEAD
    """ 权限管理的主页面 """
    user = request.cookies.get('_adtech_user') 
    user_role = get_user_role(user)
    if user_role != 1:
        page = 'admini/no_permissions.html'
    else:
        page = 'admini/index.html'
    return render_template(page)
=======
    return render_template('admini/index.html')
>>>>>>> upstream/master


@lau.route('/backup/back', methods=['POST'])
def backup_back():
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
<<<<<<< HEAD
        #r = sapi.salt_cmd(param)
        #result = yaml.load(r.text)['return']
        #for key,value in result[0].iteritems():
        #    data = {'message':str({key:value})}
        #    #sse.publish(data, type='backup_output', channel='backup')    # Ö´ÐÐÐÅÏ¢Êä³ö
=======
        r = sapi.salt_cmd(param)
        result = yaml.load(r.text)['return']
        for key,value in result[0].iteritems():
            data = {'message':str({key:value})}
            #sse.publish(data, type='backup_output', channel='backup')    # ִ????Ϣ????
        logger.info("backup %s OK." % data)
>>>>>>> upstream/master
        rv = 0
    return jsonify({'result':rv})

@lau.route('/deploy/build', methods=['POST'])
def deploy_build():
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
    data = request.form.get("module_path", "None")
    print "--------****************---------"
    print data
    tgt = data + '*'
    arg = None
    #TODO arg = session['module_path']    # ??û??·??A
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
<<<<<<< HEAD
            #sse.publish(data, type='rollback_output', channel='rollback')
        rv = 'rollback ok'
=======
            #sse.publish(data, type='backup_output', channel='backup')    # ִ????Ϣ????
        logger.info("backup %s OK." % data)
        rv = 0
>>>>>>> upstream/master
    return jsonify({'result':rv})


@lau.route('/log', methods=['GET'])
def log():
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




#cache = Cache()
#config = {
#  'CACHE_TYPE': app.config['CACHE_TYPE'],
#  'CACHE_REDIS_HOST': app.config['CACHE_REDIS_HOST'],
#  'CACHE_REDIS_PORT': app.config['CACHE_REDIS_PORT'],
#  'CACHE_REDIS_DB': app.config['CACHE_REDIS_DB'],
#  'CACHE_REDIS_PASSWORD': app.config['CACHE_REDIS_PASSWORD']
#}

#@csrf_exempt
@lau.route('/tree/getsidebar', methods=['GET'])
def sidebar_content():
    root=[]
    tmp_root=[]
    fa=[]
    tmp={}
    deal_list=[]
    sidebar_list=get_service_info()
<<<<<<< HEAD
=======
    ##logger.info( type(sidebar_list)
>>>>>>> upstream/master
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
    #return HttpResponse(json.dumps(rr_info), content_type='application/json')
    return jsonify(rr_info)

@lau.route('/api/getip', methods=['GET'])
def get_ip():
    tmp_dict = {}
    if request.method == "GET":
        #server = request.GET['server']
        server = request.args.get('server')
<<<<<<< HEAD
    return jsonify(get_service_ip(server))

class RedisOp(object):
    '''
         创建Redis链接类
    '''
    def __init__(self, host, port, db):
        self.redis_host = host
        self.redis_port = port
        self.redis_db = db

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
            redis_obj = redis.Redis(host = self.redis_host, port = self.redis_port, db = self.redis_db)
        except:
            pass

        return redis_obj

'''
    创建上线服务锁缓存的redis实例
'''
redis_inst = RedisOp(host = app.config['CACHE_REDIS_HOST'], port = app.config['CACHE_REDIS_PORT'], db = app.config['CACHE_REDIS_DB'])
redis_cache = redis_inst.redis_conn()
'''
    创建用户权限的redis实例
'''
redis_privilege_inst = RedisOp(host = app.config['PRIVILEGES_REDIS_HOST'], port = app.config['PRIVILEGES_REDIS_PORT'], db = app.config['PRIVILEGES_REDIS_DB'])
redis_privilege = redis_privilege_inst.redis_conn()

def is_book(user, server):
    '''
        判断用户要上线的服务模块是否已经预订
    
        Args:
            user: 要上线的用户的用户名
            server: 用户选中的要上线的服务模块名
    
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




def find_privilege(user):
    '''
        从Redis数据库1中查找用户权限信息

        Args:
            user: 要查找权限的用户名

        Returns:
            {'own': 拥有的权限服务的列表, 'out': 没有权限服务的列表, 'role': 用户角色}
            服务列表是以逗号分隔的字符串
            0: 表示普通用户
            1：表示管理员用户，可以给普通用户分配权限

        Raises:
            Null
    '''
    deal_server_list=[]
    privilege_list = redis_privilege.get("%s"%(user,))
    if not privilege_list:
        privilege_list=[]
        all_server_list=get_service_info()
        for line in all_server_list:
            if line:
                line_tmp = line.strip('/').split('/')
                line_list = line_tmp[:-2]
                if line_list in deal_server_list:
                    continue
                server_str="_".join(line_list)
                deal_server_list.append(line_list)
                privilege_list.append(server_str)
        privileges = {'own':'None', 'out':",".join(privilege_list), 'role': 0}
    else:
        privileges = privilege_list
    return privileges
"""    
@lau.route('/admini/getprivilege', methods=['POST'])
def set_privileges():
    '''
        设置用户权限

        Args:
            user:
            own_privilege:
            out_privilege:
            role:

        Returns:
            {'resutl': 状态码}
            0: 表示保存权限成功
            1: 表示保存失败

        Raises:
            Null
    '''
    set_user = request.form.get('user', 'None')
    own_privilege = request.form.get('own', 'None')
    out_privilege = request.form.get('out', 'None')

    set_status = save_privilege(set_user, own_privilege, out_privilege)
    if set_status == 0:
        result = {'resutl': 0}
    else:
        result = {'resutl': 1}

    return jsonify(result)
"""

@lau.route('/admini/getprivilege', methods=['POST'])
def get_privileges():
    '''
        获取用户权限列表

        Args:
            登陆的用户名

        Returns:
            返回所传用户名的权限列表
            {'own': 拥有的权限服务的列表, 'out': 没有权限服务的列表}
            服务列表是以逗号分隔的字符串

        Raises:
            Null
    '''
    get_user = request.form.get('user', 'None')
    privi_list = find_privilege(get_user)

    return jsonify(privi_list)
'''
    ##########################################################################
                            lizhansheng add end
    ##########################################################################
'''
=======
    #logger.info( server
    #tmp_dict['ip'] = get_service_ip(server)
    #logger.info( tmp_dict
    #return HttpResponse(json.dumps(get_service_ip(server)), content_type='application/json')
    return jsonify(get_service_ip(server))


>>>>>>> upstream/master

'''你好'''
