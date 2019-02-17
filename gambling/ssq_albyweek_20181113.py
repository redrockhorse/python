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
l=len(v1)
print(l)
#print(len(v1))
#print(v1.count('01')/l*1.00)

v1p=[]
v2p=[]
v3p=[]
v4p=[]
v5p=[]
v6p=[]
v7p=[]

n=100
i=1
while i<n+1:
    c = l-i+1
    #print(v1.count(v1[l-i])/c*1.00,v2.count(v2[l-i])/c*1.00,v3.count(v3[l-i])/c*1.00,v4.count(v4[l-i])/c*1.00,v5.count(v5[l-i])/c*1.00,v6.count(v6[l-i])/c*1.00,v7.count(v7[l-i])/c*1.00)
    e= v1.count(v1[l-i])/c*1.00+v2.count(v2[l-i])/c*1.00+v3.count(v3[l-i])/c*1.00+v4.count(v4[l-i])/c*1.00+v5.count(v5[l-i])/c*1.00+v6.count(v6[l-i])/c*1.00
    #print(e/6)
    v1p.append(v1.count(v1[l-i])/c*1.00)
    v2p.append(v2.count(v2[l-i])/c*1.00)
    v3p.append(v3.count(v3[l-i])/c*1.00)
    v4p.append(v4.count(v4[l-i])/c*1.00)
    v5p.append(v5.count(v5[l-i])/c*1.00)
    v6p.append(v6.count(v6[l-i])/c*1.00)
    v7p.append(v7.count(v7[l-i])/c*1.00)
    i+=1


x = lambda d:sum(d)/len(d)
print('-------------------------')
print(x(v1p))
print(x(v2p))
print(x(v3p))
print(x(v4p))
print(x(v5p))
print(x(v6p))
print(x(v7p))
print('-------------------------')
#B = Counter(v1p)
#print(B)

#from collections import Counter
B = Counter(v7)
#print(B)
#v1p=[]
for key in B:
    print(key,B[key]/l*1.00)
    #v1p.append(B[key]/l*1.00)
#print(v1p)
#x = lambda d:sum(d)/len(d)
#print(x(v1p))

#v1 0.043478260869565216
#v2 0.038461538461538464
#v3 0.037037037037037035
#v4 0.037037037037037035
#v5 0.03846153846153847
#v6 0.047619047619047616
#v7 0.06249999999999999
#print(len(v1p))
#print(v7p)
#print(v1)
'''
y=[]
for i in range(len(v1p)):
    y.append(i)
print(y)
'''