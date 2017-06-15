#coding=utf-8

#http://icp.aizhan.com/geticp/?host=suning.com&style=1
import requests

domain = 'suning.com'
 
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
if len(_tmplist)  == 3:
    icp_code = _tmplist[1].split('-')[0]
    #icp_code = 
print icp_code