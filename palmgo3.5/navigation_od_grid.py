# -*- coding: utf8 -*-
#encoding=utf-8
#By @mahy
#email:kkkkbj@163.com
#处理刘闯给的导航od数据
#网格法
import  json
import math
def gps_coord_02tobd(gps_cx_02, gps_cy_02):
    x_pi = 3.14159265358979324 * 3000.0 / 180.0
    z = math.sqrt(gps_cx_02 * gps_cx_02 + gps_cy_02 * gps_cy_02) + 0.00002 * math.sin(gps_cy_02 * x_pi)
    theta = math.atan2(gps_cy_02, gps_cx_02) + 0.000003 * math.cos(gps_cx_02 * x_pi)
    gps_cx_bd = z * math.cos(theta) + 0.0065
    gps_cy_bd = z * math.sin(theta) + 0.006
    return (gps_cx_bd, gps_cy_bd)

'''
dateDic ={}
with open('e:\\desktop\\驾车导航OD.csv','r') as inputfile:
    i=0
    for line in inputfile:
        if i==0:
            pass
        else:
            arr = line.split(',')
            if arr[8] not in dateDic:
                dateDic[arr[8]]={}
                dateDic[arr[8]]['data']=[]
            count=int(arr[5])+int(arr[6])
            workday = 100
            weekday =10
            holiday = 1
            if arr[9] =='':
                workday=0
            if arr[10]=='':
                weekday =0
            if arr[11]=='' or arr[11]=='\n':
                holiday =0
            wwh = workday+weekday+holiday
            coords = gps_coord_02tobd(float(arr[1]), float(arr[2]))
            dateDic[arr[8]]['data'].append(['%.6f' %coords[0],'%.6f' %coords[1],count])
        i+=1

for key in dateDic:
    with open('E:\\desktop\\navigation\\'+key+'.json','w') as outputfile:
        json.dump(dateDic[key],outputfile)
'''
#2017-09-12 周一做分时数据
Monday={}
Monday['data']={}
latExtentArray =[]
lngExtentArray =[]
with open('e:\\desktop\\驾车导航OD.csv','r') as inputfile:
    i=0
    for line in inputfile:
        if i==0:
            pass
        else:
            arr = line.split(',')
            if arr[8] == '2017-09-12':
                #timerange = int(arr[7].split('-')[0].split(':')[0])
                latExtentArray.append(float(arr[1]))
                lngExtentArray.append(float(arr[2]))
        i+=1
lngExtent=[min(lngExtentArray),max(lngExtentArray)]
latExtent=[min(latExtentArray),max(latExtentArray)]
cellCount =[int((lngExtent[1]-lngExtent[0])/0.01),int((latExtent[1]-latExtent[0])/0.01)]
cellSizeCoord =[0.01,0.01]
print(lngExtent)
print(latExtent)
print(cellCount)
Monday['lngExtent']=lngExtent
Monday['latExtent']=latExtent
Monday['cellCount']=cellCount
Monday['cellSizeCoord']=cellSizeCoord


with open('e:\\desktop\\驾车导航OD.csv','r') as inputfile:
    i=0
    for line in inputfile:
        if i==0:
            pass
        else:
            arr = line.split(',')
            if arr[8] == '2017-09-12':
                timerange = int(arr[7].split('-')[0].split(':')[0])
                if timerange not in Monday['data']:
                    Monday['data'][timerange]=[]
                count=int(arr[5])+int(arr[6])
                #coords = gps_coord_02tobd(float(arr[1]), float(arr[2]))
                Monday['data'][timerange].append([int((float(arr[2])-lngExtent[0])/0.01),int((float(arr[1])-latExtent[0])/0.01),count])
        i+=1


with open('E:\\desktop\\navigation\\monday_grid.json','w') as outputfile:
    json.dump(Monday,outputfile)

