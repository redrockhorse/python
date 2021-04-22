# -*- coding:utf-8 -*-
# @Time : 2020/7/20 上午11:38
# @Author: kkkkibj@163.com
# @File : pbDecoder.py
# 解析pb gps文件

import zipfile
import json
import os
import redis
import psycopg2

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)
conn = psycopg2.connect(database="postgres", user="postgres", password="root", host="127.0.0.1", port="54321")
cursor = conn.cursor()

# azip = zipfile.ZipFile('/Users/hongyanma/Downloads/20200603_044.zip')
# azip = zipfile.ZipFile('/Users/hongyanma/Downloads/20200617_101.zip')
azip = zipfile.ZipFile('/Users/hongyanma/Downloads/20200617_208.zip')

import GPS_pb2
import coordinateSystemTransform
import struct


def getGpsFromZipfile(zipFilePath):
    azip = zipfile.ZipFile(zipFilePath)
    for fbfile in azip.namelist():
        print(fbfile)
        pbFile = azip.read(fbfile)
        gpsPbDecode(pbFile)


def gpsPbDecode(pbFile):
    gpsmap = GPS_pb2.GpsMap()
    gpsmap.ParseFromString(pbFile)
    print(gpsmap.carNum)
    print(gpsmap.gpsNum)
    # print(gpsmap.gpsinfo)
    result = {}
    result_caruniq = []
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
                result_caruniq.append(bd_coord)
                result[car_identity].append(X)
                result[car_identity].append(Y)
                carId = 'carid_' + str(car_identity)
                # r.rpush(carId, '%.6f' % bd_coord[0], '%.6f' % bd_coord[1])
                timeScore = int(dateTimeUTC) - 1592265600
                r.zadd(carId, {'%.6f' % bd_coord[0] + ' ' + '%.6f' % bd_coord[1]: timeScore})
                r.sadd('carIds', carId)
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
    result_caruniq_jsonobj = {"data": result_caruniq}
    # with open('/Users/hongyanma/Downloads/hy_20200617_208.json', 'w') as outputfile:
    #     json.dump(result_caruniq_jsonobj, outputfile)
    print(result)
    # print(result_caruniq)


# 过滤迹上的不合理的点
def filterTripPoints(trip):
    filter_trip_arr = []
    filter_trip_arr.append(trip[0])
    for i in range(1, len(trip)):
        tc0 = filter_trip_arr[-1]
        tc1 = trip[i]
        c0 = tc0[0]
        c1 = tc1[0]
        tt0 = tc0[1]
        tt1 = tc1[1]
        distance = ((float(c0.split(' ')[0]) - float(c1.split(' ')[0])) ** 2 + (
                    float(c0.split(' ')[1]) - float(c1.split(' ')[1])) ** 2) ** 0.5
        dif_time = tt1 - tt0
        if dif_time > 60 * 10:
            break
        if distance < dif_time * 0.0005 and distance > 0:  # 180km/m ,每秒大概0.0005度
            filter_trip_arr.append(trip[i])

    result_arr = []
    for item in filter_trip_arr:
        result_arr.append(item[0])
    return result_arr



if __name__ == '__main__':
    # r.flushdb()

    '''
    zipFilePath = '/Users/hongyanma/Downloads/pb/20200617'
    for maindir, subdir, file_name_list in os.walk(zipFilePath):
        file_name_list.sort()
        for filename in file_name_list:
            print(zipFilePath + '/' + filename)
            getGpsFromZipfile(zipFilePath + '/' + filename)
    '''


    # getGpsFromZipfile('/Users/hongyanma/Downloads/pb/20200617/20200617_288.zip')
    #
    # r.set('food', 'beef', px=3)
    # print(r.get('food'))
    # r.rpush('testlist','a','b','c','d')
    # print(r.smembers('carIds'))

    '''
    print(len(r.smembers('carIds')))
    print(r.smembers('carIds'))
    carIds = r.smembers('carIds')
    for carId in carIds:
        trip = r.lrange(carId, 0, -1)
        if len(trip) > 10:
            # print(type(r.lrange(carId, 0, -1)))
            trip[1::2] = [x+',' for x in trip[1::2]]
            trip[::2] = [x + ' ' for x in trip[::2]]
            # print(trip)
            tripstr = ''.join(trip)
            print(tripstr)
            insertSql = 'INSERT INTO public.td_ptl_taxi_gps_bj_20200617 ("carId", trip) VALUES (\''+carId+'\',ST_GeomFromText(\'LINESTRING('+tripstr[:-1]+')\'));'
            print(insertSql)
            cursor.execute(insertSql)
    conn.commit()
    '''

    print(len(r.smembers('carIds')))
    print(r.smembers('carIds'))
    carIds = r.smembers('carIds')
    for carId in carIds:
        trip = r.zrange(carId, 0, -1, withscores=True)
        # print(trip)
        trip_arr = filterTripPoints(trip)
        if len(trip_arr) > 10:
            # print(','.join(trip_arr))
            tripstr = ','.join(trip_arr)
            insertSql = 'INSERT INTO public.td_ptl_taxi_gps_bj_20200617 ("carId", trip) VALUES (\'' + carId + '\',ST_GeomFromText(\'LINESTRING(' + tripstr[:-1] + ')\'));'
            print(insertSql)
            # cursor.execute(insertSql)
            # conn.commit()

        # if len(trip) > 10:
        #     tripstr = ','.join(trip)
        #     insertSql = 'INSERT INTO public.td_ptl_taxi_gps_bj_20200617 ("carId", trip) VALUES (\'' + carId + '\',ST_GeomFromText(\'LINESTRING(' + tripstr[:-1] + ')\'));'
        # print(insertSql)
        # cursor.execute(insertSql)
        # conn.commit()
