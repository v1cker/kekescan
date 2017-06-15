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
    
    conn.request(method='GET', url=url , headers={'Cookie': cookie})
    return conn.getresponse()

url = 'http://www.fuzzall.com/report/baidu.com'

cookie_str = ''
html_doc = request(url, cookie_str).read()
print html_doc
