# -*- coding: utf8 -*-
# !/usr/bin/python
# 抓取北京交通事件.
__author__ = 'mahy'

import requests

url = 'http://wei.fm1039.com.cn/api/app/traffics/search?token=e8acdab26bc64c64a8c267f6698bd083&_=1383681694529'
headers = {'Host': 'wei.fm1039.com.cn',
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
res = sess.post(url, data=postData)
#print(res.text)
import time
# date to str
filename= time.strftime("%Y%m%d_%H%M", time.localtime())
#print filename
file_object = open('/usr/local/nginx/html/bjte/'+filename+'.txt', 'w',"utf-8")
file_object.write(res.text)
file_object.close( )
