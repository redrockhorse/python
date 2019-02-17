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

def albyweek(datestr,week):
    sql="select *  from td_ptl_ssq_data where pdate<%s and dayofweek(pdate)=%s"
    cursor.execute(sql,(datestr,week))
    v1_result = cursor.fetchall()
    dic ={}
    for row in v1_result:
        if row['v1'] not in dic:
            dic[row['v1']]=0
        if row['v2'] not in dic:
            dic[row['v2']]=0
        if row['v3'] not in dic:
            dic[row['v3']]=0
        if row['v4'] not in dic:
            dic[row['v4']]=0
        if row['v5'] not in dic:
            dic[row['v5']]=0
        if row['v6'] not in dic:
            dic[row['v6']]=0
        dic[row['v1']]+=1
        dic[row['v2']]+=1
        dic[row['v3']] += 1
        dic[row['v4']] += 1
        dic[row['v5']] += 1
        dic[row['v6']] += 1
    #print(dic)
    hqlist =[]
    for key in dic:
        hqlist.append((key,dic[key]))
    hqlist.sort(key = lambda l: (l[1]),reverse=True)
    #print(hqlist)
    rdic ={}
    for i in range(len(hqlist)):
        rdic[hqlist[i][0]]=i+1
    return rdic



'''
sql="select DAYOFWEEK(pdate) as pweek,v7,count(*) as cnt from td_ptl_ssq_data group by DAYOFWEEK(pdate),v7 order by count(*) desc"
cursor.execute(sql)
v1_result = cursor.fetchall()
for row in v1_result:
   print(row)
'''

sql="select *,DAYOFWEEK(pdate) as pweek  from td_ptl_ssq_data order by pdate desc limit 100"
cursor.execute(sql)
v1_result = cursor.fetchall()
adic = {}
for row in v1_result:
   #print(row['pdate'].strftime("%Y-%m-%d"))
   #print(row['pweek'])
   rdic = albyweek(row['pdate'].strftime("%Y-%m-%d"), row['pweek'])
   if rdic[row['v1']] not in adic:
       adic[rdic[row['v1']]] =0
   if rdic[row['v2']] not in adic:
       adic[rdic[row['v2']]] =0
   if rdic[row['v3']] not in adic:
       adic[rdic[row['v3']]] =0
   if rdic[row['v4']] not in adic:
       adic[rdic[row['v4']]] =0
   if rdic[row['v5']] not in adic:
       adic[rdic[row['v5']]] =0
   if rdic[row['v6']] not in adic:
       adic[rdic[row['v6']]] =0
   adic[rdic[row['v1']]]+=1
   adic[rdic[row['v2']]] += 1
   adic[rdic[row['v3']]] += 1
   adic[rdic[row['v4']]] += 1
   adic[rdic[row['v5']]] += 1
   adic[rdic[row['v6']]] += 1
   print(rdic[row['v1']],print(rdic[row['v2']]),print(rdic[row['v3']]),print(rdic[row['v4']]),print(rdic[row['v5']]),print(rdic[row['v6']]))
print(adic)


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

'''