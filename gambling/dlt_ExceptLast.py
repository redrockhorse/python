#!/usr/bin/python
# encoding=utf-8
# lbp feature extraction
__author__ = 'mahy'
import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root', passwd='Qd@#$mo658', db='jc', port=3306, charset='utf8',
                       cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()
sql = "select *  from jc.td_ptl_lt_data   order by pdate desc limit 1"
cursor.execute(sql)
result = cursor.fetchall()
rs = []
for row in result:
    print(row)
    rs.append(int(row['v1']))
    rs.append(int(row['v2']))
    rs.append(int(row['v3']))
    rs.append(int(row['v4']))
    rs.append(int(row['v5']))

l = []
for i in range(1, 36):
    if i not in rs:
        l.append(i)

b = []
for i in range(1, 13):
    b.append(i)

import random
import collections
import numpy as np
import copy

def sampleByP(narr, parr, n):
    rarr = []
    narrtemp = copy.deepcopy(narr)
    parrtemp = copy.deepcopy(parr)
    for i in range(n):
        totalnum = np.sum(parrtemp)
        p = random.uniform(0, 1)
        x0 = 0
        for nitem, pitem in zip(narrtemp, parrtemp):
            x0 += pitem / totalnum
            if p < x0:
                rarr.append(nitem)
                narrtemp.remove(nitem)
                parrtemp.remove(pitem)
                break
    return rarr


d1 = collections.OrderedDict()
numArr = [29, 33, 35, 32, 30, 31, 34, 22, 1, 19, 7, 23, 3, 18, 6, 14, 25, 5, 24, 11, 27, 13, 10, 28, 20, 2, 9, 12, 21,
          17, 26, 8, 15, 4, 16]
pArr = [347, 339, 324, 322, 309, 295, 293, 289, 269, 269, 267, 265, 261, 259, 258, 257, 255, 255, 254, 254, 254, 253,
        252, 245, 244, 241, 239, 239, 238, 237, 236, 231, 230, 221, 209]
v67a = [10, 11, 12, 5, 7, 3, 2, 9, 4, 8, 6, 1]
v67p = [339, 320, 319, 317, 310, 302, 301, 301, 297, 295, 293, 290]
for i in range(len(numArr)):
    d1[numArr[i]] = pArr[i]

larr = []
lparr = []
carr = []
cparr = []

for k in d1:
    if k in rs:
        larr.append(k)
        lparr.append(d1[k])
    else:
        carr.append(k)
        cparr.append(d1[k])
print('#######################################')
print(larr)
print(lparr)
print(carr)
print(cparr)
print('#######################################')

for n in range(5):
    p = random.uniform(0, 1)
    x = 0
    if 0.43 < p <= 0.85:
        x = 1
    if 0.85 < p <= 0.98:
        x = 2
    if p > 0.98:
        x = 3
    y = 5 - x
    # rbx = random.sample(rs, x)
    # rby = random.sample(l, y)
    rbx = sampleByP(larr, lparr, x)
    rby = sampleByP(carr, cparr, y)
    result = sorted(rbx + rby)
    result_str = ''
    for num in result:
        split_str = '，'
        if result.index(num) == (len(result) - 1):
            split_str = ' - '
        if num < 10:
            result_str += '0' + str(num) + split_str
        else:
            result_str += str(num) + split_str
    # br = sorted(random.sample(b, 2))
    br = sorted(sampleByP(v67a, v67p, 2))
    if br[0] < 10:
        result_str += '0' + str(br[0])
    else:
        result_str += str(br[0])
    if br[1] < 10:
        result_str += '，0' + str(br[1])
    else:
        result_str += '，' + str(br[1])
    print(result_str)
