#!/usr/bin/python
# encoding=utf-8
# lbp feature extraction
__author__ = 'mahy'

import random

t = []
for n in range(1000):
    p = random.uniform(0, 1)
    # print(p)
    # x = random.randint(0, 2)
    x = 0
    if p > 0.9 and p < 0.98:
        x = 1
    if p >= 0.98:
        x = 2
    t.append(x)
    # print(x)
from collections import Counter

print(Counter(t))

a = []
b = [2, 3, 4]
c = set(a) & set(b)
print(c)
print(len(c))

import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root', passwd='Qd@#$mo658', db='jc', port=3306, charset='utf8',
                       cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()
sql = "select *  from jc.td_ptl_lt_data   order by pdate asc"
cursor.execute(sql)
result = cursor.fetchall()
rs = []
lastRow = []
sampleItemCount = []
all = []
rownum = 0
v67 = []
for row in result:
    # print(row)
    all.append(int(row['v1']))
    all.append(int(row['v2']))
    all.append(int(row['v3']))
    all.append(int(row['v4']))
    all.append(int(row['v5']))
    v67.append(int(row['v6']))
    v67.append(int(row['v7']))
    rs = []
    rs.append(int(row['v1']))
    rs.append(int(row['v2']))
    rs.append(int(row['v3']))
    rs.append(int(row['v4']))
    rs.append(int(row['v5']))
    # print(len(set(rs) & set(lastRow)))
    sampleItemCount.append(len(set(rs) & set(lastRow)))
    lastRow = []
    lastRow.append(int(row['v1']))
    lastRow.append(int(row['v2']))
    lastRow.append(int(row['v3']))
    lastRow.append(int(row['v4']))
    lastRow.append(int(row['v5']))
    rownum += 1
print(Counter(sampleItemCount))
print(Counter(all))
print(rownum)
totalnum = rownum * 5

numArr = []
pArr = []
orderDic = Counter(all).most_common()
for k in orderDic:
    numArr.append(k[0])
    pArr.append(k[1])
print(numArr)
print(pArr)
import collections

d1 = collections.OrderedDict()
for i in range(len(numArr)):
    # print(i)
    d1[numArr[i]] = pArr[i]
print(d1)

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


xxx = sampleByP(numArr, pArr, 5)
print(xxx)

orderDic = Counter(v67).most_common()
numArr =[]
pArr =[]
for k in orderDic:
    numArr.append(k[0])
    pArr.append(k[1])
print("vvvvvvvvvvvvvvvvvvvvvvvvvv")
print(numArr)
print(pArr)
print("vvvvvvvvvvvvvvvvvvvvvvvvvv")
