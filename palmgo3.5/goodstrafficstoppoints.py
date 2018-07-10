# -*- coding: utf8 -*-
#encoding=utf-8
#By @mahy
#email:kkkkbj@163.com
import csv
import json
'''
with open('E:\desktop\全国货运停驻点聚类分析.csv') as file:
    for line in file:
        print(line)
'''

tempDic ={}
csv_reader = csv.reader(open('E:\desktop\全国货运停驻点聚类分析.csv', encoding='utf-8'))
rdata ={}
rdata['data']=[]
i=0
for row in csv_reader:
    if i==0:
        pass
    else:
        rdata['data'].append([row[2],row[3],row[1]])
    i+=1
print(rdata)

with open('e:\\desktop\\goodsstops.json', 'w') as f:
    json.dump(rdata, f)


'''
for row in csv_reader:
    if row[0] in tempDic:
        #tempDic['coords'].append([row[2],row[3]])
        pass
    else:
        tempDic[row[0]]={
            "value":row[1],
            "coords":[]
        }
    tempDic[row[0]]['coords'].append([row[2],row[3]])



rdata ={}
rdata['data']=[]
for key in tempDic:
   rdata['data'].append(tempDic[key])
print(rdata)
'''


#print(tempDic)

