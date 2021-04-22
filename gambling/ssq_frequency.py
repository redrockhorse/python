# -*- coding:utf-8 -*-
#@Time : 2021/3/5 下午6:48
#@Author: kkkkibj@163.com
#@File : dlt_frequency.py
__author__ = 'mahy'
import pymysql
import numpy as np
import json
data = np.array(np.mat(np.zeros((7,35))))


conn = pymysql.connect(host='127.0.0.1', user='root', passwd='Qd@#$mo658', db='jc', port=3306, charset='utf8',
                       cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()


for i in range(7):
    vstr = str(i+1)
    sql = 'select v'+vstr+',count(v'+vstr+') as cv'+vstr+' from td_ptl_lt_data group by v'+vstr+' order by cv'+vstr+' desc;'
    # print(sql)
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        # print(row)
        data[i][int(row['v'+vstr])-1] = int(row['cv'+vstr])
# print(data)

xdata = np.arange(0,35,1)
# print(xdata)
print(json.dumps(xdata.tolist()))

series =[]
for i in range(7):
    tempObj = {}
    tempObj['name'] = 'p'+str(i+1)
    tempObj['data'] = data[i].tolist()
    tempObj['type'] = 'line'
    tempObj['areaStyle'] = '{}'
    series.append(tempObj)

print(json.dumps(series))


sqlall = 'select * from td_ptl_lt_data order by pdate asc;'
cursor.execute(sqlall)
result = cursor.fetchall()
print(len(result))
alldata = np.array(np.mat(np.zeros((len(result),36))))
x = 0
for row in result:
    # print(row)
    for i in range(6):
        vstr = str(i + 1)
        alldata[x][int(row['v'+vstr])] = 1
    x += 1
# print(alldata)
# print('============')
# print(alldata.T)
alldataT = alldata.T
# print(len(alldataT))
result = {}

from collections import Counter
for i in range(1,36):
    result['v'+str(i)] = []
    ctemp = alldataT[i]
    # print(ctemp.tolist())
    # print(''.join(str(int(ctemp.tolist()))))
    out_list = [str(int(c)) for c in ctemp.tolist()]
    out_list_str = ''.join(out_list)
    # print(out_list_str.split('1'))
    count_list = [len(s) for s in out_list_str.split('1')]
    print('v'+str(i))
    print(Counter(count_list))
