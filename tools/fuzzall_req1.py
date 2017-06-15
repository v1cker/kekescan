import httplib
import urlparse
 
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
 
if __name__ == '__main__':
    cookie_str = 'Cookie:XSRF-TOKEN=eyJpdiI6ImdcL3g0VE1nM2lwTXoyN2lIelc1Um9BPT0iLCJ2YWx1ZSI6InFkWG5od1NQRnJaeUsyNHVOQWprTGV6NEhlQXRkNUo3cTlFXC9KcGk4QXQ3bHVWbjFOU2RQTEJqWVpiNWJCZ1RLdVwvQzYwWkxVZklGQjZJbHl3eTVpWWc9PSIsIm1hYyI6IjRlMDM2ODYwNmM5Y2Q4NGZhZTQ2ZGMwYTdlMTQxNzQ5YzU2Zjc4MDE4ZTc4NTdjZmY3NzczMTJjNGUxMzhmNTUifQ%3D%3D; fa_session=eyJpdiI6IitqR1lnVjZyNVBxWUJTM0hCUFR2VEE9PSIsInZhbHVlIjoib2gwUUdnSEFaaUhcL1JIWXhPK2ZWQWpcL0V4U0gzNDJacjVFeVlYU2c3azNvYklXMUw2bW45TTZMRVFzNGg1U0xhVDIrRGN0ZWpyRnppV1FDU2V6ZW56QT09IiwibWFjIjoiMTg5OTZhMmU0MjEzZTA5YTk3NDRlZTU5ODgyOGIyNjUwOTE3YjM2ZjE5MmE0M2QxYWQxYTNiZTM2OWM0ZDFhZCJ9; _ga=GA1.2.1590040800.1461128225'
    url = 'http://www.fuzzall.com/'
    html_doc = request(url, cookie_str).read()
    print html_doc
    
'''
session_requests = requests.session()

login_url = "http://www.fuzzall.com/login"
result = session_requests.get(login_url)

tree = html.fromstring(result.text)
authenticity_token = list(set(tree.xpath("//input[@name='_token']/@value")))[0]

global header_info
header_info = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
    'Host':'www.fuzzall.com',
    #'Origin':'http://www.fuzzall.com',
    'Location':'http://www.fuzzall.com',
    'Connection':'keep-alive',
    'Referer':'http://www.fuzzall.com/',
    'Content-Type':'text/html; charset=UTF-8',
    }

print authenticity_token
payload = {
    "username": "2018295280@qq.com", 
    "password": "ruijiangmei", 
    "_token": authenticity_token
}
print payload
result = session_requests.post(
    'http://www.fuzzall.com/login', 
    data = payload, 
    headers = header_info
)
#print result.text
print requests.utils.dict_from_cookiejar(session_requests.cookies)


url = 'http://www.fuzzall.com/'
result = session_requests.get(
    url, 
    headers = header_info
)


print result.text
print requests.utils.dict_from_cookiejar(session_requests.cookies)
'''
