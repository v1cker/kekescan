# -*-coding:UTF-8 -*-
from urllib import urlretrieve
import re

def getWooyunUrl():
    L = []
    for i in range(1, 44):
        url = "http://www.wooyun.org/corps/page/" + str(i)
        try:
            revtal = urlretrieve(url)[0]
        except IOError:
            revtal = None
        f = open(revtal)
        lines = ''.join(f.readlines())
        regex = '_blank">(.*)</a'
        for m in re.findall(regex, lines):
            if(m[0] == 'h'):
                L.append(m)
    L = [line + '\n' for line in L]
    f = open("wooyun.txt", 'w')
    f.writelines(L)
    f.close()

if __name__ == '__main__':
    getWooyunUrl()
