#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import time
import django
django.setup()
#import logging

from app.models import *
from django.conf import settings
from subprocess import Popen,PIPE

 
from django.db import transaction
import datetime
from django.utils import timezone

from app.tasks import *
from django.db.models import Q


from app.lib.utils import get_ip_list
from libs.celeryapi import *

from libs.log import logger
    
# RUNNING_TASK = {}


# class appDict(dict):

#     def __init__(self):
#         dict.__init__(self)

# k = appDict()

 
def run_subtask(task_id):
    _task = SubTask.objects.get(id=task_id)
    attack_type = _task.attack_type
    attack_target =  _task.attack_target
    #print ">>>Run Task>>",attack_type,attack_target 
    if attack_type == 'fnascan':
        pass
   
   
def _get_detail(dic_m,ip,port):
    dic_key = "%s:%s" % (ip,port)    
    try:
        detail = dic_m[dic_key]      
    except:
        detail = "undefine"
    return detail
    
#celery运行的任务结果入库    
def result_2_db(task_id,attack_type,task_obj):
    #task_obj == RUNNING_TASK[key]
    #获得指定task_id运行输出
    _templist = task_obj.get() 
    if "The" in _templist[0][:5]:
        _templist[0] = _templist[1]
        _templist[1] = _templist[2]
    
    _simple_dic = eval(_templist[0])
    _detail_dic = eval(_templist[1])
    #_templist[0] = {'221.226.15.246': ['443', '80 web \xe5\x8d\x97\xe7\x91\x9e\xe7\xbb\xa7\xe4\xbf\x9dVPN\xe7\x99\xbb\xe9\x99\x86'], '221.226.15.249': ['8081 web Apache Tomcat/7.0.57'], '221.226.15.250': ['80'], '221.226.15.243': ['80', '9200 Elasticsearch(default)', '8000 web']}
    #print _simple_dic,_detail_dic
    for _ip in _simple_dic.keys():
        for  service_name in _simple_dic[_ip]:
            _port = service_name.split(' ')[0]
            ip_port =  '%s:%s' % (_ip,_port)
            web_title = ''
            if len(service_name.split(' ')) > 2:
                web_title = service_name.split(' ')[-1]
            detail = _get_detail(_detail_dic,_ip,_port)
            #入库
            _result = FnascanResult(task_id=task_id,ip=_ip,port = _port ,service_name = service_name,service_detail = detail,web_title = web_title)
            _result.save()         
    if attack_type == 'subdomainbrute':
        print _templist   
    transaction.commit()

#split Task to subtask
def split_main_task():
    _main_task_list = Task.objects.filter(status='WAITTING')
    for _main_task  in _main_task_list:
        attack_type = _main_task.attack_type
        attack_target =  _main_task.attack_target
        #print attack_target
        if attack_type == 'fnascan':
            attack_target_list = get_ip_list(attack_target)   
            print  ">>>>>>>attack_target_list",attack_target_list
            size = 10 #每一个任务的ip数量
            lol = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)] 
            for i in lol(attack_target_list,size):
                i = ','.join(i)
                _subtask = SubTask(main_task_id = _main_task.id, attack_target = i, attack_type = attack_type,task_name = '', status = 'WAITTING', parameter = '') 
                _subtask.save()
            #设置主任务状态为running
            _maintask  = Task.objects.get(id = _main_task.id)
            _maintask.status = 'RUNNING'
            _maintask.save()

        if attack_type == 'bugscan':
            attack_target_list = [attack_target,] 
            print  ">>>bugscan>>>>attack_target_list",attack_target_list
            _t = run_bugscan.delay(attack_target_list) ##
            _maintask  = Task.objects.get(id = _main_task.id)
            _maintask.status = 'RUNNING'
            _maintask.save()

        if attack_type == 'add':
            attack_target_list = attack_target.split('|')
            print attack_target_list
            size = 1 #每一个任务的ip数量
            lol = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)] 
            subtask_count = 0
            for i in lol(attack_target_list,size):
                subtask_count = subtask_count + 1
                logger.warning('subtask %d type:%s args:%s  add to SubTaskTable' % (subtask_count,attack_type,i))#r.json()
                _subtask = SubTask(main_task_id = _main_task.id, attack_target = i, attack_type = attack_type,task_name = '', status = 'WAITTING',parameter = '') 
                _subtask.save()
        _main_task.start_time = timezone.now()
        _main_task.status = 'SPLITED' 
        _main_task.save()
    transaction.commit()
      

#check task status
"""
maintask:
WAITTING
SPLITED     
RUNNING
PENDDING
SUCCESS
"""
"""
after run check_main_task_status()
subtask               maintask

ALL WAITTING   ->     SPLIT or WAITTING
ALL SUCCESS    ->     SUCCESS
ALL PENDING    ->      PENDING
other          ->     RUNNING
"""
def check_main_task_status():
    #except end
    _main_task_list = Task.objects.filter(~Q(status = 'SUCCESS'))
    for _main_task in _main_task_list:
        _sub_task_list = SubTask.objects.filter(main_task_id = _main_task.id)
        _tmp_dic = {}
        #logger.warning('main_task:'+str(_main_task.id))
        for _sub_task in _sub_task_list:
            _tmp_dic[_sub_task.status] = _sub_task.id
            #logger.warning('sub_task:'+str(_sub_task.id))
            #logger.warning(_tmp_dic)
            #print len(_tmp_dic.keys())
        if len(_tmp_dic.keys()) == 1:
            if _tmp_dic.keys()[0] == 'WAITTING':
                pass
                #_main_task.status = 'WAITTING'    
            if _tmp_dic.keys()[0] == 'SUCCESS':
                _main_task.status = 'SUCCESS' 
                _main_task.end_time = timezone.now() 
            if _tmp_dic.keys()[0] == 'PENDING':
                _main_task.status = 'PENDING'  
        elif len(_tmp_dic.keys()) >  1:     
            _main_task.status = 'RUNNING' 
        _main_task.save()
    transaction.commit()

#  subtask status
"""
subtask:
WAITTING (after split main task)
SENDED (send to flower success the started)  
PENDING 
STARTED
SUCCESS
"""    
#send watting task and record task-id
def send_subtask():
    _sub_task_list = SubTask.objects.filter(status = 'WAITTING')
    for _subtask in _sub_task_list:
        if _subtask.attack_type == 'add':
            data = {"args": [_subtask.attack_target,]}
        r = K_send_task(data,'app.tasks.add')
        _subtask.status = r['state']
        _subtask.start_time = timezone.now()
        _subtask.celery_task_id =  r['task-id']
        _subtask.save()
    transaction.commit()


def check_subtask_status_result(CHECK_TIME):
    #time.sleep(CHECK_TIME)
    _sub_task_list = SubTask.objects.filter(~Q(status = 'SUCCESS'))
    for _subtask in _sub_task_list:   
        r = K_get_result(_subtask.celery_task_id )
        #{"task-id": "533dee2b-0573-4fad-8662-b233852885d6", "state": "SUCCESS", "result": "[u'12']"}
        _subtask.status = r['state']
        save_result()
        _subtask.save()
    transaction.commit()

def save_result():
    pass


#三秒钟查询一次数据库查看任务
CHECK_TIME = 3 
def task_sched():
    while True:
        time.sleep(CHECK_TIME)
        #split ip range to subtask
        split_main_task()
        check_main_task_status()
        #send watting task to flower  and record task-id
        send_subtask()
        #check subtask status and try get result
        check_subtask_status_result(CHECK_TIME)


                
 