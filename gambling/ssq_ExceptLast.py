#!/usr/bin/python
# encoding=utf-8
# lbp feature extraction
__author__ = 'mahy'
import pymysql
conn = pymysql.connect(host='127.0.0.1', user='root', passwd='Qd@#$mo658', db='jc', port=3306, charset='utf8',
                       cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()
sql = "select *  from jc.td_ptl_ssq_data   order by pdate desc limit 1"
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
    rs.append(int(row['v6']))
# print(rs)

l = []
for i in range(1, 34):
    if i not in rs:
        l.append(i)
# print(l)

b = []
for i in range(1, 17):
    b.append(i)
# print(b)

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
numArr = [14, 1, 22, 20, 26, 18, 32, 8, 7, 17, 6, 19, 13, 3, 27, 5, 30, 25, 10, 2, 16, 12, 4, 11, 21, 23, 9, 29, 31, 15, 28, 24, 33]
pArr = [478, 475, 474, 471, 468, 466, 459, 458, 455, 454, 453, 448, 446, 446, 441, 440, 440, 438, 436, 435, 434, 432, 431, 431, 428, 427, 426, 422, 420, 416, 407, 401, 376]
v67a = [12, 9, 11, 16, 14, 1, 7, 15, 13, 5, 6, 10, 3, 4, 2, 8]
v67p = [169, 165, 163, 161, 157, 155, 152, 151, 150, 149, 148, 148, 147, 142, 139, 126]
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
frarr = [0,1,2]
frparr = [904,76,20]

for n in range(5):
    # x = random.randint(0, 3)
    xarr = sampleByP(frarr, frparr, 1)
    x = xarr[0]
    y = 6 - x
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
    # br = random.sample(b, 1)
    br = sampleByP(v67a, v67p, 2)
    if br[0] < 10:
        result_str += '0' + str(br[0])
    else:
        result_str += str(br[0])
    print(result_str)
