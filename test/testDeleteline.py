# -*- coding: utf8 -*-
# encoding=utf-8
# By @mahy
# email:kkkkbj@163.com

# 去掉环形里面的竖线
'''
def removeInnerLine(line):
    seachFirstFlag = True
    deleteFlagPoint = None
    linePoints = line.split()
    start_point = linePoints[0]
    end_point = linePoints[len(linePoints) - 1]
    deletePoints = []
    i = 0
    for p in linePoints:
        if linePoints.count(p) > 2:
            print(p,linePoints.count(p))
        if linePoints.count(p) > 1 and seachFirstFlag and p != deleteFlagPoint and i > 0:
            deleteFlagPoint = p
            seachFirstFlag = False
        if seachFirstFlag is False and p != start_point and p != end_point:
            deletePoints.append(p)
            if i < len(linePoints) - 1 and linePoints[i + 1] == deleteFlagPoint:
                seachFirstFlag = True
        i += 1
    for pd in deletePoints:
        linePoints.remove(pd)
    #print(deletePoints)
    return linePoints
'''

import collections
from collections import Iterator
from  GpsUtils import grid_supporter as gsp

def removeInnerLine(line):
    linePoints = line.split('\n')
    start_point = linePoints[0]
    end_point = linePoints[len(linePoints) - 1]
    it = iter(linePoints)
    while True:
        try:
            lineLength = len(linePoints)
            rline = linePoints.copy()
            rline.reverse()
            p = next(it)
            if p != start_point and p != end_point and linePoints.count(p) > 1:
                #print('----------------------------------------------------------------')
                first_index = linePoints.index(p)
                last_index = rline.index(p)
                distance = lineLength - last_index - 1 - first_index
                #print(linePoints[first_index])
                #print(linePoints[lineLength - last_index - 1])
                #print('----------------------------------------------------------------\n')
                #print('******************************************************************')
                for i in range(distance):
                    #dp = next(it)
                    dp = linePoints[first_index+1]
                    #print(dp)
                    linePoints.remove(dp)
                #print('******************************************************************\n')
                it = iter(linePoints)
        except StopIteration:
            # 没有后续元素，退出循环
            break
    for p in linePoints:
        if linePoints.count(p)>1:
            print(p)
    return linePoints




# 读取weatherinfo.

def read_weather_mid(input_path):
    dict_weathers = {}

    with open(input_path, 'r') as f:
        for line in f:
            items = line.strip('\n').split(',')

            items1 = items[1].strip('\"').split('_')
            items2 = items1[0].split(' ')

            value = items2[0] + ',' + items2[2] + ',' + items[0]
            key = items[0] + '_' + items[6]

            dict_weathers[key] = value

    f.close()
    return dict_weathers

southWest = [69.385045, 16.720233]
northEast = [136.457205, 54.046209]

# 读取路段和pline关系.
def read_links_by_pline(input_path, dict_weathers):
    dict_links_labels = {}
    with open(input_path, 'r') as f:
        for line in f:

            items = line.strip('\n').split(',')

            pline_id = items[0]
            pline_value = '0,0,0'

            if pline_id in dict_weathers.keys():
                pline_value = dict_weathers[pline_id]

            if items[1] != '':

                list_links = items[1].split('|')

                for j in range(len(list_links) - 1):
                    link_id = list_links[j]
                    link_id = link_id[:-2]

                    if link_id not in dict_links_labels.keys():
                        dict_links_labels[link_id] = pline_value

    f.close()

    return dict_links_labels

# 从mid,mif文件中生成网格索引文件,这里要被调用两次，一次是从天气区域文件生成索引，一次是路链生成索引
def createIndexFileByMap(mid_path, mif_path, link_id_index, df_index, indexer_path, southWest, northEast, grid_len,
                         link_type):
    gsp.set_grids_bound(southWest[0], southWest[1], northEast[0], northEast[1])
    gsp.set_grid_len(grid_len)  # 0.00027
    gsp.set_link_id_type(link_type)  # 2
    gsp.grid_map(mid_path, mif_path, link_id_index, df_index, indexer_path)

if __name__ == "__main__":
    '''
    line = ''
    with open('E:\\desktop\\test2\\px_s.txt', 'r') as f:
        for l in f:
            point = l.split(',')[0] + ',' + l.split(',')[1] + '\n'
            line += point
    rs = removeInnerLine(line)
    rline = "\n".join(rs)
    '''
    print('=============================\n')

    weather_kml = 'E:\\desktop\\aaa\\2017102408.kml'
    #dict_weathers = read_weather_mid(weather_kml.replace('.kml', '.mid'))
    #print(dict_weathers)
    # 读取路段和pline关系.
    #dict_links_labels = read_links_by_pline(weather_kml.replace('.kml', '') + 'link_by_weather.txt', dict_weathers)
    #print(dict_links_labels['2950670000007'])
    createIndexFileByMap('E:\\desktop\\aaa\\44186.mid', 'E:\\desktop\\aaa\\44186.mif', 2, 6,
                             'E:\\desktop\\aaa\\44186_indexer.txt', southWest, northEast, 0.01, 2)
