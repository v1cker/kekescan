#!/usr/bin/env python
# -*- coding: utf-8 -*-  

 
import django
django.setup()

from app.models import *
from django.conf import settings 
from django.db import transaction
import datetime

from app.tasks import *

def _to_subdomainbrute()
    _result = FnascanResult(task_id=task_id,ip=ip,port = port ,service_name = service_name,service_detail = detail)
    _result.save()
    transaction.commit()
    
 
