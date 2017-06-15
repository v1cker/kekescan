#!/usr/bin/python
#coding: utf-8

"""
'########:::'#######::'##::::'##::::'###::::'####:'##::: ##::'######::
 ##.... ##:'##.... ##: ###::'###:::'## ##:::. ##:: ###:: ##:'##... ##:
 ##:::: ##: ##:::: ##: ####'####::'##:. ##::: ##:: ####: ##: ##:::..::
 ##:::: ##: ##:::: ##: ## ### ##:'##:::. ##:: ##:: ## ## ##:. ######::
 ##:::: ##: ##:::: ##: ##. #: ##: #########:: ##:: ##. ####::..... ##:
 ##:::: ##: ##:::: ##: ##:.:: ##: ##.... ##:: ##:: ##:. ###:'##::: ##:
 ########::. #######:: ##:::: ##: ##:::: ##:'####: ##::. ##:. ######::
........::::.......:::..:::::..::..:::::..::....::..::::..:::......:::

Check domains on same IP.

USAGE: python domains.py <-s/-c> <IP/DOMAIN>
       -s   Check domains on the same ip
       -c   Check domains on C
EXAMPLE: python domains.py -s 2.2.2.2
         python domains.py -s www.baidu.com
         python domains.py -c 2.2.2.2
         python domains.py -c www.baidu.com
"""

import lxml.html
import requests
import socket
import sys


class GetDomains(object):
    """
    Main Class.
    API: http://dns.aizhan.com/?q=IP
    """

    def __init__(self):
        pass

    def get_domain_num(self, ip):
        """
        Get num of pages.
        @rtype : int
        @param ip: the ip you want to search.
        """
        try:
            r = requests.get("http://dns.aizhan.com/?q=%s" % ip, timeout=5)
            r.close()
            html = lxml.html.fromstring(r.text)
            num = html.get_element_by_id("yhide").text

            return int(num)
        except Exception, e:
            print "[!]ERROR: %s" % e.message
            sys.exit(0)

    def get_domains(self, ip):
        """
        Get domains from http://dns.aizhan.com/index.php?r=index/getress&q=<IP>&page=<PAGE NUM>.
        @param ip: the ip you want to search.
        """
        print "[+]Check number of domains on %s..." % ip

        domain_num = self.get_domain_num(ip)
        page_num = domain_num / 20 + 1 if (domain_num % 20) else domain_num / 20
        domains = []

        print "[+]Number of domains: %d" % domain_num
        print "[+]Number of pages: %d" % page_num

        for i in range(1, page_num + 1):
            print "[+]Checking Page %d..." % i

            url = "http://dns.aizhan.com/index.php?r=index/getress&q=%s&page=%d" % (ip, i)
            try:
                r = requests.get(url, timeout=5)
                r.close()
                for j in r.json():
                    domain = j["domain"]
                    domains.append(domain)
            except Exception:
                continue

        domains = list(set(domains))

        print "[+]Confirming domains..."
        print "-" * 30 + "Results" + "-" * 30
        domains_confirmed = []
        for domain in domains:
            try:
                if socket.gethostbyname(domain) == ip:
                    print "[+]%s" % domain
                    domains_confirmed.append(domain)
            except Exception:
                continue
        print "-" * 67
        print "Total: %d domains" % len(domains_confirmed)
        print "-" * 67
        return domains_confirmed


def main():
    """
    Main Function.
    """
    g = GetDomains()
    ip = sys.argv[-1]
    ip = ip if (ip.replace(".", "").isdigit()) else socket.gethostbyname(ip)
    domains = {}

    if "-s" in sys.argv:
        domains[ip] = g.get_domains(ip)
    elif "-c" in sys.argv:
        ip1 = ".".join(ip.split(".")[:3]) + "."
        for i in range(1, 255):
            ip2 = ip1+str(i)
            domains[ip2] = g.get_domains(ip2)
    try:
        record = open("record.txt", "w")
        for i in domains:
            record.write(i+":\n")
            for j in domains[i]:
                record.write(j+"\n")
            record.write("\n")
        record.close()
    except Exception, e:
        print "[!]ERROR: record.txt can't be created."
        print "[!]%s" % e.message


if __name__ == "__main__":
    print __doc__
    if len(sys.argv) == 3:
        main()
