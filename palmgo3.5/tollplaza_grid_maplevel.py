# -*- coding:utf-8 -*-
# @Time : 2021/1/23 下午4:20
# @Author: kkkkibj@163.com
# @File : camera_grid_maplevel.py
# 用网格法将收费站广场分级
import psycopg2

# postgresql链接
pgconn = psycopg2.connect(database="lwzx2020", user="postgres", password="postgres", host="192.168.220.246",
                          port="5432")
pgcursor = pgconn.cursor()

# startmaplevel = 20  # 假设地图最大等级为20
# grid_side_length = 9.1552734375e-07  # 初始网格边长，在20级时网格大小，网格越小，数量就越多

startmaplevel = 14  # 假设地图最大等级为20
grid_side_length = 0.0001171875 * 8  # 初始网格边长，在20级时网格大小，网格越小，数量就越多

# 每个网格只有一个点

sql = 'select id,lng,lat from public.lwzx_tollplaza'
maplevel = startmaplevel
while maplevel > 4:
    print(maplevel)
    print(grid_side_length)
    print('-------------------------------')
    maplevel = maplevel - 1
    grid_side_length = grid_side_length * 2
    pgcursor.execute(sql)
    result = pgcursor.fetchall()
    gridmap = {}
    keyarray = []
    i = 0
    for row in result:
        id = row[0]
        lng = row[1]
        lat = row[2]
        grid_x = int(float(lng) / grid_side_length)
        grid_y = int(float(lat) / grid_side_length)
        grid_no = 'g' + '_' + str(grid_x) + '_' + str(grid_y)
        # print(id,lng,lat,grid_x,grid_y)
        if grid_no in gridmap:
            pass
        else:
            gridmap[grid_no] = []
            keyarray.append(id)
            updatesql = 'update public.lwzx_tollplaza set zoom=' + str(maplevel) + ' where id=\'' + id + '\';'
            pgcursor.execute(updatesql)
        gridmap[grid_no].append(id)
        if i % 5000 == 0:
            print(i)
        i += 1
    print(len(keyarray))
    pgconn.commit()

