# -*- coding:utf-8 -*-
# @Time : 2020/4/24 下午4:43
# @Author: kkkkibj@163.com
# @File : ssq_tf_pre.py

import tensorflow as tf
import numpy as np
import pymysql


conn = pymysql.connect(host='127.0.0.1', user='root', passwd='Qd@#$mo658', db='jc', port=3306, charset='utf8',
                       cursorclass=pymysql.cursors.DictCursor)


def miniDistance(arr1,arr2):
    result = 0
    for item2 in arr2:
        # print(item1)
        tmp = 1000000000000
        for item1 in arr1:
            if tmp > abs(item2 - item1):
                tmp = abs(item2 - item1)
        result += tmp
        #print(result)
    if result < 10 and arr1[2] ==16:
        print(arr1)
        print(arr2)
        print('====================')
    return result



cursor = conn.cursor()
cursor_lt = conn.cursor()
ltdata = []
sql = "select *  from jc.td_ptl_ssq_data where pdate>'2018-02-27'  order by pdate asc"
cursor.execute(sql)
result = cursor.fetchall()
rs = []
data = []

distance_arr = []
for row in result:
    rowdata = np.zeros(64)
    # print(row)
    rowdata[int(row['v1']) - 1] = 1
    rowdata[int(row['v2']) - 1] = 1
    rowdata[int(row['v3']) - 1] = 1
    rowdata[int(row['v4']) - 1] = 1
    rowdata[int(row['v5']) - 1] = 1
    rowdata[int(row['v6']) - 1] = 1
    rowdata[int(row['v7']) + 32] = 1
    arr1 = []
    arr1.append(int(row['v1']))
    arr1.append(int(row['v2']))
    arr1.append(int(row['v3']))
    arr1.append(int(row['v4']))
    arr1.append(int(row['v5']))
    arr1.append(int(row['v6']))

    # print(row['pdate'])

    sql_lt = "select *  from jc.td_ptl_lt_data where pdate>'2018-02-27' and pdate > '" + row['pdate'].strftime(
        '%Y-%m-%d') + "'  order by pdate asc limit 1"
    cursor_lt.execute(sql_lt)
    result_lt = cursor_lt.fetchall()
    rs_lt = []
    for row_lt in result_lt:
        rowdata_lt = np.zeros(64)
        # print(row_lt)
        rowdata_lt[int(row_lt['v1']) - 1] = 1
        rowdata_lt[int(row_lt['v2']) - 1] = 1
        rowdata_lt[int(row_lt['v3']) - 1] = 1
        rowdata_lt[int(row_lt['v4']) - 1] = 1
        rowdata_lt[int(row_lt['v5']) - 1] = 1
        rowdata_lt[int(row_lt['v6']) + 34] = 1
        rowdata_lt[int(row_lt['v7']) + 34] = 1
        arr2 = []
        arr2.append(int(row_lt['v1']))
        arr2.append(int(row_lt['v2']))
        arr2.append(int(row_lt['v3']))
        arr2.append(int(row_lt['v4']))
        arr2.append(int(row_lt['v5']))
        # print(rowdata.tolist())
        #print(rowdata_lt.tolist())
        data.append(rowdata.tolist())
        ltdata.append(rowdata_lt.tolist())
        n = miniDistance(arr1, arr2)
        distance_arr.append(n)
# print(np.array(data).shape)
# print(len(data))
# print(ltdata)
# print(len(ltdata))
#print(len(data))
#print(len(ltdata))
print(distance_arr)

narr = np.array(distance_arr)
print(narr.max())
print(narr.min())
print(narr.mean())
# print(narr.median())
print(np.median(narr))
from collections import Counter
print(Counter(distance_arr))