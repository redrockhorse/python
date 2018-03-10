## -*- coding: utf8 -*-
#!/usr/bin/python
import logging #日志类.
logging.basicConfig(level = logging.INFO)

import midmif_supporter
import gis_supporter
import grid_supporter


import map_matching_supporter as mm
import const_param as cp
import highway_map as hhm

# 生成收费站与路网的匹配关系，并输出到文件中.

class toll_station_obj:

    highway_name = ''
    highway_updir = ''

    toll_station_name = ''
    toll_long = 0.
    toll_lat = 0.

    def __init__(self):
        self.highway_name = ''
        self.highway_updir = ''

        self.toll_station_name = ''
        self.toll_long = 0.
        self.toll_lat = 0.

# 读取路网索引文件.
def read_map_indexer_file(grid_path):

    print('begin to read map indexer files. ')
    line_count = 0
    dict_links_by_grid = {}

    with open(grid_path, 'r') as f:
        for line in f:

            line_count = line_count + 1

            if line_count == 1:
                continue

            if line_count % 10000 == 0:
                print('has read line: ' + '{:d}'.format(line_count))

            items = line.strip('\n').split('\t')

            grid_cx = items[0]
            grid_cy = items[1]

            # 注意这里：cx和cy是反着的.
            grid_key =  grid_cy + ':' + grid_cx

            link_count = int(items[2])
            list_links = []

            for j in range(link_count):
                link_id = items[3 + j]

                if '_2' in link_id:
                    new_link_id = link_id.replace('_2', '1')
                    list_links.append(new_link_id)

                elif '_3' in link_id:
                    new_link_id = link_id.replace('_3', '0')
                    list_links.append(new_link_id)

            dict_links_by_grid[grid_key] = list_links

    f.close()

    print('finish reading map indexer files. ')

    return

#  读取收费站POI的信息.
def read_toll_station_info(poi_path):

    list_toll_stations = []

    with open(poi_path, 'r') as f:
        for line in f:

            items = line.strip('\n').split(',')

            if items[2] != '3':
                continue

            highway_name = items[0]
            highway_updir = items[1]

            poi_count = int(items[3])

            for j in range(poi_count):

                poi_info = items[j + 4]
                poi_items = poi_info.split('|')

                poi_name = poi_items[0]

                poi_coords_list = poi_items[1].split(';')

                if len(poi_coords_list) > 2:
                    logging.error('error: toll station: ' + poi_name + ' has ' + '{:d}'.format(len(poi_coords_list)) + ' points')

                for k in range(len(poi_coords_list)):

                    poi_coords = poi_coords_list[k].split(' ')
                    poi_long = float(poi_coords[0])
                    poi_lat = float(poi_coords[1])

                    toll_station = toll_station_obj()
                    toll_station.highway_name = highway_name
                    toll_station.highway_updir = highway_updir
                    toll_station.toll_station_name = poi_name
                    toll_station.toll_long = poi_long
                    toll_station.toll_lat = poi_lat

                    list_toll_stations.append(toll_station)

    f.close()
    return list_toll_stations


# 将全国的收费站匹配到路网上.
def match_toll_to_link(mid_path, mif_path, grid_path, poi_path, output_path):

    # 读取17q2的全路网.
    dtiplus_map = hhm.map_obj(0, 5, 6)

    dtiplus_map.link_dict = {}
    dtiplus_map.fnode_topo_dict = {}
    dtiplus_map.tnode_topo_dict = {}
    dtiplus_map.pre_mif_lines = []

    dtiplus_map.create_map_obj(mid_path, mif_path)

    dict_links_by_grid = read_map_indexer_file(grid_path)
    list_toll_stations = read_toll_station_info(poi_path)

    print('grid count: ' + '{:d}'.format(len(dict_links_by_grid)))
    print('toll count: ' + '{:d}'.format(len(list_toll_stations)))

    output = open(output_path, 'w')

    for k in range(len(list_toll_stations)):
        toll_station = list_toll_stations[k]

        # if k % 1000 == 0:
        #     print('has matched: ' + '{:d}'.format(k) + ' toll stations.')

        dict_maybe_links = mm.find_maybe_link_by_grid(toll_station.toll_long, toll_station.toll_lat, dict_links_by_grid)

        # 匹配到距离最小的路段.
        min_matched_link = None
        min_matched_dis = 1000.

        for maybe_linkid in sorted(dict_maybe_links.keys()):

            if maybe_linkid not in dtiplus_map.link_dict.keys():
                continue

            maybe_link = dtiplus_map.link_dict[maybe_linkid]

            (match_ok, dis_to_link, dis_to_fnode, dis_to_tnode) = mm.node_match_link( \
                toll_station.toll_long, toll_station.toll_lat, maybe_link, 30., 95)

            if match_ok == True and dis_to_link < min_matched_dis:
                min_matched_dis = dis_to_link
                min_matched_link = maybe_link

        if min_matched_link != None:
           output.write(toll_station.highway_name + ',' + toll_station.highway_updir + ',' + \
                        toll_station.toll_station_name + ',' + \
                        '{:.6f}'.format(toll_station.toll_long) + ',' + '{:.6f}'.format(toll_station.toll_lat) + ',' \
                        + min_matched_link.link_id + ',' + '{:.2f}'.format(min_matched_dis) + '\n')
        else:
            logging.error(toll_station.highway_name + ',' + toll_station.highway_updir + ',' + \
                        toll_station.toll_station_name + ' can not find matched link.')

    output.close()

# test main.

match_toll_to_link(cp.dtiplus_17q2_mid_path, cp.dtiplus_17q2_mif_path, \
                   cp.dtiplus_17q2_grid_path, cp.poi_list_path, cp.toll_station_match_path)

print('@操作完成@')






