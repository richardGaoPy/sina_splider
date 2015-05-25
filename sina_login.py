#!/usr/bin/evn python
# -*- coding:utf-8 -*-

import urllib
import urllib2
import cookielib
import base64
import re
import json
import hashlib

cj = cookielib.LWPCookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
urllib2.install_opener(opener)

post_data = {
    'entry': 'weibo',
    'gateway': '1',
    'from': '',
    'savestate': '7',
    'userticket': '1',
    'ssosimplelogin': '1',
    'vsnf': '1',
    'vsnval': '',
    'su': '',
    'service': 'miniblog',
    'servertime': '',
    'nonce': '',
    'pwencode': 'rsa2',
    'sp': '',
    'encoding': 'UTF-8',
    'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
    'returntype': 'META',
    }

def get_server_time():
    '''获取服务器时间或随机数'''
    url = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&" \
          "su=ZHJlaHVubGljaGVuYW4lNDBzaW5hLmNvbQ==&client=ssologin.js(v1.4.18)&_=1431319512528"
    data = urllib2.urlopen(url).read()
    p = re.compile('\((.*)\)')
    try:
        json_data = p.search(data).group(1)
        data = json.loads(json_data)
        servertime = str(data['servertime'])
        nonce = data['nonce']
        return servertime, nonce
    except:
        print 'Get server info failed!'
        return None

def get_user(username):
    '''通过base64计算username'''
    username_ = urllib.quote(username)
    username = base64.encodestring(username_)[:-1]
    return username

def get_pwd(pwd, s_time, nonce):
    '''通过3次hash.sha1计算password'''
    pwd1 = hashlib.sha1(pwd).hexdigest()
    pwd2 = hashlib.sha1(pwd1).hexdigest()
    pwd3 = hashlib.sha1(pwd2+s_time+nonce).hexdigest()
    return pwd3

if __name__ == "__main__":
    print '='*36
    # s, n = get_server_time()
    # user = get_user("drehunlichenan%40sina.com")
    # pwd = get_pwd("gp5106*smdyw", '1432518594', 'NY4XQP')
    # print user
    # print s, n
    # print pwd
    username = 'drehunlichenan@sina.com'  # 微博账号
    pwd = 'gp5106*smdyw'  # 微博密码
    url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
    servertime, nonce = get_server_time()
    postdata = {}
    postdata['servertime'] = servertime
    postdata['nonce'] = nonce
    postdata['su'] = get_user(username)
    postdata['sp'] = get_pwd(pwd, servertime, nonce)
    postdata = urllib.urlencode(postdata)
    headers = {'User-Agent':'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0'}

    req = urllib2.Request(
        url=url,
        data=postdata,
        headers=headers
    )
    print req
    result = urllib2.urlopen(req)
    text = result.read()
    p = re.compile('location\.replace\(\'(.*?)\'\)')
    try:
        print "*"*20
        login_url = p.search(text).group(1)
        urllib2.urlopen(login_url)
        print "login success"
    except:
        print 'Login error!'
    # 测试读取数据，下面的URL，可以换成任意的地址，都能把内容读取下来
    req = urllib2.Request(url='http://e.weibo.com/aj/mblog/mbloglist?page=1&count=15&max_id=3463810566724276&pre_page=1&end_id=3458270641877724&pagebar=1&_k=134138430655960&uid=2383944094&_t=0&__rnd=1341384513840',)
    result = urllib2.urlopen(req)
    text = result.read()
    print len(result.read())
