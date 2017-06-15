# -*- coding: utf-8 -*-  
# code by evileo

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.utils import timezone
from forms import * 
from models import *
from models import Task
from django.db import transaction, connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse as response, Http404, HttpResponseRedirect
import json
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from bugscan.library.utils import get_poc_files
from urlparse import urlparse
from app.lib.task_control import Task_control
import os
from chtscan.tasks import sql
# get abs path 
from app.kconfig import *
# PYTHON_ROOT = '/home/leo/Desktop/envxlcscan/bin/python'
# KSCAN_ROOT = '/home/leo/Desktop/xlcscan/'
# MANAGE_ROOT = KSCAN_ROOT + 'manage.py

@login_required(login_url="/login/")
def index(request):
    return render(request,'index.html')
  
# end def index
@csrf_exempt
def save_result(request):
        try:
            target = request.POST.get('target', None)
            poc_file = request.POST.get('poc_file', None)
            result = request.POST.get('result', None)
            Result(domain=target, poc_file=poc_file, result=result).save()
            return JsonResponse({"status": 200, "result": result})
        except Exception, e:
            return JsonResponse({"status": e})
		# end try
# end def save_result


            
@login_required(login_url="/login/")
def terminal(request):
    host = request.META['HTTP_HOST'].split(':')[0]
    return render(request, 'terminal.html', {"host": host})
# end def terminal

    
@login_required(login_url="/login/") 
def sudomain(request):
    '''显示队列中的历史任务''' 
    history_tasks = Task.objects.filter(Q(status = 'SUCCESS') | Q(status ='FAILURE')).order_by('-add_time').values()
    return render(
        request,
        'task_history.html',
        context_instance = RequestContext(request,
        {
        'task_objs': history_tasks,
        'is_null': Task.objects.filter(Q(status = 'SUCCESS') | Q(status ='FAILURE')).count() == 0
        })
    )
# end def sudomain

 
    
@login_required(login_url="/login/")    
def task_add(request):
    '''添加任务'''
    if request.method == 'GET':
        form = TaskAddForm()
    else:
        form = TaskAddForm(request.POST)
	# end if
    if not form.is_valid():
        #print 1000*'A'
        return render(
        request,
        'task_add.html',
        context_instance = RequestContext(request,
        {
             'form': form ,
        })
	# end if
    )
    
    target = form.cleaned_data.get('target','') 
    attack_type   = form.cleaned_data.get('attack_type', '')    
    task_name   = form.cleaned_data.get('task_name', '')  

    if attack_type == 'fnascan':
        target = target.strip()
        target = target.strip().split('\r\n')
        if len(target)>1:
            target = ','.join(target)# fnascan 使用逗号分隔
        elif len(target)==1:
            target = target[0]
    	# end if
        param = dict(form.data)
        for k in param.keys():
            param[k] = param[k][0]
    	# end for
        param[u'ip_range'] = target
        param_str = json.dumps(param)
        print ">>>>>>>Staring Single Module ATTACK  %s<<<<<<<" ,target
        task = Task(attack_target = target, attack_type = attack_type,task_name = task_name, status = 'WAITTING', parameter = param_str) 
        task.save()
    if attack_type == 'add':
        target = target.strip()
        target = target.strip().split('\r\n')
        if len(target)>1:
            target = '|'.join(target)# add 使用|分隔
        elif len(target)==1:
            target = target[0]
        task = Task(attack_target = target, attack_type = attack_type,task_name = task_name, status = 'WAITTING', parameter =  '') 
        task.save()

    transaction.commit()
        
	# end if
    html = '<!doctype html><html><head><script>confirm("%s");  window.location = "/";</script></head><body> </html>'  
    if len('cc') > 1:
        ret = html % '任务%s已添加' % str(target) #任务已添加
    else:
        ret = html % '任务%i已添加' % str(target) #任务已添加
	# end if
    return response(ret)
# end def task_add

        
        
@login_required(login_url="/login/")    
def atk_add(request):
    '''添加自动化扫描任务'''
    #print 100*"b"
    if request.method == 'GET':
        form = TaskAddForm()
    else:
        form = TaskAddForm(request.POST)
	# end if
    if not form.is_valid():
        #print 1000*'A'
        return render(
        request,
        'task_add.html',
        context_instance = RequestContext(request,
        {
             'form': form ,
        })
	# end if
    )
    
    attack_route = form.cleaned_data.get('attack_route','') 
    target = form.cleaned_data.get('target','') 
    task_name   = form.cleaned_data.get('task_name', '')  
    target = target.strip()
    #print 100*'A'
    #ATK模式攻击类型标识为ATK_K0,ATK_K1...
    task = Task(attack_target = target, attack_type = 'ATK_'+str(attack_route),task_name = task_name, status = 'WAITTING') 
    task.save()
    transaction.commit()
        
    print ">>>>>>>Staring Multi Module ATTACK  %s<<<<<<<" % str(target)
    
    
    html = '<!doctype html><html><head><script>confirm("%s");  window.location = "/";</script></head><body> </html>'  
    if len('cc') > 1:
        ret = html % '任务%s已添加' % str(target) #任务已添加
    else:
        ret = html % '任务%i已添加' % str(target) #任务已添加
	# end if
    return response(ret)
# end def atk_add

    

    
@login_required(login_url="/login/") 
def subtask_queue(request):
    '''显示子任务队列中的任务''' 
    if request.method == 'GET':
        task_id = ''
        _main_task_id = request.GET.get('task_id')
        if _main_task_id:
            queues  = SubTask.objects.filter(main_task_id=_main_task_id).order_by('-add_time').values()
            task_id = _main_task_id
        else:
            #queues = SubTask.objects.exclude(Q(status = 'SUCCESS') | Q(status ='FAILURE')).order_by('-add_time').values()
            queues = SubTask.objects.order_by('-add_time').values()
        numOfResult = len(queues)

        paginator = Paginator(queues, 10) # Shows only 10 records per page
	# end if
        page = request.GET.get('page')
        try:
            results_pag = paginator.page(page)
        except PageNotAnInteger:
        # If page is not an integer, deliver first page.
            results_pag = paginator.page(1)
        except EmptyPage:
        # If page is out of range (e.g. 7777), deliver last page of results.
            results_pag = paginator.page(paginator.num_pages)
            
		# end try
    
    max_task = int(5)
    return render(
        request,
        'subtask_queue.html',
        context_instance = RequestContext(request,
        {
        "num": numOfResult,
        'task_objs': results_pag,
        'max_tasks': max_task,
        'task_id' : task_id,
        })
    )
# end def subtask_queue

    

@login_required(login_url="/login/") 
def task_queue(request):
    '''显示队列中的任务''' 
    if request.method == 'GET':
        #queues = Task.objects.exclude(Q(status = 'SUCCESS') | Q(status ='FAILURE')).order_by('-add_time').values()
        queues = Task.objects.order_by('-add_time').values()

        numOfResult = len(queues)
        
        
        paginator = Paginator(queues, 10) # Shows only 10 records per page
	# end if
    
        page = request.GET.get('page')
        try:
            results_pag = paginator.page(page)
        except PageNotAnInteger:
        # If page is not an integer, deliver first page.
            results_pag = paginator.page(1)
        except EmptyPage:
        # If page is out of range (e.g. 7777), deliver last page of results.
            results_pag = paginator.page(paginator.num_pages)
            
		# end try
    
    max_task = int(5)
    return render(
        request,
        'task_queue.html',
        context_instance = RequestContext(request,
        {
        "num": numOfResult,
        'task_objs': results_pag,
        'max_tasks': max_task,
        })
    )
# end def task_queue

@login_required(login_url="/login/") 
def task_history(request):
    '''显示队列中的历史任务''' 
    
    if request.method == 'GET':
        history_tasks = Task.objects.filter(Q(status = 'SUCCESS') | Q(status ='FAILURE')).order_by('-add_time').values()
        numOfResult = len(history_tasks)
        
        
        paginator = Paginator(history_tasks, 10) # Shows only 10 records per page
	# end if
    
        page = request.GET.get('page')
        try:
            results_pag = paginator.page(page)
        except PageNotAnInteger:
        # If page is not an integer, deliver first page.
            results_pag = paginator.page(1)
        except EmptyPage:
        # If page is out of range (e.g. 7777), deliver last page of results.
            results_pag = paginator.page(paginator.num_pages)
            
		# end try
    
    
    return render(
        request,
        'task_history.html',
        context_instance = RequestContext(request,
        {
        'task_objs': results_pag,
        'is_null': Task.objects.filter(Q(status = 'SUCCESS') | Q(status ='FAILURE')).count() == 0
        })
    )
# end def task_history

@login_required(login_url="/login/") 
def task_operate(request):
    if request.method == 'GET':
        operate_type = request.GET.get('type', '')
        id = request.GET.get('task_id', '')
        id = int(id)
	# end if
    _task = Task.objects.get(id = id)
    _result = Result.objects.get(task_id = _task.task_id)
    if operate_type == 'stop':
        pass
	# end if
    if operate_type == 'delete':
        _task.delete()
        _result.delete()
        pass
	# end if
    if operate_type == 'restart':
        pass
        
	# end if
    _task.save()
    _result.save()
    transaction.commit()
    
    anoncement = 'TASK %d has %s' % (id,operate_type)
    return response(anoncement)
    
# end def task_operate
import re    
import socket

def is_valid_ipv4_address(address):
    if len(address.split('.')) < 4:
        return False
	# end if
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
		# end try
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False
	# end try
# end def is_valid_ipv4_address

    return True
    
def is_valid_hostname(hostname):   
    if len(hostname.split('.')) < 2:
        return False
	# end if
    if hostname[-1] == ".":
        # strip exactly one dot from the right, if present
        hostname = hostname[:-1]
	# end if
    if len(hostname) > 253:
        return False
	# end if
    # must be not all-numeric, so that it can't be confused with an ip-address
    if re.match(r"[\d.]+$", hostname):
        return False
	# end if
# end def is_valid_hostname

    allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))
    
  
@login_required(login_url="/login/")
@csrf_exempt
def results(request):
    if request.method == 'GET':
        if 'results-post' in request.session:
            request.POST = request.session['results-post']
            request.method = 'POST'
        else:
            form = ResultsForm()
            return render(
                request,
                'results.html',
                context_instance = RequestContext(request,
                {
                     'form': form ,
                     "num": 0,
                })
                )
    #print  1000*'A'       
    if request.method == 'POST':
        form = ResultsForm(request.POST)
        request.session['results-post'] = request.POST
        
        if not form.is_valid():
            print ''
            return render(
            request,
            'results.html',
            context_instance = RequestContext(request,
            {
                 'form': form ,
                 "num": 0,
            })
		# end if
        )
	# end if
    
    target = form.cleaned_data.get('target','') 
    results_type   = form.cleaned_data.get('results_type', '')    
    print ">>>>>>>target:%s>>>>>>>>results_type:%s>>>>>>>>>>>>" % (target,results_type)
    
    results = {}
    
    #首先设置全局task_id查询
    task_id = 0
    if results_type == 'task_id': 
        try:
            task_id = int(target)
        except:
            return
		# end try
        _tmp_task =  Task.objects.get(id = task_id)
        results_type = _tmp_task.attack_type
        
	# end if
        #pass
    #获取icp_check的结果
    if results_type == 'icp_check': 
        if  is_valid_hostname(target):
            #由域名获得备案号
            try:
                _t =  DomainBeian.objects.filter(Q(domain_name = target)).values()[0] 
                beian_id = _t['beian_id']
            except:
                beian_id =  -1   
			# end try
            #由备案号查询获得该备案号下面的所有域名
            results = DomainBeian.objects.filter(Q(beian_id = int(beian_id))).order_by('-insert_time').values()
            items, item_ids = [], []
            for item in results:
                if item['domain_name'] not in item_ids:
                    items.append(item)
                    item_ids.append(item['domain_name'])
				# end if
			# end for
            results = items
        else:
            results = DomainBeian.objects.filter(Q(icp_code = target )).order_by('-insert_time').values()
            items, item_ids = [], []
            for item in results:
                if item['domain_name'] not in item_ids:
                    items.append(item)
                    item_ids.append(item['domain_name'])
				# end if
			# end for
            results = items
            
		# end if
	# end if
    #获取subdomain的结果
    if results_type == 'subdomain':
        if  is_valid_hostname(target):
            results = SubDomainBrute.objects.filter(Q(domain_name = target)).values()

            
		# end if
	# end if
    #获取fnascan的结果
    if results_type == 'fnascan':
        if  is_valid_ipv4_address(target):
            results =  FnascanResult.objects.filter(Q(ip = target)).values()
		# end if
            #print 100* 'A'
            #print results
        if task_id:
            results =  FnascanResult.objects.filter(Q(task_id = task_id)).values()

    if results_type == 'nmap':
        if  is_valid_ipv4_address(target):
            results =  ResultPorts.objects.filter(Q(address = target)).values()
        else:
            results =  ResultPorts.objects.filter(address__contains=target).order_by('address') .values()
            #print 100* 'A'
            #print results
        if task_id:
            results =  ResultPorts.objects.filter(Q(address = task_id)).values()
                  
		# end if
	# end if
# end def results

            
    numOfResult = len(results)
    
    
    paginator = Paginator(results, 10) # Shows only 10 records per page

    page = request.GET.get('page')
    try:
        results_pag = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer, deliver first page.
        results_pag = paginator.page(1)
    except EmptyPage:
    # If page is out of range (e.g. 7777), deliver last page of results.
        results_pag = paginator.page(paginator.num_pages)
        
	# end try
    return render(
        request, 'results.html', 
            {
            "results": results_pag,
              'form': form ,
              "num": numOfResult,
              "results_type" : results_type,
            })
            
  

#解析手工插入的ICP数据
def _get_icp(dt,icp_code):
    #以“详细”这个词进行分割
    _tmp_list =  dt.split(u'\u8be6\u7ec6\r\n')   
    for one_record  in _tmp_list:
        _tmp_record =  {}
        one_record  =  one_record.split('\t')
        _tmp_domainlist = one_record[5].split('\r\n')
        for _tmp_domain in _tmp_domainlist:
            if len(_tmp_domain.strip()) > 3:
                #域名地址
                _tmp_record['domain_name'] = _tmp_domain
                #主办单位名称
                _tmp_record['co_name'] =  one_record[1]
                #主板单位性质 企业/个人
                _tmp_record['domain_type'] = one_record[2]
                #网站名称
                _tmp_record['domain_title'] = one_record[4]
                #审核时间
                _tmp_record['check_time'] =  one_record[6]
                #主备案号
                #icp_code  = models.TextField(null=True, blank=True)
                #二级本案号
                _tmp_record['icp_code_2']  = one_record[3]
                #备案IDleo的标记
                #beian_id = one_record[]
                
                #insert_time = models.DateTimeField(null=True, blank=True)
                #print _tmp_record
                _t = ICPCheck(domain_name =_tmp_record['domain_name'],co_name = _tmp_record['co_name'],domain_type = _tmp_record['domain_type'],domain_title = _tmp_record['domain_title'] ,check_time = _tmp_record['check_time'],icp_code = icp_code ,icp_code_2 = _tmp_record['icp_code_2'],byhand = 1)
                _t.save()
			# end if
		# end for
        
	# end for
    transaction.commit()
        
     
# end def _get_icp
@login_required(login_url="/login/") 
def results_add(request):
    if request.method == 'GET':
        form = ResultsAddForm()
    else:
        form = ResultsAddForm(request.POST)
	# end if
    if not form.is_valid():
        #print 1000*'A'
        #print request.path
        type_tag = ""
        return render(
        request,
        'results_add.html',
        context_instance = RequestContext(request,
        {
             'action_url' : request.path,
             'form' : form ,
             'type_tag': type_tag,
        })
	# end if
    )
    
# end def results_add

     
    #根据URL判断是手动添加哪种数据
    #添加子域名数据
    domain_data = form.cleaned_data.get('domain_data','') 
    domain_name = form.cleaned_data.get('domain_name','') 
    if  str(request.path).lower() == "/results/add/subdomainbrute":
        _tmplist_foreign_data = domain_data.split('\r\n')
        for tr in _tmplist_foreign_data:
            tr = tr.split('\t')
            if len(tr) == 2:
                tr[0] = tr[0].strip()
                tr[1] = tr[1].strip()
                _templist_ip = tr[1].split(',')
                for _tempstr_ip in _templist_ip:
                    print _tempstr_ip,tr[0] 
                    _result = SubDomainBrute(domain_name=domain_name,sub_domain=tr[0] ,sub_ip = _tempstr_ip,fuzzall_id = -1)
                    _result.save()  
				# end for
			# end if
		# end for
	# end if
    transaction.commit()
    # fuzzall_id = -1 为手工插入标识
    #手工添加备案数据
    icp_data = form.cleaned_data.get('icp_data','') 
    icp_code = form.cleaned_data.get('icp_code','') 
    if  str(request.path).lower() == "/results/add/icp":
        _get_icp(icp_data,icp_code) 
        
	# end if
    return render(
    request,
    'results_add.html',
    context_instance = RequestContext(request,
    {
        'type_tag': 0,
        'action_url':request.path,
        'form': form ,
    })
    )
    
    
import collections     
@login_required(login_url="/login/")    
def data_analysis(request):
    '''添加任务'''
    if request.method == 'GET':
        form = DataAnalysisForm()
    else:
        form = DataAnalysisForm(request.POST)
	# end if
    if not form.is_valid():
        #print 1000*'A'
        return render(
        request,
        'data_analysis.html',
        context_instance = RequestContext(request,
        {
             'form': form ,
             
        })
	# end if
    )
    
    target = form.cleaned_data.get('target','') 
    analysis_type   = form.cleaned_data.get('analysis_type', '')    
 
    #results =  FnascanResult.objects.filter(Q(ip = target)).values()
    #var servers    = {"221.226.15.243": ["80", "9200 Elasticsearch(default)", "8000 web"], "221.226.15.245": ["80 web"], "221.226.15.246": ["443", "80 web \u5357\u745e\u7ee7\u4fddVPN\u767b\u9646"], "221.226.15.252": ["21 ftp", "22 ssh", "3306 mysql", "80 web", "8081 web", "11211 memcached(default)"], "221.226.15.253": ["80 web NR_SRM\u6b63\u5f0f\u73af\u5883"], "221.226.15.250": ["80 web"], "221.226.15.251": ["80"], "221.226.15.249": ["8081 web Apache Tomcat/7.0.57"]}
# Convert query to row arrays
    rows = FnascanResult.objects.all() 
    rowarray_list = []
    for row in rows:
        t = (row.ip, row.port, row.service_name, row.service_detail, 
             row.web_title)
        rowarray_list.append(t)
     
	# end for
    j = json.dumps(rowarray_list)
    rowarrays_file = 'student_rowarrays.js'
    f = open(rowarrays_file,'w')
    print >> f, j
     
    # Convert query to objects of key-value pairs
    re_data = {}
    port_data = {}
    statistics = {}
    
    objects_list = []
    for row in rows:
        d = collections.OrderedDict()
       
        d[str(row.ip)+str(row.port)] = row.service_name
        #d['port'] = row.port
        #d['service_name'] = row.service_name
        #d['service_detail'] = row.service_detail
        #d['web_title'] = row.web_title
        objects_list.append(d)
	# end for
    """
    port_data = []
    for row in rows:
        d = collections.OrderedDict()
       
        d[str(row.ip)+':'+str(row.port)] = row.service_detail
        #d['port'] = row.port
        #d['service_name'] = row.service_name
        #d['service_detail'] = row.service_detail
        #d['web_title'] = row.web_title
        port_data.append(d)
        
	# end for
    statistics = []
    for row in rows:
        d = collections.OrderedDict()
        _temp_key = (str(row.ip)+str(row.port)).strip()
        d[_temp_key] = row.service_detail
        #d['port'] = row.port
        #d['service_name'] = row.service_name
        #d['service_detail'] = row.service_detail
        #d['web_title'] = row.web_title
        statistics.append(d)
	# end for
    """
    j = json.dumps(objects_list)
    print j
    port_list = []
# end def data_analysis

    servers = str(json.dumps(re_data))
    portdata = json.dumps(port_data)
    statistics = str(json.dumps(statistics))
    return render(
        request,
        'data_analysis.html',
        context_instance = RequestContext(request,
        {
             'form': form ,
             'portdata': portdata , 
        })
           )
    
    


################chrome -> sqlmap############################3
@login_required(login_url="/login/")
def get_req(request):
    try:
        offset = int(request.GET['offset'])
        offend = int(request.GET['limit']) + offset
        try:
            scanhost = request.GET['search']
            infobj = Req_list.objects.filter(host=scanhost).values()
            info = list(infobj)
            return JsonResponse({"total": len(info), "rows": info})
        except Exception, e:
            infobj = Req_list.objects.values()
            allinfo = list(infobj)
            info = allinfo[offset:offend]
            return JsonResponse({"total": len(allinfo), "rows": info})
		# end try
    except Exception, e:
        return JsonResponse({"total": "0", "rows": []})
	# end try
# end def get_req


@login_required(login_url="/login/")
def del_req(request):
    try:
        reqids = request.POST['reqid']
        reqids = reqids.split(',')
        for reqid in reqids:
            Req_list.objects.get(id=reqid).delete()
		# end for
        return HttpResponse("Success")
    except Exception, e:
        return HttpResponse("Error")
	# end try
# end def del_req


@login_required(login_url="/login/")
def reqlist(request):
    return render(request, 'reqlist.html')
# end def reqlist


@login_required(login_url="/login/")
def sxcheck(request):
    try:
        reqids = request.POST['reqid']
        reqids = reqids.split(',')
        for reqid in reqids:
            sql.delay(reqid)
		# end for
        return HttpResponse("Success")
    except Exception, e:
        return HttpResponse("Error")
	# end try
# end def sxcheck

from app.lib.utils import check_status

@csrf_exempt
def scancheck(request):
    module = request.POST.get('module')
    #print 1000*'>',module
    if module == 'pocscan':
        domains = str(request.POST.get('domains', "bilibili.com"))
        targets = list(set(domains.split(',')))
        tmp_targets = list(set(domains.split(',')))
        for target in tmp_targets:
            cannt_scan_target, status = check_status(target)
            if cannt_scan_target:
                targets.remove(cannt_scan_target)
			# end if
		# end for
        if targets:
            Task_control().launch(targets, "", "")
            return JsonResponse({"status": 200})
        else:
            return JsonResponse({"status": 1})
		# end if
    elif module == 'sqlmap':
        chromeapi(request)
        
	# end if
    
    else:
        return JsonResponse({'status': "error"})
    return JsonResponse({'status': "200"})
# end def scancheck


@csrf_exempt
def chromeapi(request):
    method = request.POST.get('method')
    url = request.POST.get('url')
    cookie = request.POST.get('cookie', '')
    ua = request.POST.get('ua', '')
    referer = request.POST.get('referer', '')
    data = request.POST.get('data', '')
    tmparse = urlparse(url)
    host = tmparse.netloc
    uri = tmparse.path
    white_list = ['', '.php', 'cgi',
                  '.asp', '.aspx', 'ashx',
                  '.do', '.action', 'jsp',
                  '.html', 'htm', '.shtml', '.stm', '.shtm',
                  'json',
                  ]
    print '>>>>',url
    try:
        file_type = os.path.splitext(uri.replace('//', '/'))[1]
        #print file_type
        if file_type in white_list:
            req = Req_list(method=method,
                           url=url,
                           host=host,
                           uri=uri,
                           data=data,
                           referer=referer,
                           ua=ua,
                           cookie=cookie,
                           )
            req.save()
            sql.delay(req.id)
            return JsonResponse({"status": req.id})
        else:
            return JsonResponse({"status": "haved in the reqlist"})
		# end if
    except Exception, e:
        return JsonResponse({"status": "error"})
	# end try
# end def chromeapi

################chrome -> sqlmap############################3
@login_required(login_url="/login/")    
def ksettings(request):
    pass
    return render(
        request,
        'settings.html',
        context_instance = RequestContext(request,
        {
              
        })
    )
    
    # if request.method == 'GET':
    #     form = TaskAddForm()
    # else:
    #     form = TaskAddForm(request.POST)
    # #start stop flower
    # flower_process = ''
    # if  str(request.path).lower() == "/settings/flower/start":  
    #     #xmanage celery   flower --broker=redis://localho:6379/0
    #     print '##############start flower'
    #     import subprocess
    #     import psutil
    #     from subprocess import PIPE
    #     flower_process = psutil.Popen(["/home/leo/Desktop/envxlcscan/bin/python",'/home/leo/Desktop/xlcscan/manage.py','celery','flower',"--broker=redis://localhost:6379/0"],stdout=PIPE)

    #     return render(
    #     request,
    #     'settings.html',
    #     context_instance = RequestContext(request,
    #     {
    #          'form': form ,
    #     })
    #     )

    # if  str(request.path).lower() == "/settings/flower/stop":  
    #     print '##############kill flower'
    #     try:
    #         flower_process.kill()
    #     except:
    #         pass
    
    # #start stop local worker
    # worker_process = ''
    # if  str(request.path).lower() == "/settings/localworker/start":  
    #     print '##############start flower'
    #     import subprocess
    #     import psutil
    #     from subprocess import PIPE
    #     worker_process = psutil.Popen(["/home/leo/Desktop/envxlcscan/bin/python",'/home/leo/Desktop/xlcscan/manage.py','celery','worker',"--loglevel=info"],stdout=PIPE)

    # if  str(request.path).lower() == "/settings/localworker/stop":  
    #     print 'kill xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'


    
# end def ksettings
@login_required(login_url="/login/")
def poc_list(request):
    poc_list = get_poc_files('')
    return render(request, 'poc_list.html', {"poc_list": poc_list})
# end def poc_list

        
    '''    
    try:
        page = (int(request.GET['page'])-1)*10
        try:
            results = Result.objects.all()[page:(page+10)]
            return render(request, 'reslist.html', {"results": results})
        except Exception,e:
            pass
		# end try
    except Exception, e:
        numOfResult = len(Result.objects.all())
        return render(request, 'results.html', 
            {"num": numOfResult,
            'form': form ,
        })'''
        
        
	# end try

@login_required(login_url="/login/") 
def http_flow(request):
    '''显示http数据流''' 
    
    if request.method == 'GET':
        history_tasks = Task.objects.filter(Q(status = 'SUCCESS') | Q(status ='FAILURE')).order_by('-add_time').values()
        numOfResult = len(history_tasks)
        
        
        paginator = Paginator(history_tasks, 10) # Shows only 10 records per page
	# end if
    
        page = request.GET.get('page')
        try:
            results_pag = paginator.page(page)
        except PageNotAnInteger:
        # If page is not an integer, deliver first page.
            results_pag = paginator.page(1)
        except EmptyPage:
        # If page is out of range (e.g. 7777), deliver last page of results.
            results_pag = paginator.page(paginator.num_pages)
            
		# end try
    
    
    return render(
        request,
        'http_flow.html',
        context_instance = RequestContext(request,
        {
        'task_objs': results_pag,
        'is_null': Task.objects.filter(Q(status = 'SUCCESS') | Q(status ='FAILURE')).count() == 0
        })
    )
# end def http_flow


from lib.burpflowlib import distinct_http
@login_required(login_url="/login/") 
def burpflow(request):
    if request.method == 'GET':
        #Show Single http packet
        http_id = request.GET.get('id')
        if http_id:
            results_pag = Burp.objects.get(id = http_id)
            return render(
                request,
                'http_raw.html',
                context_instance = RequestContext(request,
                {
  
                'burp_flow':results_pag,
                })
            )

        #Httpflow after distinct
        if  "/burpflow/distinct/" in str(request.path).lower():
            distinct_http()
            #call disinct .py
            test_ids = list(Burpk.objects.all().values_list('p_id', flat=True))
            #print test_ids
            burp_flow_list = Burp.objects.filter(id__in=test_ids).order_by('-id').values()
        #Httpflow 
        else:
            burp_flow_list = Burp.objects.filter().order_by('-id').values()
        numOfResult = len(burp_flow_list)
        
        
        paginator = Paginator(burp_flow_list, 20) # Shows only 10 records per page
    # end if
    
        page = request.GET.get('page')
        try:
            results_pag = paginator.page(page)
        except PageNotAnInteger:
        # If page is not an integer, deliver first page.
            results_pag = paginator.page(1)
        except EmptyPage:
        # If page is out of range (e.g. 7777), deliver last page of results.
            results_pag = paginator.page(paginator.num_pages)

    return render(
        request,
        'burp_flow.html',
        context_instance = RequestContext(request,
        {
        'num' : numOfResult,
        'burp_flow':results_pag,
        })
    )



job_workspace =   KSCAN_ROOT + '/app/'
from tempfile import mkstemp
from os import fdopen,unlink,kill
from subprocess import Popen
import signal
from django.http import HttpResponse
from django.core import serializers
import psutil
def startjob(request):
    request.session.modified = True
    """Start a new long running process unless already started."""
    if not request.session.has_key('running_job'):
        request.session['running_job'] = {}

    job_name = request.GET.get('job_name')
    # print request.session['running_job']
    #
    if job_name  not in request.session['running_job']:
        job_execfile = ''

        if job_name == 'flower':
            job_execfile = PYTHON_ROOT + " " + MANAGE_ROOT + "  celery flower --broker=redis://localhost:6379/0"
            

        if job_name == 'localworker':
            job_execfile = PYTHON_ROOT +  " " + MANAGE_ROOT + "  celery worker --loglevel=info "
        
        print job_execfile
        if job_execfile:   
            # create a temporary file to save the results
            outfd,outname=mkstemp()
            # request.session['jobfile']=outname
            outfile=fdopen(outfd,'a+')
            # print job_workspace
            proc=Popen(job_execfile.split(),shell=False,stdout=outfile,cwd=job_workspace)
            # remember pid to terminate the job later
            request.session['running_job'][job_name]=proc.pid
            # remember tempfile to delete the job later
            request.session['running_job'][job_name+'_tmpfile']=outname

    return JsonResponse(request.session['running_job'], safe=False) 

def showjob(request):
    """Show the last result of the running job."""
    # print request.session
    if not  request.session.has_key('running_job'):
        RUNNING_JOB_DIC = {}
        return JsonResponse(RUNNING_JOB_DIC, safe=False) 
    else:
        RUNNING_JOB_DIC = request.session['running_job']
        return JsonResponse(RUNNING_JOB_DIC, safe=False) 

def rmjob(request):
    """Terminate the runining job."""
    request.session.modified = True
    if request.session.has_key('running_job'):
        job_name = request.GET.get('job_name')
        
        #mutilprocess
        if job_name == 'localworker':
            proc=Popen('pkill -f "celery worker"',shell=True,stdout=False)

        #if the job in running dict()
        if request.session['running_job'].has_key(job_name):
            jobpid =  request.session['running_job'][job_name]
            filename = request.session['running_job'][job_name + '_tmpfile']
            #print jobpid,filename
            # if the job has finished already
            if not psutil.pid_exists(jobpid):
                # make sure running_job dictionary   has delete
                #try:
                del request.session['running_job'][job_name]

                del request.session['running_job'][job_name + '_tmpfile']
                #print  request.session['running_job'] 
                return JsonResponse(request.session['running_job'], safe=False) 
            try:
                #print  jobpid,filename
                kill(jobpid,signal.SIGKILL) # unix only
                unlink(filename)
            except OSError, e:
                # probably the job has finished already
                return JsonResponse({'error':'kill pid or unlink tmpfile error!'})

            del request.session['running_job'][job_name]
            del request.session['running_job'][job_name + '_tmpfile']

    return JsonResponse(request.session['running_job'], safe=False) 