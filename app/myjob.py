import sys
from time import sleep

i = 0
while i < 1000:
    print 'myjob:', i  
    i=i+1
    sleep(0.1)
    sys.stdout.flush()
