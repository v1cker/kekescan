import lxml.html
import requests

import requests


from tld import get_tld
from tld.utils import update_tld_names
update_tld_names()
import MySQLdb


import random
 
def randHeader():
    
    head_connection = ['Keep-Alive','close']
    head_accept = ['text/html, application/xhtml+xml, */*']
    head_accept_language = ['zh-CN,fr-FR;q=0.5','en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3']
    head_user_agent = ['Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
                       'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
                       'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
                       'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11']
    
    
    header = {
        'Connection': head_connection[0],
        'Accept': head_accept[0],
        'Accept-Language': head_accept_language[1],
        'User-Agent': head_user_agent[random.randrange(0,len(head_user_agent))]
    }
    return header



from libs import chardet
import time 
def _get_beiandomain(db,cursor):

    f = open('beian.txt')
    for i in f:
        i = (i.strip()).split(',')
        
        #print i
        if len(i) <3:
            continue
        domain_name  = i[1]
        icp_code  = str(i[2])
        beian_id = int(i[0])
        if beian_id > 1151:
            
            url = 'http://www.beianbeian.com/s?keytype=1&q=%s' % icp_code

             
            headers = {'User-Agent':'Mozilla/6.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36' }

            r = requests.get(url,   headers=randHeader())


            html = lxml.html.fromstring(r.text)

            rows = html.xpath('//table')

        
            try:
                tr = rows[0].xpath('.//tr')
     
            except:
                print '>>>>',beian_id
                time.sleep(60)
                
            for k in tr:
                domain_list = {}
                c =  k.xpath('.//td//div//text()')
                 
                if len(c) > 3:
                    domain_list['company_name'] = c[0] 
                    #fencoding=chardet.detect(c[0] )
                    #print fencoding

                    domain_list['type'] = c[1] 
                    #print c 
                    if 1:

                        try:
                            domain_list['domain_name']  =   get_tld('http://'+c[2])
                        except:
                            domain_list['domain_name'] = c[2]
                         
                        #print domain_list 
                 
                        sql = "INSERT INTO app_domainbeian(domain_name,company_name, domain_type ,beian_id,insert_time) \
                               VALUES ( '%s','%s', '%s','%d',NOW())" % \
                               (domain_list['domain_name'],domain_list['company_name'],domain_list['type'],beian_id)
                        #print sql
                        print beian_id
                        cursor.execute(sql)
      
            db.commit()

def _ass_beian():
    for i in open('beian.txt'):
        i = i.split(',')
        #print i
        if len(i) >1:
            i[0] = i[0].strip()
            i[1] =  i[1].strip()
            tmp_list = i[1].split('-')
            #print tmp_list
            if len(tmp_list[-1])<5:
                tmp_list.pop()
            tmp = '-'.join(tmp_list)
            print i[0],',',tmp 
          
           #     print i[1][:-3]
if __name__ == '__main__':
    
    db = MySQLdb.connect("127.0.0.1","root","wenjunnengyoujiduochou","xlcscan",charset='utf8' )
    cursor = db.cursor()

    

    #_ass_beian()
    _get_beiandomain(db,cursor)
    db.close()
