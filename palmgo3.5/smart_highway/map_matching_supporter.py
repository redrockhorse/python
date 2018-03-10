## -*- coding: utf8 -*-
#!/usr/bin/python
# 日志类.
import logging
logging.basicConfig(level = logging.INFO)

import midmif_supporter
import gis_supporter
import grid_supporter
import const_param as cp

import math

# 地图匹配类.
# 基于格网找到可能匹配的路段.

def find_maybe_link_by_grid(node_long, node_lat, dict_links_by_grid, search_grid = 1):

    node_cx = int((node_long - cp.min_long) / cp.grid_len)
    node_cy = int((node_lat - cp.min_lat) / cp.grid_len)

    dict_maybe_links = {}

    for i in range(2 * search_grid + 1):
        grid_cx = node_cx - search_grid + i
        for j in range(2 * search_grid + 1):
            grid_cy = node_cy - search_grid + j
            grid_key = '{:d}'.format(grid_cx) + ':' + '{:d}'.format(grid_cy)

            if grid_key in dict_links_by_grid.keys():
                link_list = dict_links_by_grid[grid_key]

                sss = set(link_list) # 排重.
                for link_id in sss:

                    if link_id not in dict_maybe_links.keys():
                        dict_maybe_links[link_id] = 1

    return dict_maybe_links

# 点匹配到路段上.
def node_match_link(node_long, node_lat, link_obj, match_dis_threshold, angle_threshold = 93):

    dis_to_link = 0.    # 点到路段距离.
    dis_to_fnode = 0.   # 点到路段起点距离.
    dis_to_tnode = 0.   # 点到路段终点距离.

    list_node_long = []
    list_node_lat = []
    list_sublink_len = []

    for j in range(len(link_obj.node_coord_list)):
        items = link_obj.node_coord_list[j].split(' ')

        list_node_long.append(float(items[0]))
        list_node_lat.append(float(items[1]))

        if j == 0:
            continue

        sublink_len = gis_supporter.cal_dis(list_node_long[j - 1], list_node_lat[j - 1], \
                                            list_node_long[j], list_node_lat[j])

        list_sublink_len.append(sublink_len)

    for j in range(len(link_obj.node_coord_list) - 1):

        pre_long = list_node_long[j]
        pre_lat = list_node_lat[j]

        next_long = list_node_long[j + 1]
        next_lat = list_node_lat[j + 1]

        angle12 = gis_supporter.cal_angle(pre_long, pre_lat, next_long, next_lat)
        angle13 = gis_supporter.cal_angle(pre_long, pre_lat, node_long, node_lat)

        inc_angle1 = gis_supporter.cal_inc_angle(angle12, angle13)
        if inc_angle1 > angle_threshold:
            continue

        angle21 = angle12 + 180
        if angle21 >= 360:
            angle21 = angle21 - 360

        angle23 = gis_supporter.cal_angle(next_long, next_lat, node_long, node_lat)
        inc_angle2 = gis_supporter.cal_inc_angle(angle23, angle21)

        if inc_angle2 > angle_threshold:
            continue

        dis13 = gis_supporter.cal_dis(pre_long, pre_lat, node_long, node_lat)
        dis_to_link = dis13 * math.sin(inc_angle1 * math.pi / 180)

        if dis_to_link > match_dis_threshold:
            continue

        else:
            dis_to_fnode = dis13 * math.cos(inc_angle1 * math.pi / 180)
            dis_to_tnode = -1 * dis_to_fnode

            for k in range(j):
                dis_to_fnode = dis_to_fnode + list_sublink_len[k]

            for k in range(len(list_sublink_len) - j):
                dis_to_tnode = dis_to_tnode + list_sublink_len[j + k]

            return (True, dis_to_link, dis_to_fnode, dis_to_tnode)

    return (False, 0., 0., 0.)


# 深度优先遍历.
# 从一条路段开始延伸寻找匹配的结果.

# 定义relation_unit_obj 来 存储路径内link之间的上下游关系.
class relation_unit_obj:
    father_index = -1   # 前继路段在数组中的位置.
    search_len = 0.
    search_angle = 0
    search_link = None

    def __init__(self):
        self.father_index = -1
        self.search_len = 0.
        self.search_angle = 0
        self.search_link = None

# 搜索的路段原子实体.
class search_unit_obj:

    search_index = -1
    search_link = None

    def __init__(self):
        self.search_index = -1
        self.search_link = None

# 判断link是否匹配到收费站.
def find_match_toll_station(cur_link_id, dict_toll_match_infos, dict_highway_name):
    if cur_link_id in dict_toll_match_infos.keys():

        list_toll_matched = dict_toll_match_infos[cur_link_id]

        for k in range(len(list_toll_matched)):
            toll_station = list_toll_matched[k]

            # 保证匹配上的收费站是属于这条高速的收费站.
            if toll_station.highway_name in dict_highway_name.keys():
                return toll_station
            else:
                continue

        return None

    else:
        return None


def path_derive(bgn_link, dict_toll_match_infos, len_threshold, dict_highway_name, highway_links, forward_search = True):

    # 结果返回.
    list_links_in_path = []

    # 用一个数组来保持路段的位置关系.
    list_relation_vector = []

    # 用一个栈来实现后续路段的深度优先遍历.
    list_search_stack = []

    # 初始化，将bgn_link 放到数据结构中.

    ru = relation_unit_obj()
    ru.father_index = -1
    ru.search_len = 0.
    ru.search_link = bgn_link
    list_relation_vector.append(ru)

    su = search_unit_obj()
    su.search_index = 0
    su.search_link = bgn_link
    list_search_stack.append(su)

    # 深度优先遍历.
    while len(list_search_stack) != 0:

        # 取出栈顶link.
        su1 = list_search_stack.pop()
        cur_link = su1.search_link

        toll_station = find_match_toll_station(cur_link.link_id, dict_toll_match_infos, dict_highway_name)

        # 找到了结果，路径搜索结束.
        if toll_station != None:

            list_temp_links = []
            temp_index = su1.search_index

            while True:
                ru3 = list_relation_vector[temp_index]
                list_temp_links.append(ru3.search_link)

                if ru3.father_index == -1:
                    break
                else:
                    temp_index = ru3.father_index

            if forward_search == True:
                for j in range(len(list_temp_links)):
                    list_links_in_path.append(list_temp_links[len(list_temp_links) - j - 1])
            else:
                for j in range(len(list_temp_links)):
                    list_links_in_path.append(list_temp_links[j])

            return (True, list_links_in_path, toll_station, cur_link)

        else:   # 插入前继或后继路段.

            if forward_search == True:  # 搜索下游.

                list_angle_index = []

                for k in range(len(cur_link.next_links)):
                    next_link = cur_link.next_links[k]

                    if next_link.link_id in highway_links.keys(): # 搜到主线就回退了.
                        continue

                    inc_angle = gis_supporter.cal_inc_angle(cur_link.tangle, next_link.fangle)
                    if inc_angle > 120:
                        continue

                    arr = [0, 0]
                    arr[0] = inc_angle
                    arr[1] = k

                    list_angle_index.append(arr)

                list_angle_index.sort(key = lambda x:(-x[0], x[1]))

                for k in range(len(list_angle_index)):
                    next_link = cur_link.next_links[list_angle_index[k][1]]

                    ru2 = relation_unit_obj()
                    ru2.search_link = next_link
                    ru2.father_index = su1.search_index
                    ru2.search_len = next_link.len + list_relation_vector[ru2.father_index].search_len
                    ru2.search_angle = list_angle_index[k][0] + list_relation_vector[ru2.father_index].search_angle

                    if ru2.search_len > len_threshold: # 超出阈值范围.
                       continue

                    else:
                        list_relation_vector.append(ru2)

                        su2 = search_unit_obj()
                        su2.search_index = len(list_relation_vector) - 1
                        su2.search_link = next_link

                        list_search_stack.append(su2)

            elif forward_search == False:   # 搜索上游.

                list_angle_index = []

                for k in range(len(cur_link.pre_links)):
                    pre_link = cur_link.pre_links[k]

                    if pre_link.link_id in highway_links.keys(): # 搜到主线就回退.
                        continue

                    inc_angle = gis_supporter.cal_inc_angle(cur_link.fangle, pre_link.tangle)
                    if inc_angle > 120:
                        continue

                    arr = [0, 0]
                    arr[0] = inc_angle
                    arr[1] = k

                    list_angle_index.append(arr)

                list_angle_index.sort(key=lambda x: (-x[0], x[1]))

                for k in range(len(list_angle_index)):
                    pre_link = cur_link.pre_links[list_angle_index[k][1]]

                    ru2 = relation_unit_obj()
                    ru2.search_link = pre_link
                    ru2.father_index = su1.search_index
                    ru2.search_len = pre_link.len + list_relation_vector[ru2.father_index].search_len
                    ru2.search_angle = list_angle_index[k][0] + list_relation_vector[ru2.father_index].search_angle

                    if ru2.search_len > len_threshold:  # 超出阈值范围.
                        continue

                    else:
                        list_relation_vector.append(ru2)

                        su2 = search_unit_obj()
                        su2.search_index = len(list_relation_vector) - 1
                        su2.search_link = pre_link

                        list_search_stack.append(su2)


    return (False, list_links_in_path, None, None)


# 通过上下游搜索，找到最直（角度最小且学角度小于80度）的路径.

# 直线搜索
def straight_path(begin_link, len_threshold, highway_links, forward_search, check_highway_links = True):

    # 已经搜索的距离.
    search_len = 0.
    cur_link = begin_link

    list_links_in_path = [] # 不包含当前路段.

    while True:

        if forward_search == True:

            if search_len > len_threshold:
                return (1, list_links_in_path, search_len)

            final_next_link = None
            final_next_inc_angle = 180

            for k in range(len(cur_link.next_links)):
                next_link = cur_link.next_links[k]

                if next_link.link_id in highway_links.keys() and check_highway_links == True:
                    continue

                inc_angle = gis_supporter.cal_inc_angle(cur_link.tangle, next_link.fangle)

                if inc_angle > 80:
                    continue

                else:
                    if inc_angle < final_next_inc_angle:
                        final_next_inc_angle = inc_angle
                        final_next_link = next_link
                        search_len = search_len + next_link.len


            if final_next_link != None:
                list_links_in_path.append(final_next_link)
                cur_link = final_next_link
            else:
                return (3, list_links_in_path, search_len)

        elif forward_search == False:

            if search_len > len_threshold:
                return (2, list_links_in_path, search_len)

            final_pre_link = None
            final_pre_inc_angle = 180

            for k in range(len(cur_link.pre_links)):
                pre_link = cur_link.pre_links[k]

                if pre_link.link_id in highway_links.keys() and check_highway_links == True:
                    continue

                inc_angle = gis_supporter.cal_inc_angle(cur_link.fangle, pre_link.tangle)

                if inc_angle > 80:
                    continue

                else:
                    if inc_angle < final_pre_inc_angle:
                        final_pre_inc_angle = inc_angle
                        final_pre_link = pre_link
                        search_len = search_len + pre_link.len

            if final_pre_link != None:
                list_links_in_path.append(final_pre_link)
                cur_link = final_pre_link
            else:
                return (4, list_links_in_path, search_len)

