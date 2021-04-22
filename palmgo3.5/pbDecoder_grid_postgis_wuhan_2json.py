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
import math
from scipy.stats import norm
pb_file_path = '/Users/hongyanma/Downloads/pb/42/20200617'
conn = pymysql.connect(host='127.0.0.1', user='root', passwd='123456', db='innovation', port=3786, charset='utf8',
                       cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()


def st_norm(u):
    '''标准正态分布'''

    x = abs(u) / math.sqrt(2)
    T = (0.0705230784, 0.0422820123, 0.0092705272,
         0.0001520143, 0.0002765672, 0.0000430638)
    E = 1 - pow((1 + sum([a * pow(x, (i + 1))
                          for i, a in enumerate(T)])), -16)
    p = 0.5 - 0.5 * E if u < 0 else 0.5 + 0.5 * E
    return (p)


def norm(a, sigma, x):
    '''一般正态分布'''
    u = (x - a) / sigma
    return (st_norm(u))

arr = []

for i in range(24):

    jsondic = {}
    jsondic['data'] = []
    sql = 'select grid_no, value as v, hour from innovation.wuhan_gps_static where hour='+str(i)+';'
    print(sql)
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        # print(row)
        x = (int(row['grid_no'].split('_')[1]) + 0.5) * 0.009
        y = (int(row['grid_no'].split('_')[2]) + 0.5) * 0.009
        # value = int(((st_norm(row['v'])-0.37026096833071903)/(1-0.37026096833071903)) * 100)
        value = int((row['v']-1)*100/26883)
        # print('%.6f' %x)
        # print('%.6f' %y)
        if value >60:
            print(value)
        jsondic['data'].append({'x':'%.6f' %x, 'y':'%.6f' %y,'value':value})
    with open('/Users/hongyanma/Downloads/pb/result/wh_'+str(i)+'.json','w') as outfile:
        json.dump(jsondic,outfile)

# print(max(arr))
# print(min(arr))
# 0.37026096833071903
# 1.0