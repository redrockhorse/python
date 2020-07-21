# -*- coding:utf-8 -*-
# @Time : 2020/7/20 上午11:38
# @Author: kkkkibj@163.com
# @File : pbDecoder.py
# 解析pb gps文件

import zipfile

test = '1234567890'
print(test[:2])
print(test[2:6])
azip = zipfile.ZipFile('/Users/hongyanma/Downloads/20200603_044.zip')

print(azip.namelist())
# # 返回该zip的文件名
print(azip.filename)
a = azip.read('20200603_044.dat')
# print(a)
import GPS_pb2
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
for provinceCode in gpsmap.gpsinfo:
    print(provinceCode)
    gpsSourceMap = gpsmap.gpsinfo[provinceCode].source
    for source in gpsSourceMap:
        print(source)
        gpsList = gpsSourceMap[source].gps
        for gpsSequence in gpsList:
            print('=================')
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

            print(car_identity)
            state = struct.unpack('<?', gpsSequence[10:11])[0]
            print(state)
            count = struct.unpack('<b', gpsSequence[11:12])[0]
            print(count)

            X = struct.unpack('<l', gpsSequence[12:16])[0]
            print(X)

            firstX = X / 1000000.0
            print(firstX)

            Y = struct.unpack('<l', gpsSequence[16:20])[0]
            print(Y)

            firstY = Y / 1000000.0
            print(firstY)

            dateTimeUTC = struct.unpack('<L', gpsSequence[20:24])[0]
            print(dateTimeUTC)

            speed = struct.unpack('<B', gpsSequence[24:25])[0]
            print(speed)

            direction = struct.unpack('<h', gpsSequence[25:27])[0]
            print(direction)
            i = 1
            sequencetIndex = 27
            result_caruniq.append([firstX,firstY])
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
print(result[9322179061480346339])
print(result[2143375899162136896])
print(result_caruniq)