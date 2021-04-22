# -*- coding:utf-8 -*-
# @Time : 2020/7/20 上午11:38
# @Author: kkkkibj@163.com
# @File : pbDecoder.py
# 解析pb gps文件

import zipfile
import json
import os
import GPS_pb2
import coordinateSystemTransform
import struct
import pymysql

max_val = 0

# 1度是111km ,1km约等于 0.009度
grid_width = 0.00009
grid_heigth = 0.00009
lefttop = [113.638019, 31.194814]
rightbottom = [115.552387, 30.00809]


def findBigestFile(pb_file_path):
    bigFileList = []
    for parent, dirnames, filenames in os.walk(pb_file_path):
        fileSizeMap = {}
        largestFile = ''
        for filename in filenames:
            fsize = os.path.getsize(parent + '/' + filename)
            # if parent not in fileSizeMap:
            fileSizeMap[parent] = fsize
            largestFile = parent + '/' + filename
            bigFileList.append(largestFile)
        #     else:
        #         if fsize < fileSizeMap[parent]:
        #             fileSizeMap[parent] = fsize
        #             largestFile = parent + '/' + filename
        # bigFileList.append(largestFile)
    return bigFileList

staticdic = {}
fileterDic = {}
def pdZipFileDeCode(zipFilePath,hour,hourData):
    azip = zipfile.ZipFile(zipFilePath)
    # print(azip.namelist())
    # print(azip.filename)
    a = azip.read(azip.namelist()[0])
    gpsmap = GPS_pb2.GpsMap()
    gpsmap.ParseFromString(a)
    # print(gpsmap.carNum)
    # print(gpsmap.gpsNum)
    result = {}
    result_caruniq = []
    tmpDic = {}
    gridData = {}
    filterGPSDic = {}

    for provinceCode in gpsmap.gpsinfo:
        # if provinceCode != 4201:
        #     continue
        # print(provinceCode)
        gpsSourceMap = gpsmap.gpsinfo[provinceCode].source
        for source in gpsSourceMap:
            # print(source)
            gpsList = gpsSourceMap[source].gps
            for gpsSequence in gpsList:

                length = struct.unpack('<h', gpsSequence[:2])[0]

                if length + 2 != len(gpsSequence):
                    print("接收数据不完整，丢弃 gps=")
                    break
                car_identity = struct.unpack('<Q', gpsSequence[2:10])[0]
                if car_identity not in result:
                    result[car_identity] = []

                state = struct.unpack('<?', gpsSequence[10:11])[0]
                count = struct.unpack('<b', gpsSequence[11:12])[0]

                X = struct.unpack('<l', gpsSequence[12:16])[0]

                firstX = X / 1000000.0

                Y = struct.unpack('<l', gpsSequence[16:20])[0]

                firstY = Y / 1000000.0

                dateTimeUTC = struct.unpack('<L', gpsSequence[20:24])[0]

                speed = struct.unpack('<B', gpsSequence[24:25])[0]

                direction = struct.unpack('<h', gpsSequence[25:27])[0]
                i = 1
                sequencetIndex = 27
                # if firstX > lefttop[0] and firstX < rightbottom[0] and firstY > rightbottom[1] and firstY<lefttop[1]: #矩形框过滤
                bd_coord = coordinateSystemTransform.wgs84_to_gcj02(firstX, firstY)
                # bd_coord = [firstX, firstY]

                lng = '%.6f' % bd_coord[0]
                lat = '%.6f' % bd_coord[1]
                # grid_x = int(float(lng) / grid_width)
                # grid_y = int(float(lat) / grid_heigth)
                # grid_no = 'g' + '_' + str(grid_x) + '_' + str(grid_y)
                if lng+'_'+lat not in hourData:
                    hourData[lng+'_'+lat] = 0
                hourData[lng + '_' + lat] += 1
                global max_val
                if max_val < hourData[lng + '_' + lat] :
                    max_val = hourData[lng + '_' + lat]
                # if hourData[lng + '_' + lat] > 1:
                #     print(hourData[lng + '_' + lat])

    return hourData


def putGPSData2DB(gridData):
    i = 0
    for key in gridData:
        i += 1
        tripstr = ','.join(gridData[key])
        insertSql = 'INSERT INTO public.td_ptl_bd_gps_20200617 (id, points) VALUES (\'' + key + '\',ST_GeomFromText(\'MULTIPOINT(' + tripstr + ')\'));'
        # print(insertSql)
        # cursor.execute(insertSql)
        # conn.commit()
    print(i)


if __name__ == '__main__':
    print('start')
    hourData = {}
    for i in range(0,24):
        print(i)
        hour = str(i)

        for j in range(1,13):
            timeId = ''
            n = i*12+j
            if n<10:
                timeId = '00'+str(n)
            if n>=10 and n<100:
                timeId = '0' + str(n)
            if n>=100:
                timeId = str(n)
            # print(timeId)
            zipfilename = '/Users/hongyanma/Desktop/baidu_navi/20210308/20210308_'+timeId+'.zip'
            pdZipFileDeCode(zipfilename, hour,hourData)
        # print(hourData)
    rs = {}
    rs['points'] = []
    for xy in hourData:
        x = xy.split('_')[0]
        y = xy.split('_')[1]
            # value = int((hourData[xy]/237)*100)
            # rs['points'].append({"x":x,"y":y,"value":value})
        rs['points'].append(float(x))
        rs['points'].append(float(y))
        if len(rs['points']) > 99999999:
            break
    print(str(i)+' : ' + str(len(rs['points'])/2))
    with open('/Users/hongyanma/Desktop/nankai/nk_points.json','w') as outf:
            json.dump(rs,outf)
    # print(max_val)



