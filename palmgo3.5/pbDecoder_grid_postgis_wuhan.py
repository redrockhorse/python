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

pb_file_path = '/Users/hongyanma/Downloads/pb/42/20200617'
conn = pymysql.connect(host='127.0.0.1', user='root', passwd='123456', db='innovation', port=3786, charset='utf8',
                       cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()
cursor = conn.cursor()
# 1度是111km ,1km约等于 0.009度
grid_width = 0.009
grid_heigth = 0.009
lefttop = [113.638019, 31.194814]
rightbottom = [115.552387, 30.00809]
staticdic = {}


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


def pdZipFileDeCode(zipFilePath):
    staticdic = {}
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
        if provinceCode != 4201:
            continue
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
                # if firstX > lefttop[0] and firstX < rightbottom[0] and firstY > rightbottom[1] and firstY<lefttop[1]: #矩形框过滤
                bd_coord = coordinateSystemTransform.wgs84_to_gcj02(firstX, firstY)

                lng = '%.6f' % bd_coord[0]
                lat = '%.6f' % bd_coord[1]
                grid_x = int(float(lng) / grid_width)
                grid_y = int(float(lat) / grid_heigth)
                grid_no = 'g' + '_' + str(grid_x) + '_' + str(grid_y)
                # sgrid_x = (grid_x+0.5)*grid_width
                # sgrid_y = (grid_y+0.5)*grid_width
                # sgrid_no = 's'+'_' + '%.6f' % sgrid_x + "_" +'%.6f' % sgrid_x
                if grid_no not in staticdic:
                    staticdic[grid_no] = 0
                staticdic[grid_no] += 1

                # if grid_no not in gridData:
                #     gridData[grid_no] = []
                # if lng + '_' + lat not in filterGPSDic:
                #     filterGPSDic[lng + '_' + lat] = 1
                #     gridData[grid_no].append(lng+' '+lat)
                #
                # result[car_identity].append(X)
                # result[car_identity].append(Y)
                # while count > i:
                #     differx = struct.unpack('<h', gpsSequence[sequencetIndex:sequencetIndex + 2])[0]
                #     differy = struct.unpack('<h', gpsSequence[sequencetIndex + 2:sequencetIndex + 4])[0]
                #     differTime = struct.unpack('<B', gpsSequence[sequencetIndex + 4:sequencetIndex + 5])[0]
                #     speed = struct.unpack('<B', gpsSequence[sequencetIndex + 5:sequencetIndex + 6])[0]
                #     direction = struct.unpack('<h', gpsSequence[sequencetIndex + 6:sequencetIndex + 8])[0]
                #     i += 1
                #     sequencetIndex += 8
                #     result[car_identity].append(differx)
                #     result[car_identity].append(differy)

    return staticdic


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
    filelist = findBigestFile(pb_file_path)
    # print(filelist)
    # print(len(filelist))
    for f in filelist:
        # print(f.split('/')[-1].split('.')[0])
        t = f.split('/')[-1].split('.')[0]
        timeId = str(int(t.split('_')[1])) + ''
        print(timeId)
        sd = pdZipFileDeCode(f)
        for grid_no in sd:
            sql_str = 'INSERT INTO `innovation`.`wuhan_gps`(`grid_no`,`timeid`,`vcount`)VALUES(%s,%s,%s);'
            cursor.execute(sql_str, (grid_no, timeId, str(sd[grid_no])))
            conn.commit()
        print(sd)
