#!usr/bin/evn python
# -*- coding:utf-8 -*-

import threading
import re

from  login import Weibo
from get_datas import main_thread, worker_thread
from recommend import user_reommendations

class GetUriData(threading.Thread):
    """get user id"""
    def __init__(self, uri_s):
        threading.Thread.__init__(self)
        self.uri_s = uri_s

    def run(self):
        worker_thread()

    def stop(self):
        pass

def main():
    user = raw_input("Input your sina username: ")
    pwd = raw_input("Input your sina password:")
    weibo = Weibo(user, pwd)
    if weibo.login():
        print "-"*40
        #get my follow and fans.
        w_uris, s_uris ,follow_list, fans_list = main_thread(weibo)
        print "myfollow's follow and fans!"
        worker_thread(weibo, w_uris)   #myfollow's follow and fans
        print '\n'
        print "myfans's follow and fans!"
        worker_thread(weibo, s_uris)        #myfans's follow and fans
    recommendationuser = user_reommendations("richard")
    print recommendationuser
    for uid in recommendationuser:
        #content = weibo.urlopen("http://weibo.com/" + str(uid) + "/follow?rightmod=1&wvr=6").read()
        print "http://weibo.com/" + str(uid) + "/follow?rightmod=1&wvr=6"
if __name__ == "__main__":
    print "-"*40
    main()