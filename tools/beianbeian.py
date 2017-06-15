import lxml.html
import requests

import requests


from tld import get_tld
from tld.utils import update_tld_names
update_tld_names()
import MySQLdb






def _get_beiandomain(domain,db,cursor):
    url = 'http://icp.aizhan.com/geticp/?host=%s&style=1' % domain
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
     

    print icp_code

    url = 'http://www.beianbeian.com/s?keytype=1&q=%s' % icp_code
     
    headers = { }

    r = requests.get(url,   headers=headers)


    html = lxml.html.fromstring(r.text)

    rows = html.xpath('//table')


    if 1:
        tr = rows[0].xpath('.//tr')
 
        
        for k in tr:
            domain_list = {}
            c =  k.xpath('.//td//div//text()')
             
            if len(c) > 3:
                domain_list['company_name'] = c[0] 
                 
                domain_list['type'] = c[1] 
                #print c 
                if 1:
                     
                    domain_list['domain_name']  =   get_tld('http://'+c[2])
                     
                    print domain_list 
             
                    sql = "INSERT INTO app_domainbeian(domain_name, \
                           company_name, domain_type, icp_code, insert_time) \
                           VALUES ('%s', '%s', '%s', '%s',NOW() )" % \
                           (domain_list['domain_name'], domain_list['company_name'],domain_list['type'], icp_code.code("utf-8"))
                    print sql
                    cursor.execute(sql)
  
        db.commit()

if __name__ == '__main__':
    
    db = MySQLdb.connect("127.0.0.1","root","x","xlcscan" )
    cursor = db.cursor()
    domain = 'suning.com'
    
    _get_beiandomain(domain,db,cursor)
    db.close()
