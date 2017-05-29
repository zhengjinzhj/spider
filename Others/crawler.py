# -*- coding:utf-8 -*-
import urllib2

# page = 1
url = 'http://www.3dmgame.com'
request = urllib2.Request(url)
response = urllib2.urlopen(request).read()
# response = response.decode('euc-jp').encode('utf-8')
print response.decode('utf-8').encode('utf-8')
