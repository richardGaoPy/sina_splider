#!/usr/bin/evn python
# -*- coding:utf-8 -*-

import threading
import urllib2
import webbrowser
import re

from pyquery import PyQuery as pq
from lxml import etree
import json

from login import Weibo

def main_thread():
    weibo = Weibo('drehunlichenan@sina.com', 'gp5106*smdyw')
    if weibo.login():
        with open('down.html', 'w') as f:
            print >> f, weibo.urlopen('http://weibo.com').read()
    fp = open('down.html', 'r')
    text = fp.read()
    fp.close()
    text = text.replace('\\', '')
    p1 = re.compile('<li class="S_line1">(.+)<span class="S_txt2">')
    result_1 = p1.findall(text)
    result_1 = result_1[0].replace(' ','')

    #pipei uri
    ph = re.compile('href="(.+)"class="S_txt1"><strongnode-type="follow">')
    result_h = ph.findall(result_1)

    #pipei follow, fans number
    p2 = re.compile('<strongnode-type="follow">(\d+)</strong>')
    result_2 = p2.findall(result_1)
    p3 = re.compile('<strongnode-type="fans">(\d+)</strong>')
    result_3 = p3.findall(result_1)

    #print result_h, result_2, result_3

    url1 = 'http://weibo.com' + result_h[0]
    result_s = result_h[0].replace('follow', 'fans')
    url2 = 'http://weibo.com' + result_s
    follow_num = int(result_2[0])
    fans_num = int(result_3[0])

    print url1, follow_num
    print url2, fans_num

    follow_uri_list = list()
    fans_uri_list = list()

    # ========= myfollow page ===============
    with open('follow1.html', 'w') as f:
        print >> f, weibo.urlopen(url1).read()
    fp = open('follow1.html', 'r')
    textw = fp.read()
    fp.close()
    pp = re.compile('page_id(.+);')
    result_w = pp.search(textw).group(1)
    result_w = re.search('(\d+)', result_w).group(1)

    #print result_w
    total_follow_page_num = (int(follow_num) / 30) + 1
    for page_num in xrange(1, total_follow_page_num+1):
        url_follow = "http://weibo.com/p/" + str(result_w) + \
                    "/myfollow?t=1&cfs=&Pl_Official_RelationMyfollow__104_page=" + str(page_num) + "#Pl_Official_RelationMyfollow__104"
        follow_uri_list.append(url_follow)

    # ========== fans page ============

     #myfollow page
    with open('fans1.html', 'w') as f:
        print >> f, weibo.urlopen(url2).read()
    fp = open('fans1.html', 'r')
    texts = fp.read()
    fp.close()
    pp = re.compile('page_id(.+);')
    result_s = pp.search(texts).group(1)
    result_s = re.search('(\d+)', result_s).group(1)

    #print result_w
    total_fans_page_num = (int(fans_num) / 30) + 1
    for page_num in xrange(1, total_fans_page_num+1):
        url_follow = "http://weibo.com/p/" + str(result_w) + \
                    "/myfollow?t=1&cfs=&Pl_Official_RelationMyfollow__104_page=" + str(page_num) + "#Pl_Official_RelationMyfollow__104"
        follow_uri_list.append(url_follow)
if __name__ == "__main__":
    main_thread()