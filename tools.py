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


def save_file(url, file_name=None):
    # file_path = folder + '/' + file_name
    # If file name is not provided, use its name original name in the url
    if not file_name:
        file_name = url.split('/').pop()
    elif file_name == 'with_subdir':
        parts = url.split('/')
        file_name = parts[-2] + '_' + parts[-1]
    elif file_name == 'subdir':
        name = url.split('/')[-2]
        extension = url.split('.')[-1]
        file_name = name + '.' + extension
    if not os.path.isfile(file_name):
        print('Downloading %s' % file_name)
        response = requests.get(url)
        file = open(file_name, 'wb')
        file.write(response.content)
        file.close()
    else:
        print('%s already exists, skip...' % file_name)


def make_folder(location, folder):  # make folder and switch to the directory
    directory = os.path.join(location, folder.strip())
    if not os.path.exists(directory):
        print('Creating directory: %s' % directory)
        os.makedirs(directory)
        os.chdir(directory)  # Switch to the directory
        # print(os.getcwd())  # Print current directory
    else:
        print('%s already exists, skip...' % directory)
        os.chdir(directory)



