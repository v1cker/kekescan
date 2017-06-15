from os import path
import subprocess
from subprocess import Popen,PIPE

TASKS_ROOT = path.dirname(path.abspath(path.dirname(__file__)))

def run_fnascan(target):     
    fnascan_workspace =   path.join(TASKS_ROOT, 'tools','FNAScan').replace('\\', '/')
    #"D:/Projects/xlcscan/xlcscan/tools/FNAScan/"
    #print fnascan_workspace
    cmd = 'python F-NAScan.kscan.py -h %s' % target #221.226.15.243-221.226.15.245 , 221.226.15.243,221.226.15.245
    p=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT ,cwd=fnascan_workspace,)  
    process_output = p.stdout.readlines()
    return process_output   

print run_fnascan('222.45.194.1')
