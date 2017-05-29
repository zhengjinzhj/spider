# -*- coding:utf-8 -*-

# import urllib2
import re
import csv
import os
import requests


# http://smovie.caribbeancom.com/sample/movies/110616-297/1080p.mp4
class Caribbeancom(object):

    def __init__(self):
        self.proxy = {'http': '127.0.0.1:1080'}
        self.base_url = 'http://www.caribbeancom.com/listpages/all'

    def get_total_page(self):
        first_page = self.base_url + '1.htm'
        data = requests.get(first_page, proxies=self.proxy)
        content = data.text.encode('utf-8')
        page_pattern = re.compile('<input id="go-page" type="text" value="1"> /(.*?)ページ', re.S)
        total_page = re.findall(page_pattern, content)
        # print total_page[0]
        return int(total_page[0])

    def get_content(self, page_no):
        one_page_data = []
        page_url = self.base_url + str(page_no) + '.htm'
        # response = self.opener.open(page_url)
        # response = response.read().decode('euc-jp').encode('utf-8')
        data = requests.get(page_url, proxies=self.proxy)
        content = data.text.encode('utf-8')
        response = self.remove_quota(content)
        pattern = re.compile('<div itemscope itemtype=.*?VideoObject>.*?<a href=\/moviepages\/(.*?)\/index.html.*?'
                             '<img.*?thumbnail src=(.*?) alt=(.*?) title=(.*?)>.*?movie-date>(.*?)</span>', re.S)
        items = re.findall(pattern, response)
        for item in items:
            thumbnail = item[1].replace('256x144', '')
            actress = item[2].replace(item[3], '')
            # item[2]=title + actress, item[3]=title
            one_page_data.append([item[0], thumbnail, actress.strip(), item[3].strip(), item[4]])
        return one_page_data

    def save_picture(self, image_url, movie_id):
        picture_name = movie_id + '.jpg'
        picture_address = 'Caribbeancom' + '/' + picture_name
        if not os.path.isfile(picture_address):
            print 'Downloading ' + picture_name
            # response = self.opener.open(image_url)
            # data = response.read()
            response = requests.get(image_url, proxies=self.proxy)
            data = response.content
            f = open(picture_address, 'wb')
            f.write(data)
            f.close()
        else:
            print picture_name + ' already exists, skip...'

    @staticmethod
    def make_folder(folder_name):
        if not os.path.exists(folder_name):
            print 'Creating folder: ' + folder_name
            os.makedirs(folder_name)
        else:
            print 'Folder "' + folder_name + '" already exists, skip...'

    @staticmethod
    def remove_quota(content):
        pattern = re.compile('\"')
        content = re.sub(pattern, '', content)
        return content

    def write_csv(self):
        csv_file = file('carib_newest.csv', 'wb')
        writer = csv.writer(csv_file, dialect='excel')
        writer.writerow(['Movie ID', 'Release Date', 'Title', 'Actress', 'Thumbnail'])
        total_page = 2  # 2017-03-20
        # total_page = self.get_total_page()
        self.make_folder('Caribbeancom')
        for page in xrange(1, total_page+1):
            print '*'*20 + 'Crawling page ' + str(page) + '*'*20
            data = self.get_content(page)
            for movie in data:
                writer.writerow([movie[0], movie[4], movie[3], movie[2], movie[1]])
        csv_file.close()

    def save_thumbnails(self):
        with open('caribbeancom_temp.csv', 'rb') as csv_file:
            reader = csv.DictReader(csv_file)
            data = [row for row in reader]
            picture_link = [row['Thumbnail'] for row in data]
            picture_id = [row['Movie ID'] for row in data]
            link_id = dict(zip(picture_link, picture_id))
            for (link, name) in link_id.items():
                link = link.replace('https', 'http')
                self.save_picture(link, name)

demo = Caribbeancom()
demo.write_csv()
# demo.save_thumbnails()




