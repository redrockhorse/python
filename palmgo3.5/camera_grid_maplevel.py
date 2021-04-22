# -*- coding:utf-8 -*-
#@Time : 2021/1/23 下午4:20
#@Author: kkkkibj@163.com
#@File : camera_grid_maplevel.py
#用网格法将视频点位分级

startmaplevel = 20 # 假设地图最大等级为20
grid_side_length = 9.1552734375e-07 #初始网格边长，在20级时网格大小，网格越小，数量就越多

# 每个网格只有一个点

maplevel = startmaplevel
while maplevel > 4:
    print(maplevel)
    print(grid_side_length)
    print('-------------------------------')
    maplevel = maplevel - 1
    grid_side_length = grid_side_length * 2
