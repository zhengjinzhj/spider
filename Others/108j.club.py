# -*- coding:utf-8 -*-

import requests
import csv
from bs4 import BeautifulSoup


def get_info():
    base_url = 'http://www.108j.club/category/'
    csv_file = file('108tv.csv', 'wb')
    csv_write = csv.writer(csv_file, dialect='excel')
    csv_write.writerow(['category', 'title', 'link'])
    end_url = ['korea', 'korea/page/2', 'western',
               'western/page/2', 'japan', 'japan/page/2', 'vr']
    for i in end_url:
        url = base_url + i
        if i[:5] == 'korea':
            category = '韩系'
        elif i[:7] == 'western':
            category = '欧美'
        elif i[:5] == 'japan':
            category = '日系'
        else:
            category = 'VR'
        print '**************** Crawling: %s *****************' % url
        content = requests.get(url)
        soup = BeautifulSoup(content.text, 'html.parser')
        # print soup.prettify()
        # print soup.find('ul', class_='update_area_lists')
        row = [category]
        for item in soup.find('ul', class_='update_area_lists').find_all('a'):
            row.append(item['title'])
            row.append(item['href'])
            csv_write.writerow(row)
            row = [category]
    csv_file.close()

# get_info()

test_url = 'http://www.108j.club/211.html'
source = requests.get(test_url)
soup1 = BeautifulSoup(source.text, 'html.parser')
print soup1.prettify()
