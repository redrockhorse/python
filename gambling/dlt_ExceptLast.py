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
numArr = [29, 33, 35, 32, 30, 31, 34, 22, 19, 1, 7, 23, 3, 18, 27, 5, 6, 14, 25, 13, 10, 11, 24, 20, 28, 2, 17, 9, 21, 12, 26, 15, 8, 4, 16]
pArr = [349, 344, 331, 325, 317, 299, 299, 294, 280, 276, 273, 272, 269, 266, 266, 266, 263, 262, 260, 260, 258, 258, 256, 251, 250, 248, 245, 245, 245, 244, 243, 236, 236, 225, 214]
v67a = [10, 12, 11, 5, 7, 2, 3, 4, 9, 6, 8, 1]
v67p = [346, 330, 326, 325, 316, 312, 310, 305, 305, 303, 298, 294]
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
frarr = [1,0,2,3]
frparr = [225,222,73,9]
for n in range(5):
    # p = random.uniform(0, 1)
    # x = 0
    # if 0.43 < p <= 0.85:
    #     x = 1
    # if 0.85 < p <= 0.98:
    #     x = 2
    # if p > 0.98:
    #     x = 3
    xarr = sampleByP(frarr, frparr, 1)
    x = xarr[0]
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
