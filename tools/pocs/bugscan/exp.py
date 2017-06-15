# -*- coding: utf-8 -*-
from dummy import *
from miniCurl import Curl
curl = Curl()
import urlparse
from miniCurl import  Curl 
curl = Curl()
from dummy import *

def assign(service, arg):
    if service != "www":
        return
    arr = urlparse.urlparse(arg)
    return True, '%s://%s/' % (arr.scheme, arr.netloc)

def audit(arg):
    url = arg
    code, head, res, errcode, _ = curl.curl(url)
    if code == 200:
        security_info(url)

if __name__ == '__main__':
    from __loader import *
    audit(assign('www', 'http://www.jjoobb.cn/')[1])
    audit(assign('www', 'http://hbjw.gov.cn/web/')[1])
    audit(assign('www', 'http://www.hbjw.gov.cn/')[1])
