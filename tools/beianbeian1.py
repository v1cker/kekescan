#!/usr/bin/env python
# coding=utf-8
# code by evileo

import lxml.html
import requests

import requests


from tld import get_tld
from tld.utils import update_tld_names
update_tld_names()
import MySQLdb



 
import re

def _get_beiandomain(domain,db,cursor):
    url = 'http://icp.aizhan.com/geticp/?host=%s&style=1' % domain
    print url
    f = requests.get(url, timeout = 3, allow_redirects = True)
    content = f.content
    if f.encoding.lower() != 'utf-8':
        charset = re.compile(r'content="text/html;.?charset=(.*?)"').findall(content)
        print charset, f.encoding.lower(), f.headers['content-type']
        try:
            if len(charset)>0 and charset[0].lower()!=f.encoding.lower():
                content = content.decode('gbk').encode('utf-8')
        except:
            pass
            
    _tmplist = str(content).split("'")
    #print _tmplist
    if len(_tmplist)  == 3:
        if '-' in  _tmplist[1][-2:]:
            icp_code = _tmplist[1][:-2]
        else:
            icp_code = _tmplist[1]
     
 
    try:
        icp_code ==1
    except:
        icp_code = 'undefine'
    sql = "INSERT INTO app_domainbeian(domain_name,  icp_code, insert_time)  VALUES ('%s', '%s',NOW() )" % \
                           (domain, icp_code)
    #print sql
    cursor.execute(sql)
  
    db.commit()

if __name__ == '__main__':
    
    db = MySQLdb.connect("127.0.0.1","root","wenjunnengyoujiduochou","xlcscan",charset='utf8')
    cursor = db.cursor()
    
    #domain = 'qq.com'
    for i in open('domain.txt'):
        domain = i.strip()
        print domain
        _get_beiandomain(domain,db,cursor)
    db.close()
