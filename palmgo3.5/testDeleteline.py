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
import xml.dom.minidom

inner_start = 0
out_start = 0
def removeInnerLine(line):
    global inner_start
    global out_start
    linePoints = line.split('\n')
    start_point = linePoints[0]
    end_point = linePoints[len(linePoints) - 1]
    it = iter(linePoints)
    if linePoints.count(linePoints[1])>1:
        inner_start +=1
        #print(len(linePoints))
        inner_start_points = list(map(lambda x:x.split(),linePoints))
        if len(linePoints) < 20 and len(linePoints)>10:
            print(inner_start_points)
    else:
        out_start +=1
    while True:
        try:
            lineLength = len(linePoints)
            rline = linePoints.copy()
            rline.reverse()
            p = next(it)
            p_2 = next(it)
            if p != end_point and linePoints.count(p) > 1 and linePoints.count(p_2)>1:#p != start_point and
                # print('----------------------------------------------------------------')
                first_index = linePoints.index(p)
                last_index = rline.index(p)
                distance = lineLength - last_index - 1 - first_index
                # print(linePoints[first_index])
                # print(linePoints[lineLength - last_index - 1])
                # print('----------------------------------------------------------------\n')
                # print('******************************************************************')
                for i in range(distance):
                    # dp = next(it)
                    dp = linePoints[first_index + 1]
                    # print(dp)
                    linePoints.remove(dp)
                # print('******************************************************************\n')
                it = iter(linePoints)
        except StopIteration:
            # 没有后续元素，退出循环
            break
    # for p in linePoints:
    #     if linePoints.count(p) > 1:
    #         print(p)
    return '\n'.join(linePoints)
    #return linePoints


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


# 将weather的网格索引转一个格式.
def change_weather_format(input_path, output_path):
    line_count = 0

    dict_plines = {}

    with open(input_path, 'r') as f:
        for line in f:

            line_count = line_count + 1
            if line_count == 1:
                continue

            items = line.strip('\n').split('\t')

            cx = int(items[0])
            cy = int(items[1])

            pline_count = int(items[2])

            for j in range(pline_count):
                pline_id = items[3 + j]

                if pline_id not in dict_plines.keys():

                    dict_cxs = {}

                    dict_cys = {}
                    dict_cys[cy] = 1
                    dict_cxs[cx] = dict_cys

                    dict_plines[pline_id] = dict_cxs
                else:

                    dict_cxs = dict_plines[pline_id]

                    if cx not in dict_cxs.keys():
                        dict_cys = {}
                        dict_cys[cy] = 1
                        dict_cxs[cx] = dict_cys
                    else:
                        dict_cys = dict_cxs[cx]
                        dict_cys[cy] = 1
    f.close()

    output = open(output_path, 'w')

    for pline_id in sorted(dict_plines.keys()):
        dict_cxs = dict_plines[pline_id]

        for cx in sorted(dict_cxs.keys()):

            output.write(pline_id + ',' + '{:d}'.format(cx) + ',')

            dict_cys = dict_cxs[cx]

            for cy in sorted(sorted(dict_cys.keys())):
                output.write('{:d}'.format(cy) + '|')

            output.write('\n')
    output.close()


# 填充间断数组
def fillInterrupted(array):
    interruptePoint = []
    for i in range(len(array) - 1):
        if array[i + 1] - array[i] > 1:
            interruptePoint.append([array[i], array[i + 1]])
    n = len(interruptePoint)
    for j in range(n):
        if n % 2 == (j + 1) % 2:
            tmp = interruptePoint[j]
            p = array.index(tmp[0]) + 1
            for a in range(tmp[0] + 1, tmp[1]):
                array.insert(p, a)
                p += 1
    return array


# 处理凸多边形，将中间空白的格网填充起来.
def fill_weather_blank_grids(input_path, output_path):
    output = open(output_path, 'w')
    with open(input_path, 'r') as f:

        for line in f:
            items = line.strip('\n').split(',')
            pline_id = items[0]
            cx = items[1]
            output.write(pline_id + ',' + cx + ',')
            cys = items[2].split('|')
            cys.pop()
            cys = list(map(lambda x: int(x), cys))
            cys = fillInterrupted(cys)
            for cy in cys:
                output.write(str(cy) + '|')
            output.write('\n')
    f.close()
    output.close()


def create_map_file_by_kml(kml_file):
    mid_mif_dic = collections.OrderedDict()
    mid_file = open(kml_file.replace('.kml', '.mid'), 'w')
    mif_file = open(kml_file.replace('.kml', '.mif'), 'w')
    DOMTree = xml.dom.minidom.parse(kml_file)
    collection = DOMTree.documentElement
    placemarks = collection.getElementsByTagName("Placemark")
    mif_header = 'Version 450' + '\n' + 'Charset "WindowsSimpChinese"' + '\n' + 'Delimiter ","' + '\n' + 'CoordSys Earth Projection 1, 0' \
                 + '\n' + 'Columns 7' + '\n' + '  ID Integer' + '\n' + '  NAME Char(50)' + '\n' + '  CLASS Integer' + '\n' + '  other Integer' \
                 + '\n' + '  ns Integer' + '\n' + '  ne Integer' \
                 + '\n' + '  DF Integer' + '\n' + 'Data' + '\n'
    mif_file.write(mif_header)
    i = 0
    for pm in placemarks:
        rname = pm.getElementsByTagName("name")[0]
        visibility = rname.childNodes[0].data.split(' to ')
        # if visibility[0] != '-100' or visibility[1] != '20':
        i += 1
        region = pm.getElementsByTagName("coordinates")[0]
        path = region.childNodes[0].data
        path = path.replace('\n', '')
        path = path.replace(',0 ', '\n')
        path = path.replace(' ', '')
        path = path.replace(',', ' ')
        path = removeInnerLine(path)
        #print(path)
        mid_mif_dic[str(i) + '_2'] = path.split('\n')
        pointnum = path.count("\n")
        path = 'Pline ' + str(pointnum) + '\n' + path + '    Pen (1,2,0)\n'
        mif_file.write(path)
        midline = str(i) + ',"' + rname.childNodes[0].data + '_' + str(i) + '",' + str(i) + ',0,' + visibility[ \
            0] + ',' + visibility[1] + ',2\n'
        mid_file.write(midline)
    #print(mid_mif_dic['44186_2'])
    mid_file.close()
    mif_file.close()
    #print(mid_mif_dic)
    return mid_mif_dic


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

    #weather_kml = 'E:\\desktop\\aaa\\2017102408.kml'
    #weather_kml = 'E:\\ctfo\\ctfodayfile\\201712\\天气匹配路链\\aaa\\unmachregion_2_d.kml'
    weather_kml = 'E:\\ctfo\\ctfodayfile\\201712\\天气匹配路链\\aaa\\2017102408_test.kml'
    # dict_weathers = read_weather_mid(weather_kml.replace('.kml', '.mid'))
    # print(dict_weathers)
    # 读取路段和pline关系.
    # dict_links_labels = read_links_by_pline(weather_kml.replace('.kml', '') + 'link_by_weather.txt', dict_weathers)
    # print(dict_links_labels['2950670000007'])
    # createIndexFileByMap('E:\\desktop\\aaa\\44186.mid', 'E:\\desktop\\aaa\\44186.mif', 2, 6,
    #                          'E:\\desktop\\aaa\\44186_indexer_3.txt', southWest, northEast, 0.01, 3)
    # change_weather_format('E:\\desktop\\aaa\\44186_indexer_1.txt',
    #                           'E:\\desktop\\aaa\\44186_indexer_2.txt')
    # 天气影响区域网格填充
    # fill_weather_blank_grids('E:\\desktop\\aaa\\44186_indexer_2.txt',
    #                          'E:\\desktop\\aaa\\44186_indexer_3.txt')
    create_map_file_by_kml(weather_kml)
    print(inner_start)
    print(out_start)
