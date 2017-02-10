import time
import os
import subprocess
import yaml
from flask import Blueprint, render_template, session
from flask import jsonify, abort, make_response, request


adm = Blueprint('adm', __name__, template_folder='templates', static_folder='static')

@adm.route('/')
def index():
    return render_template('index.html')
    #return render_template('base.html')


#@lau.route('/backup')
#def backup():
#    return render_template('backup.html')
#
#@lau.route('/api/backup/back')
#def backup_output():
#    #popen = subprocess.Popen(['ping', 'www.baidu.com', '-c', '5'], stdout = subprocess.PIPE)
#    tgt = session['module_text'] + '*'
#    ping_param = {'client':'local', 'tgt':tgt, 'fun':'test.ping', 'expr_form':'glob'}
#    param = {'client':'local', 'tgt':tgt, 'fun':'network.ipaddrs', 'arg':'eth0', 'expr_form':'glob'}
#    #r = sapi.salt_cmd(ping_param)
#    
#    if param['tgt'] == '*':
#        rv = 'PAEAM: tgt or arg is *.'
#    else:
#        try:
#            r = sapi.salt_cmd(ping_param)
#        except:
#            result = "ping error."
#        else:
#            result = yaml.load(r.text)
#        rv = result
#    return jsonify({'result':rv})
##            for item in result['return']:
##            for ip in item.values():
##                data = {'message':'hello'}
##                sse.publish(data, type='backup_output', channel='backup')
##    popen = subprocess.Popen(['sh', '/search/odin/flasky/app/hemera/launcher/scripts/backup.sh', 'was', '10.134.79.161', '2012'], stdout = subprocess.PIPE)
##    while True:
##        next_line = popen.stdout.readline()
##        if next_line == '' and popen.poll() != None:
##            break
##        data = {'message':result}
##        sse.publish(data, type='backup_output', channel='backup')
##    return jsonify({'result':'backup ok'})
#
########################################################################################################################
#
#@lau.route('/deploy')
#def deploy():
#    return render_template('deploy.html')
#
#@lau.route('/deploy/build')
#def build_job():
#    info = {}
#    module = session['module_text']
#    data = 'you are building the job:' + module + '.<br />'
#    sse.publish({'message':data}, type='deploy_output', channel='deploy')
#    try:
#        next_build_number = japi.get_job_info(module)['nextBuildNumber']
#    except:
#        rv = "No module job"
#    else:
#        session['build_number'] = next_build_number
#        try:
#            japi.build_job(module)
#        except:
#            rv = "Build job error"
#        else:
#            flag = True
#            while flag:
#                time.sleep(5)
#                try:
#                    japi.get_build_info(module, next_build_number)
#                except:
#                    flag = True
#                else:
#                    flag = japi.get_build_info(module, next_build_number)['building']
#            result = japi.get_build_info(module, next_build_number)
#            info['Name'] = result['fullDisplayName'].split(' ')[0]
#            info['Status'] = result['result']
#            info['Time'] = result['timestamp']/1000
#            info['BuildNo'] = result['displayName']
#            db.build_info.insert(info)
#            data = 'the job is already builded, and the result is:' + result['result'] + '.<br />'
#            sse.publish({'message':data}, type='deploy_output', channel='deploy')
#            rv = result['result']
#    finally:
#        return jsonify({'result':rv})
#
#@lau.route('/deploy/launch')
#def launch_job():
#    tgt = session['route_target']
#    arg = session['module_text']
#    param = {'client':'local', 'tgt':tgt, 'fun':'pkg.install', 'arg':arg}
#    cmd = {'client':'local', 'tgt':tgt, 'fun':'test.ping'}
#    if param['tgt'] is None or param['arg'] is None:
#        rv = 'PAEAM: tgt or arg is None.'
#    else:
#        r = sapi.salt_cmd(cmd)
#        #r = sapi.salt_cmd(param)
#        #result = yaml.load(r.text)['return']
#        rv = yaml.load(r.text)['return']
#    return jsonify({'result':rv})
#
#@lau.route('/deploy/machine')
#def machine():
#    return render_template('machine.html')
#
#@lau.route('/deploy/ip/<text>', methods=['GET'])
#def display_ip(text):
#    li = []
#    session['route_target'] = session['module_target'] + '_' + text + '*'
#    tgt = session['route_target']
#    param = {'client':'local', 'tgt':tgt, 'fun':'network.ipaddrs', 'arg':'eth0', 'expr_form':'glob'}
#
#    if param['tgt'] == '*':
#        rv = 'PAEAM: tgt or arg is *.'
#    else:
#        r = sapi.salt_cmd(param)
#        result = yaml.load(r.text)
#        for item in result['return']:
#            for ip in item.values():
#                li.append(ip[0])
#        rv = li
#
#    return render_template('ip.html', ip_list=rv)
#
########################################################################################################################
#
#@lau.route('/rollback')
#def rollback():
#    return render_template('rollback.html')
#
#@lau.route('/rollback/output')
#def rollback_output():
#    popen = subprocess.Popen(['ping', 'www.baidu.com', '-c', '5'], stdout = subprocess.PIPE)
#    while True:
#        next_line = popen.stdout.readline()
#        if next_line == '' and popen.poll() != None:
#            break
#        data = {'message':next_line}
#        sse.publish(data, type='rollback_output', channel='rollback')
#    return jsonify({'result':'rollback ok'})
#
########################################################################################################################
#
#@lau.route('/log')
#def log():
#    li = []
#    module = session['module_text']
#    info = db.build_info.find({"Name" : module})
#    #info = db.build_info.find({'Name': 'Adtech_MB-union_was'})
#    for item in info.sort('BuildNo',pymongo.DESCENDING):
#        li.append(item)
#        if len(li) > 10:
#            break
#    return render_template('log.html', list=li)
#
########################################################################################################################
#
#@lau.route('/database')
#def database():
#    li = []
#    module = session['module_text']
#    info = db.build_info.find({"Name" : module})
#    #info = db.build_info.find({'Name': 'Adtech_MB-union_was'})
#    for item in info.sort('BuildNo',pymongo.DESCENDING):
#        li.append(item)
#        if len(li) > 5:
#            break
#    return render_template('database.html', list=li)
#
#
#############################################    api    ###########################################
#
#@lau.route('/api/salt/cmd', methods=['GET', 'POST'])
#def exe_cmd():
#    if request.method == 'POST':
#        param = {
#                'client':'local',
#                'tgt': request.form['tgt'],
#                'fun': request.form['cmd'],
#                'arg': request.form['arg'],
#                'expr_form': request.form['expr_form']
#                }
#        if param['arg'] == 'None':
#            del param['arg']
#        r = sapi.salt_cmd(param)
#        rv = yaml.load(r.text)
#        return jsonify({'result':rv})
#    return render_template('cmd.html')
#
#@lau.route('/api/tree/modules', methods=['GET'])
#def get_modules():
#    pass
#
#@lau.route('/api/tree/modules', methods=['POST'])
#def add_modules():
#    pass
#
#@lau.route('/api/node/<text>', methods=['GET'])
#def get_node(text):
#    session['module_text'] = text
#    session['module_target'] = text.split('_')[-1]
#    return jsonify({'module_text':text})
#
#
#@lau.route('/api/job/info', methods=['GET'])
#def get_job_info():
#    module = session['module_text']
#    job_info = japi.get_job_info(module)
#    return jsonify(job_info)
#
#@lau.route('/api/build/info', methods=['GET'])
#def get_build_info():
#    module = session['module_text']
#    build_number = 20
#    #build_number = session['build_number']
#    build_info = japi.get_build_info(module, build_number)
#    return jsonify(build_info)
#
#@lau.route('/api/rpm/info', methods=['GET'])
#def get_rmp_info():
#    rpm_list = [os.path.basename(li.strip('\n')) for li in os.popen('ls /tmp/*.rpm').readlines()]
#    return jsonify({'rpm':rpm_list})
#
#@lau.route('/api/tree/node', methods=['GET', 'POST'])
#def tree_node():
#    li = []
#    file = '/search/odin/flasky/app/hemera/launcher/api_ip'
#    dic = file_to_dict(file)
#    dict_to_tree(dic,li)
#    return jsonify(li)
#
#
#@lau.route('/api/tree/dict', methods=['GET', 'POST'])
#def tree_dict():
#    dic = {}
#    tmp = dic
#
#    with open('/search/odin/flasky/app/hemera/launcher/api_ip') as f:
#        lines = f.readlines()
#
#    for line in lines:
#        path = line.split('\t')[0]
#        ip = line.split('\t')[1].strip()
#        dic = tmp
#        for key in path.split('/')[1:-1]:
#            if key in dic:
#                dic = dic[key]
#                continue
#            else:
#                dic[key] = {}
#                dic = dic[key]
#        else:
#            key = path.split('/')[-1:][0]
#            try:
#                dic[key]
#            except:
#                dic[key] = []
#            dic[key].append(ip)
#    return jsonify(tmp)
#
#
#
#
#
#
#
#
#
#
#
