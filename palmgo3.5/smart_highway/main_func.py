## -*- coding: utf8 -*-
#!/usr/bin/python
# 日志类.
import logging
logging.basicConfig(level = logging.INFO)


import midmif_supporter
import gis_supporter
import grid_supporter

import const_param as cp
import map_matching_supporter as mm

import highway_map as hhm

import math


# 操作的主文件.
# # test main (20171205）

# 读取输入的高速公路路网.
high_way = hhm.map_obj(0, 9, 4)
high_way.create_map_obj(cp.input_mid_path, cp.input_mif_path)    # 计算出link的一些几何属性.
high_way.create_topo()
print('read highway input map ok.')

# 读取17q2的全路网.
dtiplus_map = hhm.map_obj(0, 5, 6)

dtiplus_map.link_dict = {}
dtiplus_map.fnode_topo_dict = {}
dtiplus_map.tnode_topo_dict = {}
dtiplus_map.pre_mif_lines = []

dtiplus_map.create_map_obj(cp.dtiplus_17q2_mid_path, cp.dtiplus_17q2_mif_path)
dtiplus_map.create_topo()
print('read cennavi 17q2 map ok.')

output_mid = open(cp.output_mid_path, 'w')
output_mif = open(cp.output_mif_path, 'w')

# 对高速路网进行格网索引.
grid_supporter.set_grids_bound(cp.min_long, cp.min_lat, cp.max_long, cp.max_lat)
grid_supporter.set_grid_len(cp.grid_len)
grid_supporter.set_link_id_type(1)

dict_links_by_grid = grid_supporter.return_grid_map2(high_way.link_dict)

# 打印mif文件头.
hhm.print_pre_mif_lines(output_mif)

# 1: 读取输入路网mid line，获取label所用的有用信息.
for link_id in sorted(high_way.link_dict.keys()):
    link_obj = high_way.link_dict[link_id]
    hhm.extract_label_info(link_obj)        # 目的：解决编号、第一条路的上下行、名称、类型的问题.

# 2: 对处在同一个trip中的路段按照拓扑进行排序.
hhm.sort_link_by_topo(high_way.link_dict) # 目的：解决了序号、全体道路上下行
# 全体道路上下行标记以后，将highway_code 加上 上下行的标记.
hhm.add_high_code_updir(high_way.link_dict)

# 收费站延伸出来的link，并进行属性标记.
dict_final_added_links = hhm.extract_toll_station_infos(dtiplus_map, high_way.link_dict, cp.toll_station_match_path)
print('******* toll station finished.******* ')

# 加载原始地图(四维17q2)中获取的信息.
hhm.extract_label_by_map(high_way.link_dict, cp.dtiplus_17q2_mid_path)
hhm.extract_label_by_map(dict_final_added_links, cp.dtiplus_17q2_mid_path)

# 加载里程桩信息.
hhm.add_mile_stake_info(dict_links_by_grid, high_way.link_dict, cp.stake_list_path)
print('******* mile stake finished.******* ')

# 加载桥梁/隧道信息.
hhm.add_bridge_info(dict_links_by_grid, high_way.link_dict, cp.poi_list_path, '9', 2)   # 桥梁
hhm.add_bridge_info(dict_links_by_grid, high_way.link_dict, cp.poi_list_path, '15', 1)  # 隧道.

print('******* bridge and tunnle finished.******* ')


# 因为服务区的影响范围是多边形，用格网表达，以利于后续的处理.
hhm.print_service_cover_grids(dict_links_by_grid, high_way.link_dict, cp.poi_list_path, '2', cp.service_cover_grids_path)
print('******* service zoo finished.******* ')

# 加载城市编码信息.
hhm.decode_city_code(high_way.link_dict, cp.city_encode_path)

# 寻找出入区域范围的路段.
hhm.find_in_out_links(high_way.link_dict)

# 打印结果.
for link_id in sorted(high_way.link_dict.keys()):
    link_obj = high_way.link_dict[link_id]
    link_obj.link_label.print_mid_line(output_mid)
    link_obj.print_mif_lines(output_mif)

# 打印新增道路的路段.
for link_id in sorted(dict_final_added_links.keys()):
    link_obj = dict_final_added_links[link_id]
    link_obj.link_label.print_mid_line(output_mid)
    link_obj.print_mif_lines(output_mif)

print("# 操作结束##")