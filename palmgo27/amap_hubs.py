# -*- coding: utf-8 -*-
#encoding=utf-8
__author__ = 'mahy'
import httplib2

from random import Random
def random_str(randomlength=32):
    str = ''
    chars = '123456789abcdef'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str


url='http://report.amap.com/api/100000/hubs.do'
http = httplib2.Http()
response, content = http.request(url, 'GET',headers = {
        'Host': 'report.amap.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding':'gzip, deflate',
        'Cookie': 'guid=9f78-95a4-0cc0-c681; CNZZDATA1256662931=1594195656-1483512419-%7C1483695746;user_unique_id='+random_str(32),
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    })
import time,datetime
# date to str
filename= time.strftime("%Y%m%d_%H%M", time.localtime())
#print filename
file_object = open('/usr/local/nginx/html/hubs/'+filename+'.txt', 'w')
file_object.write(content)
file_object.close( )
#print random_str(32)
#print(response)
#print(content)
