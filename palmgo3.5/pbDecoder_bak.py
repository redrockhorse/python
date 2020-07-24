# -*- coding:utf-8 -*-
# @Time : 2020/7/20 上午11:38
# @Author: kkkkibj@163.com
# @File : pbDecoder.py
# 解析pb gps文件

import zipfile
import json


# azip = zipfile.ZipFile('/Users/hongyanma/Downloads/20200603_044.zip')
# azip = zipfile.ZipFile('/Users/hongyanma/Downloads/20200617_101.zip')
azip = zipfile.ZipFile('/Users/hongyanma/Downloads/20200617_208.zip')
print(azip.namelist())
# # 返回该zip的文件名
print(azip.filename)
a = azip.read(azip.namelist()[0])
# print(a)
import GPS_pb2
import coordinateSystemTransform
import struct

gpsmap = GPS_pb2.GpsMap()
gpsmap.ParseFromString(a)

# print(gpsmap)
# for item in gpsmap:
#     print(item)
print(gpsmap.carNum)
print(gpsmap.gpsNum)
# print(gpsmap.gpsinfo)
result ={}
result_caruniq = []
tmpDic = {}
grid_width = 0.001
grid_heigth = 0.001
for provinceCode in gpsmap.gpsinfo:
    print(provinceCode)
    gpsSourceMap = gpsmap.gpsinfo[provinceCode].source
    for source in gpsSourceMap:
        print(source)
        gpsList = gpsSourceMap[source].gps
        for gpsSequence in gpsList:
            # print('=================')
            # print(gpsSequence)
            length = struct.unpack('<h', gpsSequence[:2])[0]
            # print(length)
            # print(len(gpsSequence))
            if length + 2 != len(gpsSequence):
                print("接收数据不完整，丢弃 gps=")
                break
            car_identity = struct.unpack('<Q', gpsSequence[2:10])[0]
            if car_identity not in result:
                result[car_identity] = []

            # print(car_identity)
            state = struct.unpack('<?', gpsSequence[10:11])[0]
            # print(state)
            count = struct.unpack('<b', gpsSequence[11:12])[0]
            # print(count)

            X = struct.unpack('<l', gpsSequence[12:16])[0]
            # print(X)

            firstX = X / 1000000.0
            # print(firstX)

            Y = struct.unpack('<l', gpsSequence[16:20])[0]
            # print(Y)

            firstY = Y / 1000000.0
            # print(firstY)

            dateTimeUTC = struct.unpack('<L', gpsSequence[20:24])[0]
            # print(dateTimeUTC)

            speed = struct.unpack('<B', gpsSequence[24:25])[0]
            # print(speed)

            direction = struct.unpack('<h', gpsSequence[25:27])[0]
            # print(direction)
            i = 1
            sequencetIndex = 27
            bd_coord = coordinateSystemTransform.wgs84_to_bd09(firstX, firstY)

            lng = '%.6f' % bd_coord[0]
            lat = '%.6f' % bd_coord[1]
            grid_x = int(float(lng) / grid_width)
            grid_y = int(float(lat) / grid_heigth)
            grid_no = 'g' + '_' + str(grid_x) + '_' + str(grid_y)
            if grid_no not in tmpDic:
                result_caruniq.append([lng, lat])
                tmpDic[grid_no] = 1

            # result_caruniq.append([firstX,firstY])
            # if ('%.6f' % bd_coord[0])+'_'+('%.6f' % bd_coord[1]) not in tmpDic:
            #     result_caruniq.append(['%.6f' % bd_coord[0],'%.6f' % bd_coord[1]])
            #     tmpDic[('%.6f' % bd_coord[0])+'_'+('%.6f' % bd_coord[1])] = 1
            # print(coordinateSystemTransform.gcj02_to_bd09(firstX,firstY))

            result[car_identity].append(X)
            result[car_identity].append(Y)
            while count > i:
                differx = struct.unpack('<h', gpsSequence[sequencetIndex:sequencetIndex + 2])[0]
                differy = struct.unpack('<h', gpsSequence[sequencetIndex + 2:sequencetIndex + 4])[0]
                differTime = struct.unpack('<B', gpsSequence[sequencetIndex + 4:sequencetIndex + 5])[0]
                speed = struct.unpack('<B', gpsSequence[sequencetIndex + 5:sequencetIndex + 6])[0]
                direction = struct.unpack('<h', gpsSequence[sequencetIndex + 6:sequencetIndex + 8])[0]
                # print('************************************')
                # print(differx)
                # print(differy)
                # print(differTime)
                # print(speed)
                # print(sequencetIndex)
                # print('************************************')
                i += 1
                sequencetIndex += 8
                result[car_identity].append(differx)
                result[car_identity].append(differy)

            # break
# print(result[9322179061480346339])
# print(result[2143375899162136896])
print(result_caruniq)
print(len(result_caruniq))
result_caruniq_jsonobj = {"data":result_caruniq}
# with open('/Users/hongyanma/Downloads/bd_20200617_101.json','w') as outputfile:
with open('/Users/hongyanma/Downloads/hy_20200617_208.json','w') as outputfile:
    json.dump(result_caruniq_jsonobj,outputfile)

def getGpsFromZipfile(zipFilePath):
    azip = zipfile.ZipFile(zipFilePath)
    # for
    # a = azip.read(azip.namelist()[0])

def gpsPbDecode(zipFilePath):
    azip = zipfile.ZipFile(zipFilePath)
    gpsmap = GPS_pb2.GpsMap()

    gpsmap.ParseFromString(a)