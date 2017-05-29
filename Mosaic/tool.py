# -*- coding:utf-8 -*-

import os
import requests
from bs4 import BeautifulSoup


proxy = {'http': '127.0.0.1:8087', 'https': '127.0.0.1:8087'}


# 抓取页面并返回通过BeautifulSoup解析后的页面源码
def get_page_source(url):
    html = requests.get(url, proxy)
    soup = BeautifulSoup(html.text, 'html.parser')
    return soup


# 创建文件夹
def make_folder(folder_name):
    if not os.path.exists(folder_name):
        print 'Creating folder: %s' % folder_name
        os.mkdir(folder_name)
    else:
        print 'Folder already exists, skip...'


# 下载图片
def save_img(thread_name, picture_url, file_name):
    if not os.path.isfile(file_name):
        data = requests.get(picture_url, proxy)
        print '%s now downloading picture: %s' % (thread_name, file_name)
        f = open(file_name, 'wb')
        f.write(data.content)
        f.close()
    else:
        print '%s already exists, skip...' % file_name



