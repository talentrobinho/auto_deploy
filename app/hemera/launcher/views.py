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
from ..logger import *
from .cgi.make_server_info import *
#from flask.ext.cache import Cache

logger = Logger(file="/search/odin/flasky/app/hemera/console/lau.out",name='lau').getlog()
logger.info("log begin...")
#from flask_sse import sse

lau = Blueprint('lau', __name__, template_folder='templates', static_folder='static')
japi = Serjenkins(app)
sapi = SersaltAPI(app)
#db = Mongodb(app)


@lau.route('/online/index', methods=['GET'])
def index_online():
    return render_template('online/index.html')

@lau.route('/admini/index', methods=['GET'])
def admini_index():
    return render_template('admini/index.html')


@lau.route('/backup/back', methods=['POST'])
def backup_back():
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
        r = sapi.salt_cmd(param)
        result = yaml.load(r.text)['return']
        for key,value in result[0].iteritems():
            data = {'message':str({key:value})}
            #sse.publish(data, type='backup_output', channel='backup')    # ִ????Ϣ????
        logger.info("backup %s OK." % data)
        rv = 0
    return jsonify({'result':rv})

@lau.route('/deploy/build', methods=['POST'])
def deploy_build():
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
    data = request.form.get("module_path", "None")
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
            #sse.publish(data, type='backup_output', channel='backup')    # ִ????Ϣ????
        logger.info("backup %s OK." % data)
        rv = 0
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
    return jsonify(get_service_ip(server))



