# -*- coding: utf8 -*-
# !/usr/bin/python
# 抓取上海交通事件.python 版本2.5
__author__ = 'mahy'

import requests

url = 'http://www.jtcx.sh.cn/TravelServlet?type=TrafficialEvent.xml'
headers = {'Host': 'www.jtcx.sh.cn',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
           'Accept-Encoding': 'gzip, deflate',
           'Cookie': 'guid=9f78-95a4-0cc0-c681; CNZZDATA1256662931=1594195656-1483512419-%7C1483695746;user_unique_id=',
           'DNT': '1',
           'Connection': 'keep-alive',
           'Upgrade-Insecure-Requests': '1'}
postData = {'degree': 0,
            'source': 0,
            'groups': 0,
            'submit': ''}
sess = requests.Session()
sess.headers.update(headers)
res  = sess.get(url)
#print(res.text)
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import time
# date to str
filename= time.strftime("%Y%m%d_%H%M", time.localtime())
#print filename
file_object = open('/usr/local/nginx/html/shte/'+filename+'.xml','w')
file_object.write(res.text)
file_object.close( )