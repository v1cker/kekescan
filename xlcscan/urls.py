#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# code by evileo

from django.conf.urls import include, url
from datetime import datetime
from django.conf.urls import patterns, url
from app.forms import BootstrapAuthenticationForm
from django.contrib import admin
from django.contrib.auth import views
#from  djcelery import urls as djurls
from app import views as app_view
urlpatterns = patterns('',
    # Examples:
 
 
 
    #url(r'^djcelery/', include(djurls)),
 
    url(r'^save_result',  app_view.save_result , name='save_result'),
 
    url(r'^terminal/', app_view.terminal, name='terminal'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', app_view.index, name='home'),
    url(r'^task/queue$',app_view.task_queue,name='task_queue'),
    url(r'^subtask/queue$',app_view.subtask_queue,name='subtask_queue'),
    url(r'^task/add$',app_view.task_add,name='task_add'),
    url(r'^atk/add$',app_view.atk_add,name='atk_add'),
    url(r'^task/history/?$',app_view.task_history,name='task_history'),
    url(r'^task/history/category$',app_view.task_history,name='task_history_category'),
    
    url(r'^task/operate/?$',app_view.task_operate,name='task_operate'),
    #EXP管理
    url(r'^poclist/', app_view.poc_list, name='poc_list'),
    #结果
    url(r'^results/$', app_view.results, name='results'),
    url(r'^results/add/', app_view.results_add, name='results_add'),
    #数据分析
    url(r'^data/analysis', app_view.data_analysis, name='data_analysis'),
    
    url(r'^burpflow',  app_view.burpflow, name='burpflow'),
################chrome -> sqlmap############################3
    url(r'^getreq',  app_view.get_req, ),
    url(r'^reqlist',  app_view.reqlist, name='reqlist'),
    url(r'^delreq',  app_view.del_req, ),
    url(r'^autocheck',  app_view.sxcheck, ),
    
    #浏览器插件接口
    url(r'^chromeapi', app_view.scancheck,name='chromeapi' ),
################chrome -> sqlmap############################3
    #设置
    url(r'^settings', app_view.ksettings,name='settings' ),
    url(r'^login/$',
         views.login ,
        {
            'template_name': 'login.html',
            'authentication_form': BootstrapAuthenticationForm,
            'extra_context':
            {
                'title':'Log in',
                'year':datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        views.logout,
        {
            'template_name': 'logout.html',
            'next_page': '/',   
        },
        name='logout'), 


    ################DJANGO start kill job############################
    (r'^startjob/$', app_view.startjob),
    (r'^showjob/$',  app_view.showjob),
    (r'^rmjob/$',    app_view.rmjob),
    ################DJANGO start kill job############################
 
)
