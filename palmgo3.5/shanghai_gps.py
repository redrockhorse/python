# -*- coding: utf8 -*-
#encoding=utf-8
#By @mahy
#email:kkkkbj@163.com
#上海12小时gps数据处理
import os
import json
dir = 'E:\desktop\shanghai-UGC-gps'
for root, dirs, files in os.walk(dir):
    for file in files:
        print(int(int(file.split('.')[0].split('_')[1])/12)-1)
        tstr = str(int(int(file.split('.')[0].split('_')[1])/12)-1)+'.json'
        coorddict ={}
        res ={}
        res['data']=[]
        with open(os.path.join(root, file),'r') as filehandle:
            for line in filehandle:
                lon=line.split(',')[4]
                lat=line.split(',')[5]
                #print(line.split(',')[4],line.split(',')[5])
                if lon+'_'+lat not in coorddict:
                    coorddict[lon+'_'+lat]=1
                else:
                     coorddict[lon+'_'+lat]+=1
            for key in coorddict:
                res['data'].append([key.split('_')[0],key.split('_')[1],coorddict[key]])
            with open(os.path.join('E:\desktop\shanghaigpsjson\\', tstr),'w') as tfile:
                json.dump(res,tfile)





