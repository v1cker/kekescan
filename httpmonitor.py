#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import time
import django
django.setup()
#import logging

from app.models import *
from django.conf import settings
from subprocess import Popen,PIPE
import os
from os import path
 
from django.db import transaction
import datetime
from django.utils import timezone

from app.tasks import *
from django.db.models import Q


from app.lib.utils import get_ip_list
from libs.celeryapi import *

from libs.log import logger
    
def main_task():
    pass


#三秒钟查询一次数据库查看任务
CHECK_TIME = 3 
def sql_sched():
    while True:
        time.sleep(CHECK_TIME)
        #split ip range to subtask
        main_task()


                
 