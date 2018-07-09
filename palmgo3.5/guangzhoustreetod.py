# -*- coding: gbk -*-
#encoding=gbk
# coding=gbk
#By @mahy
#email:kkkkbj@163.com
#处理广东街镇级别od数据

csvfiledir = '/Users/hongyanma/Desktop/20171010'

import os
import numpy
import pandas as pd
from urllib.request import urlopen, quote
import  json

streetnamedic={}

def eachFile(filepath):
    pathDir =  os.listdir(filepath)
    for allDir in pathDir:
        child = os.path.join('%s/%s' % (filepath, allDir))
        #print(child)
        handleData(child)



#my_matrix = numpy.loadtxt(open("/Users/hongyanma/Desktop/20171010/23.csv","rb"),delimiter=",",skiprows=0)
#df = pd.read_csv("/Users/hongyanma/Desktop/20171010/23.csv",encoding = "gbk")
#print(df.values)
#print(df.columns)

def handleData(flieName):
    cnames = []
    df = pd.read_csv(flieName, encoding="gbk")
    for name in df.columns:
        #print(name,name.find(u"广州"))
        if name =='O|D' or (name.find(u"广州") != -1 and len(name)>3):
            cnames.append(name)
    df=df[cnames]
    #print(df.values)

    for v in df.values:
        if v[0].find(u"广州") != -1 and len(v[0])>3:
            #print(v)
            for i in range(len(v)):
                if i>0 and v[0] != cnames[i]:
                    if v[0]+'_'+cnames[i] in streetnamedic:
                        streetnamedic[v[0]+'_'+cnames[i]] += v[i]
                    elif cnames[i]+'_'+v[0] in streetnamedic:
                        streetnamedic[cnames[i]+'_'+v[0]] += v[i]
                    else:
                        streetnamedic[v[0] + '_' + cnames[i]] = v[i]

def searchBaiduLocationByName(name):
    add = quote(name.encode('utf8'))  # 由于本文城市变量为中文，为防止乱码，先用quote进行编码
    uri = url + '?' + 'address=' + add + '&output=' + output + '&ak=' + ak
    req = urlopen(uri)
    res = req.read().decode()
    temp = json.loads(res)  # 对json数据进行解析
    return [temp["result"]["location"]["lng"], temp["result"]["location"]["lat"]]


locationDic ={}
eachFile(csvfiledir)
print(streetnamedic)
url = 'http://api.map.baidu.com/geocoder/v2/'
output = 'json'
ak = '1XjLLEhZhQNUzd93EjU5nOGQ'
resultObj ={}
resultObj['data']=[]
for key in streetnamedic:
    fname = key.split('_')[0]
    tname = key.split('_')[1]

    if fname not in locationDic:
        locationDic[fname] = searchBaiduLocationByName(fname)
    if tname not in locationDic:
        locationDic[tname] = searchBaiduLocationByName(tname)
    resultObj['data'].append({
        "fromName": fname,
        "toName": tname,
        "coords": [
            locationDic[fname],
            locationDic[tname]
        ],
        "count": streetnamedic[key]
    })

odinguangzhou = open('/Users/hongyanma/Desktop/20171012/20171012/in_guangzhou.json', 'w')
json.dump(resultObj, odinguangzhou, ensure_ascii=False, indent=4)
print(resultObj)








