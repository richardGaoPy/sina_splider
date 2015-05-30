
# -*- coding: utf-8 -*-
import urllib
import urllib2
import cookielib
import base64
import re
import json
import hashlib,rsa,binascii
import webbrowser
cj = cookielib.LWPCookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
urllib2.install_opener(opener)
postdata = {
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

    print '********get:servertime, nonce...********'
    try:
       r = re.compile(r'\((.*)\)')
       json_data = re.findall(r,data)
       data = eval(json_data[0])
       nonce = data['nonce']
       servertime = str(data['servertime'])
       #print data['pubkey']
       #print data['rsakv']
       #print servertime,nonce
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
    #print rsaPublickey
    key = rsa.PublicKey(rsaPublickey, 65537) #创建公钥
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(pwd) #拼接明文js加密文件中得到
    passwd = rsa.encrypt(message, key) #加密
    passwd = binascii.b2a_hex(passwd) #将加密信息转换为16进制。
    return passwd

def login():
    username = 'drehunlichenan@sina.com'
    pwd = 'gp5106*smdyw'
    url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
    try:
        servertime, nonce = get_servertime()
    except:
        return
    global postdata
    postdata['servertime'] = servertime
    postdata['nonce'] = nonce
    postdata['su'] = get_user(username)
    postdata['sp'] = get_pwd(pwd, servertime, nonce)
    postdata = urllib.urlencode(postdata)
    headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0'}
    req  = urllib2.Request(url = url,data = postdata,headers = headers)
    result = urllib2.urlopen(req)
    text = result.read()


    p = re.compile('location\.replace\(\'(.*?)\'\)')

    try:

        login_url = p.search(text).group(1)
        #webbrowser.open(login_url)
        urllib2.urlopen(login_url)

        html = urllib2.urlopen("weibo.com/2792942741/follow?rightmod=1&wvr=6")
        print '########welcome sina weibo###'
        #response = urllib2.urlopen('weibo.com/2792942741/follow?rightmod=1&wvr=6')
        text = html.read()
        fy = open("resu.html", 'w')
        fy.write(text)
        fy.close()

    except:
        print 'Login error!'
if __name__ == '__main__':
     #print 'sdf'
     #servertime,nonce = get_servertime()
     #print get_pwd('密码','sertime','nonce')
     login()