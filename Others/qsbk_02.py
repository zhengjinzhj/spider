# !/usr/bin/python
# filename: qsbk_02.py

# -*- coding: utf-8 -*-

import urllib2
import re


class QSBK:
    def __init__(self):
        self.pageindex = raw_input("please enter the page number:")
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': self.user_agent}

    def getpage(self):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(self.pageindex)
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            pagecode = response.read().decode('utf-8')
            pattern = re.compile('<div.*?author.*?>.*?<img.*?>.*?<h2>(.*?)</h2>.*?<div.*?' +
                                 'content">(.*?)</div>(.*?)<div class="stats.*?class="number">(.*?)</i>', re.S)

            items = re.findall(pattern, pagecode)

            for item in items:
                haveimg = re.search("img", item[2])
                if not haveimg:
                    replacebr = re.compile('<br/>')
                    text = re.sub(replacebr, "\n", item[1])
                    print item[0], item[3], text

        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason
            return None


spider = QSBK()
spider.getpage()
