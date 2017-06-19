#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import requests
import datetime

logger = logging.getLogger('')
logger.setLevel(logging.DEBUG)

# log format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# console log
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)


user_agent = ('User-Agent:Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) '
              'AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5')
session = requests.session()
session.headers['User-Agent'] = user_agent


def get_cookie():
    with open('jd_cookie.txt') as f:
        cookies = {}
        for line in f.read().split(';'):
            name, value = line.strip().split('=', 1)
            cookies[name] = value
    f.close()
    return cookies


def get_coupon():
    timer = '2017-06-19 14:09'  # 抢券时间
    # 抢券url
    coupon_url = 'https://coupon.m.jd.com/coupons/show.action?key=705a9053c1bb4507b5aa5d857bff15cb&roleId=6729255&to=sale.jd.com/m/act/ZFMnErV8z0tAGxs1.html'
    test_url = 'https://coupon.m.jd.com/center/receiveCoupon.json?couponId=146106&roleId=5368B169A2115E2BF4B11EBE0DFE4846&actId=3039B4CCB3FCF148F02AB1F67F517E349929C4D613B44F6E5E092EA85A6D12EA50AC93F8FAD90D456227C60734534054&takeRule=5'
    # 抢券referer
    referer = 'https://sale.jd.com/m/act/ZFMnErV8z0tAGxs1.html'
    test = 'https://coupon.m.jd.com/center/getCouponCenter.action'
    while True:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        if now == timer:
            cj = requests.utils.cookiejar_from_dict(get_cookie())
            session.cookies = cj
            resp = session.get(url=coupon_url, headers={'Referer': referer, })
            logger.info(resp.text)
            break


if __name__ == '__main__':
    get_coupon()

