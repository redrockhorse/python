# -*- coding:utf-8 -*-
#@Time : 2020/6/13 下午10:09
#@Author: kkkkibj@163.com
#@File : g102shigu.py
#事故路段
import json
import math
x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 偏心率平方



def gcj02_to_bd09(lng, lat):
    """
    火星坐标系(GCJ-02)转百度坐标系(BD-09)
    谷歌、高德——>百度
    :param lng:火星坐标经度
    :param lat:火星坐标纬度
    :return:
    """
    z = math.sqrt(lng * lng + lat * lat) + 0.00002 * math.sin(lat * x_pi)
    theta = math.atan2(lat, lng) + 0.000003 * math.cos(lng * x_pi)
    bd_lng = z * math.cos(theta) + 0.0065
    bd_lat = z * math.sin(theta) + 0.006
    return [bd_lng, bd_lat]

with open('/Users/hongyanma/Downloads/沈海事故段_polyline.json','r') as infile:
    geoobj = json.load(infile)
    features = geoobj['features']
    lines = []
    for f in features:
        line = []
        for n in f['geometry']['coordinates']:
            bdzb = gcj02_to_bd09(n[0], n[1])
            line.append(bdzb)
        # lines.append(f['geometry']['coordinates'])
        lines.append(line)
    print(lines)
    outobj ={''}
