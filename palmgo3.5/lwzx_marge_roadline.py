# -*- coding:utf-8 -*-
# @Time : 2020/9/27 下午3:33
# @Author: kkkkibj@163.com
# @File : lwzx_marge_roadline.py
# 监测预警平台创建测试数据

import psycopg2

# postgresql链接
pgconn = psycopg2.connect(database="lwzx2020", user="postgres", password="123456", host="192.168.220.246", port="5432")
pgcursor = pgconn.cursor()

parr = [13, 14, 15, 21, 22, 23, 31, 32, 33, 34, 35, 36, 37, 41, 42, 43, 44, 45, 46, 50, 51, 52, 53, 54, 61, 62, 63, 64,
        65, 81, 82]


def insertData(d):
    sql = 'insert into public.roadline_polyline_temp  select lxbm,ST_Union(geom) as geom from public.roadline_polyline_' + str(
        d) + ' where lxbm is not null group by lxbm;'
    print(sql)


def main():
    for a in parr:
        insertData(a)


if __name__ == '__main__':
    main()
