# -*- coding: utf-8 -*-  
# code by evileo



"""
Definition of models.
"""

from django.db import models
import datetime
# Create your models here.

class IpPool(models.Model):
    """
    存放所有IP，数据结构来自portmap result_ip表
    """
    task_id = models.IntegerField(null=False, blank=False)
    #domain_name = models.CharField(max_length=256, blank=True, default='')
    ip_address = models.CharField(max_length=256, blank=True, default='')
    is_up = models.IntegerField(blank=True, default=0)
    os = models.CharField(max_length=256, blank=True, default='')
    inserted_time = models.DateTimeField(null=True, blank=True)
    
class PortsServicesPool(models.Model):
    """
    存放所有IP，数据结构来自portmap result_ip表
    """
    task_id = models.IntegerField(null=False, blank=False)
    #domain_name = models.CharField(max_length=256, blank=True, default='')
    ip_address = models.CharField(max_length=256, blank=True, default='')
    is_up = models.IntegerField(blank=True, default=0)
    os = models.CharField(max_length=256, blank=True, default='')
    inserted_time = models.DateTimeField(null=True, blank=True)
    
class FnascanResult(models.Model):
    """
    存放portscan的结果；
    """
    task_id = models.IntegerField(null=False, blank=False)
    ip = models.TextField(null=True, blank=True)
    port =  models.CharField(max_length=10)
    service_name = models.TextField(null=True, blank=True, default='')
    web_title = models.TextField(null=True, blank=True, default='')
    service_detail = models.TextField(null=True, blank=True, default='')
    
class ServiceDetail(models.Model):
    """
    存放portscan的结果；
    """
    task_id = models.IntegerField(null=False, blank=False)
    ip = models.TextField(null=True, blank=True)
    port =  models.CharField(max_length=10)
    service_name = models.TextField(null=True, blank=True, default='')
    
class DNSServerRecord(models.Model):
    """
    存放DNS服务器记录；
    """
    domain = models.TextField(null=True, blank=True)
    #dns_server =   models.TextField(null=True, blank=True)
    domain_admin  = models.TextField(null=True, blank=True)
    domain_company  = models.TextField(null=True, blank=True)
    domain_email  = models.TextField(null=True, blank=True)
    domain_phone  = models.TextField(null=True, blank=True)
    domain_create_time  = models.TextField(null=True, blank=True)
    domain_expire_time  = models.TextField(null=True, blank=True)
    domain_update_time  = models.TextField(null=True, blank=True)
    domain_city  = models.TextField(null=True, blank=True)
    domain_location  = models.TextField(null=True, blank=True)
    domain_isp  = models.TextField(null=True, blank=True)
    

class DomainIpRange(models.Model):
    """
    存放fuzzall获得的ip段信息
    """
    domain_name = models.TextField(null=True, blank=True)
    #dns_server =   models.TextField(null=True, blank=True)
    data_tag  = models.TextField(null=True, blank=True)
    ip_range  = models.TextField(null=True, blank=True)
    fuzz_time = models.DateTimeField(null=True, blank=True)
    fuzzall_id = models.IntegerField(null=False, blank=False, default=0)
    
class DomainBeian(models.Model):
    """
    存放由备案号查询到的域名信息
    """
    domain_name = models.TextField(null=True, blank=True)
    company_name = models.TextField(null=True, blank=True)
    domain_type = models.TextField(null=True, blank=True)
    icp_code  = models.TextField(null=True, blank=True)
    beian_id = models.IntegerField(null=False, blank=False ,default = 0)
    #ip_range  = models.TextField(null=True, blank=True)
    insert_time = models.DateTimeField(null=True, blank=True)
    

class ICPCheck(models.Model):
    """
    临时存放由域名查询到的备案号
    """
    #域名
    domain_name = models.TextField(null=True, blank=True)
    #主办单位名称
    co_name = models.TextField(null=True, blank=True)
    #主板单位性质 企业/个人
    domain_type = models.TextField(null=True, blank=True)
    #网站名称
    domain_title = models.TextField(null=True, blank=True)
    #审核时间
    check_time =  models.TextField(null=True, blank=True)
    #主备案号
    icp_code  = models.TextField(null=True, blank=True)
    #二级本案号
    icp_code_2  = models.TextField(null=True, blank=True)
    #备案IDleo的标记
    beian_id = models.IntegerField(null=False, blank=False ,default = 0)
    #ip_range  = models.TextField(null=True, blank=True)
    
    insert_time = models.DateTimeField(null=True, blank=True ,default = datetime.datetime.now())
    #手工添加标记 1代表手工添加 0代表自动化工具
    byhand = models.IntegerField(null=False, blank=False ,default = 0)
    
class SubDomainBrute(models.Model):
    """
    存放SubDomainBrute的结果；

    """
    #task_id = models.IntegerField(null=False, blank=False)
    domain_name = models.TextField(null=True, blank=True)
    sub_domain = models.TextField(null=True, blank=True)
    sub_ip = models.TextField(null=True, blank=True)
    c_range = models.TextField(null=True, blank=True)
    fuzz_time = models.DateTimeField(null=True, blank=True,default = datetime.datetime.now())
    fuzzall_id = models.IntegerField(null=False, blank=False, default=0)

class SubDomainBruteTask(models.Model):
    """
    存放SubDomainBrute的结果；
    """
    #task_id = models.IntegerField(null=False, blank=False)
    domain_name = models.TextField(null=True, blank=True)
    add_time = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(default='WAITTING', max_length=32)
    result = models.CharField(max_length=256, blank=True, default='')
    #sub_domain = models.TextField(null=True, blank=True)
    #sub_ip = models.TextField(null=True, blank=True)
     

class SiteDesc(models.Model):
    """
    存放网站描述
    """
    #task_id = models.IntegerField(null=False, blank=False)
    site = models.TextField(null=True, blank=True)
    port =  models.CharField(max_length=10,null=True, blank=True)
    site_title = models.TextField(blank=True, default='')
    add_time = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(default='WAITTING', max_length=32)
    result = models.CharField(max_length=256, blank=True, default='')
    #sub_domain = models.TextField(null=True, blank=True)
    #sub_ip = models.TextField(null=True, blank=True)     

    
class HttpFlow(models.Model):
    host = models.CharField(max_length=250,default='', blank=True)
    path = models.CharField(max_length=2500,default='', blank=True)
    isPost = models.IntegerField(default=2, blank=True)
    postData =  models.TextField(blank=True, default='')
    filetype = models.CharField(max_length=250,default='', blank=True)
    isComplete =  models.IntegerField(default=2, blank=True)
 
 

class Req_list(models.Model):
    method = models.CharField('METHOD', max_length=5, )
    host = models.CharField('HOST', max_length=40, )
    uri = models.CharField('FILE', max_length=100, default='/', )
    url = models.TextField('URL', )
    ua = models.TextField('User-agent', )
    referer = models.TextField('REFERER', null=True)
    data = models.TextField('REQUEST BODY', null=True)
    cookie = models.TextField('COOKIE', default='', )


    class Meta:
        unique_together = (('method', 'host', 'uri',))


    def __self__(self):
        return self.url

class Burp(models.Model):
    host = models.CharField('HOST', max_length=200, )
    path = models.CharField('FILE', max_length=10000, default='/', )
    isPost = models.IntegerField('isPost', max_length=1, )
    postData = models.TextField('postData', )
    filetype  = models.CharField('filetype', max_length=40, )
    isComplete = models.IntegerField('isComplete', max_length=1, default=0, )
    # queryed  = models.IntegerField('queryed', max_length=1, default=0,)
 


    class Meta:
        db_table = 'burp'  
 

class Burpk(models.Model):
    host = models.CharField('HOST', max_length=40, default='',  )
    p_hash = models.CharField('p_hash', max_length=100, default='', )
    p_id = models.IntegerField('p_id', default=0,)

    class Meta:
        db_table = 'burpk'  

 


class RequestsFlow(models.Model):
    method = models.CharField('METHOD', max_length=5, )
    host = models.CharField('HOST', max_length=40, )
    uri = models.CharField('FILE', max_length=100, default='/', )
    url = models.TextField('URL', )
    ua = models.TextField('User-agent', )
    referer = models.TextField('REFERER', null=True)
    data = models.TextField('REQUEST BODY', null=True)
    cookie = models.TextField('COOKIE', default='', )


    class Meta:
        unique_together = (('method', 'host', 'uri',))


    def __self__(self):
        return self.url

        
class Task(models.Model): 
    """
    存放一个任务的信息
   """
    #task_id = models.CharField(max_length=128, blank=True, default='')
    task_name  = models.CharField(max_length=128, blank=True, default='')
    attack_type = models.CharField(max_length=128, blank=True, default='')
    attack_target = models.CharField(max_length=256, blank=True, default='')
    add_time = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=32)  # 状态：WAITTING,RUNNING,[FAILURE,SUCCESS]
    except_message = models.CharField(max_length=256, blank=True, default='')
    for_recover_data = models.TextField(blank=True, default='')
    parameter = models.CharField(max_length=512, default='') #命令行参数
    root_url = models.CharField(max_length=512)
    site = models.CharField(max_length=128, blank=True, default='')
    degree_detail = models.CharField(max_length=512, blank=True, default='')
    scan_result = models.CharField(max_length=256, blank=True, default='') 

    #scan_result = models.CharField(max_length=256, blank=True, default='') 
    def __unicode__(self):
        return '%s %d %s %s' % (self.root_url,
         self.id,
         self.status,
         self.scan_result)
         
class SubTask(models.Model): 
    """
    存放一个任务的信息
   """
    celery_task_id = models.CharField(max_length=128, blank=True, default='')
    main_task_id  = models.CharField(max_length=128, blank=True, default='')
    task_name  = models.CharField(max_length=128, blank=True, default='')
    attack_type = models.CharField(max_length=128, blank=True, default='')
    attack_target = models.CharField(max_length=256, blank=True, default='')
    add_time = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=32)  # 状态：WAITTING,RUNNING,[FAILURE,SUCCESS]
    except_message = models.CharField(max_length=256, blank=True, default='')
    for_recover_data = models.TextField(blank=True, default='')
    parameter = models.CharField(max_length=512, default='') #命令行参数
    root_url = models.CharField(max_length=512)
    site = models.CharField(max_length=128, blank=True, default='')
    degree_detail = models.CharField(max_length=512, blank=True, default='')
    scan_result = models.CharField(max_length=256, blank=True, default='') 

    
    def __unicode__(self):
        return '%s %d %s %s' % (self.root_url,
         self.id,
         self.status,
         self.scan_result)
         
class Result(models.Model):
    """
    存放一个任务的 扫描结果 信息
    """
    task_id = models.CharField(max_length=128, blank=True, default='')
    detail = models.TextField(null=True, blank=True)
 
 
class PResult(models.Model):
    domain = models.TextField()
    poc_file = models.TextField(default='', null=True)
    result = models.TextField()
    date = models.DateTimeField(auto_now_add=True, blank=True)
    is_fixed = models.NullBooleanField(default=False)

    def __unicode__(self):
        return self.result


class PTasks_status(models.Model):
    domains = models.TextField()
    task_name = models.TextField()
    status = models.NullBooleanField(default=False)

    def __unicode__(self):
        return self.domains

class ResultIp(models.Model):
    taskid = models.IntegerField(blank=True, null=True)
    inserted = models.DateTimeField(blank=True, null=True)
    domain = models.CharField(max_length=256, blank=True, null=True)
    address = models.CharField(max_length=32, blank=True, null=True)
    is_up = models.IntegerField(blank=True, null=True)
    os = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'result_ip'


class ResultPorts(models.Model):
    taskid = models.IntegerField(blank=True, null=True)
    inserted = models.DateTimeField(blank=True, null=True)
    address = models.CharField(max_length=256, blank=True, null=True)
    port = models.IntegerField(blank=True, null=True)
    service = models.CharField(max_length=256, blank=True, null=True)
    state = models.CharField(max_length=12, blank=True, null=True)
    protocol = models.CharField(max_length=12, blank=True, null=True)
    product = models.CharField(max_length=64, blank=True, null=True)
    product_version = models.CharField(max_length=64, blank=True, null=True)
    product_extrainfo = models.CharField(max_length=128, blank=True, null=True)
    scripts_results = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'result_ports'


class ResultDirbrute(models.Model):
    taskid = models.IntegerField(blank=True, null=True)
    inserted = models.DateTimeField(blank=True, null=True)
    address = models.CharField(max_length=32, blank=True, null=True)
    dir_results = models.TextField(blank=True, null=True)
 