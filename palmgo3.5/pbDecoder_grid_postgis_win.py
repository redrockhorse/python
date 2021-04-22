# -*- coding:utf-8 -*-
# @Time : 2020/7/20 上午11:38
# @Author: kkkkibj@163.com
# @File : pbDecoder.py
# 解析pb gps文件

import zipfile
import json
import psycopg2
import os
import GPS_pb2
import coordinateSystemTransform
import struct

pb_file_path = 'e:\\PB\\baidu'
conn = psycopg2.connect(database="postgres", user="postgres", password="root", host="127.0.0.1", port="54321")
cursor = conn.cursor()
grid_width = 0.05
grid_heigth = 0.05

def findBigestFile(pb_file_path):
    bigFileList = []
    for parent, dirnames, filenames in os.walk(pb_file_path):
        fileSizeMap = {}
        largestFile = ''
        for filename in filenames:
            fsize = os.path.getsize(parent+'\\'+filename)
            if parent not in fileSizeMap:
                fileSizeMap[parent] = fsize
                largestFile = parent+'\\'+filename
            else:
                if fsize < fileSizeMap[parent]:
                    fileSizeMap[parent] = fsize
                    largestFile = parent + '\\' + filename
        bigFileList.append(largestFile)
    return bigFileList

def pdZipFileDeCode(zipFilePath):
    azip = zipfile.ZipFile(zipFilePath)
    print(azip.namelist())
    print(azip.filename)
    a = azip.read(azip.namelist()[0])
    gpsmap = GPS_pb2.GpsMap()
    gpsmap.ParseFromString(a)
    print(gpsmap.carNum)
    print(gpsmap.gpsNum)
    result = {}
    result_caruniq = []
    tmpDic = {}
    gridData = {}
    filterGPSDic = {}

    for provinceCode in gpsmap.gpsinfo:
        print(provinceCode)
        gpsSourceMap = gpsmap.gpsinfo[provinceCode].source
        for source in gpsSourceMap:
            print(source)
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
                bd_coord = coordinateSystemTransform.wgs84_to_bd09(firstX, firstY)

                lng = '%.6f' % bd_coord[0]
                lat = '%.6f' % bd_coord[1]
                grid_x = int(float(lng) / grid_width)
                grid_y = int(float(lat) / grid_heigth)
                grid_no = 'g' + '_' + str(grid_x) + '_' + str(grid_y)

                if grid_no not in gridData:
                    gridData[grid_no] = []
                if lng + '_' + lat not in filterGPSDic:
                    filterGPSDic[lng + '_' + lat] = 1
                    gridData[grid_no].append(lng+' '+lat)

                result[car_identity].append(X)
                result[car_identity].append(Y)
                while count > i:
                    differx = struct.unpack('<h', gpsSequence[sequencetIndex:sequencetIndex + 2])[0]
                    differy = struct.unpack('<h', gpsSequence[sequencetIndex + 2:sequencetIndex + 4])[0]
                    differTime = struct.unpack('<B', gpsSequence[sequencetIndex + 4:sequencetIndex + 5])[0]
                    speed = struct.unpack('<B', gpsSequence[sequencetIndex + 5:sequencetIndex + 6])[0]
                    direction = struct.unpack('<h', gpsSequence[sequencetIndex + 6:sequencetIndex + 8])[0]
                    i += 1
                    sequencetIndex += 8
                    result[car_identity].append(differx)
                    result[car_identity].append(differy)
    return gridData


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

