#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from hashlib import md5
import random
import json
import os
import time
import re
from bs4 import BeautifulSoup

login_url = 'https://passport.jd.com/new/login.aspx'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
    'ContentType': 'text/html; charset=utf-8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
}

session = requests.session()
session.headers = headers

req1 = session.get(login_url, headers=headers)
soup = BeautifulSoup(req1.content, 'html.parser')
uuid = soup.find(id='uuid')['value']
eid = soup.find(id='eid')['value']
sa_token = soup.find(id='sa_token')['value']
pub_key = soup.find(id='pubKey')['value']
token = soup.find(id='token')['value']

r = random.random()
login_request_url = 'https://passport.jd.com/uc/loginService'


class JD:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.track_id = ''
        self.pid = ''

    def login(self):
        params = {
            'uuid': uuid,
            'eid': eid,
            '_t': token,
            'loginType': 'c',
            'loginname': self.username,
            'nloginpwd': self.password,
            'chkRememberMe': '',
            'authcode': '',
            'pubKey': pub_key,
            'sa_token': sa_token
        }
        headers2 = {
            'Referer': 'https://passport.jd.com/uc/login?ltype=logout',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

        img_code = 'http:' + soup.find(id='JD_Verification1')['src2']
        img = requests.get(img_code)
        with open(r'C:\Users\Administrator\PycharmProjects\work/a.jpg', 'wb') as f:
            f.write(img.content)
        im = open('a.jpg', 'rb').read()
        print('开始识别验证码...')

        #

        req2 = session.post(login_request_url, data=params, headers=headers2)
        patt = '<Cookie TrackID=(.*?) for .jd.com/>'
        self.track_id = re.compile(patt).findall(str(session.cookies))
        js = json.loads(req2.text[1:-1])
        print(js)


# demo = JD('zheng_jin', 'zhengjin341281')
# demo.login()












