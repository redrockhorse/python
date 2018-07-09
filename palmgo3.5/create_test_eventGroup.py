# -*- coding: utf8 -*-
#encoding=utf-8
#By @mahy
#email:kkkkbj@163.com
#生成测试交通事件

import json

json_file = open('/Users/hongyanma/Desktop/blockGroup.json','r')
model =json.load(json_file)
#print(type(model))
import datetime

data = model['data']
for key in data:
    starttime = datetime.datetime.now()
    for c in range(len(data[key])):
        delta = datetime.timedelta(minutes=c * 30)
        delta1 = datetime.timedelta(minutes=(c+0.2) * 60)
        data[key][c]['estimatetime'] = (starttime-delta).strftime('%Y-%m-%d %H:%M:%S')
        data[key][c]['releasetime'] = (starttime + delta1).strftime('%Y-%m-%d %H:%M:%S')
        #print(c['estimatetime'])
        #c['estimatetime'] =''
        #c['releasetime']='1111'

for key in model['data']:
    for c in data[key]:
        print(c['estimatetime'])
        #c['estimatetime'] =''
        #c['releasetime']='1111'
import collections
out_file = open('/Users/hongyanma/Desktop/blockGroup1.json','w')
json.dump(model,out_file,ensure_ascii=False)



