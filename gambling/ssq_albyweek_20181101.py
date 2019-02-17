# -*- coding: utf8 -*-
# !/usr/bin/python
# 根据周几进行分析

import pymysql
import sys
import datetime
import numpy as np
import decimal


#在 B 出现的条件下A出现的概率
#B出现的概率
#B且A出现的概率
#P(A|B)=P(AB)/P(B)
conn=pymysql.connect(host='127.0.0.1',user='root',passwd='Qd@#$mo658',db='jc',port=3306,charset='utf8', cursorclass = pymysql.cursors.DictCursor)
cursor = conn.cursor()

from collections import Counter
def counter(arr):
    return Counter(arr).most_common(3)

sql="select *  from td_ptl_ssq_data"
cursor.execute(sql)
v1_result = cursor.fetchall()
v1=[]
v2=[]
v3=[]
v4=[]
v5=[]
v6=[]
v7=[]
for row in v1_result:
    #print(row)
    v1.append(row['v1'])
    v2.append(row['v2'])
    v3.append(row['v3'])
    v4.append(row['v4'])
    v5.append(row['v5'])
    v6.append(row['v6'])
    v7.append(row['v7'])


v1dic = {}
v2dic = {}
v3dic = {}
v4dic = {}
v5dic = {}
v6dic = {}
v7dic = {}

for i in range(len(v1) - 1):
    if v1[i] not in v1dic:
        v1dic[v1[i]] = []
    v1dic[v1[i]].append(v1[i + 1])

for i in range(len(v2) - 1):
    if v2[i] not in v2dic:
        v2dic[v2[i]] = []
    v2dic[v2[i]].append(v2[i + 1])

for i in range(len(v3) - 1):
    if v3[i] not in v3dic:
        v3dic[v3[i]] = []
    v3dic[v3[i]].append(v3[i + 1])

for i in range(len(v4) - 1):
    if v4[i] not in v4dic:
        v4dic[v4[i]] = []
    v4dic[v4[i]].append(v4[i + 1])

for i in range(len(v5) - 1):
    if v5[i] not in v5dic:
        v5dic[v5[i]] = []
    v5dic[v5[i]].append(v5[i + 1])

for i in range(len(v6) - 1):
    if v6[i] not in v6dic:
        v6dic[v6[i]] = []
    v6dic[v6[i]].append(v6[i + 1])

for i in range(len(v7) - 1):
    if v7[i] not in v7dic:
        v7dic[v7[i]] = []
    v7dic[v7[i]].append(v7[i + 1])


'''
print(v1dic['01'])
print(v2dic['03'])
print(v3dic['04'])
print(v4dic['11'])
print(v5dic['29'])
print(v6dic['08'])
print(v7dic['12'])


print(counter(v1dic['02']))
print(counter(v2dic['05']))
print(counter(v3dic['06']))
print(counter(v4dic['07']))
print(counter(v5dic['11']))
print(counter(v6dic['15']))
print(counter(v7dic['12']))
'''

from collections import Counter
AB = Counter(v7dic['12'])

B = Counter(v7)

PB=B['12']/len(v7)*1.00

for key in AB:

    PAB=AB[key]/len(v7)*1.00

    print(key + " : " + str(PAB / PB))

#1,2,3
#6,8
#13,14,10
#20,23,26
#32,16,13
#31,32,22
#09,13,10

