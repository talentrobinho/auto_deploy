#-*- coding: UTF-8 -*-

import time
import os
import subprocess
import yaml
from flask import Blueprint, render_template, session
from flask import jsonify, abort, make_response, request
from .util import *
from .. import app

from flask_sse import sse

lau = Blueprint('lau', __name__, template_folder='templates', static_folder='static')
japi = Serjenkins(app)
sapi = SersaltAPI(app)
db = Mongodb(app)


@lau.route('/', methods=['GET'])
def index_route():
    """ 主页面 """
    return render_template('base.html')

@lau.route('/backup/back', methods=['GET'])
def backup_back():
    """ 用于页面备份按钮调用 """
    tgt = session['module_path'] + '*'
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
            sse.publish(data, type='backup_output', channel='backup')    # 执行信息输出
        rv = 'backup ok'
    return jsonify({'result':rv})

@lau.route('/deploy/build', methods=['GET'])
def deploy_build():
    """ jenkins job 远程构建，用于页面触发job构建按钮调用 """
    job = session['module_path']
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

@lau.route('/deploy/launch', methods=['GET'])
def deploy_launch():
    """ salt 文件分发部署，用于页面触发上线按钮调用 """
    tgt = session['module_path'] + '*'
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

@lau.route('/rollback/roll', methods=['GET'])
def rollback_roll():
    """ 用于页面回滚按钮调用 """
    tgt = session['module_path'] + '*'
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
            sse.publish(data, type='rollback_output', channel='rollback')
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

@lau.route('/api/node/<text>', methods=['GET'])
def get_node(text):
    #TODO session['module_path'] = text
    session['module_path'] = 'adtech_Wireless_Union_WWW'
    rv = session['module_path']
    return jsonify(rv)

@lau.route('/api/ip/<module>')
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

@lau.route('/api/job/info', methods=['GET'])
def get_job_info():
    module = session['module_path']
    job_info = japi.get_job_info(module)
    return jsonify(job_info)

@lau.route('/api/build/info', methods=['GET'])
def get_build_info():
    module = session['module_path']
    build_number = 20
    #TODO build_number = session['build_number']
    build_info = japi.get_build_info(module, build_number)
    return jsonify(build_info)

@lau.route('/api/tree/modules', methods=['GET'])
def get_modules():
    pass

@lau.route('/api/tree/modules', methods=['POST'])
def add_modules():
    pass

@lau.route('/api/tree/node', methods=['GET'])
def tree_node():
    li = []
    file = '/search/odin/flasky/app/hemera/launcher/api_ip'
    dic = file_to_dict(file)
    dict_to_tree(dic,li)
    return jsonify(li)

@lau.route('/api/tree/dict', methods=['GET'])
def tree_dict():
    dic = {}
    tmp = dic
    with open('/search/odin/flasky/app/hemera/launcher/api_ip') as f:
        lines = f.readlines()
    for line in lines:
        path = line.split('\t')[0]
        ip = line.split('\t')[1].strip()
        dic = tmp
        for key in path.split('/')[1:-1]:
            if key in dic:
                dic = dic[key]
                continue
            else:
                dic[key] = {}
                dic = dic[key]
        else:
            key = path.split('/')[-1:][0]
            try:
                dic[key]
            except:
                dic[key] = []
            dic[key].append(ip)
    return jsonify(tmp)



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
