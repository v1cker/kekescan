# coding=utf-8

#coding=utf-8
import imp
import sys

from xlcscan.settings import SAVE_RESULT_API
import requests as req

from bugscan.config import POCS_DIR
 

class Bugscan(object):

    plugins_name = 'bugscan'
    result = {
        'vul_info': {},
        'result': {}
    }

    def import_poc(self, path):
        filename = path.split("/")[-1].split(".py")[0]
        poc_path = path.split(filename+".py")[0]
        sys.path.append(poc_path)
        poc = imp.load_source('audit', path)
        audit_function = poc.audit
        return audit_function

    def get_vul_info(self, poc):
        vul_info = {
            'name': self.plugins_name,
        }
        return vul_info

    def run(self, target, path):
        try:
            target +='/'
            audit_function = self.import_poc(path)
            #assign_function = self.import_poc(path)
            sys.path.append(PLUGINS_DIR+'bugscan/')
            from dummy import *
            audit_function.func_globals.update(locals())
            ret = audit_function(target)
            return self.result
        except Exception,e:
            print e
            return self.result
            


class Poc_Launcher(object):

    gevent_num = 100            # 协程数
    process_num = 5             # 进程数
    count = 0   # 每个进程，单独计数
    progress = 100              # 进度提醒的单位

    def __get_pocs_count(self, poc_files):
        return len(poc_files)

    def save_result(self, target, poc_file, result):
        result = str(result)
        save_result_api_addr = SAVE_RESULT_API
        post = {
             'target': target,
             'poc_file': poc_file,
             'result': result,

        }
        req.post(url=save_result_api_addr, data=post)
        return result

    def poc_verify(self, target, poc_file = 'cms_recognition.py'):
        #poc_file = 
        result = Bugscan.run(target, poc_file)
        if result.get('result', False):
            self.save_result(target, poc_file, result.get('result'))
        return result




