# coding: utf-8
import requests
from lxml.html import fromstring
import sys

def get_title(url):
    r = requests.get(url,timeout=3)
    tree = fromstring(r.content)
    tttt = tree.findtext('.//title')
    return tttt
    


if __name__ == '__main__':
    try:
        ff = open(sys.argv[1])
    except:
        print "Usage: get_title.py urllist.txt \n"
        sys.exit()
    res  = open('title_result_'+sys.argv[1],'a')
    for i in ff:
        i = i.strip()
        if 'http' in i:
            url = i
        else:
            url = "http://"+i
        try :
            tt = get_title(url)
            output =  url+" "+tt
            print output
        except:
            output =  url+" someting error"
        #print output
        #res.write(output+'\n')
    ff.close()
    res.close()
