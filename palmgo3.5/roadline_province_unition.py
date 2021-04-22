# -*- coding:utf-8 -*-
#@Time : 2021/4/16 下午2:49
#@Author: kkkkibj@163.com
#@File : roadline_province_unition.py

import psycopg2

# postgresql链接
pgconn = psycopg2.connect(database="lwzx2020", user="postgres", password="postgres", host="192.168.220.246", port="5432")
pgcursor = pgconn.cursor()

pcode_arr = [11,12,13,14,15,21,22,23,31,32,33,34,35,36,37,41,42,43,44,45,35,46,50,51,52,53,54,61,62,63,64,65,81,82]


with open('/Users/hongyanma/Desktop/roadname_provincename.csv','w') as wfile:
    for i in pcode_arr:
        tablename = 'public.roadline_polyline_' + str(i)
        sql = "select lxbm || '_' || lxmc as roadname,fdsss as provincename from public.roadline_polyline_"+str(i)+" where kind like '00%' and lxbm is not null group by roadname,provincename;"
        pgcursor.execute(sql)
        result = pgcursor.fetchall()
        for row in result:
            print(row)
            wfile.write(row[0]+','+row[1]+'\n')


# for i in pcode_arr:
#     sql = 'insert into public.roadline_polyline_highway_temp  select lxbm,lxmc,fdsss, ST_Union(geom) as geom from public.roadline_polyline_'+str(i)+' where lxbm is not null group by lxbm,lxmc,fdsss;'
#     print(sql)