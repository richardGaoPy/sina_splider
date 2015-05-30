#!/usr/bin/evn python
# -*- coding:utf-8 -*-

import urllib
import urllib2
import cookielib
import re
import base64
import rsa
import binascii

web_login_url = "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)"
check_code_url = "http://login.sina.com.cn/cgi/pin.php?p=xd-c304d604f2879ec7a43a89800f82c551e046&r=1432875188601"

headers = {
    "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Host":"login.sina.com.cn",
    "Referer":"http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)"
}

username = "drehunlichenan@sina.com"
password = "gp5106*smdyw"

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
    'rsakv' :'1330428213',
    'pagerefer':'http://login.sina.com.cn/sso/logout.php?entry=miniblog&r=http%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl%3D%252F'
}

def get_servertime():
    url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=eGlnZTg2MDAyMTUxOSU0MHNpbmEuY29t&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)&_=1412755829501'
    data = urllib2.urlopen(url).read()

    print '********get:servertime, nonce...*********'
    try:
       r = re.compile(r'\((.*)\)')
       json_data = re.findall(r,data)
       data = eval(json_data[0])
       nonce = data['nonce']
       servertime = str(data['servertime'])
       return servertime,nonce
    except:
        print 'Get severtime error!'
        return None

def get_user(username):
    username = base64.encodestring(urllib.quote(username))[:-1]
    return username

def get_pwd(pwd, servertime, nonce):
    pubkey = 'EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D245A87AC253062882729293E5506350508E7F9AA3BB77F4333231490F915F6D63C55FE2F08A49B353F444AD3993CACC02DB784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928EE0CCEE1F6739884B9777E4FE9E88A1BBE495927AC4A799B3181D6442443'
    rsaPublickey = int(pubkey, 16)
    key = rsa.PublicKey(rsaPublickey, 65537)
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(pwd)
    passwd = rsa.encrypt(message, key)
    passwd = binascii.b2a_hex(passwd)
    return passwd

def login_weibo():
    global check_code_url
    cookiejar = cookielib.LWPCookieJar()
    cookieSupport = urllib2.HTTPCookieProcessor(cookiejar)
    opener = urllib2.build_opener(cookieSupport, urllib2.HTTPHandler)
    urllib2.install_opener(opener)

    send_data(web_login_url, post_data, headers)

def send_data(url, data, header):
    global post_data
    servertime, nonce = get_servertime()
    post_data['servertime'] = servertime
    post_data['nonce'] = nonce
    post_data['su'] = get_user(username)
    post_data['sp'] = get_pwd(password, servertime, nonce)
    postdata = urllib.urlopen(post_data)
    req  = urllib2.Request(url = web_login_url,data = postdata,headers = headers)
    result = urllib2.urlopen(req)
    text = result.read()

    p = re.compile('location\.replace\(\'(.*?)\'\)')