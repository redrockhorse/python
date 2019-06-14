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
sql="select *,DAYOFWEEK(pdate) as pweek  from td_ptl_lt_data"
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
    dic[row['pweek']][row['v1']]+=1
    dic[row['pweek']][row['v2']]+=1
    dic[row['pweek']][row['v3']] += 1
    dic[row['pweek']][row['v4']] += 1
    dic[row['pweek']][row['v5']] += 1
#print(dic)

sql="select *,DAYOFWEEK(pdate) as pweek  from td_ptl_lt_data"
cursor.execute(sql)
v1_result = cursor.fetchall()
tdic ={}
for row in v1_result:
    #print(row)
    if row['pweek'] not in tdic:
        tdic[row['pweek']]={}
    if row['v6'] not in tdic[row['pweek']]:
        tdic[row['pweek']][row['v6']]=0
    if row['v7'] not in tdic[row['pweek']]:
        tdic[row['pweek']][row['v7']]=0
    tdic[row['pweek']][row['v6']]+=1
    tdic[row['pweek']][row['v7']]+=1
#print(tdic)

weekindex=2
qqlist =[]
for key in dic[weekindex]:
    qqlist.append((key,dic[weekindex][key]))
#print(qqlist)
#print(qqlist.sort(key = lambda l: (l[1]),reverse=True))
qqlist.sort(key = lambda l: (l[1]),reverse=True)
print(qqlist)
hqlist=[]
for key in tdic[weekindex]:
    hqlist.append((key,tdic[weekindex][key]))
hqlist.sort(key = lambda l: (l[1]),reverse=True)
print(hqlist)


n=[1,5,7]
r=[]
t=-1
i=0
while len(r)<7:
    t+=n[i%3]
    r.append(qqlist[t%len(qqlist)])
    i+=1
print(r)
