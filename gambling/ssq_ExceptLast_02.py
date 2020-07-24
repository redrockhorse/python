#!/usr/bin/python
# encoding=utf-8
# lbp feature extraction
__author__ = 'mahy'
import pymysql
import numpy as np
# import tensorflow as tf

conn = pymysql.connect(host='127.0.0.1', user='root', passwd='Qd@#$mo658', db='jc', port=3306, charset='utf8',
                       cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()

rs = []
max_arr = []
min_arr = []
avg_arr = []
std_arr = []
sql = "select max(v1),max(v2),max(v3),max(v4),max(v5),max(v6),max(v7) from td_ptl_ssq_data"
cursor.execute(sql)
result = cursor.fetchall()
for row in result:
    max_arr.append(int(row['max(v1)']))
    max_arr.append(int(row['max(v2)']))
    max_arr.append(int(row['max(v3)']))
    max_arr.append(int(row['max(v4)']))
    max_arr.append(int(row['max(v5)']))
    max_arr.append(int(row['max(v6)']))
    max_arr.append(int(row['max(v7)']))
print(max_arr)

sql = "select min(v1),min(v2),min(v3),min(v4),min(v5),min(v6),min(v7) from td_ptl_ssq_data"
cursor.execute(sql)
result = cursor.fetchall()
for row in result:
    min_arr.append(int(row['min(v1)']))
    min_arr.append(int(row['min(v2)']))
    min_arr.append(int(row['min(v3)']))
    min_arr.append(int(row['min(v4)']))
    min_arr.append(int(row['min(v5)']))
    min_arr.append(int(row['min(v6)']))
    min_arr.append(int(row['min(v7)']))
print(min_arr)

sql = "select avg(v1),avg(v2),avg(v3),avg(v4),avg(v5),avg(v6),avg(v7) from td_ptl_ssq_data"
cursor.execute(sql)
result = cursor.fetchall()
for row in result:
    avg_arr.append(float(row['avg(v1)']))
    avg_arr.append(float(row['avg(v2)']))
    avg_arr.append(float(row['avg(v3)']))
    avg_arr.append(float(row['avg(v4)']))
    avg_arr.append(float(row['avg(v5)']))
    avg_arr.append(float(row['avg(v6)']))
    avg_arr.append(float(row['avg(v7)']))
print(avg_arr)

sql = "select std(v1),std(v2),std(v3),std(v4),std(v5),std(v6),std(v7) from td_ptl_ssq_data"
cursor.execute(sql)
result = cursor.fetchall()
for row in result:
    std_arr.append(float(row['std(v1)']))
    std_arr.append(float(row['std(v2)']))
    std_arr.append(float(row['std(v3)']))
    std_arr.append(float(row['std(v4)']))
    std_arr.append(float(row['std(v5)']))
    std_arr.append(float(row['std(v6)']))
    std_arr.append(float(row['std(v7)']))
print(std_arr)

import random
print(random.uniform(-1,1))
print(random.uniform(-1,1))
print(random.uniform(-1,1))
print(random.uniform(-1,1))
luck_arr =[]
for i in range(5):
    # print(int(avg_arr[0]+random.uniform(-1,1)*std_arr[0]))
    tmparr = []
    last_num = 0
    for n in range(6):
        tr_v = int(avg_arr[n] + random.uniform(-1, 1) * std_arr[n])
        if tr_v > last_num:
            tmparr.append(tr_v)
        else:
            tr_v = int(max_arr[n] - random.uniform(0, 1) * std_arr[n])
            tmparr.append(tr_v)
        last_num = tr_v
    luck_arr.append(tmparr)
#print(luck_arr)
for item in luck_arr:
    print(','.join('%s' %id for id in item)+'-'+str(random.randint(1,16)))


