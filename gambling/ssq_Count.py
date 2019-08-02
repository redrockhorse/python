#!/usr/bin/python
#encoding=utf-8
#lbp feature extraction
__author__ = 'mahy'

import pymysql
import numpy as np
from PIL import Image
import matplotlib.pyplot as pyplot
# conn=pymysql.connect(host='127.0.0.1',user='root',passwd='Qd@#$mo658',db='jc',port=3306,charset='utf8', cursorclass = pymysql.cursors.DictCursor)
# cursor = conn.cursor()
#
# sql="select *  from jc.td_ptl_ssq_data   order by pdate asc"
# cursor.execute(sql)
# result = cursor.fetchall()
#
# rs = []
# for row in result:
#     #print(row)
#     rs.append(row['v1'])
#     rs.append(row['v2'])
#     rs.append(row['v3'])
#     rs.append(row['v4'])
#     rs.append(row['v5'])
#     rs.append(row['v6'])
#
# from collections import Counter
# #print(Counter(rs))
# c = Counter(rs)
# for key in Counter(rs):
#     print(key)
#     print(c[key] / 440)
import random
#print(random.uniform(0.8,1.1))
l =[]
for i in range(1,20):
    l.append(i)
print(l)

r =[]
for i in range(24,34):
    r.append(i)
print(r)

b = []
for i in range(1,17):
    b.append(i)
print(b)

#print(random.sample(l,4))
#print(random.sample(r,2))

n=4
for i in range(n):
    lr = random.sample(l,4)
    rr = random.sample(r,2)
    br = random.sample(b,1)
    lr.extend(rr)
    red = sorted(lr)
    result = ''
    for num in red :
        if num <10:
            result += '0'+str(num)+','
        else:
            result += str(num) + ','
    if br[0] < 10:
        result +='-'+'0'+str(br[0])
    else:
        result += '-'  + str(br[0])
    #print(result)

h=[]
for i in range(34):
    h.append(i)
x = random.randint(1,4)
y = sorted(random.sample(h,6))
print(y)