# -*- coding: utf-8 -*-  
# code by evileo



"""
Definition of forms.
"""

from django.forms import *
from django import forms


from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))



class TaskAddForm(Form):
    """TaskAdd表单"""
	#pass
    target = CharField(label=u'目标地址', required=True, widget=forms.Textarea(attrs={'class': 'form-control',
                                                                                            'placeholder': "可添加多条，回车分割"}))
    task_name = CharField(label=u'task_name', required=False, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                            'placeholder': ""}))
    #module_name = CharField(label=u'scan_mode', required=False, widget=TextInput(attrs={'class': 'form-control'}))
    attack_type = ChoiceField(label=u'attack_type',required=False,  widget=forms.Select(attrs={'class':'form-control'}),initial='F-NAScan', 
    choices=[('fnascan', _('F-NAScan')),
             ('subdomainbrute', _('subDomainBrute')),
             ('bugscan', _('Bugscan')),
             ('nmap', _("Nmap-Default")),
            # ('pocscan', _("PocScan")),
             ('add', _("add")),])
             
    attack_route = ChoiceField(label=u'attack_type',required=False, widget=forms.Select(attrs={'class':'form-control'}),initial='F-NAScan',
    choices=[('K0', _('DOMAIN -> SUBDOMAIN -> IPSERVICE')),
             ('K1', _('DOMAIN -> SUBDOMAIN ->IPCRANGE-> IPSERVICE')),
             ('K2', _('DOMAIN -> ICP ->DOMAIN -> SUBDOMAIN -> SUBIP -> IP-C-RANGE')),
             ('K3', _('DOMAIN -> SUBDOMAIN  -> SUBIP -> IP-CRANGE -> IP-PORT -> PORT-SERVICE')),
             ('K4', _('DOMAIN -> ICP ->DOMAIN -> SUBDOMAIN -> SUBIP')),
             ('K5', _('DOMAIN -> ICP ->DOMAIN -> SUBDOMAIN -> SUBIP -> IP-C-RANGE')),
             ('K6', _('DOMAIN -> SUBDOMAIN -> SUBIP -> IP-C-RANGE')),
             ('K7', _('DOMAIN -> ICP ->DOMAIN -> SUBDOMAIN')),
             ('K8', _('IP -> IP-CRANGE -> IP-PORT -> PORT-SERVICE')),])

class ResultsAddForm(Form):
    """手工添加数据表单"""
    domain_data = CharField(label=u'手工添加数据', required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': "可添加多条，回车分割，如:\n\
	www.99designs.com             	52.201.36.245\n \
	admin.99designs.com           	54.85.221.109, 52.72.149.213\n \
	account.99designs.com         	52.4.13.32, 54.173.220.213, 54.175.82.55\n \
	gmail.99designs.com           	64.233.187.123\n "}))
	
    icp_data = CharField(label=u'手工添加数据', required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': """可添加多条，回车分割，暂时支持http://www.miitbeian.gov.cn/ 如: \n \
1 	深圳市腾讯计算机系统有限公司 	企业 	 粤B2-20090059-1	腾讯官方网 	
izhuye.tencent.com
izhuye.tencent.com.cn
 	2016-05-03 	  详细
2 	深圳市腾讯计算机系统有限公司 	企业 	 粤B2-20090059-10	滔滔 	
izhuye.taotao.com
 	2016-05-03 	  详细
3 	深圳市腾讯计算机系统有限公司 	企业 	 粤B2-20090059-100	手机QQ网站 	
izhuye.mqqurl.com
 	2016-05-03 	  详细
    """ }))
    
    icp_code =CharField(label=u'icp_code', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "备案号,如粤B2-20090059"}))
    domain_name =CharField(label=u'domain_name', required=False, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': "主域名,,如99designs.com  "}))
                                                                                            
                                                                                            
             
    
             
class ResultsForm(Form):
    """Result结果表单"""
    target = CharField(label=u'', required=True,  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                            'placeholder': ""}))
    #module_name = CharField(label=u'scan_mode', required=False, widget=TextInput(attrs={'class': 'form-control'}))
    results_type = ChoiceField(label=u'results_type', widget=forms.Select(attrs={'class':'form-control'}),initial='F-NAScan', 
    choices=[('icp_check', _('ICP CHECK')),
             ('subdomain', _("SubDomain")),
              ('task_id', _("Task Id")),
              ('nmap', _("Nmap-Default")),
              ('dirbrute', _("DirBrute")),
             ('SubDomain/PortService', _("SubDomain -> PortService")),
             ('an ', _("SubDomain -> CRange -> PortService")),
             ('fnascan', _("F-Nascan")),
            ('pocscan', _("PocScan")),] )
            
class DataAnalysisForm(Form):
    """Result结果表单"""
    target = CharField(label=u'', required=True,  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                            'placeholder': ""}))
    #module_name = CharField(label=u'scan_mode', required=False, widget=TextInput(attrs={'class': 'form-control'}))
    analysis_type = ChoiceField(label=u'results_type', widget=forms.Select(attrs={'class':'form-control'}),initial='F-NAScan', 
    choices=[('crange', _('C RANGE INFO')),
             ('subdomain', _("SubDomain")),
             ('fnascan', _("F-Nascan")),
            ('pocscan', _("PocScan")),] )
            
class SubDomainBruteForms(Form):
    """subdomainbrute爆破表单"""
    domain = CharField(label=u'域名', required=True, widget=TextInput(attrs={'class': 'text mid'}))

    
class PortScanForms(Form):
    """subdomainbrute爆破表单"""
    ip_range = CharField(label=u'IP地址', required=True, widget=TextInput(attrs={'class': 'text mid'}))
    port_range = CharField(label=u'端口范围', required=False, widget=TextInput(attrs={'class': 'text mid'}))

class SiteDescForms(Form):
    """网站描述表单"""
    ip_range = CharField(label=u'IP地址', required=True, widget=TextInput(attrs={'class': 'text mid'}))
    port_range = CharField(label=u'端口范围', required=False, widget=TextInput(attrs={'class': 'text mid'}))
    
