import subprocess 
import psutil
from subprocess import PIPE
p = psutil.Popen(["/home/leo/Desktop/envxlcscan/bin/python",'/home/leo/Desktop/xlcscan/manage.py','celery','flower',"--broker=redis://localhost:6379/0"],stdout=PIPE)

import time
time.sleep(5)

p.kill()
#print 10000*'a'
