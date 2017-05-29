# -*- coding:utf-8 -*-

import csv
import re
import requests

proxy = {'http': '127.0.0.1:1080'}
main_url = 'http://www.1pondo.tv/dyn/ren/movie_lists/list_newest_'
# http://smovie.1pondo.tv/sample/movies/092916_394/1080p.mp4


def get_contents():
    csv_file = file('1pondo_newest.csv', 'wb')
    csv_writer = csv.writer(csv_file, dialect='excel')
    csv_writer.writerow(['Actor', 'Desc', 'MovieID', 'Release', 'Thumbnail', 'Title', 'Keywords', 'Year'])
    for page in xrange(0, 40, 50):  # 2017-03-19
        url = main_url + str(page) + '.json'
        print 'Now crawling ' + str(page) + '.json'
        request = requests.get(url, proxies=proxy)
        response = request.text
        response = remove_quote(response)
        pattern = re.compile('\{Actor:(.*?),.*?,Desc:(.*?),Duration:.*?,MovieID:(.*?),.*?,Release:(.*?),'
                             '.*?,ThumbHigh:(.*?),.*?Title:(.*?),.*?,UCNAME:\[(.*?)],Year:(.*?)}', re.S)
        items = re.findall(pattern, response)
        for item in items:
            csv_writer.writerow([item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7]])
    csv_file.close()


def remove_quote(content):
    pattern = re.compile('\"')
    content = re.sub(pattern, '', content)
    return content


# def remove_line_feed(text):
#     pattern = re.compile('\\r')
#     text = re.sub(pattern, '', text)
#     return text


get_contents()

