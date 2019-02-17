# -*- coding: utf8 -*-
#!/usr/bin/python
#处理省份边界，中心，和省份下属地级市边界中心信息


import json

resultObj ={}
resultObj['data']={}
resultObj['data']['全国']={}
resultObj['data']['全国']['childen']=[]

dir = '/Users/hongyanma/gitspace/front/front/palmgo-bigdata-front/data/administrativeDivision/'
pcode={}
pcodeDic={}
with open(dir+"province.json","r") as pfile:
    pcode = json.load(pfile)
#print(pcode['data'])

for item in pcode['data']:
    #print(item)
    pcodeDic[item['code']]=item['name']
    resultObj['data']['全国']['childen'].append(item['name'])
    if item['name'] not in resultObj['data']:
        resultObj['data'][item['name']]={}
        resultObj['data'][item['name']]['childen']=[]
#print(resultObj)

ccode ={}
with open(dir+"cities.json","r") as cfile:
    ccode = json.load(cfile)

for item in ccode['data']:
    #print(pcodeDic[item['provinceCode']])
    resultObj['data'][pcodeDic[item['provinceCode']]]['childen'].append(item['name'])


pbObj ={}
with open(dir+"provinceBoundary.json","r") as pbfile:
    pbObj = json.load(pbfile)

for key in pbObj['data']:
    #print(key)
    resultObj['data'][key]['boundary']=pbObj['data'][key]

pcObj ={}
with open(dir+"provinceCenter.json","r") as pcfile:
    pcObj = json.load(pcfile)

for item in pcObj['data']:
    #print(key)
    resultObj['data'][item['xname']]['center']=item['pline']

cbObj ={}
with open(dir+"cityBoundaryAll.json","r") as cbfile:
    cbObj = json.load(cbfile)


for key in cbObj['data']:
    if key not in resultObj['data']:
        resultObj['data'][key]={}
        resultObj['data'][key]['boundary'] = cbObj['data'][key]

ccObj ={}
with open(dir+"cityCenter.json","r") as ccfile:
    ccObj = json.load(ccfile)

for key in ccObj['data']:
   # resultObj['data'][key]['childen']=[]
    resultObj['data'][key]['center'] = ccObj['data'][key]

with open(dir+'adInfo.json','w') as adfile:
    json.dump(resultObj, adfile, ensure_ascii=False)
print(resultObj)





