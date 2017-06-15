#coding:utf-8
import re,urllib
 
def gethtml(url):
  page = urllib.urlopen(url)
  html=page.read()
  return html
 
def getlink(html):
 
  link = re.findall(r'<td  align="left" style="padding-left:20px;">(.*?)</td>',html)
  #linklist = re.findall(link,html)
  return link
 
def save(links):
  f=open('360.txt','a')
  for i in links:
    f.write(i+"\n")
    #f.close()
    #print 'ok' 
 
for page in range(1, 200):
  url = "http://loudong.360.cn/company/lists/page/" +str(page)
  html = gethtml(url)
  print str(page)+"ye"
  links = getlink(html)
  print links
  save(links)
