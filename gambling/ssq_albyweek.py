# -*- coding: utf8 -*-
# !/usr/bin/python
# 根据周几进行分析

import pymysql
import sys
import datetime
import numpy as np
import decimal

conn=pymysql.connect(host='127.0.0.1',user='root',passwd='Qd@#$mo658',db='jc',port=3306,charset='utf8', cursorclass = pymysql.cursors.DictCursor)
cursor = conn.cursor()

#sql="select DAYOFWEEK(pdate) as pweek,v7,count(*) as cnt from td_ptl_ssq_data group by DAYOFWEEK(pdate),v7 order by count(*) desc"
#sql="select DAYOFWEEK(pdate) as pweek,v1,count(*) as cnt from td_ptl_ssq_data group by DAYOFWEEK(pdate),v1 order by count(*) desc"
#sql="select DAYOFWEEK(pdate) as pweek,v7,count(*) as cnt from td_ptl_ssq_data group by DAYOFWEEK(pdate),v7 order by count(*) desc"
#sql="select DAYOFWEEK(pdate) as pweek,v7,count(*) as cnt from td_ptl_ssq_data group by DAYOFWEEK(pdate),v7 order by count(*) desc"
#sql="select DAYOFWEEK(pdate) as pweek,v7,count(*) as cnt from td_ptl_ssq_data group by DAYOFWEEK(pdate),v7 order by count(*) desc"
#sql="select DAYOFWEEK(pdate) as pweek,v7,count(*) as cnt from td_ptl_ssq_data group by DAYOFWEEK(pdate),v7 order by count(*) desc"
#sql="select DAYOFWEEK(pdate) as pweek,v7,count(*) as cnt from td_ptl_ssq_data group by DAYOFWEEK(pdate),v7 order by count(*) desc"
sql="select *,DAYOFWEEK(pdate) as pweek  from td_ptl_ssq_data"
cursor.execute(sql)
v1_result = cursor.fetchall()
dic ={}
for row in v1_result:
    #print(row)
    if row['pweek'] not in dic:
        dic[row['pweek']]={}
    if row['v1'] not in dic[row['pweek']]:
        dic[row['pweek']][row['v1']]=0
    if row['v2'] not in dic[row['pweek']]:
        dic[row['pweek']][row['v2']]=0
    if row['v3'] not in dic[row['pweek']]:
        dic[row['pweek']][row['v3']]=0
    if row['v4'] not in dic[row['pweek']]:
        dic[row['pweek']][row['v4']]=0
    if row['v5'] not in dic[row['pweek']]:
        dic[row['pweek']][row['v5']]=0
    if row['v6'] not in dic[row['pweek']]:
        dic[row['pweek']][row['v6']]=0
    dic[row['pweek']][row['v1']]+=1
    dic[row['pweek']][row['v2']]+=1
    dic[row['pweek']][row['v3']] += 1
    dic[row['pweek']][row['v4']] += 1
    dic[row['pweek']][row['v5']] += 1
    dic[row['pweek']][row['v6']] += 1
#print(dic)
weekindex=1
hqlist =[]
for key in dic[weekindex]:
    hqlist.append((key,dic[weekindex][key]))
hqlist.sort(key = lambda l: (l[1]),reverse=True)
print(hqlist)

n=[5,1,7]
r=[]
t=-1
i=0
while len(r)<7:
    t+=n[i%3]
    r.append(hqlist[t%len(hqlist)])
    i+=1
print(r)

sql="select DAYOFWEEK(pdate) as pweek,v7,count(*) as cnt from td_ptl_ssq_data group by DAYOFWEEK(pdate),v7 order by count(*) desc"
cursor.execute(sql)
v1_result = cursor.fetchall()
for row in v1_result:
   print(row)
'''
SELECT
    CASE dayofweek(now())
WHEN 1 THEN
    '星期日'
WHEN 2 THEN
    '星期一'
WHEN 3 THEN
    '星期二'
WHEN 4 THEN
    '星期三'
WHEN 5 THEN
    '星期四'
WHEN 6 THEN
    '星期五'
WHEN 7 THEN
    '星期六'
END
FROM
    DUAL

sql = "select v1,v2,v3,v4,v5,v6,v7,pdate from td_ptl_ssq_data  order by pdate asc"
cursor.execute(sql)
v1_result = cursor.fetchall()
tmp ={}
i=0
n=0
tarr =[]
for row in v1_result:
    n+=1
    t=0
    #if row['v1'] in tmp or row['v2'] in tmp or row['v3'] in tmp or row['v4'] in tmp  or row['v5'] in tmp or row['v6'] in tmp:
    #    i+=1
    if row['v1'] in tmp:
        t+=1
    if row['v2'] in tmp:
        t += 1
    if row['v3'] in tmp:
        t+=1
    if row['v4'] in tmp:
        t+=1
    if row['v5'] in tmp:
        t+=1
    if row['v6'] in tmp:
        t+=1
    if t==2:
        i+=1
    tarr.append(t)
    tmp.clear()
    tmp[row['v1']]=1
    tmp[row['v2']] = 1
    tmp[row['v3']] = 1
    tmp[row['v4']] = 1
    tmp[row['v5']] = 1
    tmp[row['v6']] = 1
print(i)
print(n)
print(i/n*1.00)
print(tarr)

sql = "select v1,v2,v3,v4,v5,v6,v7,pdate from td_ptl_ssq_data  order by pdate asc"
cursor.execute(sql)
v1_result = cursor.fetchall()
tmp ={}
i=0
n=0
tarr =[]
for row in v1_result:
    n+=1
    t=0
    #if row['v1'] in tmp or row['v2'] in tmp or row['v3'] in tmp or row['v4'] in tmp  or row['v5'] in tmp or row['v6'] in tmp:
    #    i+=1
    if str(int(row['v1'])+1) in tmp or str(int(row['v1'])-1) in tmp:
        t+=1
    if str(int(row['v2'])+1) in tmp or str(int(row['v2'])-1) in tmp:
        t += 1
    if str(int(row['v3'])+1) in tmp or str(int(row['v3'])-1) in tmp:
        t+=1
    if str(int(row['v4'])+1) in tmp or str(int(row['v4'])-1) in tmp:
        t+=1
    if str(int(row['v5'])+1) in tmp or str(int(row['v5'])-1) in tmp:
        t+=1
    if str(int(row['v6'])+1) in tmp or str(int(row['v6'])-1) in tmp:
        t+=1
    if t>0:
        i+=1
    tarr.append(t)
    tmp.clear()
    tmp[row['v1']]=1
    tmp[row['v2']] = 1
    tmp[row['v3']] = 1
    tmp[row['v4']] = 1
    tmp[row['v5']] = 1
    tmp[row['v6']] = 1
print(i)
print(n)
print(i/n*1.00)
print(tarr)

'''