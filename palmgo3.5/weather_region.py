# -*- coding: utf8 -*-
# !/usr/bin/python
# 日志类.
import logging

logging.basicConfig(level=logging.INFO)
import xml.dom.minidom
from  GpsUtils import grid_supporter as gsp
import os
import time
import datetime

# 使用时需要修改的部分
weather_kml = 'E:\\desktop\\aaa\\2017102408.kml'
link_mid = 'E:\\desktop\\aaa\\FCD_1000_16Q2_SN.MID'
link_mif = 'E:\\desktop\\aaa\\FCD_1000_16Q2_SN.MIF'
southWest = [69.385045, 16.720233]
northEast = [136.457205, 54.046209]


# 处理weather基于Region的mid/mif文件变为line 的MID/MIF文件.
# 这里修改了一下，直接由kml文件生成天气影响区域的mid,mif文件
def create_map_file_by_kml(kml_file):
    mid_file = open(kml_file.replace('.kml', '.mid'), 'w')
    mif_file = open(kml_file.replace('.kml', '.mif'), 'w')
    DOMTree = xml.dom.minidom.parse(kml_file)
    collection = DOMTree.documentElement
    placemarks = collection.getElementsByTagName("Placemark")
    mif_header = 'Version 450' + '\n' + 'Charset "WindowsSimpChinese"' + '\n' + 'Delimiter ","' + '\n' + 'CoordSys Earth Projection 1, 0' \
                 + '\n' + 'Columns 7' + '\n' + '  ID Integer' + '\n' + '  NAME Char(50)' + '\n' + '  CLASS Integer' + '\n' + '  other Integer' + '\n' + '  ns Integer' + '\n' + '  ne Integer' \
                 + '\n' + '  DF Integer' + '\n' + 'Data' + '\n'
    mif_file.write(mif_header)
    i = 0
    for pm in placemarks:
        rname = pm.getElementsByTagName("name")[0]
        visibility = rname.childNodes[0].data.split(' to ')
        if visibility[0] != '-100' or visibility[1] != '20':
            i += 1
            region = pm.getElementsByTagName("coordinates")[0]
            path = region.childNodes[0].data
            pointnum = path.count(",0 ")
            path = path.replace('\n', '')
            path = path.replace(',0 ', '\n')
            path = path.replace(' ', '')
            path = path.replace(',', ' ')
            path = 'Pline ' + str(pointnum) + '\n' + path + '    Pen (1,2,0)\n'
            mif_file.write(path)
            midline = str(i) + ',"' + rname.childNodes[0].data + '_' + str(i) + '",' + str(i) + ',0,' + visibility[
                0] + ',' + visibility[1] + ',2\n'
            mid_file.write(midline)
    mid_file.close()
    mif_file.close()


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

            is_good_blank = True
            for j in range(len(cys) - 2):
                pre_cy = int(cys[j])

                if j == 0:
                    output.write('{:d}'.format(pre_cy) + '|')

                next_cy = int(cys[j + 1])

                if next_cy != pre_cy + 1:
                    if is_good_blank == True:

                        for i in range(next_cy - pre_cy):
                            output.write('{:d}'.format(i + pre_cy + 1) + '|')

                        is_good_blank = False

                    elif is_good_blank == False:

                        output.write('{:d}'.format(next_cy) + '|')
                        is_good_blank = True

                else:
                    output.write('{:d}'.format(next_cy) + '|')

            output.write('\n')

    f.close()
    output.close()


# 读取路网索引文件.
def read_map_indexer(input_path):
    dict_indexs = {}

    line_count = 0

    with open(input_path, 'r') as f:
        for line in f:

            line_count = line_count + 1
            if line_count == 1:
                continue

            items = line.strip('\n').split('\t')

            grid_key = items[0] + '_' + items[1]

            link_count = int(items[2])

            if grid_key not in dict_indexs.keys():

                list_links = []

                for j in range(link_count):
                    list_links.append(items[j + 3])

                dict_indexs[grid_key] = list_links

    f.close()

    return dict_indexs


# 打印每个格网包含的路段.

def get_links_by_weather_pline(input_path, output_path, dict_indexs):
    dict_plines = {}

    with open(input_path, 'r') as f:
        for line in f:

            items = line.strip('\n').split(',')

            pline_id = items[0]
            cx = items[1]
            cys = items[2].split('|')

            dict_links_by_temp = {}

            for j in range(len(cys) - 1):
                cy = cys[j]
                grid_key = cx + '_' + cy

                if grid_key in dict_indexs.keys():
                    list_links = dict_indexs[grid_key]
                    for k in range(len(list_links)):
                        link_id = list_links[k]
                        if link_id not in dict_links_by_temp.keys():
                            dict_links_by_temp[link_id] = 1

            if pline_id not in dict_plines.keys():

                dict_links_by_pline = {}

                for link_id_temp in dict_links_by_temp.keys():
                    dict_links_by_pline[link_id_temp] = 1

                dict_plines[pline_id] = dict_links_by_pline

            else:
                dict_links_by_pline = dict_plines[pline_id]

                for link_id_temp in dict_links_by_temp.keys():
                    dict_links_by_pline[link_id_temp] = 1

    output = open(output_path, 'w')

    for pline_id in sorted(dict_plines.keys()):

        dict_links_by_pline = dict_plines[pline_id]

        output.write(pline_id + ',')
        for link_id in sorted(dict_links_by_pline.keys()):
            output.write(link_id + '|')

        output.write('\n')

    output.close()


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


# 重新标记mid文件.
def label_map_mid_file(input_path, output_path, dict_links_labels):
    output = open(output_path, 'w')
    with open(input_path, 'r') as f:
        for line in f:

            items = line.strip('\n').split(',')

            link_id = items[0].strip('\"')

            if link_id in dict_links_labels.keys():
                output.write(line.strip('\n') + ',' + dict_links_labels[link_id] + '\n')
            else:
                output.write(line.strip('\n') + ',0,0,-1\n')

    f.close()
    output.close()


if __name__ == "__main__":
    print('start-time', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    starttime = datetime.datetime.now()
    # 从region kml文件生成 mid,mif文件
    create_map_file_by_kml(weather_kml)
    # 从region mid mif文件生成索引文件
    if os.path.exists(weather_kml.replace('.kml', '') + '_indexer_fill.txt'):
        pass
    else:
        createIndexFileByMap(weather_kml.replace('.kml', '.mid'), weather_kml.replace('.kml', '.mif'), 2, 6,
                             weather_kml.replace('.kml', '') + '_indexer.txt', southWest, northEast, 0.01, 2)
        # 修改索引文件格式
        change_weather_format(weather_kml.replace('.kml', '') + '_indexer.txt',
                              weather_kml.replace('.kml', '') + '_indexer_1.txt')
        # 天气影响区域网格填充
        fill_weather_blank_grids(weather_kml.replace('.kml', '') + '_indexer_1.txt',
                                 weather_kml.replace('.kml', '') + '_indexer_fill.txt')

    # 路网文件生成索引，最好判断一下，如果已经存在则不需要重复生成
    if os.path.exists(link_mid.replace('.MID', '') + '_indexer.txt'):
        pass
    else:
        createIndexFileByMap(link_mid, link_mif, 0, 5, link_mid.replace('.MID', '') + '_indexer.txt', southWest,
                             northEast, 0.01, 2)

    # 读取路网索引文件.
    dict_indexs = read_map_indexer(link_mid.replace('.MID', '') + '_indexer.txt')
    # 生成区域包含路链文件
    get_links_by_weather_pline(weather_kml.replace('.kml', '') + '_indexer_fill.txt',
                               weather_kml.replace('.kml', '') + 'link_by_weather.txt', dict_indexs)
    # 读取weatherinfo.
    dict_weathers = read_weather_mid(weather_kml.replace('.kml', '.mid'))
    # 读取路段和pline关系.
    dict_links_labels = read_links_by_pline(weather_kml.replace('.kml', '') + 'link_by_weather.txt', dict_weathers)
    # 生成包含天气信息的路链
    label_map_mid_file(link_mid, weather_kml.replace('.kml', '') + '_weather_link.mid', dict_links_labels)
    print('end-time', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    endtime = datetime.datetime.now()
    usetime = (endtime - starttime).seconds
    print('done!!!,usedtime', usetime)
