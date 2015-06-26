#!/usr/bin/evn python
# -*- coding:utf -*-

import base64
import binascii
import cookielib
import json
import os
import random
import re
import rsa
import time
import urllib
import urllib2
import urlparse

import webbrowser

__client_js_ver__ = 'ssologin.js(v1.4.18)'

class Weibo(object):

    """"Login Sina weibo."""

    def __init__(self, username, password):
        self.username = self.__encode_username(username).rstrip()
        self.password = password

        # get a cookie obj
        cj = cookielib.LWPCookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

    @staticmethod
    def __encode_username(username):
        return base64.encodestring(urllib2.quote(username))

    @staticmethod
    def __encode_password(password, info):
        key = rsa.PublicKey(int(info['pubkey'], 16), 65537)
        msg = ''.join([
            str(info['servertime']),
            '\t',
            str(info['nonce']),
            '\n',
            str(password)
        ])
        return binascii.b2a_hex(rsa.encrypt(msg, key))

    def __prelogin(self):
        """get before info for check image"""
        url = ('http://login.sina.com.cn/sso/prelogin.php?'
               'entry=weibo&callback=sinaSSOController.preloginCallBack&rsakt=mod&checkpin=1&'
               'su={username}&_={timestamp}&client={client}'
               ).format(username=self.username, timestamp=int(time.time() * 1000), client=__client_js_ver__)

        resp = urllib2.urlopen(url).read()
        return self.__prelogin_parse(resp)

    @staticmethod
    def __prelogin_parse(resp):
        p = re.compile('preloginCallBack(.+)')
        data = p.search(resp).group(1)
        data = json.loads(data[1:-1])
        return data

    @staticmethod
    def __process_verify_code(pcid):
        url = 'http://login.sina.com.cn/cgi/pin.php?r={randint}&s=0&p={pcid}'.format(
            randint=int(random.random() * 1e8), pcid=pcid)
        filename = 'pin.png'
        if os.path.isfile(filename):
            os.remove(filename)

        urllib.urlretrieve(url, filename)
        if os.path.isfile(filename):        #get verify code successfully
            #  display the code and require to input
            from PIL import Image
            import subprocess
            filename = os.getcwd() + '/' + filename
            proc = subprocess.Popen(['eog', filename])
            code = raw_input(u'Enter check code:')
            os.remove(filename)
            proc.kill()
            print pcid, code
            return dict(pcid=pcid, door=code)
        else:
            return dict()

    def login(self):
        info = self.__prelogin()

        login_data = {
            'entry': 'weibo',
            'gateway': '1',
            'from': '',
            'savestate': '7',
            'useticket': '1',
            'pagerefer': '',
            'pcid': '',
            'door': '',
            'vsnf': '1',
            'su': '',
            'service': 'miniblog',
            'servertime': '',
            'nonce': '',
            'pwencode': 'rsa2',
            'rsakv': '',
            'sp': '',
            'sr': '',
            'encoding': 'UTF-8',
            'prelt': '115',
            'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype': 'META'
        }
        if ('showpin' in info) and info["showpin"]:    # need to input verify code
            login_data.update(self.__process_verify_code(info['pcid']))
        login_data['servertime'] = info['servertime']
        login_data['nonce'] = info['nonce']
        login_data['rsakv'] = info['rsakv']
        login_data['su'] = self.username
        login_data['sp'] = self.__encode_password(self.password, info)

        return self.__do_login(login_data)

    def __do_login(self, data):
        url = 'http://login.sina.com.cn/sso/login.php?client=%s' % __client_js_ver__
        headers = {
            'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0"
        }
        req = urllib2.Request(
            url=url, data=urllib.urlencode(data), headers=headers)
        resp = urllib2.urlopen(req).read()
        return self.__parse_real_login_and_do(resp)

    def __parse_real_login_and_do(self, resp):
        p = re.compile('location\.replace\(\'(.*?)\'\)')
        url = p.search(resp).group(1)

        # check login seccess
        query = urlparse.parse_qs(urlparse.urlparse(url).query)
        if int(query['retcode'][0]) == 0:       #successful
            #print query['retcode'][0]
            self.opener.open(url)       #log in and get cookies
            print u'Login success!'
            return True
        else:  # fail
            print u'Error Number:', query['retcode'][0]
            print u'Error Log:', query['reason'][0].decode('gbk')
            return False

    def urlopen(self, url="http://weibo.com"):
        return self.opener.open(url)

# if __name__ == "__main__":
#     weibo = Weibo('username', 'password')
#     if weibo.login():
#         with open('myhome.html', 'w') as f:
#             print >> f, weibo.urlopen().read()
