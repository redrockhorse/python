# -*- coding: utf8 -*-
#encoding=utf-8
#By @mahy
#email:kkkkbj@163.com
#基于百度地图，根据地图等级简化路链，地图等级较小时简化为较小的点
import math
#地球半径
EARTH_RADIUS= 6378.137
#π
PI = 3.14159265358979323846
# 角度到弧度
DEG_TO_RAD = PI /180.00

#地图等级对应每像素表示的长度
mapScale={}
mapScale[4] = 9783.94
mapScale[5] = 4891.97
mapScale[6] = 2445.98
mapScale[7] = 1222.99
mapScale[8] = 611.5
mapScale[9] = 305.75
mapScale[10] = 152.87
mapScale[11] = 76.44
mapScale[12] = 38.22
mapScale[13] = 19.11
mapScale[14] = 9.55
mapScale[15] = 4.78
mapScale[16] = 2.39
mapScale[17] = 1.19
mapScale[18] = 0.6

#根据地图等级返回长度每像素
def getDisPrefab(zoomLevel):
    if zoomLevel <= 18 and zoomLevel >= 4:
        return mapScale[zoomLevel] * 20
    else:
        return 0.00

#计算两个坐标之间的直线距离，返回单位米制长度
def calculateLength(dLng1,dLat1,dLng2,dLat2):
	radLat1= dLat1 * DEG_TO_RAD
	radLat2=dLat2 * DEG_TO_RAD
	a=radLat1 - radLat2
	b=((dLng1 - dLng2) * DEG_TO_RAD)
	s = 2 * math.asin(math.sqrt(math.pow(math.sin(a / 2), 2) + math.cos(radLat1) * math.cos(radLat2) * pow(math.sin(b / 2), 2)))
	s = s * EARTH_RADIUS * 1000
	return s


#对路链上的点集根据没像素显示的实际距离进行抽样简化
def samplingCoord(vecOriCoords,distence):
    vecNewCoords = []
    vecNewCoords.append(vecOriCoords[0])
    totol_dis = 0.00
    startCoord = vecOriCoords[0]
    #for i in range(len(vecOriCoords)-1):
    i=0
    while i<len(vecOriCoords)-1:
        dis_a2b = calculateLength(startCoord[0],startCoord[1],vecOriCoords[i+1][0],vecOriCoords[i+1][1])
        if totol_dis+dis_a2b >= distence:
            dis_subdis =  distence - totol_dis
            persent = dis_subdis / dis_a2b
            base_x = vecOriCoords[i+1][0] if startCoord[0] > vecOriCoords[i+1][0] else startCoord[0]
            base_y = vecOriCoords[i+1][1] if startCoord[1] > vecOriCoords[i+1][1] else startCoord[1]
            sampCoord = []
            sampCoord.append(math.fabs(startCoord[0] - vecOriCoords[i+1][0]) * persent + base_x)
            sampCoord.append(math.fabs(startCoord[1] - vecOriCoords[i+1][1]) * persent + base_y)
            vecNewCoords.append(sampCoord)
            startCoord = sampCoord
            totol_dis = 0.0
        else:
            #print('sss')
            totol_dis += dis_a2b
            i+=1
            startCoord = vecOriCoords[i]
    vecNewCoords.append(vecOriCoords[-1])
    return vecNewCoords

import json
import numpy
import pandas as pd
#将字符串转换为json对象
def parseJson2Object(str):
    return json.loads(str)

#采样文件，json格式
def simpleLinkFile(inputFile,outputFile,zoomlevel):
    outputData =[]
    distence = mapScale[zoomlevel]
    f=open(inputFile)
    ay =  numpy.array([])
    for line in f:
        obj = parseJson2Object(line)
        data = obj['data']
        for p in data:
            pline = p['pline']
            #spline = samplingCoord(pline,distence)
            #outputData.append({"count":p['count'],"pline":spline})
            outputData.append(pline)
    #outputObj = {"avg":0,"data":outputData}
    #outputStr = json.dumps(outputObj)
    of=open(outputFile,'wb+')
    #of.write(outputStr)
    #of.write(outputData)
    #print(outputData)
    #print(type(outputData[0][0]))
    ay =  numpy.array(outputData)
    print(ay.shape)
    ay.astype('float64').tofile(of)
    of.close()
    f.close()

if __name__ == "__main__":
    inputFile='E:\\desktop\\corridor_link.json'
    outputFile='E:\\desktop\\sp_link.bin'
    zoomlevel=5
    simpleLinkFile(inputFile,outputFile,zoomlevel)


