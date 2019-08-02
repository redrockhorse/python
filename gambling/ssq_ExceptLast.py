#!/usr/bin/python
# encoding=utf-8
# lbp feature extraction
__author__ = 'mahy'
import pymysql
conn = pymysql.connect(host='127.0.0.1', user='root', passwd='Qd@#$mo658', db='jc', port=3306, charset='utf8',
                       cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()
sql = "select *  from jc.td_ptl_ssq_data   order by pdate desc limit 1"
cursor.execute(sql)
result = cursor.fetchall()
rs = []
for row in result:
    print(row)
    rs.append(int(row['v1']))
    rs.append(int(row['v2']))
    rs.append(int(row['v3']))
    rs.append(int(row['v4']))
    rs.append(int(row['v5']))
    rs.append(int(row['v6']))
# print(rs)

l = []
for i in range(1, 34):
    if i not in rs:
        l.append(i)
# print(l)

b = []
for i in range(1, 17):
    b.append(i)
# print(b)

import random

for n in range(5):
    x = random.randint(0, 3)
    y = 6 - x
    rbx = random.sample(rs, x)
    rby = random.sample(l, y)
    result = sorted(rbx + rby)
    result_str = ''
    for num in result:
        split_str = '，'
        if result.index(num) == (len(result) - 1):
            split_str = ' - '
        if num < 10:
            result_str += '0' + str(num) + split_str
        else:
            result_str += str(num) + split_str
    br = random.sample(b, 1)
    if br[0] < 10:
        result_str += '0' + str(br[0])
    else:
        result_str += str(br[0])
    print(result_str)
