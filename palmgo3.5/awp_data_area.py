# -*- coding: utf8 -*-
#encoding=utf-8
#By @mahy
#email:kkkkbj@163.com
#安联数据增加地理信息，语义地图

import pymysql
import math
import requests
import sys
import datetime
import numpy as np
import decimal

def gps_coord_02tobd(gps_cx_02, gps_cy_02):
    x_pi = 3.14159265358979324 * 3000.0 / 180.0
    z = math.sqrt(gps_cx_02 * gps_cx_02 + gps_cy_02 * gps_cy_02) + 0.00002 * math.sin(gps_cy_02 * x_pi)
    theta = math.atan2(gps_cy_02, gps_cx_02) + 0.000003 * math.cos(gps_cx_02 * x_pi)
    gps_cx_bd = z * math.cos(theta) + 0.0065
    gps_cy_bd = z * math.sin(theta) + 0.006
    return (gps_cx_bd, gps_cy_bd)

conn=pymysql.connect(host='127.0.0.1',user='root',passwd='root',db='palmgo',port=3306,charset='utf8', cursorclass = pymysql.cursors.DictCursor)
cursor = conn.cursor()

sql='select BRAND,Case_Time,Case_Type,Fault,Longitude,Latitude from td_awp_source_data where province is null order by Case_Time asc'
cursor.execute(sql)
results = cursor.fetchall()
i=0
for row in results:
    i+=1
    #print(row['Longitude'],row['Latitude'])
    coords = gps_coord_02tobd(float(row['Longitude']), float(row['Latitude']))
    #print(coords[0],coords[1])
    r = requests.get(url='http://api.map.baidu.com/geocoder/v2/',
                             params={'location': '%.6f' % coords[1]+','+'%.6f' % coords[0], 'ak': '1XjLLEhZhQNUzd93EjU5nOGQ', 'output': 'json'})

    result = r.json()
    addressComponent=result['result']['addressComponent']
    update_sql ='update td_awp_source_data set province=%s ,city=%s,district=%s,town=%s,street=%s where Longitude=%s and Latitude=%s'
    cursor.execute(update_sql,(addressComponent['province'],addressComponent['city'],addressComponent['district'],addressComponent['town'],addressComponent['street'],str(row['Longitude']),str(row['Latitude'])))
    if i%100==0:
        print(i,len(results))
        conn.commit()
        cursor.execute(sql)
        results = cursor.fetchall()