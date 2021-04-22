# -*- coding:utf-8 -*-
#@Time : 2021/4/21 上午11:31
#@Author: kkkkibj@163.com
#@File : get_heat_map_data.py
# 从gps中获取 热力图数据
import json
# rs['data'].append({"x":x,"y":y,"value":value})
grid_data = {}
grid_width = 0.03
grid_heigth = 0.03
with open('/Users/hongyanma/Desktop/china_goods.json') as infile:
    data = json.load(infile)
    # print(data['data'])
    for gps in data['data']:
        # print(gps)
        lng = gps[0]
        lat = gps[1]
        grid_x = int(float(lng) / grid_width)
        grid_y = int(float(lat) / grid_heigth)
        grid_no = 'g' + '_' + str(grid_x) + '_' + str(grid_y)
        if grid_no not in grid_data:
            grid_data[grid_no] = 0
        grid_data[grid_no] += 1
    print(grid_data)
    i = 0
    maxval = 0
    rs = {}
    rs['data'] = []
    for gkey in grid_data:
        i += 1
        if maxval < grid_data[gkey]:
            maxval = grid_data[gkey]
        val = int((grid_data[gkey] / 61.00)* 100)
        if val == 0:
            val = 1
        print(val)
        x = int(gkey.split('_')[1]) * grid_width + grid_width / 2
        y = int(gkey.split('_')[2]) * grid_heigth + grid_heigth / 2
        x = float(('%.3f' % x))
        y = float(('%.3f' % y))
        rs['data'].append({"x": x, "y": y, "value": val})
        print(x,y,val)
    with open('/Users/hongyanma/Desktop/china_goods_heatmap.json','w') as outf:
        json.dump(rs,outf)
    print(i)
    print(maxval)




