import jenkins
import pymongo
import requests
import yaml

class SaltAPI(object):
    def __init__(self, url, username=None, password=None, eauth='pam'):
        if url[-1] == '/':
            self.__url = url
        else:
            self.__url = url + '/'
        if username is not None and password is not None:
            self.auth = self._login(username, password, eauth)
        else:
            self.auth = None

    def _login(self, username, password, eauth):
        param = {'username':username, 'password':password, 'eauth':eauth}
        url = self.__url + 'login'
        r = requests.post(url, data=param)
        token = r.json()['return'][0]['token']
        return token
 
    def _post_request(self, obj, prifix='/'):
        headers = {'Accept':'application/x-yaml', 'X-Auth-Token':self.auth}
        url = self.__url + prifix
        r = requests.post(url, data=obj, headers=headers)
        return r
 
    def salt_cmd(self, params):
        result = self._post_request(params)
        return result

def Serjenkins(app):
    url = app.config['JENKINS_URL']
    user = app.config['JENKINS_USERNAME']
    passwd = app.config['JENKINS_PASSWD']
    rv = jenkins.Jenkins(url, user, passwd)
    return rv

def SersaltAPI(app):   
    url = app.config['SALTAPI_URL']
    user = app.config['SALTAPI_USERNAME']
    passwd = app.config['SALTAPI__PASSWD']
    #rv = saltapi.SaltAPI(url, user, passwd)
    rv = SaltAPI(url, user, passwd)
    return rv

def Mongodb(app):
    client = pymongo.MongoClient('localhost', 27017)
    #client = pymongo.Connection('localhost',27017)
    rv = client.job_info
    return rv


def file_to_dict(file):
    dic = {}
    d = dic

    with open(file) as f:
        lines = f.readlines()

    for line in lines:
        path = line.split('\t')[0]
        ip = path.split('/')[-3:-2][0]
        d = dic
        for key in path.split('/')[1:-4]:
            if key in d:
                d = d[key]
                continue
            else:
                d[key] = {}
                d = d[key]
        else:
            key = path.split('/')[-4:-3][0]
            try:
                d[key]
            except:
                d[key] = []
            if ip not in d[key]:
                d[key].append(ip)
    return dic

def dict_to_tree(d,li):
    if isinstance(d,dict):
        for k in d:
            td = {'text':k, 'children':[]}
            #td['state'] = 'closed'
            li.append(td)
            dict_to_tree(d[k],td['children'])
    else:
        for i in d:
            td = {'text':i, 'children':[]}
            li.append(td)
        return 0
