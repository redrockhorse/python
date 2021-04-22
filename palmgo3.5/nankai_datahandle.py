# -*- coding:utf-8 -*-
#@Time : 2021/3/8 下午4:25
#@Author: kkkkibj@163.com
#@File : nankai_datahandle.py
#处理天津南开数据
import json
nankai_data = []
result = {}
result['data'] = []
with open('/Users/hongyanma/Desktop/chinaall.json','r') as gpsfile:
    rawdata = json.load(gpsfile)
    print(rawdata['data'])
    for cood in rawdata['data']:
        print(cood)
        if float(cood[0]) >= 117.134924 and float(cood[0]) <= 117.200393 and float(cood[1]) >= 39.067549 and  float(cood[1]) <= 39.152165:
            nankai_data.append(cood)
            result["data"].append({"x":cood[0],"y":cood[1],"value":1})
print(nankai_data)
print(len(nankai_data))
print(result)
with open('/Users/hongyanma/Desktop/nankai.json','w') as outputfile:
    json.dump(result,outputfile)

