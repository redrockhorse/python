# -*- coding:utf-8 -*-
#@Time : 2021/1/12 下午3:03
#@Author: kkkkibj@163.com
#@File : gridgps.py
#网格算法

import  math
#初始化 网格大小 此时地图 zoom = 5
grid_width = 0.03
grid_heigth = 0.03


def gridGPS(gpsArry,zoom):
    if zoom < 5:
        zoom =5
    if zoom > 18:
        zoom = 18

    result = []
    gridData = {}
    for i in len(gpsArry):
        lng = gpsArry[i][0]
        lat = gpsArry[i][1]
        grid_x = int(float(lng) / grid_width / 2**(5-zoom)) #x网格编号
        grid_y = int(float(lat) / grid_heigth / 2**(5-zoom)) #y网格编号
        grid_no = 'g' + '_' + str(grid_x) + '_' + str(grid_y)  #网格编号

        if grid_no not in gridData:
            gridData[grid_no] = []

        if len(gridData[grid_no]) < 1: #每个网格里有一条数据库
            gridData[grid_no].append(gpsArry[i])
            result.append(gpsArry[i])

    return result