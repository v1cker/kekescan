import httplib
import urlparse
import lxml
import lxml.html
import ast
import MySQLdb

def request(url, cookie=''):
    ret = urlparse.urlparse(url)    # Parse input URL
    if ret.scheme == 'http':
        conn = httplib.HTTPConnection(ret.netloc)
    elif ret.scheme == 'https':
        conn = httplib.HTTPSConnection(ret.netloc)
        
    url = ret.path
    if ret.query: url += '?' + ret.query
    if ret.fragment: url += '#' + ret.fragment
    if not url: url = '/'
    
    conn.request(method='GET', url=url , headers={'Cookie': cookie,'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'})
    return conn.getresponse()




def _to_db(html,db,cursor,domain_name):
    #print html
    html = lxml.html.fromstring(html)

    rows = html.xpath('//table')

    
    dic_domain = {}
    elements = rows[1].xpath('.//tr')
    print len(elements)
    if len(elements) < 2:
        return False
    for k in elements:
        c =  k.xpath('.//td//text()')
        
        if len(c) >1:
            for ip in ast.literal_eval(str(c[4])):
                
            #print c[0]
                dic_domain['id'] = int(c[0])
                dic_domain['sub_domain_name'] = c[2]
                dic_domain['ip'] = ip
                    
                dic_domain['find_time'] =c[5]
                #print dic_domain
                sql = "INSERT INTO app_subdomainbrute(domain_name, \
                       sub_domain, sub_ip, fuzz_time, fuzzall_id) \
                       VALUES ('%s', '%s', '%s', '%s', '%d' )" % \
                       (domain_name, dic_domain['sub_domain_name'], dic_domain['ip'], dic_domain['find_time'], dic_domain['id'])
                #print sql
                cursor.execute(sql)
  
    db.commit()
    return True     




if __name__ == '__main__':
    
    db = MySQLdb.connect("127.0.0.1","root","wenjunnengyoujiduochou","xlcscan" )
    cursor = db.cursor()

    cookie_str = 'Cookie:_gat=1; XSRF-TOKEN=eyJpdiI6IlJCY1UyNTN3QVAza1E5VHdQaytiUWc9PSIsInZhbHVlIjoiS0U1dm1aU1RqQTZnUHU4K2xpSG1GYmVCK2VtXC94RWlreGVpNWxwWld2SzJ0ajdcLzI5YlRtWm9PaDljU2VwbTJQWTgzYmdCOHcrQzlpUEVNNEpRbFNuUT09IiwibWFjIjoiYzg1ODU5NWJiM2Y0MmIyMzliZWZjNWJkNTcwODdmMGE5ODc2NDdkMWM5ZDI0ZTBlMGNlOWFjZmVlNTA1ZTkwYSJ9; fa_session=eyJpdiI6IkNyK29BZkpWTk5CanYwWTIrSzVCNWc9PSIsInZhbHVlIjoiMnNqXC9GcFhrWjRIaFR1aWd4Z0FuSE5nMHAySVk3bGk1aUlvMm5INERwMjZPaThFQm8rdlwvYVlVXC9Uc1NwSzVYTVFvSzFKRzIzekhMNHZ4cHdYaFNIUkE9PSIsIm1hYyI6IjE0YjM1ZDQ4MWNjMTM0NmQ5ODRlYjg0ZDcxMWM2Y2E0Zjg1M2YzYTBjMjliODQ3ZjYxMDJhMGYxMjlmZjI1M2UifQ%3D%3D; _ga=GA1.2.1590040800.1461128225'
    domain_list = open('domain.txt')
    for domain in domain_list:
        domain = domain.strip()
        
        Ta = True
        page = 1
        while Ta:
            print domain,page
            url = 'http://www.fuzzall.com/search/%s?page=%d' % (domain,page)
            html_doc = request(url, cookie_str).read()
            Ta = _to_db(html_doc,db,cursor,domain)
            page = page+1
            
    #print html_doc
    
    db.close()
