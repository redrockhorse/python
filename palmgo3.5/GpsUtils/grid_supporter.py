
# 网格索引的支持类.
# Author：guoshengmin@chinatransinfo.com
# Date: 20170803

## -*- coding: utf8 -*-
#!/usr/bin/python
# 日志类.
import logging
logging.basicConfig(level = logging.INFO)

import math
import collections


from .import midmif_supporter as msup

# 坐下和右上角经纬度.
global min_long
global min_lat

global max_long
global max_lat

global grid_len

global dict_links_by_grid

global max_grid_cx
global max_grid_cy

global link_id_type  # 1: link_id, 2:link_id:dir 3: link_id:dir:sub_index

# format.
def set_link_id_type(type):
    global link_id_type
    link_id_type = type

# format.
def set_grids_bound(cx1, cy1, cx2, cy2):
    global min_long
    global min_lat

    global max_long
    global max_lat

    global dict_links_by_grid

    min_long = cx1
    min_lat = cy1

    max_long = cx2
    max_lat = cy2

    dict_links_by_grid = {}

# format.
def set_grid_len(gl):
    global grid_len
    grid_len = gl


    global min_long
    global min_lat

    global max_long
    global max_lat

    # 通过最大最小经纬度计算网格号的最大值，超过最大值的将不被记录.
    global max_grid_cx
    global max_grid_cy

    max_grid_cx = int((max_long - min_long) / grid_len) + 1
    max_grid_cy = int((max_lat - min_lat) / grid_len) + 1


# 得到向量的直线方程表达.
def get_line_equation(long1, lat1, long2, lat2):
    a = lat2 - lat1
    b = long1 - long2
    c = long2 * lat1 - long1 * lat2

    return (a, b, c)

# 得到点所在网格.
def get_grid_of_point(linkid, updir, sublink_up_index, sublink_down_index, grid_cx, grid_cy):
    global dict_links_by_grid

    global min_long
    global min_lat
    global grid_len

    global max_grid_cx
    global max_grid_cy

    global link_id_type

    #if grid_cx >= 0 and grid_cx <= max_grid_cx and grid_cy >= 0 and grid_cy <= max_grid_cy:
    if True:
        grid_key = '{:d}'.format(grid_cx) + '\t{:d}'.format(grid_cy)

        if updir == 1:

            key1 = ''
            key2 = ''

            if link_id_type == 1:
                key1 = linkid
                key2 = linkid
            elif link_id_type == 2:
                key1 = linkid + '_2'
                key2 = linkid + '_3'
            elif link_id_type == 3:
                key1 = linkid + '_2_' + '{:d}'.format(sublink_up_index)
                key2 = linkid + '_3_' + '{:d}'.format(sublink_down_index)

            if grid_key in dict_links_by_grid.keys():
                link_list = dict_links_by_grid[grid_key]
                link_list.append(key1)
                link_list.append(key2)

            else:
                link_list = []
                link_list.append(key1)
                link_list.append(key2)

                dict_links_by_grid[grid_key] = link_list

        elif updir == 2:

            key1 = ''
            if link_id_type == 1:
                key1 = linkid
            elif link_id_type == 2:
                key1 = linkid + '_2'
            elif link_id_type == 3:
                key1 = linkid + '_2_' + '{:d}'.format(sublink_up_index)

            if grid_key in dict_links_by_grid.keys():
                link_list = dict_links_by_grid[grid_key]
                link_list.append(key1)
                dict_links_by_grid[grid_key] = link_list
            else:
                link_list = []
                link_list.append(key1)

                dict_links_by_grid[grid_key] = link_list

        elif updir == 3:

            key2 = ''
            if link_id_type == 1:
                key2 = linkid
            elif link_id_type == 2:
                key2 = linkid + '_3'
            elif link_id_type == 3:
                key2 = linkid + '_3_' + '{:d}'.format(sublink_down_index)

            if grid_key in dict_links_by_grid.keys():
                link_list = dict_links_by_grid[grid_key]
                link_list.append(key2)

            else:
                link_list = []
                link_list.append(key2)

                dict_links_by_grid[grid_key] = link_list

        else: # updir == 4:
            pass



def get_grid_middle_x(linkid, updir, sublink_up_index, sublink_down_index, bgn_grid_cx, end_grid_cx, a, b, c):

    global min_long
    global min_lat
    global grid_len

    min_grid_cx = bgn_grid_cx
    max_grid_cx = end_grid_cx

    if end_grid_cx < bgn_grid_cx:
        min_grid_cx = end_grid_cx
        max_grid_cx = bgn_grid_cx

    for j in range(max_grid_cx - min_grid_cx):
        x = min_long + (j + min_grid_cx + 1) * grid_len
        y = (-1 * c - a * x) / b

        grid_cy = int((y - min_lat) / grid_len)

        get_grid_of_point(linkid, updir, sublink_up_index, sublink_down_index, j + min_grid_cx, grid_cy)
        get_grid_of_point(linkid, updir, sublink_up_index, sublink_down_index, j + min_grid_cx + 1, grid_cy)


def get_grid_middle_y(linkid, updir, sublink_up_index, sublink_down_index, bgn_grid_cy, end_grid_cy, a, b, c):

    global min_long
    global min_lat
    global grid_len

    min_grid_cy = bgn_grid_cy
    max_grid_cy = end_grid_cy

    if end_grid_cy < bgn_grid_cy:
        min_grid_cy = end_grid_cy
        max_grid_cy = bgn_grid_cy


    for i in range(max_grid_cy - min_grid_cy):
        y = min_lat + (i + min_grid_cy + 1) * grid_len
        x = (-1 * c - b * y) / a

        grid_cx = int((x - min_long) / grid_len)

        get_grid_of_point(linkid, updir, sublink_up_index, sublink_down_index, grid_cx, i + min_grid_cy)
        get_grid_of_point(linkid, updir, sublink_up_index, sublink_down_index, grid_cx, i + min_grid_cy + 1)

def get_grid_of_sublink(linkid, updir, sublink_up_index, sublink_down_index, long1, lat1, long2, lat2):

    global dict_links_by_grid

    global min_long
    global min_lat

    global grid_len

    global max_grid_cx
    global max_grid_cy


    grid_cx1 = int((long1 - min_long) / grid_len)
    grid_cy1 = int((lat1 - min_lat) / grid_len)

    grid_cx2 = int((long2 - min_long) / grid_len)
    grid_cy2 = int((lat2 - min_lat) / grid_len)

    get_grid_of_point(linkid, updir, sublink_up_index, sublink_down_index, grid_cx1, grid_cy1)
    get_grid_of_point(linkid, updir, sublink_up_index, sublink_down_index, grid_cx2, grid_cy2)

    # 对线进行操作.
    (a, b, c) = get_line_equation(long1, lat1, long2, lat2)

    if math.fabs(a) < 1e-6:
        get_grid_middle_x(linkid, updir, sublink_up_index, sublink_down_index, grid_cx1, grid_cx2, a, b, c)

    elif math.fabs(b) < 1e-6:
        get_grid_middle_y(linkid, updir, sublink_up_index, sublink_down_index, grid_cy1, grid_cy2, a, b, c)

    else:
        get_grid_middle_x(linkid, updir, sublink_up_index, sublink_down_index, grid_cx1, grid_cx2, a, b, c)
        get_grid_middle_y(linkid, updir, sublink_up_index, sublink_down_index, grid_cy1, grid_cy2, a, b, c)


# 对路网进行格网化.
def grid_map(mid_path, mif_path, link_id_index, df_index, output_path):

    global dict_links_by_grid

    msup.load_mid_file(mid_path)
    msup.load_mif_file(mif_path)

    msup.read_pre_mif_lines()

    link_index = 0
    while msup.read_all_links() == False:
        (mid_line, mif_coord_list) = msup.read_one_link_info()

        link_index = link_index + 1

        if link_index % 1000 == 0:
            logging.info('proc link: ' + '{:d}'.format(link_index))

        # 处理过程.

        items = mid_line.split(',')

        link_id = items[link_id_index].strip('\"')
        up_dir = int(items[df_index])

        for i in range(len(mif_coord_list) - 1):

            bgn_coord_str = mif_coord_list[i]
            end_coord_str = mif_coord_list[i + 1]

            bgn_coord_items = bgn_coord_str.split(' ')
            long1 = float(bgn_coord_items[0])
            lat1 = float(bgn_coord_items[1])

            end_coord_items = end_coord_str.split(' ')
            long2 = float(end_coord_items[0])
            lat2 = float(end_coord_items[1])


            get_grid_of_sublink(link_id, up_dir, i, len(mif_coord_list) - 2 - i, long1, lat1, long2, lat2)


    output = open(output_path, 'w')
    logging.info('begin print map indexer.\n')

    global min_long
    global min_lat

    global max_long
    global max_lat

    global grid_len

    global max_grid_cx
    global max_grid_cy


    title_str = '{:.6f}'.format(min_long) + '\t{:.6f}'.format(min_lat) \
                + '\t{:.6f}'.format(max_long) + '\t{:.6f}'.format(max_lat) + '\t{:.6f}'.format(grid_len) \
                + '\t{:d}'.format(max_grid_cx) + '\t{:d}'.format(max_grid_cy)

    output.write(title_str + '\n')
    result_dic = collections.OrderedDict()
    for grid_id in sorted(dict_links_by_grid.keys()):

        link_list = dict_links_by_grid[grid_id]

        sss = set(link_list)

        output.write(grid_id + '\t' + '{:d}'.format(len(sss)) + '\t')
        result_dic[grid_id] = []
        for link_ss_id in sss:
            output.write(link_ss_id + '\t')
            result_dic[grid_id].append(link_ss_id)
        output.write('\n')
    output.close()
    return result_dic



# # test main.
'''
mid_path = 'D:\\PY_Data\\parallel\\map_4r_17q2\\1100-4ring-sel.MID'
mif_path = 'D:\\PY_Data\\parallel\\map_4r_17q2\\1100-4ring-sel.MIF'

indexer_path = 'D:\\PY_Data\\parallel\\map_4r_17q2\\1100-4ring-sel-indexer-1.txt'

link_id_index = 1
df_index = 6

#set_grids_bound(119.799270, 29.907131, 120.692316, 30.529783)
#set_grids_bound(120.144770, 30.134490, 120.230684, 30.212019)
set_grids_bound(116.256602, 39.820674, 116.508628, 39.994656)
set_grid_len(0.00027)
set_link_id_type(3)
grid_map(mid_path, mif_path, link_id_index, df_index, indexer_path)
'''