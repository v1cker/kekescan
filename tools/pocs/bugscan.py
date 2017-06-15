#coding=utf-8
 
import imp
import sys

bugscan_name_list = ['xy']
PLUGINS_DIR = 'D:\\Projects\\xlcscan\\tools\\pocs\\'
 
class Bugscan(object):

    plugins_name = 'bugscan'
    result = {
        'vul_info': {},
        'result': {}
    }

    def import_poc(self, path):
        sys.path.append(PLUGINS_DIR+self.plugins_name)
        poc = imp.load_source('MyPoc', path)
        return poc

    def get_vul_info(self, poc):
        vul_info = {
            'name': poc.MyPoc.poc_info['poc']['name'],
            'desc': poc.MyPoc.poc_info['vul']['desc'],
        }
        return vul_info

    def run(self, target, path):
        try:
            poc = self.import_poc(path)
 
            ret = poc.audit(target)
            return ret
            '''
            if ret['success'] == True:
                self.result['vul_info'] = self.get_vul_info(poc)
                self.result['result'] = ret['poc_ret']
                return self.result
            else:
                return {}'''
        except Exception,e:
            print e
            return

if __name__ == '__main__':
    
    for plugin in bugscan_name_list:
        x = Bugscan()
        path = PLUGINS_DIR+'bugscan' + '\\' + plugin
        print plugin
        x.run('http://testphp.vulnweb.com', path)