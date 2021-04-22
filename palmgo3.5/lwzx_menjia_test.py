# -*- coding:utf-8 -*-
# @Time : 2021/1/13 上午11:21
# @Author: kkkkibj@163.com
# @File : lwzx_menjia_test.py
# 检测门架数据
import psycopg2
import csv

# postgresql链接
pgconn = psycopg2.connect(database="lwzx2020", user="postgres", password="postgres", host="192.168.220.246",
                          port="5432")
pgcursor = pgconn.cursor()

with open('/Users/hongyanma/gitspace/python/python/palmgo3.5/省界门架.csv', 'r',encoding='gbk') as f:
    line = f.readline()
    while line:
        # print(line)
        line = f.readline()
        row = line.split(',')
        # print(row)
        if len(row) > 3:
            tollpointid = row[1]
            name = row[2]
            sql = 'select * from public.lwzx_tollpoint where tollpointi=\''+tollpointid+'\'  limit 3'
            # print(sql)
            pgcursor.execute(sql)
            result = pgcursor.fetchall()
            # print(result)
            if len(result) > 0:
                if name != result[0][3]:
                    print(tollpointid+','+name+','+result[0][3])
            else:
                print(tollpointid)
