#!/usr/bin/evn python
# -*- coding:utf-8 -*-

import re
import threading

from login import Weibo

def main_thread(url="http://weibo.com"):
    """"""
    # =========== my main page ============
    with open('down.html', 'w') as f:
        print >> f, weibo.urlopen(url).read()
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

    #print url1, follow_num
    #print url2, fans_num

    fans_uri_list = list()

    # ========= myfollow list===============
    with open('follow1.html', 'w') as f:
        print >> f, weibo.urlopen(url1).read()
    fp = open('follow1.html', 'r')
    textw = fp.read()
    fp.close()
    pp = re.compile('page_id(.+);')
    result_w = pp.search(textw).group(1)
    result_w = re.search('(\d+)', result_w).group(1)

    #print result_w
    follow_uri_list = list()
    total_follow_page_num = (int(follow_num) / 30) + 1
    for page_num in xrange(1, total_follow_page_num+1):
        follow_uri_list_i = list()
        url_follow = "http://weibo.com/p/" + str(result_w) + \
                    "/myfollow?t=1&cfs=&Pl_Official_RelationMyfollow__104_page=" + str(page_num) + "#Pl_Official_RelationMyfollow__104"
        #   follow_uri_list.append(url_follow)
        filename = "myfollow_%s.html" % page_num
        with open(filename, 'w') as f:
            print >> f, weibo.urlopen(url_follow).read()

        f = open(filename, 'r')
        data = f.read()
        f.close()

        data = data.replace('\\', '')

        p = re.compile('<ul class="member_ul clearfix" node-type="relation_user_list">(.+)</ul>')
        result = p.search(data).group(1)
        result = result.replace('rn', '')
        pl = re.compile('action-data="uid=(\d+)&profile')
        data_list = pl.findall(result)
        # print data_list

        for uid in data_list:
            uri = "http://weibo.com/u/" + uid + "?from=myfollow_all"
            follow_uri_list_i.append(uri)

        follow_uri_list.extend(follow_uri_list_i)
    # print follow_uri_list
    # print follow_uri_list.__len__()

        # =========== get fans_uri ist ==================
    with open('fans1.html', 'w') as f:
        print >> f, weibo.urlopen(url2).read()
    fp = open('fans1.html', 'r')
    texts = fp.read()
    fp.close()

    ps = re.compile('page_id(.+);')
    result_s = ps.search(texts).group(1)
    result_s = re.search('(\d+)', result_s).group(1)

    fans_uri_list = list()
    total_fans_page_num = (int(fans_num) / 20) + 1
    for page_num in xrange(1, total_fans_page_num+1):
        fans_uri_list_i = list()
        url_fans = "http://weibo.com/p/" + str(result_s) + \
                    "/follow?relate=fans&page=" + str(page_num) + "#Pl_HisRelation__61"
        filename = "myfans_%s.html" % page_num
        with open(filename, 'w') as f:
            print >> f, weibo.urlopen(url_fans).read()

        f = open(filename, 'r')
        data_s = f.read()
        f.close()

        data_s = data_s.replace('\\', '')

        p = re.compile('<ul class="follow_list">(.+)</ul>')
        result = p.search(data_s).group(1)
        p1 = re.compile('usercard="id=(\d+)"')
        result_fs = p1.findall(result)
        result_fs = set(result_fs)
        # print result_fs

        for usercard in result_fs:
            uri = "http://weibo.com/u/" + usercard + "?from=myfollow_all"
            fans_uri_list_i.append(uri)
        fans_uri_list.extend(fans_uri_list_i)
    # print fans_uri_list
    # print fans_uri_list.__len__()

    return follow_uri_list, fans_uri_list , data_list, result_fs


# son_thread run function
# fans de follow and fans
def worker_thread(weibo, uris):
    print "begain son thread."
    #main_thread()
    i = 0
    for uri in uris:
        text = weibo.urlopen(uri).read()
        text = text.replace('\\', '')
        p = re.compile('page_id(.+);')
        result = p.search(text).group(1)
        result = re.search('(\d+)', result).group(1)

        p2 = re.compile('<strong class="W_f18">(\d+)</strong>')
        result_2 = p2.findall(text)

        follow_page_total = (int(result_2[0]) / 20) + 1
        fans_page_total = (int(result_2[1]) / 20) + 1

        follow_list = list()
        fans_list = list()
        for i in xrange(1, follow_page_total):
            url_w = "http://weibo.com/p/" + str(result) + \
                "/follow?page=" + str(i) + "#Pl_Official_HisRelation__61"
            text = weibo.urlopen(url_w).read()
            text = text.replace('\\', '')
            pl = re.compile('action-data="uid=(\d+)&fnick')
            data_list = pl.findall(text)
            follow_list.extend(data_list[1:-1])
        for j in xrange(1, fans_page_total):
            url_s = "http://weibo.com/p/" + str(result) + \
                    "/follow?relate=fans&page=" + str(j) + "#Pl_Official_HisRelation__61"
            text = weibo.urlopen(url_s).read()
            text = text.replace('\\', '')
            pl = re.compile('action-data="uid=(\d+)&nick')
            data_list = pl.findall(text)
            fans_list.extend(data_list[1:-1])
        print "================================================="
        #sina limit user number.
        print follow_list
        print follow_list.__len__()
        print fans_list
        print fans_list.__len__()

if __name__ == "__main__":
    weibo = Weibo('drehunlichenan@sina.com', 'gp5106*smdyw')
    if weibo.login():
        w_uris, s_uris ,follow_list, fans_list= main_thread()
        print w_uris
        print s_uris
        worker_thread(weibo, s_uris)
        worker_thread(weibo, w_uris)