# -*- coding: utf8 -*-
# !/usr/bin/python
# 马自达要求的全国区域划分边界
import json

regionList =[]
result={}
i=0
regionNames =["华东一区","华南大区","东北大区","华北大区","中西部大区","华南大区","华东二区","华东一区"]
with open('/Users/hongyanma/Desktop/马自达全国销售服务店各分区.MIF','r') as miffile:
    line = miffile.readline()
    while line:
        if line.find('Region') != -1:
            points =[]
            rname = regionNames[i]
            i+=1
            pointsnumstr = miffile.readline()
            pointsnum = pointsnumstr.strip(' ')
            #print(pointsnum)
            for n in range(int(pointsnum)-1):
                #print(miffile.readline().strip('\n'))
                pointsline = miffile.readline().strip('\n')
                points.append([pointsline.split(' ')[0],pointsline.split(' ')[1]])
            #print(points)
            center=[]
            tmpline = miffile.readline()
            while tmpline.find('Center') == -1:
                tmpline = miffile.readline()
            centerstr = tmpline.strip('\n')
            print(centerstr)
            center = [centerstr.split(' ')[5],centerstr.split(' ')[6]]
            print(center)

            regionList.append({
                'name':rname,
                'points':points,
                'center':center
            })
            #break
        line = miffile.readline()
    result['data']=regionList
    with open('/Users/hongyanma/Desktop/mzdregions.json','w') as jsonfile:
        json.dump(result,jsonfile,ensure_ascii=False)


