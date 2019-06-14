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


#'2431','2019-05-26','03','04','14','20','23','27','01','2019060'
sql="select *  from jc.td_ptl_ssq_data where v1='03' and v2='04' order by pdate asc"
cursor.execute(sql)
v1_result = cursor.fetchall()
dic ={}
v1arr = []
v2arr = []
v3arr = []
v4arr = []
v5arr = []
v6arr = []
v7arr = []

tmp_date =''
for row in v1_result:
    #print(row['pdate'].strftime('%Y-%m-%d'))
    subsql = "select *  from jc.td_ptl_lt_data where pdate > '"+row['pdate'].strftime('%Y-%m-%d')+"' and pdate>'2009-07-10'  order by pdate asc limit 1" #and pdate>'2009-07-10'
    cursor.execute(subsql)
    #print(row['pdate'])
    sub_result = cursor.fetchall()
    for sub_row in sub_result:
        if tmp_date != sub_row['pdate']:
            #print(sub_row)
            v1arr.append(sub_row['v1'])
            v2arr.append(sub_row['v2'])
            v3arr.append(sub_row['v3'])
            v4arr.append(sub_row['v4'])
            v5arr.append(sub_row['v5'])
            v6arr.append(sub_row['v6'])
            v7arr.append(sub_row['v7'])
        tmp_date = sub_row['pdate']
from collections import Counter

print(Counter(v1arr).most_common(1)[0][0])
print(Counter(v2arr).most_common(1)[0][0])
print(Counter(v3arr).most_common(2)[1][0])
print(Counter(v4arr).most_common(1)[0][0])
print(Counter(v5arr).most_common(4)[3][0])
print(Counter(v6arr).most_common(1)[0][0])
print(Counter(v7arr).most_common(3)[2][0])

'''
col_sql = "select v3,count(v3) from  jc.td_ptl_ssq_data where v1='02' and v2='03' group by v3  order by count(v3) desc limit 3"
#col_sql = "select v3,count(v3) from  jc.td_ptl_ssq_data where v2='03' group by v2  order by count(v2) desc"
cursor.execute(col_sql)
col_result = cursor.fetchall()
for col_row in col_result:
    print(col_row)

#02,03,07,14,16,26
#02,03,20,21,28,27
2,3,7,20,26,28
'3865','2019-05-25','07','08','15','27','32','08','12','19059'

'''