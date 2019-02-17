# -*- coding: utf8 -*-
# !/usr/bin/python
# 根据周几进行分析

import pymysql
conn=pymysql.connect(host='127.0.0.1',user='root',passwd='Qd@#$mo658',db='jc',port=3306,charset='utf8', cursorclass = pymysql.cursors.DictCursor)
cursor = conn.cursor()

from collections import Counter
lastnum=[4,14,16,23,28,29]
total =[]
total_blue=[]
sql="select * from td_ptl_ssq_data order by pdate asc"#td_ptl_ssq_data,td_ptl_lt_data
cursor.execute(sql)
v1_result = cursor.fetchall()
#8,12,16,19,26,32
for row in v1_result:
    tmpstr =row['v1']+','+row['v2']+','+row['v3']+','+row['v4']+','+row['v5']+','+row['v6']
    #print(tmpstr)
    if tmpstr.find('02') ==-1 and tmpstr.find('04') ==-1 and tmpstr.find('05') ==-1 and tmpstr.find('08') ==-1 and tmpstr.find('11') ==-1 and tmpstr.find('30') ==-1:
        #print(tmpstr)
        total.append(row['v1'])
        total.append(row['v2'])
        total.append(row['v3'])
        total.append(row['v4'])
        total.append(row['v5'])
        total.append(row['v6'])
        total_blue.append(row['v7'])

import itertools
sequence=[]
print(Counter(total).most_common(10))
for item in Counter(total).most_common(10):
    sequence.append(item[0])
print(Counter(total_blue).most_common(5))
print('-----------------------------------')
n =0

for i in itertools.combinations(sequence,6):
    n+=1
    if n%39==0:
        print(i[0]+','+i[1]+','+i[2]+','+i[3]+','+i[4]+','+i[5])