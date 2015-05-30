#!usr/bin/evn python
# -*- coding:utf-8 -*-

import urllib
import urllib2
import cookielib
import base64
import rsa
import binascii
import re
import json

cj = cookielib.LWPCookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
urllib2.install_opener(opener)

post_data = {
    'entry':'weibo',
    'gateway':'1',
    'from':'',
    'savestate':'7',
    'useticket':'1',
    'vsnf':'1',
    'su':'',
    'service':'miniblog',
    'servertime':'',
    'nonce':'',
    'pwencode':'rsa2',
    'rsakv':'',
    'sp':'',
    'encoding':'UTF_8',
    'url':'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
    'returntype':'META'
}

def get_servertime(username):
    url = "http://login.sina.com.cn/sso/prelogin.php?" \
          "entry=weibo&callback=sinaSSOController.preloginCallBack&su=%s&client=ssologin.js(v1.4.18)" % username
    data = urllib2.urlopen(url).read()
    p = re.compile('\((.*)\)')
    try:
        json_data = p.search(data).group(1)
        data = json.loads(json_data)
        servertime = str(data['servertime'])
        nonce = data['nonce']
        pubkey = data['pubkey']
        rsakv = data['rsakv']
        return servertime, nonce, pubkey, rsakv
    except:
        print "Get servertime or nonce error!"
        return None

def get_user(username):
    username_ = urllib.quote(username)
    username = base64.encodestring(username_)[:-1]
    return username

def get_password(password, servertime, nonce, pubkey):
    rsa_public_key = int(pubkey, 16)
    key = rsa.PublicKey(rsa_public_key, 65537)
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)
    passwd = rsa.encrypt(message, key)
    passwd = binascii.b2a_hex(passwd)
    return passwd

def get_account(filename):
    f = file(filename)
    flag = 0
    for line in f:
        if flag == 0:
            username = line.strip()
            flag += 1
        else:
            pwd = line.strip()
    f.close()
    return username, pwd

def login(filename):
    username, pwd = get_account()

    url = "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)"
    try:
        servertime, nonce, pubkey, rsakv = get_servertime(username)
    except:
        print "get servertime error!"
        return
    post_data['servertime'] = servertime
    post_data['nonce'] = nonce
    post_data['rsakv'] = rsakv
    post_data['su'] = get_user(username)
    post_data['sp'] = get_password(pwd, servertime, nonce, pubkey)
    post_data = urllib.urlencode(post_data)

    headers = {
        'User-Agent':"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0"
    }

    req = urllib2.Request(
        url = url,
        data = post_data,
        headers = headers
    )

    result = urllib2.urlopen(req)
    text = result.read()
    p = re.compile('location\.replace\"(.*)\"')
    try:
        login_url = p.search(text).group(1)
        urllib2.urlopen(login_url)
        print "login success!"
        return 1
    except:
        print "login error!"
        return 0

if __name__ == "__main__":
    filename = './config/account'
    web_login = login(filename)
    if web_login == 1:
        print "login success!"
    else:
        print "login error!"
