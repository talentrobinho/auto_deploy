#-*- coding: UTF-8 -*-

import urllib2
import re
import logging

logger = logging.getLogger('test')

"""
    以下是定义的各个cgi函数
"""

def get_service_info():
    """
        Explain: 
            从凯撒获取 Server 信息

        Args: 
            None

        Returns: 
           返回一个列表，列表里是各个服务的信息，如下：
           ["/adtech/Mobile_Search/main/RS/B/ring0", "/adtech/PC_Search/main/Query/B/ring0", "/adtech/PC_Search/main/BiddingServer/A/ring0"]

        Raises:
            HTTPError
    """

    try:
        caesar_list = urllib2.urlopen("http://stat.union.sogou-inc.com/server/GetIpByPath.php?path=/&type=text").read()
    except urllib2.HTTPError as error:
       logger.error(error.code)
       logger.error("Fetch server info fail")

    ip_re = re.compile(r'\t(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
    server_info_list = ip_re.sub("", caesar_list).split("\n")
    return server_info_list 

def get_service_ip(server):
    """
        Explain: 
            从凯撒获取 Server 信息

        Args: 
            None

        Returns: 
           返回一个列表，列表里是各个服务的信息，如下：
           ["/adtech/Mobile_Search/main/RS/B/ring0", "/adtech/PC_Search/main/Query/B/ring0", "/adtech/PC_Search/main/BiddingServer/A/ring0"]

        Raises:
            HTTPError
    """

    try:
        caesar_list = urllib2.urlopen("http://stat.union.sogou-inc.com/server/GetIpByPath.php?path=%s&type=json"%(server,)).read()
    except urllib2.HTTPError as error:
       logger.error(error.code)
       logger.error("Fetch server info fail")

    #print "%s"%caesar_list
    server_info_list= eval(caesar_list)
    #for info in aa:
    #    print "%s" % (info,)
    #    print "%s" % (info['path'].replace("\\", ""),)
    #    print "%s"% (" ".join(info['ips']),)

    #server_info_list = '1.1.1.1'
    return server_info_list 



#def make_tree_json(fa_list, str):
def Make_Tree_Json(fa_list, str):
    """
        Expain:
            将server信息生成 easyUITree 的Json数据

        Args:
            fa_list:
            str:

        Returns:
        Raises:
    """

    IS_FIND = 0
    tmp = {}
    root = fa_list
    father = fa_list
    str_list_uniq = str

    try:
        for i in range(len(str_list_uniq)):
            if not str_list_uniq[i]:
                continue
            if len(father) == 0 and str_list_uniq[i] != str_list_uniq[-1]:
                tmp['text'] = str_list_uniq[i]
                tmp['children'] = []
                father.append(tmp)
                father = father[-1]['children']
                tmp = {}
                continue
            elif i == len(str_list_uniq)-1:
                tmp['text'] = str_list_uniq[i]
                tmp['attributes'] = {}
                father.append(tmp)
                tmp = {}
                continue
            else:
                for j in range(len(father)):
                    if str_list_uniq[i] == father[j]['text']:
                        father = father[j]['children']
                        IS_FIND = 1
                        break
                    else:
                        IS_FIND = 0
                if IS_FIND == 1:
                    continue

            tmp['text'] = str_list_uniq[i]
            tmp['children'] = []
            tmp['state'] = 'closed'
            father.append(tmp)
            father = father[-1]['children']
            tmp = {}
    except Exceptions as error:
        logger.error(error)

    return root


def route_map_ring(service_info):
    """
        Expain:
            生成 Route 和 Ring 的对应关系

        Args:
            server_info: 接收服务信息列表
            格式如: ["/adtech/Mobile_Search/main/RS/B/ring0", "/adtech/PC_Search/main/Query/B/ring0", "/adtech/PC_Search/main/BiddingServer/A/ring0"]

        Returns:
            返回route和ring的对应关系列表
            格式如：[{
                        'content':'adtech_PC_Search_main_BiddingServer', 
                        'children':[
                                        {
                                            'content':'A', 
                                            'children':['ring0', 'ring1']
                                        }, 
                                        {
                                            'content':'B', 
                                            'children':['ring0', 'ring1']
                                        }
                                    ]
                     },
                     {
                        'content':'adtech_PC_Search_main_Query', 
                        'children':[
                                        {
                                            'content':'A', 
                                            'children':['ring0', 'ring1']
                                        }, 
                                        {
                                            'content':'B', 
                                            'children':['ring0', 'ring1']
                                        }
                                    ]
                     }]
        Raises:
    """
    join_str='_'
    tmp_dict={}
    route_info=[]
    ring_list=[]
    server_route_ring_relation_list=[]
    deal_list=[]
    count=1
    route_count=1
    for line in service_info:
        if line and line not in deal_list:
            deal_list.append(line)
            service_rr=line.strip('/').split('/')
            service=service_rr[:-2]
            route=service_rr[-2]
            ring=service_rr[-1]
            service_str=join_str.join(service)
            if len(server_route_ring_relation_list) == 0:
                ring_list.append(ring)
                tmp_dict['content']=service_str
                tmp_dict['children']=[{'content':route,'children':ring_list}]
                server_route_ring_relation_list.append(tmp_dict)
                tmp_dict={}
                ring_list=[]
                continue
            for service_dict in server_route_ring_relation_list:
                if service_str != service_dict['content'] and count != len(server_route_ring_relation_list):
                    count+=1
                    continue
                if service_str == service_dict['content']:
                    for route_dict in service_dict['children']:
                        if route != route_dict['content'] and route_count != len(service_dict['children']):
                            route_count+=1
                            continue
                        if route == route_dict['content']:
                            route_dict['children'].append(ring)
                            route_count=1
                            break
                        else:
                            tmp_dict['content']=route
                            ring_list.append(ring)
                            tmp_dict['children']=ring_list
                            service_dict['children'].append(tmp_dict)
                            tmp_dict={}
                            ring_list=[]
                            route_count=1
                            break
                    count=1
                    break
                else:
                    ring_list.append(ring)
                    tmp_dict['content']=service_str
                    tmp_dict['children']=[{'content':route,'children':ring_list}]
                    server_route_ring_relation_list.append(tmp_dict)
                    tmp_dict={}
                    ring_list=[]
                    count=1
                    break
    return server_route_ring_relation_list
