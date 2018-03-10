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

import math

# 城市编码对象.
class city_encode_obj:
    province_name = ''
    city_name = ''
    county_name = ''

    change_city_encode = ''   # 有的区县经过了改名.


# node 对象.
class node_obj:
    def __init__(self):
        pass


# 用于里程桩与路段的关联（基于高速名称）.
class stake_match_obj:

    # 一条trip的所有link.
    dict_trip_links = {}

    # tirp对应的里程桩信息.
    mile_stake_info = ''

    def __init__(self):
        dict_trip_links = {}



# POI匹配到路段上的结果.
class poi_match_result_obj:
    match_link_obj = None
    list_matched_pois = []
    list_lens_to_group = []

    def __init__(self):
        match_link_obj = None
        list_matched_pois = []
        list_lens_to_group = []

# 服务区匹配格网存储结果.
class service_grid_result_obj:
    match_link_id = ''

    grid_center_cx = 0
    grid_center_cy = 0

    grid_center_long = 0.
    grid_center_lat = 0.

    def __init__(self):
        self.match_link_id = ''

        self.grid_center_cx = 0
        self.grid_center_cy = 0

        self.grid_center_long = 0.
        self.grid_center_lat = 0.

# 里程桩匹配到路段上的结果.
class stake_match_result_obj:

    stake_value = 0.
    city_code = ''
    match_link_obj = None

    dis_to_link = 100.
    dis_to_fnode = 0.
    dis_to_tnode = 0.

    def __init__(self):
        match_link_obj = None
        dis_to_link = 100.

# 收费站匹配结果.
class toll_station_match_obj:
    highway_name = ''
    highway_updir = ''

    toll_station_name = ''

    toll_long = ''
    toll_lat = ''

    matched_link_id = ''

    def __init__(self):
        self.highway_name = ''
        self.highway_updir = ''

        self.toll_station_name = ''
        self.matched_link_id = ''

        self.toll_long = ''
        self.toll_lat = ''


# Link Label对象. (将来SmartHighway项目中作为Mid属性使用）.
class link_label_obj:

    mesh_id = ''
    link_id = ''
    father_link_id = ''      # 如果多条link是共线的，那么其father_link_id是一致的.
    fnode_id = ''
    tnode_id = ''

    df = 0
    nr = 0

    highway_code = ''           # 路线编号.
    highway_name_degree1 = '' # 一级名称 （高速） 注意这里用简称.
    highway_name_degree2 = '' # 二级名称（支线、联络线、出入口、互通立交 etc.）
    highway_name_degree3 = '' # 预留.

    highway_name_identify = '' # 唯一标识一条高速的名称. identify = degree1+degree2+degree3
    highway_name_segment = ''   # 高速未全线修通前，分段的名称.
    highway_name_other = ''     # 别名 （曾用名/融合名称）.

    highway_updir = 0          # 1-上行 2-下行 3-内环（闭合圈）4-外环（闭合圈） 5- 内环（非闭合圈） 6-外环（非闭合圈） 7-进（入）城（京） 8-出城（京）

    len = 0.                 # 路段长度.

    trip_code = ''  # trip定义为若干条link收尾相接构成的. （如果link属于多条trip，则trip_id用"|"顺序隔开）
    trip_type = 0  # trip类型. 1-主线 2-复线 3-支线 4-连接线 5-入口匝道 6-出口匝道 7-连通匝道 8-出口收费站所在匝道 9-入口收费站所在匝道 10-出口收费站下游匝道 11- 入口收费站上游匝道
    trip_index = 0  # link在trip中的序号.

    trip_from_code = ''  # 连通的上游trip的编码
    trip_to_code = ''  # 连通的下游trip的编码.

    city_code = ''          # 城市/区域代码. 6位数字.

    bgn_stake = 0.          # 起点里程桩号.
    end_stake = 0.          # 终点里程桩号.

    point_poi_name = ''     # 点POI名称（用于事件录入用）
    point_poi_type = 0      # 点POI类型. 1- 收费站 2-服务区 3-桥梁 4-隧道 5-

    #### 以下为区域POI.
    area_poi_g71118 = ''     # Y/N - 属于/不属于G71118.
    area_poi_zoo = ''        # 4大经济区：京津冀/长三角/珠三角/成渝.
    area_poi_security = ''   # 保障区：多个用"|"隔开.
    area_poi_province = ''   # 省（包括直辖市）名称. 注意这里用简称.
    area_poi_city = ''       # 市(包括直辖市）名称. 注意这里用简称.
    area_poi_county = ''     # 县（县级市)、区名称. 注意这里用简称.

    area_poi_bridge = ''     # 桥梁名称.
    area_poi_tunnle = ''     # 隧道名称.
    area_poi_toll = ''       # 收费站名称.
    area_poi_service = ''    # 服务区名称.
    area_poi_flyover = ''    # 立交桥名称.
    area_poi_scenic = ''     # 景区名称.

    area_poi_airport = ''    # 机场名称.
    area_poi_railway = ''    # 火车站.
    area_poi_passenger = ''  # 客运站点.
    area_poi_logistic = ''   # 物流园区.

    ### 以下为跨界标识.
    cross_zoo = ''          # 进/出[4大经济区名]，例如 进京津冀/出长三角.
    cross_security = ''     # 进/出[保障区]: 多个用"|"隔开.
    cross_province = ''     # [省/直辖市名称]-[省直辖市名称]. 例如：四川-重庆 重庆-四川 代表了2个方向.
    cross_city = ''         # [市名称]-[市名称]. 例如：北京-天津
    cross_county = ''       # [区名称]-[区名称].


       # 新增2个要素.
    len_of_bridge = 0.  # 桥梁长度 （如果是桥梁的话）.
    len_of_tunnle = 0.  # 隧道长度 （如果是隧道的话）.

    # 打印mid Line.
    def print_mid_line(self, output):
        output.write('\"' + self.mesh_id + '\",')
        output.write('\"' + self.link_id + '\",')
        output.write('\"' + self.father_link_id + '\",')
        output.write('\"' + self.fnode_id + '\",')
        output.write('\"' + self.tnode_id + '\",')
        output.write('{:d}'.format(self.df) + ',')
        output.write('{:d}'.format(self.nr) + ',')
        output.write('\"' + self.highway_code + '\",')
        output.write('\"' + self.highway_name_degree1 + '\",')
        output.write('\"' + self.highway_name_degree2 + '\",')
        output.write('\"' + self.highway_name_degree3 + '\",')
        output.write('\"' + self.highway_name_other + '\",')
        output.write('\"' + self.highway_name_identify + '\",') # 新增.
        output.write('\"' + self.highway_name_segment + '\",') # 新增.
        output.write('{:d}'.format(self.highway_updir) + ',')
        output.write('{:.2f}'.format(self.len) + ',')
        output.write('\"' + self.trip_code + '\",')
        output.write('{:d}'.format(self.trip_type) + ',')
        output.write('{:d}'.format(self.trip_index) + ',')
        output.write('\"' + self.trip_from_code + '\",')
        output.write('\"' + self.trip_to_code + '\",')
        output.write('\"' + self.city_code + '\",')
        output.write('{:.3f}'.format(self.bgn_stake) + ',')
        output.write('{:.3f}'.format(self.end_stake) + ',')
        output.write('\"' + self.point_poi_name + '\",')
        output.write('{:d}'.format(self.point_poi_type) + ',')
        output.write('\"' + self.area_poi_g71118 + '\",')
        output.write('\"' + self.area_poi_zoo + '\",')
        output.write('\"' + self.area_poi_security + '\",')
        output.write('\"' + self.area_poi_province + '\",')
        output.write('\"' + self.area_poi_city + '\",')
        output.write('\"' + self.area_poi_county + '\",')
        output.write('\"' + self.area_poi_bridge + '\",')
        output.write('\"' + self.area_poi_tunnle + '\",')
        output.write('\"' + self.area_poi_toll + '\",')
        output.write('\"' + self.area_poi_service + '\",')
        output.write('\"' + self.area_poi_flyover + '\",')
        output.write('\"' + self.area_poi_scenic + '\",')
        output.write('\"' + self.area_poi_airport + '\",')
        output.write('\"' + self.area_poi_railway + '\",')
        output.write('\"' + self.area_poi_passenger + '\",')
        output.write('\"' + self.area_poi_logistic + '\",')
        output.write('\"' + self.cross_zoo + '\",')
        output.write('\"' + self.cross_security + '\",')
        output.write('\"' + self.cross_province + '\",')
        output.write('\"' + self.cross_city + '\",')
        output.write('\"' + self.cross_county + '\",')
        output.write('{:.2f}'.format(self.len_of_bridge) + ',')
        output.write('{:.2f}'.format(self.len_of_tunnle) + '\n')


# 取得link_label 对应的mif文件的pre_mif_line的输出内容.
def print_pre_mif_lines(output):

    output.write('Version   300\n')
    output.write('Charset \"WindowsSimpChinese\"\n')
    output.write('Delimiter \",\"\n')
    output.write('Index 1\n')
    output.write('CoordSys Earth Projection 1, 104\n')

    output.write('Columns 49\n')

    output.write('\tMESH_ID Char(6)\n')               # 1
    output.write('\tLINK_ID Char(14)\n')              # 2
    output.write('\tFATHER_LINK_ID Char(14)\n')       # 3
    output.write('\tFJCID Char(6)\n')                   # 4
    output.write('\tTJCID Char(6)\n')                   # 5
    output.write('\tDF Integer\n')                      # 6
    output.write('\tNR Integer\n')                      # 7

    output.write('\tHIGHWAY_CODE Char(50)\n')    # 8
    output.write('\tHIGHWAY_NAME_DEGREE1 Char(100)\n')  # 9
    output.write('\tHIGHWAY_NAME_DEGREE2 Char(100)\n')  # 10
    output.write('\tHIGHWAY_NAME_DEGREE3 Char(100)\n')  # 11
    output.write('\tHIGHWAY_NAME_OTHER Char(100)\n')  # 12
    output.write('\tHIGHWAY_NAME_IDENTIFY Char(100)\n') # 新增 12-1
    output.write('\tHIGHWAY_NAME_SEGMENT Char(100)\n') # 新增12-2
    output.write('\tHIGHWAY_UPDIR Integer\n')  # 13
    output.write('\tLEN Float\n')  # 14

    output.write('\tTRIP_CODE Char(100)\n')  # 15
    output.write('\tTRIP_TYPE Integer\n')  # 16
    output.write('\tTRIP_INDEX Integer\n')  # 17
    output.write('\tTRIP_FROM_CODE Char(100)\n')  # 18
    output.write('\tTRIP_TO_CODE Char(100)\n')  # 19

    output.write('\tCITY_CODE Char(10)\n')  # 20
    output.write('\tBGN_STAKE Float\n')  # 21
    output.write('\tEND_STAKE Float\n')  # 22

    output.write('\tPOINT_POI_NAME Char(50)\n')  # 23
    output.write('\tPOINT_POI_TYPE Integer\n')  # 24

    output.write('\tAREA_POI_G71118 Char(5)\n')  # 25
    output.write('\tAREA_POI_ZOO Char(10)\n')  # 26
    output.write('\tAREA_POI_SECURITY Char(100)\n')  # 27
    output.write('\tAREA_POI_PROVINCE Char(20)\n')  # 28
    output.write('\tAREA_POI_CITY Char(20)\n')  # 29
    output.write('\tAREA_POI_COUNTY Char(20)\n')  # 30

    output.write('\tAREA_POI_BRIDGE Char(50)\n')  # 31
    output.write('\tAREA_POI_TUNNLE Char(50)\n')  # 32
    output.write('\tAREA_POI_TOLL Char(50)\n')  # 33
    output.write('\tAREA_POI_SERVICE Char(50)\n')  # 34
    output.write('\tAREA_POI_FLYOVER Char(50)\n')  # 35
    output.write('\tAREA_POI_SCENIC Char(50)\n')  # 36

    output.write('\tAREA_POI_AIRPORT Char(50)\n')  # 37
    output.write('\tAREA_POI_RAILWAY Char(50)\n')  # 38
    output.write('\tAREA_POI_PASSENGER Char(50)\n')  # 39
    output.write('\tAREA_POI_LOGISTIC Char(50)\n')  # 40

    output.write('\tCROSS_ZOO Char(50)\n')  # 41
    output.write('\tCROSS_SECURITY Char(100)\n')  # 42
    output.write('\tCROSS_PROVINCE Char(50)\n')  # 43
    output.write('\tCROSS_CITY Char(50)\n')  # 44
    output.write('\tCROSS_COUNTY Char(50)\n')  # 45

    # 新增.
    output.write('\tLEN_OF_BRIDGE Float\n') # 46
    output.write('\tLEN_OF_TUNNLE Float\n') # 47

    output.write('Data\n')
    output.write('\n')


# link对象.
class link_obj:

    link_id = ''            # linkid.
    link_label = link_label_obj()

    bro_link_id = ''        # 共线的对向linkid.

    merge_name = ''         # 路段名称.

    line_str = ''           # 存储Mid Line.

    fnode_coord = ''        # 起点经纬度.
    tnode_coord = ''        # 终点经纬度.

    service_area_id = ''    # 服务区.
    tool_station_id = ''    # 收费站.

    pre_links = []          # 上游link_id.
    next_links = []         # 下游link_id.

    node_coord_list = []    # 内点坐标.

    fangle = 0              # 起点角度.
    tangle = 0              # 终点角度.
    vec_angle = 0           # 向量角度.

    len = 0.                # 长度.
    circle_rate = 0.        # 曲率.

    bridge_type = -1          # 1 桥梁 2 隧道.

    highway_updir_labeled = False

    def __init__(self):
        self.node_coord_list = []
        self.pre_links = []
        self.next_links = []

        self.link_label = link_label_obj()

        self.highway_updir_labeled = False
        self.bridge_type = -1


    def print_mif_lines(self, output):
        if len(self.node_coord_list) == 2:

            output.write('Line ' + self.node_coord_list[0] + ' ' + self.node_coord_list[1] + '\n')
            output.write('\tPen (1,2,0) \n')

        else:

            output.write('Pline ' + '{:d}'.format(len(self.node_coord_list)) + '\n')
            for j in range(len(self.node_coord_list)):
                output.write(self.node_coord_list[j] + '\n')
            output.write('\tPen (1,2,0) \n')

# 地图对象.
class map_obj:

    link_dict = {}
    fnode_topo_dict = {}
    tnode_topo_dict = {}

    pre_mif_lines = []


    link_index = 0
    len_index = 0
    df_index = 0

    def __init__(self, lk_idx, len_idx, df_idx):
        self.link_index = lk_idx
        self.len_index = len_idx
        self.df_index = df_idx


    # 创建link对象.
    def create_up_link_obj(self, mid_line, mif_coord_list):

        mid_items = mid_line.replace('\"', '').split(',')
        up_dir = int(mid_items[self.df_index])

        up_link = link_obj()
        up_link.link_id = mid_items[self.link_index] + '1'
        up_link.line_str = mid_line
        up_link.merge_name = mid_items[-1]

        if up_link == 1:
            up_link.bro_link_id = mid_items[self.link_index] + '0'
        else:
            up_link.bro_link_id = ''

        up_link.len = float(mid_items[self.len_index])

        up_link.fnode_coord = mif_coord_list[0]
        up_link.tnode_coord = mif_coord_list[-1]

        for node_coord in mif_coord_list:
            up_link.node_coord_list.append(node_coord)

        fnode_items = up_link.fnode_coord.split(' ')
        tnode_items = up_link.tnode_coord.split(' ')

        up_vec_len = gis_supporter.cal_dis(float(fnode_items[0]), float(fnode_items[1]), \
                                           float(tnode_items[0]), float(tnode_items[1]))

        up_link.circle_rate = 100.
        if up_vec_len > 1e-8:
            up_link.circle_rate = up_link.len / up_vec_len

        fnode1_items = mif_coord_list[1].split(' ')
        fnode2_items = mif_coord_list[-2].split(' ')

        up_link.fangle = gis_supporter.cal_angle(float(fnode_items[0]), float(fnode_items[1]), \
                                                 float(fnode1_items[0]), float(fnode1_items[1]))

        up_link.tangle = gis_supporter.cal_angle(float(fnode2_items[0]), float(fnode2_items[1]), \
                                                 float(tnode_items[0]), float(tnode_items[1]))

        up_link.vec_angle = gis_supporter.cal_angle(float(fnode_items[0]), float(fnode_items[1]), \
                                                    float(tnode_items[0]), float(tnode_items[1]))

        self.link_dict[up_link.link_id] = up_link

        if up_link.fnode_coord in self.fnode_topo_dict.keys():
            fnode_link_list = self.fnode_topo_dict[up_link.fnode_coord]
            fnode_link_list.append(up_link.link_id)
        else:
            fnode_link_list = []
            fnode_link_list.append(up_link.link_id)
            self.fnode_topo_dict[up_link.fnode_coord] = fnode_link_list

        if up_link.tnode_coord in self.tnode_topo_dict.keys():
            tnode_link_list = self.tnode_topo_dict[up_link.tnode_coord]
            tnode_link_list.append(up_link.link_id)
        else:
            tnode_link_list = []
            tnode_link_list.append(up_link.link_id)
            self.tnode_topo_dict[up_link.tnode_coord] = tnode_link_list

    def create_down_link_obj(self, mid_line, mif_coord_list):

        mid_items = mid_line.replace('\"', '').split(',')
        up_dir = int(mid_items[self.df_index])

        down_link = link_obj()

        down_link.link_id = mid_items[self.link_index] + '0'
        down_link.line_str = mid_line
        down_link.merge_name = mid_items[-1]

        if up_dir == 1:
            down_link.bro_link_id = mid_items[self.link_index] + '1'
        else:
            down_link.bro_link_id = ''

        down_link.len = float(mid_items[self.len_index])

        down_link.fnode_coord = mif_coord_list[-1]
        down_link.tnode_coord = mif_coord_list[0]

        # 反向遍历.
        for node_coord in reversed(mif_coord_list):
            down_link.node_coord_list.append(node_coord)

        fnode_items = down_link.fnode_coord.split(' ')
        tnode_items = down_link.tnode_coord.split(' ')

        down_vec_len = gis_supporter.cal_dis(float(fnode_items[0]), float(fnode_items[1]), \
                                             float(tnode_items[0]), float(tnode_items[1]))

        down_link.circle_rate = 100.
        if down_vec_len > 1e-8:
            down_link.circle_rate = down_link.len / down_vec_len

        fnode1_items = mif_coord_list[-2].split(' ')
        fnode2_items = mif_coord_list[1].split(' ')

        down_link.fangle = gis_supporter.cal_angle(float(fnode_items[0]), float(fnode_items[1]), \
                                                   float(fnode1_items[0]), float(fnode1_items[1]))

        down_link.tangle = gis_supporter.cal_angle(float(fnode2_items[0]), float(fnode2_items[1]), \
                                                   float(tnode_items[0]), float(tnode_items[1]))

        down_link.vec_angle = gis_supporter.cal_angle(float(fnode_items[0]), float(fnode_items[1]), \
                                                      float(tnode_items[0]), float(tnode_items[1]))

        self.link_dict[down_link.link_id] = down_link

        if down_link.fnode_coord in self.fnode_topo_dict.keys():
            fnode_link_list = self.fnode_topo_dict[down_link.fnode_coord]
            fnode_link_list.append(down_link.link_id)
        else:
            fnode_link_list = []
            fnode_link_list.append(down_link.link_id)
            self.fnode_topo_dict[down_link.fnode_coord] = fnode_link_list

        if down_link.tnode_coord in self.tnode_topo_dict.keys():
            tnode_link_list = self.tnode_topo_dict[down_link.tnode_coord]
            tnode_link_list.append(down_link.link_id)
        else:
            tnode_link_list = []
            tnode_link_list.append(down_link.link_id)
            self.tnode_topo_dict[down_link.tnode_coord] = tnode_link_list


    # 创建地图对象.

    def create_map_obj(self, mid_path, mif_path):

        midmif_supporter.load_mid_file(mid_path)
        midmif_supporter.load_mif_file(mif_path)

        midmif_supporter.read_pre_mif_lines()

        for p_mif_line in midmif_supporter.pre_mif_lines:
            self.pre_mif_lines.append(p_mif_line)

        line_count = 0
        link_count = 0
        while midmif_supporter.read_all_links() == False:

            # 读取一行的信息.
            (mid_line, mif_coord_list) = midmif_supporter.read_one_link_info()
            line_count = line_count + 1

            mid_items = mid_line.split(',')
            # link_id = mid_items[1].strip('\"')

            #########################################################
            # 以下需要重写.
            up_dir = int(mid_items[self.df_index])

            if up_dir == 1:
                self.create_up_link_obj(mid_line, mif_coord_list)
                self.create_down_link_obj(mid_line, mif_coord_list)
                link_count = link_count + 2

            elif up_dir == 2:
               self.create_up_link_obj(mid_line, mif_coord_list)
               link_count = link_count + 1

            elif up_dir == 3:
                self.create_down_link_obj(mid_line, mif_coord_list)
                link_count = link_count + 1

            else:
                pass

        logging.info('total read line: %d ' % line_count)
        logging.info('total create link: %d' % link_count)

    # 创建拓扑.

    def create_topo(self):

        for link_obj in self.link_dict.values():

            if link_obj.fnode_coord in self.tnode_topo_dict.keys():
                tnode_links = self.tnode_topo_dict[link_obj.fnode_coord]

                for pre_link_id in tnode_links:
                    pre_link_obj = self.link_dict[pre_link_id]

                    if pre_link_obj.link_id != link_obj.link_id and pre_link_obj.link_id != link_obj.bro_link_id:
                        link_obj.pre_links.append(pre_link_obj)

            if link_obj.tnode_coord in  self.fnode_topo_dict.keys():
                fnode_links = self.fnode_topo_dict[link_obj.tnode_coord]

                for next_link_id in fnode_links:
                    next_link_obj = self.link_dict[next_link_id]

                    if next_link_obj.link_id != link_obj.link_id and next_link_obj.link_id != link_obj.bro_link_id:
                        link_obj.next_links.append(next_link_obj)

# 基于原始路网提取信息.
def extract_label_by_map(dict_links, map_mid_path):

    with open(map_mid_path, 'r') as f:
        for line in f:
            mid_items = line.replace('\"', '').split(',')

            link_id = mid_items[0]

            link_obj = None

            if link_id + '1' in dict_links.keys():
                link_obj = dict_links[link_id + '1']
            elif link_id + '0' in dict_links.keys():
                link_obj = dict_links[link_id + '0']
            else:
                pass

            if link_obj != None:
                link_obj.link_label.mesh_id = mid_items[1]
                link_obj.link_label.link_id = link_obj.link_id
                link_obj.link_label.df = 2
                link_obj.link_label.nr = int(mid_items[7])
                link_obj.link_label.len = float(mid_items[5])

                link_obj.link_label.city_code = mid_items[15]

                link_obj.link_label.fnode_id = mid_items[2]
                link_obj.link_label.tnode_id = mid_items[3]
                link_obj.bridge_type = int(mid_items[10])       # 桥梁和隧道 （RS）属性.


    f.close()


# 读输入路网，获取label所用的一些信息.
def extract_label_info(link_obj):

    mid_items = link_obj.line_str.replace('\"', '').split(',')

    link_obj.link_label.link_id = link_obj.link_id

    # 现在看能把有用的东西拿一下也是好的.
    link_obj.link_label.mesh_id = mid_items[1]
    link_obj.link_label.fnode_id = mid_items[2]
    link_obj.link_label.tnode_id = mid_items[3]
    link_obj.link_label.df = int(mid_items[4])
    link_obj.link_label.nr = int(mid_items[5])
    link_obj.link_label.len = float(mid_items[9])

    #上下行.
    if int(mid_items[12]) != 0:
        link_obj.link_label.highway_updir = int(mid_items[12])
    elif int(mid_items[13]) != 0:
        link_obj.link_label.highway_updir = int(mid_items[13])

    # 去掉code中的[]
    higyway_code = mid_items[16]
    code_temp = higyway_code.replace('[', '')
    code_temp = code_temp.replace(']', '')

    code_items = code_temp.split('_')

    link_obj.link_label.highway_code = code_items[0]
    link_obj.link_label.trip_code = code_temp

    link_obj.link_label.highway_name_degree1 = mid_items[6] # 一级名称. #mid_items[6].replace('公路', '')
    link_obj.link_label.highway_name_degree2 = mid_items[7] # 二级名称.
    link_obj.link_label.highway_name_degree3 = mid_items[8] # 三级名称.

    link_obj.link_label.highway_name_identify =  mid_items[6] +  mid_items[7] +  mid_items[8]

    link_obj.link_label.highway_name_other = mid_items[10]
    link_obj.link_label.highway_name_segment = mid_items[15]   # 段名.

    # 经过了重新定义.
    if int(mid_items[14]) == 1: # 主线..
        link_obj.link_label.trip_type = 1
    elif int(mid_items[14]) == 2: # 复线.
        link_obj.link_label.trip_type = 2
    elif int(mid_items[14]) == 3: # 支线.
        link_obj.link_label.trip_type = 3
    elif int(mid_items[14]) == 4: # 连接线.
        link_obj.link_label.trip_type = 4



# 基于Topo对link进行排序.
def sort_link_by_topo(dict_links):

   dict_links_by_triptype = {}

   for link_id in sorted(dict_links.keys()):
       link_obj = dict_links[link_id]

       trip_type = link_obj.link_label.trip_type

       if trip_type not in dict_links_by_triptype.keys():
           list_links_one_triptype = []
           list_links_one_triptype.append(link_obj)
           dict_links_by_triptype[trip_type] = list_links_one_triptype
       else:
           list_links_one_triptype = dict_links_by_triptype[trip_type]
           list_links_one_triptype.append(link_obj)


   for trip_type in sorted(dict_links_by_triptype.keys()):
       list_links_one_triptype = dict_links_by_triptype[trip_type]

       for j in range(len(list_links_one_triptype)):
           link_obj = list_links_one_triptype[j]

           if link_obj.link_label.highway_updir != 0 and link_obj.highway_updir_labeled == False:

               print('cur bgn link_obj: ' + link_obj.link_label.link_id)

               link_obj.link_label.trip_index = 1
               link_obj.highway_updir_labeled = True

               cur_link_obj = link_obj
               cur_link_index = 1

               # 往下循环遍历.
               while True:

                   if len(cur_link_obj.next_links) == 0:
                       break

                   # print('cur link: ' + cur_link_obj.link_label.link_id)

                   find_next = False
                   for k in range(len(cur_link_obj.next_links)):
                       next_link_obj = cur_link_obj.next_links[k]

                       if next_link_obj.link_label.trip_type != cur_link_obj.link_label.trip_type:
                           continue

                       if next_link_obj.highway_updir_labeled == True:
                           continue

                       next_link_obj.link_label.highway_updir = cur_link_obj.link_label.highway_updir
                       next_link_obj.link_label.trip_index = cur_link_index + 1
                       next_link_obj.highway_updir_labeled = True # 防止被重新标记.

                       cur_link_obj = next_link_obj
                       cur_link_index = cur_link_index + 1
                       find_next = True
                       break # 这里cur_link_obj已经改过了，所以必须跳出循环.

                   if find_next == False:    # 防止标记绕城高速的时候出现死循环.
                       break



# 遍历路段，形成拓扑序.
def topo_sort_links(dict_links, bgn_link, end_link):

    list_sorted_links = []
    list_sorted_links.append(bgn_link)

    sum_link_len = bgn_link.len
    cur_link = bgn_link

    find_sort = False
    sort_count = 1

    while True:

        sort_count = sort_count + 1

        if sort_count > 1000:
            find_sort = False
            break

        if cur_link.link_id == end_link.link_id:
            find_sort = True
            break

        else:

            find_next = False

            for j in range(len(cur_link.next_links)):

                next_link = cur_link.next_links[j]
                if next_link.link_id in dict_links.keys():

                    list_sorted_links.append(next_link)
                    sum_link_len = sum_link_len + next_link.len

                    cur_link = next_link
                    find_next = True
                    break

            if find_next == False:
                find_sort = False
                break

    return (find_sort, list_sorted_links, sum_link_len)

# 对路网建立索引.
def get_map_indexer(mid_path, mif_path):


    grid_supporter.set_grids_bound(cp.min_long, cp.min_lat, cp.max_long, cp.max_lat)
    grid_supporter.set_grid_len(cp.grid_len)
    grid_supporter.set_link_id_type(4)

    link_id_index = 0
    df_index = 4

    return grid_supporter.return_grid_map(mid_path, mif_path, link_id_index, df_index)

# 加载mile_stake的数据.
def add_mile_stake_info(dict_links_by_grid, dict_links, stake_path):

    # 基于当前高速的名称获取stake文件中相应名称的里程桩点信息.

    # step1：获取高速名称（包括主线、支路等）.
    dict_trip_keys = {}

    print('dict_links count: ' + '{:d}'.format(len(dict_links)))
    for link_id in sorted(dict_links.keys()):

        link_obj = dict_links[link_id]

        link_name = link_obj.link_label.highway_name_identify
        link_updir = link_obj.link_label.highway_updir

        trip_key = link_name + '_' + '{:d}'.format(link_updir)

        if trip_key not in dict_trip_keys.keys():
            stake_match = stake_match_obj()
            stake_match.dict_trip_links = {}
            stake_match.mile_stake_info = ''
            stake_match.dict_trip_links[link_id] = link_obj

            dict_trip_keys[trip_key] = stake_match
        else:
            stake_match = dict_trip_keys[trip_key]
            stake_match.dict_trip_links[link_id] = link_obj

    # step2： 遍历里程桩文件，获取相应高速名称的所有里程桩点信息.
    with open(stake_path, 'r') as f:
        for line in f:

            items = line.strip('\n').split(',')

            trip_key = items[1] + '_' + items[2]

            if trip_key in dict_trip_keys.keys():
                stake_match = dict_trip_keys[trip_key]

                print('trip: ' + trip_key + ', link count: ' + '{:d}'.format(len(stake_match.dict_trip_links)))
                stake_match.mile_stake_info = line.strip('\n')

    # step3: 匹配.
    for trip_key in sorted(dict_trip_keys.keys()):

        trip_items = trip_key.split('_')
        trip_updir = trip_items[1]              # 上下行.

        stake_match = dict_trip_keys[trip_key]

        if stake_match.mile_stake_info == '':
            logging.error('can not find trip key: ' + trip_key)
            continue

        items = stake_match.mile_stake_info.split(',')

        list_match_results = []

        node_count = int(items[3])
        print('trip key = ' + trip_key + ' node count = ' + '{:d}'.format(node_count))

        last_stake = 0.
        for k in range(node_count):
            node_info = items[4 + k]

            node_items = node_info.split('|')
            node_stake = float(node_items[0])

            if k == 0:
                last_stake = node_stake
            else:
                # 防止距离太近的点出现.
                if abs(node_stake - last_stake) < 0.2:
                    continue
                else:
                    last_stake = node_stake

            city_code = node_items[2]

            node_coords = node_items[1].split(' ')
            node_long = float(node_coords[0])
            node_lat = float(node_coords[1])

            dict_maybe_links = mm.find_maybe_link_by_grid(node_long, node_lat, dict_links_by_grid)

            stake_match_result = stake_match_result_obj()
            stake_match_result.stake_value = node_stake
            stake_match_result.match_link_obj = None
            stake_match_result.dis_to_link = 100.
            stake_match_result.dis_to_fnode = 0.
            stake_match_result.dis_to_tnode = 0.

            for maybe_linkid in sorted(dict_maybe_links.keys()):

                if maybe_linkid in stake_match.dict_trip_links.keys():
                    link = stake_match.dict_trip_links[maybe_linkid]
                    (match_ok, dis_to_link, dis_to_fnode, dis_to_tnode) = mm.node_match_link(node_long, node_lat, link, 50.)

                    if match_ok == True:

                        if dis_to_link < stake_match_result.dis_to_link:
                            stake_match_result.match_link_obj = link
                            stake_match_result.dis_to_link = dis_to_link
                            stake_match_result.dis_to_fnode = dis_to_fnode
                            stake_match_result.dis_to_tnode = dis_to_tnode

                        continue
                    else:
                        continue

            if stake_match_result.match_link_obj != None:
                stake_match_result.city_code = city_code
                list_match_results.append(stake_match_result)

        # step4: 标记.
        print('list match result count: ' + '{:d}'.format(len(list_match_results)))
        for j in range(len(list_match_results) - 1):

            pre_match_result = list_match_results[j]
            next_match_result = list_match_results[j + 1]

            # 匹配到同一条路段上.
            if pre_match_result.match_link_obj.link_id == next_match_result.match_link_obj.link_id:
                continue

            if trip_updir == '1' or trip_updir == '3':       # 上行.

                # 里程桩的差.
                stake_minus = next_match_result.stake_value - pre_match_result.stake_value

                (find_sort, list_sorted_links, sum_link_len) = topo_sort_links(stake_match.dict_trip_links, \
                                                                pre_match_result.match_link_obj, \
                                                                next_match_result.match_link_obj)

                if find_sort == False:
                    logging.error('trip_key = ' + trip_key)
                    logging.error('stake error 1 -> from [ ' + '{:.3f}'.format(pre_match_result.stake_value) + \
                                  ' ] to [ ' + '{:.3f}'.format(next_match_result.stake_value) + ' ] ')
                    continue

                total_link_len = sum_link_len - pre_match_result.dis_to_fnode - next_match_result.dis_to_tnode
                stake_rate = stake_minus / total_link_len

                if abs(stake_rate) > 10. or abs(stake_rate) < 0.0001:
                    logging.error('trip_key = ' + trip_key)
                    logging.error('stake error 2 -> from [ ' + '{:.3f}'.format(pre_match_result.stake_value) + \
                                  ' ] to [ ' + '{:.3f}'.format(next_match_result.stake_value) + ' ] ')
                    continue

                for k in range(len(list_sorted_links) - 1):
                    if k == 0:
                        list_sorted_links[k].link_label.end_stake = pre_match_result.stake_value + pre_match_result.dis_to_tnode * stake_rate
                        list_sorted_links[k + 1].link_label.bgn_stake = list_sorted_links[k].link_label.end_stake

                        list_sorted_links[k].link_label.city_code = pre_match_result.city_code
                        list_sorted_links[k + 1].link_label.city_code = pre_match_result.city_code

                    else:
                        list_sorted_links[k].link_label.end_stake = list_sorted_links[k].link_label.bgn_stake + \
                                                                    list_sorted_links[k].link_label.len * stake_rate
                        list_sorted_links[k + 1].link_label.bgn_stake = list_sorted_links[k].link_label.end_stake

                        list_sorted_links[k].link_label.city_code = pre_match_result.city_code
                        list_sorted_links[k + 1].link_label.city_code = pre_match_result.city_code

            elif trip_updir == '2' or trip_updir == '4':     # 下行.
                # 里程桩的差.
                stake_minus = pre_match_result.stake_value - next_match_result.stake_value

                (find_sort, list_sorted_links, sum_link_len) = topo_sort_links(stake_match.dict_trip_links, \
                                                                    next_match_result.match_link_obj,
                                                                    pre_match_result.match_link_obj)

                if find_sort == False:
                    logging.error('trip_key = ' + trip_key)
                    logging.error('stake error 1 -> from [ ' + '{:.3f}'.format(pre_match_result.stake_value) + \
                                  ' ] to [ ' + '{:.3f}'.format(next_match_result.stake_value) + ' ] ')
                    continue

                total_link_len = sum_link_len - pre_match_result.dis_to_tnode - next_match_result.dis_to_fnode
                stake_rate = stake_minus / total_link_len

                if abs(stake_rate) > 10. or abs(stake_rate) < 0.0001:
                    logging.error('trip_key = ' + trip_key)
                    logging.error('stake error 2 -> from [ ' + '{:.3f}'.format(pre_match_result.stake_value) +\
                                  ' ] to [ ' + '{:.3f}'.format(next_match_result.stake_value) + ' ] ')
                    continue


                for k in range(len(list_sorted_links) - 1):
                    if k == 0:
                        list_sorted_links[k].link_label.end_stake = next_match_result.stake_value + next_match_result.dis_to_tnode * stake_rate
                        list_sorted_links[k + 1].link_label.bgn_stake = list_sorted_links[k].link_label.end_stake

                        list_sorted_links[k].link_label.city_code = next_match_result.city_code
                        list_sorted_links[k + 1].link_label.city_code = next_match_result.city_code

                    else:
                        list_sorted_links[k].link_label.end_stake = list_sorted_links[k].link_label.bgn_stake + \
                                                                    list_sorted_links[k].link_label.len * stake_rate
                        list_sorted_links[k + 1].link_label.bgn_stake = list_sorted_links[k].link_label.end_stake

                        list_sorted_links[k].link_label.city_code = next_match_result.city_code
                        list_sorted_links[k + 1].link_label.city_code = next_match_result.city_code

        if trip_updir == '1' or trip_updir == '2':  # 只对单线执行.

            dict_order_links = {}
            # 建立基于下标的索引.
            for trip_linkid in sorted(stake_match.dict_trip_links.keys()):
                trip_link = stake_match.dict_trip_links[trip_linkid]

                dict_order_links[trip_link.link_label.trip_index] = trip_link

            for trip_linkid in sorted(stake_match.dict_trip_links.keys()):
                trip_link = stake_match.dict_trip_links[trip_linkid]

                # 分界的link.
                if trip_link.link_label.bgn_stake == 0. and trip_link.link_label.end_stake != 0.:

                    if trip_link.link_label.highway_updir == 1:  # 上行的头.
                        last_end_stake = trip_link.link_label.end_stake

                        for k in range(trip_link.link_label.trip_index):
                            yellow_trip_link = dict_order_links[trip_link.link_label.trip_index - k]

                            if yellow_trip_link.link_label.bgn_stake == 0.:
                                yellow_trip_link.link_label.end_stake = last_end_stake
                                yellow_trip_link.link_label.bgn_stake = last_end_stake - \
                                            yellow_trip_link.link_label.len / 1000.

                                if  yellow_trip_link.link_label.bgn_stake < 0.:
                                    yellow_trip_link.link_label.bgn_stake = 0.

                                last_end_stake = yellow_trip_link.link_label.bgn_stake

                    elif trip_link.link_label.highway_updir == 2:  # 下行的尾.
                        last_end_stake = trip_link.link_label.end_stake

                        for k in range(trip_link.link_label.trip_index):
                            yellow_trip_link = dict_order_links[trip_link.link_label.trip_index - k]

                            if yellow_trip_link.link_label.bgn_stake == 0.:
                                yellow_trip_link.link_label.end_stake = last_end_stake
                                yellow_trip_link.link_label.bgn_stake = last_end_stake + \
                                            yellow_trip_link.link_label.len / 1000.
                                last_end_stake = yellow_trip_link.link_label.bgn_stake


                elif trip_link.link_label.bgn_stake != 0. and trip_link.link_label.end_stake == 0.:

                    if trip_link.link_label.highway_updir == 1:  # 上行的尾.
                        last_bgn_stake = trip_link.link_label.bgn_stake

                        for k in range(len(stake_match.dict_trip_links) - trip_link.link_label.trip_index + 1):

                            yellow_trip_link = dict_order_links[trip_link.link_label.trip_index + k]

                            if yellow_trip_link.link_label.end_stake == 0.:
                                yellow_trip_link.link_label.bgn_stake = last_bgn_stake
                                yellow_trip_link.link_label.end_stake = last_bgn_stake + \
                                                yellow_trip_link.link_label.len / 1000.
                                last_bgn_stake = yellow_trip_link.link_label.end_stake

                    elif trip_link.link_label.highway_updir == 2:  # 下行的头.
                        last_bgn_stake = trip_link.link_label.bgn_stake

                        for k in range(len(stake_match.dict_trip_links) - trip_link.link_label.trip_index + 1):
                            yellow_trip_link = dict_order_links[trip_link.link_label.trip_index + k]

                            if yellow_trip_link.link_label.end_stake == 0.:
                                yellow_trip_link.link_label.bgn_stake = last_bgn_stake
                                yellow_trip_link.link_label.end_stake = last_bgn_stake - \
                                                yellow_trip_link.link_label.len / 1000.

                                if  yellow_trip_link.link_label.end_stake < 0.:
                                    yellow_trip_link.link_label.end_stake = 0.

                                last_bgn_stake = yellow_trip_link.link_label.end_stake

        elif trip_updir == '3' or trip_updir == '4':  # 只对环线执行.
            for trip_linkid in sorted(stake_match.dict_trip_links.keys()):
                trip_link = stake_match.dict_trip_links[trip_linkid]

                if trip_link.link_label.highway_updir == 3 and \
                                        trip_link.link_label.bgn_stake - trip_link.link_label.end_stake > 0:
                    trip_link.link_label.end_stake = trip_link.link_label.bgn_stake + trip_link.link_label.len / 1000.

                elif trip_link.link_label.highway_updir == 4 and \
                    trip_link.link_label.end_stake - trip_link.link_label.bgn_stake > 0.:
                    trip_link.link_label.end_stake = trip_link.link_label.bgn_stake - trip_link.link_label.len / 1000.
                    if trip_link.link_label.end_stake < 0.:
                        trip_link.link_label.end_stake = 0.

            # 按照里程桩的顺序调整路段序号.
            dict_order_lines = {}
            for trip_linkid in sorted(stake_match.dict_trip_links.keys()):
                trip_link = stake_match.dict_trip_links[trip_linkid]
                dict_order_lines[trip_link.link_label.bgn_stake] = trip_link

            index_value = 1
            for bgn_stake_value in sorted(dict_order_lines.keys()):

                order_link = dict_order_lines[bgn_stake_value]
                if order_link.link_label.highway_updir == 3:
                    order_link.link_label.trip_index = index_value
                    index_value = index_value + 1

                elif order_link.link_label.highway_updir == 4:
                    order_link.link_label.trip_index = len(dict_order_lines) + 1 - index_value
                    index_value = index_value + 1


        logging.error('print error mile stake.')
        logging.error('trip_key = ' + trip_key)
        for trip_linkid in sorted(stake_match.dict_trip_links.keys()):

            trip_link = stake_match.dict_trip_links[trip_linkid]

            if trip_link.link_label.bgn_stake < 0. or trip_link.link_label.end_stake < 0.:
                logging.error('stake error 3 -> linkid: ' + trip_link.link_label.link_id + ', bgn_stake = [ ' \
                              + '{:.3f}'.format(trip_link.link_label.bgn_stake) + \
                              ' ], end_stake = [ ' + '{:.3f}'.format(trip_link.link_label.end_stake) + ' ] ')

            if trip_link.link_label.len < 1e-6:
                print(trip_link.link_label.link_id + ' link len zero.')

            link_stake_rate = (trip_link.link_label.bgn_stake - trip_link.link_label.end_stake) / trip_link.link_label.len * 1000.
            if abs(link_stake_rate) > 10. or abs(link_stake_rate) < 0.0001:
                logging.error('stake error 4 -> linkid: ' + trip_link.link_label.link_id + ', bgn_stake = [ ' \
                              + '{:.3f}'.format(trip_link.link_label.bgn_stake) + \
                              ' ], end_stake = [ ' + '{:.3f}'.format(trip_link.link_label.end_stake) + ' ] ')

# 在一众POI名称中寻找最优的POI名称.
def find_best_poi_name(dict_names_of_pois, bridge_type):
    if bridge_type == 2: # 桥.
        for poi_name in sorted(dict_names_of_pois.keys()):

            if '大桥' in poi_name:
                dict_names_of_pois[poi_name] = dict_names_of_pois[poi_name] + 1

            if '.' in poi_name or '#' in poi_name: # 出现点或数字.
                dict_names_of_pois[poi_name] = dict_names_of_pois[poi_name] - 1

        max_value = 0
        best_poi_name = '未命名桥'

        for poi_name in sorted(dict_names_of_pois.keys()):
            poi_name_value = dict_names_of_pois[poi_name]
            if poi_name_value > max_value:
                max_value = poi_name_value
                best_poi_name = poi_name

        return best_poi_name

    elif bridge_type == 1:   # 隧道.

        best_poi_name = '未命名隧道'

        for poi_name in sorted(dict_names_of_pois.keys()):
            return poi_name

        return best_poi_name

# 加载桥梁的信息.
def add_bridge_info(dict_links_by_grid, dict_links, bridge_path, bridge_label, bridge_type):

    # step1：获取高速名称（包括主线、支路等）.
    dict_trip_keys = {}

    print('dict_links count: ' + '{:d}'.format(len(dict_links)))
    for link_id in sorted(dict_links.keys()):

        link_obj = dict_links[link_id]

        link_name = link_obj.link_label.highway_name_identify
        link_updir = link_obj.link_label.highway_updir

        trip_key = link_name + '_' + '{:d}'.format(link_updir) + '_' + bridge_label  # 桥梁9 隧道15.

        if trip_key not in dict_trip_keys.keys():
            poi_match = stake_match_obj()
            poi_match.dict_trip_links = {}
            poi_match.mile_stake_info = ''
            poi_match.dict_trip_links[link_id] = link_obj

            dict_trip_keys[trip_key] = poi_match
        else:
            poi_match = dict_trip_keys[trip_key]
            poi_match.dict_trip_links[link_id] = link_obj

    # step2： 遍历里程桩文件，获取相应高速名称的所有桥梁和隧道信息.
    with open(bridge_path, 'r') as f:
        for line in f:

            items = line.strip('\n').split(',')

            trip_key = items[0] + '_' + items[1] + '_' + items[2]

            if trip_key in dict_trip_keys.keys():
                poi_match = dict_trip_keys[trip_key]

                print('trip: ' + trip_key + ', link count: ' + '{:d}'.format(len(poi_match.dict_trip_links)))
                poi_match.mile_stake_info = line.strip('\n')

    # step3: 匹配.
    for trip_key in sorted(dict_trip_keys.keys()):

        poi_match = dict_trip_keys[trip_key]

        if poi_match.mile_stake_info == '':
            logging.error('can not find trip key: ' + trip_key)
            continue

        items = poi_match.mile_stake_info.split(',')

        # 1- 建立按照序号的索引.
        dict_links_by_order = {}
        for link_id in sorted(poi_match.dict_trip_links.keys()):
            link = poi_match.dict_trip_links[link_id]
            dict_links_by_order[link.link_label.trip_index] = link


        node_count = int(items[3])
        # 每条Link匹配上了那几个POI.
        dict_matched_pois_by_link = {}

        for k in range(node_count):
            node_info = items[4 + k]
            node_items = node_info.split('|')

            poi_name = node_items[0]
            poi_coords = node_items[1].split(' ')
            poi_long = float(poi_coords[0])
            poi_lat = float(poi_coords[1])

            dict_maybe_links = mm.find_maybe_link_by_grid(poi_long, poi_lat, dict_links_by_grid)

            for maybe_linkid in sorted(dict_maybe_links.keys()):

                if maybe_linkid in poi_match.dict_trip_links.keys():
                    link = poi_match.dict_trip_links[maybe_linkid]
                    (match_ok, dis_to_link, dis_to_fnode, dis_to_tnode) = mm.node_match_link(poi_long, poi_lat, link, 50.)

                    if match_ok == True:

                        # logging.info('poi name = ' + poi_name + ', match link: ' + link.link_label.link_id)

                        # 如果当前匹配的link属性不是bridge.
                        if link.bridge_type != bridge_type:

                            if ('大桥' in poi_name or '立交桥' in poi_name or '隧道' in poi_name) \
                                    and ('.' not in poi_name and '#' not in poi_name): # 说明是个值得保留的POI.

                                link.link_label.point_poi_name = poi_name

                                if bridge_type == 2:    # 桥梁
                                    link.link_label.point_poi_type = 3
                                elif bridge_type == 1:  # 隧道
                                    link.link_label.point_poi_type = 4

                                # logging.info('[1] link: ' + link.link_label.link_id + ', poi name = ' + poi_name + ', poi type = ' + '{:d}'.format(link.link_label.point_poi_type))

                                # 同时往前往后搜索，找到距离最小的一个标记为bridge属性的link，标记上名称.

                                # 往下游搜索2km.
                                dis_f_search = dis_to_tnode
                                find_f_link = None
                                for i in range(10):
                                    f_index = link.link_label.trip_index + i + 1
                                    if f_index > len(poi_match.dict_trip_links):
                                        break

                                    f_link = dict_links_by_order[f_index]
                                    if f_link.bridge_type != bridge_type:
                                        dis_f_search = dis_f_search + f_link.link_label.len
                                    else:
                                        find_f_link = f_link
                                        break

                                    if dis_f_search > 2000.:
                                        break

                                # if find_f_link != None:
                                #     logging.info('forward search ok, f_link = ' + find_f_link.link_label.link_id + ', dis = ' + '{:.3f}'.format(dis_f_search))
                                # else:
                                #     logging.info('forward search false.')

                                # 往上游搜索2km.
                                dis_b_search = dis_to_fnode
                                find_b_link = None

                                for i in range(10):
                                    b_index = link.link_label.trip_index - i -1

                                    if b_index < 1:
                                        break

                                    b_link = dict_links_by_order[b_index]

                                    if b_link.bridge_type != bridge_type:
                                        dis_b_search = dis_b_search + b_link.link_label.len
                                    else:
                                        find_b_link = b_link
                                        break

                                    if dis_b_search > 2000.:
                                        break

                                # if find_b_link != None:
                                #     logging.info('forward search ok, b_link = ' + find_b_link.link_label.link_id + ', dis = ' + '{:.3f}'.format(dis_b_search))
                                # else:
                                #     logging.info('backward search false.')

                                if (find_f_link != None and find_b_link == None) or \
                                        (find_f_link != None and find_b_link != None and dis_b_search >= dis_f_search):

                                    if find_f_link.link_label.link_id not in dict_matched_pois_by_link.keys():
                                        poi_match_result = poi_match_result_obj()

                                        poi_match_result.list_matched_pois = []
                                        poi_match_result.list_lens_to_group = []

                                        poi_match_result.match_link_obj = find_f_link
                                        poi_match_result.list_matched_pois.append(poi_name)

                                        # logging.info('[1] link ' + find_f_link.link_label.link_id + ' add poi_name: ' + poi_name)
                                        poi_match_result.list_lens_to_group.append(dis_f_search)

                                        dict_matched_pois_by_link[find_f_link.link_label.link_id] = poi_match_result
                                    else:
                                        poi_match_result = dict_matched_pois_by_link[find_f_link.link_label.link_id]
                                        poi_match_result.list_matched_pois.append(poi_name)
                                        # logging.info('[2] link ' + find_f_link.link_label.link_id + ' add poi_name: ' + poi_name)
                                        poi_match_result.list_lens_to_group.append(dis_f_search)

                                elif (find_f_link == None and find_b_link != None) or \
                                        (find_f_link != None and find_b_link != None and dis_b_search < dis_f_search) :

                                    if find_b_link.link_label.link_id not in dict_matched_pois_by_link.keys():
                                        poi_match_result = poi_match_result_obj()

                                        poi_match_result.list_matched_pois = []
                                        poi_match_result.list_lens_to_group = []

                                        poi_match_result.match_link_obj = find_b_link
                                        poi_match_result.list_matched_pois.append(poi_name)
                                        # logging.info('[3] link ' + find_b_link.link_label.link_id + ' add poi_name: ' + poi_name)
                                        poi_match_result.list_lens_to_group.append(dis_b_search)

                                        dict_matched_pois_by_link[find_b_link.link_label.link_id] = poi_match_result
                                    else:
                                        poi_match_result = dict_matched_pois_by_link[find_b_link.link_label.link_id]
                                        poi_match_result.list_matched_pois.append(poi_name)
                                        # logging.info('[4] link ' + find_b_link.link_label.link_id + ' add poi_name: ' + poi_name)
                                        poi_match_result.list_lens_to_group.append(dis_b_search)

                                elif find_f_link == None and find_b_link == None:
                                    pass


                        else: # link.bridge_type == bridge_type:
                            link.link_label.point_poi_name = poi_name

                            if bridge_type == 2:  # 桥梁
                                link.link_label.point_poi_type = 3
                            elif bridge_type == 1:  # 隧道
                                link.link_label.point_poi_type = 4

                            # logging.info('[2] link: ' + link.link_label.link_id + ', poi name = ' + poi_name + ', poi type = ' + '{:d}'.format(link.link_label.point_poi_type))

                            if link.link_label.link_id not in dict_matched_pois_by_link.keys():
                                poi_match_result = poi_match_result_obj()

                                poi_match_result.match_link_obj = link
                                poi_match_result.list_matched_pois = []   # ******** 切记这里也要初始化.
                                poi_match_result.list_lens_to_group = []
                                poi_match_result.list_matched_pois.append(poi_name)
                                # logging.info('[5] link ' + link.link_label.link_id + ' add poi_name: ' + poi_name)
                                poi_match_result.list_lens_to_group.append(0.)

                                dict_matched_pois_by_link[link.link_label.link_id] = poi_match_result
                            else:
                                poi_match_result = dict_matched_pois_by_link[link.link_label.link_id]
                                poi_match_result.list_matched_pois.append(poi_name)
                                # logging.info('[6] link ' + link.link_label.link_id + ' add poi_name: ' + poi_name)
                                poi_match_result.list_lens_to_group.append(0.)


                        break # 匹配成功就跳出.

                    else:
                        continue
                else:
                    continue


        # logging.info('华丽的分割线+++++++++++++++++++++++')

        # 梳理匹配后的结果.

        # 2- 按照序号遍历是否出现了连续的POI类型的link.

        link_index = 0
        is_bridge = False
        bridge_len = 0.

        list_conn_links = []    # 连续的是某种类型POI的link.
        dict_names_of_bridge = {}

        while True:

            link_index = link_index + 1
            if link_index == len(dict_links_by_order) + 1:
                break

            link = dict_links_by_order[link_index]

            if link.bridge_type == bridge_type: # 是桥.
                if is_bridge == False:
                    is_bridge = True

                bridge_len = bridge_len + link.link_label.len
                list_conn_links.append(link)

                if link.link_label.link_id in dict_matched_pois_by_link.keys():
                    poi_match_result = dict_matched_pois_by_link[link.link_label.link_id]

                    for j in range(len(poi_match_result.list_matched_pois)):
                        matched_poi_name = poi_match_result.list_matched_pois[j]
                        matched_poi_dis = poi_match_result.list_lens_to_group[j]

                        if matched_poi_name not in dict_names_of_bridge.keys():

                            # 按照距离进行扣权值.
                            if matched_poi_dis == 0.:
                                dict_names_of_bridge[matched_poi_name] = 0
                            elif matched_poi_dis < 500.:
                                dict_names_of_bridge[matched_poi_name] = -0.5
                            elif matched_poi_dis < 1000.:
                                dict_names_of_bridge[matched_poi_name] = -0.8
                            else:
                                dict_names_of_bridge[matched_poi_name] = -1


            elif link.bridge_type != bridge_type or link_index == len(dict_links_by_order):   # 不是桥.

                if is_bridge == True:
                    is_bridge = False

                    # 标记结果.
                    best_poi_name = find_best_poi_name(dict_names_of_bridge, bridge_type)

                    for k in range(len(list_conn_links)):
                        conn_link = list_conn_links[k]

                        best_poi_name1 = best_poi_name
                        if conn_link.link_label.highway_updir == 1:
                            best_poi_name1 = best_poi_name + '(上行)'
                        elif conn_link.link_label.highway_updir == 2:
                            best_poi_name1 = best_poi_name + '(下行)'
                        elif conn_link.link_label.highway_updir == 3 or conn_link.link_label.highway_updir == 5:
                            best_poi_name1 = best_poi_name + '(内环)'
                        elif conn_link.link_label.highway_updir == 4 or conn_link.link_label.highway_updir == 6:
                            best_poi_name1 = best_poi_name + '(外环)'

                        elif conn_link.link_label.highway_updir == 7:
                            best_poi_name1 = best_poi_name + '(入城)'
                        elif conn_link.link_label.highway_updir == 8:
                            best_poi_name1 = best_poi_name + '(出城)'

                        if bridge_type == 2:
                            conn_link.link_label.len_of_bridge = bridge_len
                            conn_link.link_label.area_poi_bridge = best_poi_name1

                            # logging.info('set link ' + conn_link.link_label.link_id + ', poi name = ' + best_poi_name)

                            conn_link.link_label.point_poi_name = best_poi_name1
                            conn_link.link_label.point_poi_type = 3

                        elif bridge_type == 1:
                            conn_link.link_label.len_of_tunnle = bridge_len
                            conn_link.link_label.area_poi_tunnle = best_poi_name1

                            conn_link.link_label.point_poi_name = best_poi_name1
                            conn_link.link_label.point_poi_type = 4

                    list_conn_links = []
                    dict_names_of_bridge = {}
                    bridge_len = 0.


# 重写点匹配算法 ( 基于角度和最短匹配距离的要求）.
def service_grid_match_link(node_long, node_lat, link_obj):

    dis_to_link = 0.  # 点到路段距离.

    list_node_long = []
    list_node_lat = []


    for j in range(len(link_obj.node_coord_list)):
        items = link_obj.node_coord_list[j].split(' ')

        list_node_long.append(float(items[0]))
        list_node_lat.append(float(items[1]))

    for j in range(len(link_obj.node_coord_list) - 1):

        pre_long = list_node_long[j]
        pre_lat = list_node_lat[j]

        next_long = list_node_long[j + 1]
        next_lat = list_node_lat[j + 1]

        angle12 = gis_supporter.cal_angle(pre_long, pre_lat, next_long, next_lat)
        angle13 = gis_supporter.cal_angle(pre_long, pre_lat, node_long, node_lat)

        # 算一下3是否在12的右侧.
        angle_turn_3 = angle13 - angle12
        if angle_turn_3 < 0:
            angle_turn_3 = angle_turn_3 + 360

        if angle_turn_3 > 95: # 说明不在第一象限(正右侧）.
            continue

        inc_angle1 = gis_supporter.cal_inc_angle(angle12, angle13)
        if inc_angle1 > 95:
            continue

        angle21 = angle12 + 180
        if angle21 >= 360:
            angle21 = angle21 - 360

        angle23 = gis_supporter.cal_angle(next_long, next_lat, node_long, node_lat)
        inc_angle2 = gis_supporter.cal_inc_angle(angle23, angle21)

        if inc_angle2 > 95:
            continue

        dis13 = gis_supporter.cal_dis(pre_long, pre_lat, node_long, node_lat)
        dis_to_link = dis13 * math.sin(inc_angle1 * math.pi / 180)

        if dis_to_link > 300.:
            continue

        if dis_to_link < 30.: # 匹配距离太短.
            return (False, 0., 0., 0.)

        else:
            return (True, dis_to_link, 0., 0.)



    return (False, 0., 0., 0.)

# 判断格网中心点是否能够匹配到服务区的路段上.
def grid_center_match_service_links(list_service_links, poi_long, poi_lat):

    list_service_grids = []

    search_grid_len = 0.00018 # 20米格网.

    center_grid_cx = int((poi_long - cp.min_long) / search_grid_len)
    center_grid_cy = int((poi_lat - cp.min_lat) / search_grid_len)

    search_grid_count = 50

    for i in range(search_grid_count * 2 + 1):
        grid_cx = center_grid_cx + i - search_grid_count

        for j in range(search_grid_count * 2 + 1):
            grid_cy = center_grid_cy + j - search_grid_count

            grid_long = cp.min_long + (grid_cx + 0.5) * search_grid_len
            grid_lat = cp.min_lat + (grid_cy + 0.5) * search_grid_len

            for k in range(len(list_service_links)):
                service_link = list_service_links[k]
                (match_ok, dis_to_link, dis_to_fnode, dis_to_tnode) = service_grid_match_link(grid_long, grid_lat, service_link)

                if match_ok == True:
                    service_grid_result = service_grid_result_obj()
                    service_grid_result.match_link_id = service_link.link_label.link_id
                    service_grid_result.grid_center_cx = grid_cx
                    service_grid_result.grid_center_cy = grid_cy
                    service_grid_result.grid_center_long = grid_long
                    service_grid_result.grid_center_lat = grid_lat

                    list_service_grids.append(service_grid_result)
                    break


    return list_service_grids


# 打印服务区的影响范围，是一个多边形，用格网来表达，以利于后续处理.
def print_service_cover_grids(dict_links_by_grid, dict_links, service_info_path, service_label, service_output_path):

    service_output = open(service_output_path, 'w')

    # step1：获取高速名称（包括主线、支路等）.
    dict_trip_keys = {}

    print('dict_links count: ' + '{:d}'.format(len(dict_links)))
    for link_id in sorted(dict_links.keys()):

        link_obj = dict_links[link_id]

        link_name = link_obj.link_label.highway_name_identify
        link_updir = link_obj.link_label.highway_updir

        trip_key = link_name + '_' + '{:d}'.format(link_updir) + '_' + service_label  # 服务区 2.

        if trip_key not in dict_trip_keys.keys():
            poi_match = stake_match_obj()
            poi_match.dict_trip_links = {}
            poi_match.mile_stake_info = ''
            poi_match.dict_trip_links[link_id] = link_obj

            dict_trip_keys[trip_key] = poi_match
        else:
            poi_match = dict_trip_keys[trip_key]
            poi_match.dict_trip_links[link_id] = link_obj

    # step2： 遍历里程桩文件，获取相应高速名称的所有服务区.
    with open(service_info_path, 'r') as f:
        for line in f:

            items = line.strip('\n').split(',')

            trip_key = items[0] + '_' + items[1] + '_' + items[2]

            if trip_key in dict_trip_keys.keys():
                poi_match = dict_trip_keys[trip_key]

                print('trip: ' + trip_key + ', link count: ' + '{:d}'.format(len(poi_match.dict_trip_links)))
                poi_match.mile_stake_info = line.strip('\n')


    # step3: 匹配.
    for trip_key in sorted(dict_trip_keys.keys()):

        poi_match = dict_trip_keys[trip_key]

        if poi_match.mile_stake_info == '':
            logging.error('can not find trip key: ' + trip_key)
            continue

        items = poi_match.mile_stake_info.split(',')

        # 1- 建立按照序号的索引.
        dict_links_by_order = {}
        for link_id in sorted(poi_match.dict_trip_links.keys()):
            link = poi_match.dict_trip_links[link_id]
            dict_links_by_order[link.link_label.trip_index] = link

        node_count = int(items[3])
        # print('node count = ' + '{:d}'.format(node_count))

        for k in range(node_count):
            node_info = items[4 + k]
            node_items = node_info.split('|')

            poi_name = node_items[0]

            # print('k = ' + '{:d}'.format(k) + ', proc poi_name = ' + poi_name)

            if poi_name == '':
                poi_name = '未命名服务区'

            # if poi_name != '安阳服务区':
            #     continue

            poi_coords = node_items[1].split(' ')
            poi_long = float(poi_coords[0])
            poi_lat = float(poi_coords[1])

            dict_maybe_links = {}
            for search_count in range(10): # 因为服务区的POI可能离路比较远，要扩大搜索范围.
                 dict_maybe_links = mm.find_maybe_link_by_grid(poi_long, poi_lat, dict_links_by_grid, search_count + 5)

                 if len(dict_maybe_links) != 0:
                     break

            find_poi_match_link = False

            for maybe_linkid in sorted(dict_maybe_links.keys()):
                if maybe_linkid in poi_match.dict_trip_links.keys():
                    link = poi_match.dict_trip_links[maybe_linkid]
                    (match_ok, dis_to_link, dis_to_fnode, dis_to_tnode) = mm.node_match_link(poi_long, poi_lat, link, 300., 95)

                    if match_ok == True:

                        # logging.info('poi name = ' + poi_name + ', match link: ' + link.link_label.link_id)

                        poi_name1 = poi_name

                        if link.link_label.highway_updir == 1:
                            poi_name1 = poi_name + '(上行)'
                        elif link.link_label.highway_updir == 2:
                            poi_name1 = poi_name + '(下行)'
                        elif link.link_label.highway_updir == 3 or link.link_label.highway_updir == 5:
                            poi_name1 = poi_name + '(内环)'
                        elif link.link_label.highway_updir == 4 or link.link_label.highway_updir == 6:
                            poi_name1 = poi_name + '(外环)'

                        elif link.link_label.highway_updir == 7:
                            poi_name1 = poi_name + '(入城)'
                        elif link.link_label.highway_updir == 8:
                            poi_name1 = poi_name + '(出城)'


                        link.link_label.point_poi_name = poi_name1
                        link.link_label.point_poi_type = 2 # 服务区.

                        # 往前往后搜索1km作为服务区的范围.

                        list_service_links = []   # 存放服务区的links.
                        list_service_links.append(link)

                        # 往下游搜索1km.
                        dis_f_search = dis_to_tnode

                        for i in range(10):
                            f_index = link.link_label.trip_index + i + 1
                            if f_index > len(poi_match.dict_trip_links):
                                break

                            if dis_f_search > 500.:
                                break

                            f_link = dict_links_by_order[f_index]
                            list_service_links.append(f_link)
                            dis_f_search = dis_f_search + f_link.link_label.len

                        # 往上游搜索1km.
                        dis_b_search = dis_to_fnode

                        for i in range(10):
                            b_index = link.link_label.trip_index - i - 1

                            if b_index < 1:
                                break

                            if dis_b_search > 500.:
                                break

                            b_link = dict_links_by_order[b_index]
                            list_service_links.append(b_link)
                            dis_b_search = dis_b_search + b_link.link_label.len


                        # 找到服务区匹配道路右侧的满足匹配关系的格网.
                        list_service_grids = grid_center_match_service_links(list_service_links, poi_long, poi_lat)
                        logging.info('trip_key = ' + trip_key + ', poi_name = ' + poi_name + ', get match grids: ' + '{:d}'.format(len(list_service_grids)))

                        # 打印结果.
                        for j in range(len(list_service_grids)):
                            service_grid = list_service_grids[j]

                            service_output.write(trip_key + ',' + poi_name1 + ',' + service_grid.match_link_id + ','\
                                                 + '{:d}'.format(service_grid.grid_center_cx) + ',' \
                                                 + '{:d}'.format(service_grid.grid_center_cy) + ','\
                                                 + '{:.6f}'.format(service_grid.grid_center_long) + ','\
                                                 + '{:.6f}'.format(service_grid.grid_center_lat) + '\n')

                        find_poi_match_link = True
                        break  # 匹配成功就跳出.

                    else:
                        continue
                else:
                    continue

            if find_poi_match_link == False:
                logging.error('can not find link of poi: ' + poi_name)

    service_output.close()

# 对于主线延伸出来的收费站，拷贝主线的名称和收费站名称.
def copy_highway_name(toll_expand_link, highway_link):
    toll_expand_link.link_label.highway_name_degree1 = highway_link.link_label.highway_name_degree1
    toll_expand_link.link_label.highway_name_degree2 = highway_link.link_label.highway_name_degree2
    toll_expand_link.link_label.highway_name_degree3 = highway_link.link_label.highway_name_degree3
    toll_expand_link.link_label.highway_name_identify = highway_link.link_label.highway_name_identify
    toll_expand_link.link_label.highway_name_segment = highway_link.link_label.highway_name_segment


# 读取收费站和路段的匹配关系.
def read_toll_match_info(toll_match_path):

    dict_toll_match_infos = {}

    with open(toll_match_path, 'r') as f:
        for line in f:

            items = line.strip('\n').split(',')

            toll_match = toll_station_match_obj()
            toll_match.highway_name = items[0]
            toll_match.highway_updir = items[1]
            toll_match.toll_station_name = items[2]

            toll_match.toll_long = items[3]
            toll_match.toll_lat = items[4]

            toll_match.matched_link_id = items[5]

            if toll_match.matched_link_id not in dict_toll_match_infos.keys():
                list_toll_matched = []
                list_toll_matched.append(toll_match)
                dict_toll_match_infos[toll_match.matched_link_id] = list_toll_matched
            else: # 可能有多个收费站属于不同的高速，是重名的.
                list_toll_matched = dict_toll_match_infos[toll_match.matched_link_id]
                list_toll_matched.append(toll_match)
    f.close()

    return dict_toll_match_infos

# 判定是否是出口link.
def check_out_high_link(dtiplus_link, dict_highway_links):

    if len(dtiplus_link.next_links) != 2:
        return (1, None)

    else:

        next_link1 = dtiplus_link.next_links[0]
        next_link2 = dtiplus_link.next_links[1]

        if next_link1.link_id in dict_highway_links.keys() and next_link2.link_id not in dict_highway_links.keys():
            return (0, next_link2)
        elif next_link1.link_id not in dict_highway_links.keys() and next_link2.link_id in dict_highway_links.keys():
            return (0, next_link1)
        elif next_link1.link_id in dict_highway_links.keys() and next_link2.link_id in dict_highway_links.keys():
            return (-1, None)
        elif next_link1.link_id not in dict_highway_links.keys() and next_link2.link_id not in dict_highway_links.keys():
            return (-2, None)

# 判定是否入口link.
def check_in_high_link(dtiplus_link, dict_highway_links):
    if len(dtiplus_link.pre_links) != 2:
        return (1, None)

    else:
        pre_link1 = dtiplus_link.pre_links[0]
        pre_link2 = dtiplus_link.pre_links[1]

        if pre_link1.link_id in dict_highway_links.keys() and pre_link2.link_id not in dict_highway_links.keys():
            return (0, pre_link2)
        elif pre_link1.link_id not in dict_highway_links.keys() and pre_link2.link_id in dict_highway_links.keys():
            return (0, pre_link1)
        elif pre_link1.link_id in dict_highway_links.keys() and pre_link2.link_id in dict_highway_links.keys():
            return (-1, None)
        elif pre_link1.link_id not in dict_highway_links.keys() and pre_link2.link_id not in dict_highway_links.keys():
            return (-2, None)


#  获取收费站外延的道路并进行属性补充.
def extract_toll_station_infos(dtiplus_map, highway_links, toll_match_path):

    # 返回新增的收费站的道路.
    dict_added_links = {}

    # Step1: 提取highway_link里边的高速名称.
    dict_highway_name = {}
    for link_id in sorted(highway_links.keys()):
        highway_link = highway_links[link_id]

        if highway_link.link_label.highway_name_identify not in dict_highway_name.keys():
            dict_highway_name[highway_link.link_label.highway_name_identify] = 1

    # 得到收费站和路段的匹配关系.
    dict_toll_match_infos = read_toll_match_info(toll_match_path)

    for high_link_id in sorted(highway_links.keys()):
        high_link = highway_links[high_link_id]

        if high_link_id not in dtiplus_map.link_dict.keys():
            logging.error('can not find same link: ' + high_link_id + ' in dtiplus 17q2 maps.')
            continue

        dtiplus_link = dtiplus_map.link_dict[high_link_id]

        # 主线上的收费站.
        if dtiplus_link.link_id in dict_toll_match_infos.keys():

            toll_station = mm.find_match_toll_station(dtiplus_link.link_id, dict_toll_match_infos, dict_highway_name)

            if toll_station == None:
                logging.error('can not find right toll station on link: ' + dtiplus_link.link_id)
                continue

            toll_station_name = toll_station.toll_station_name
            if '主线' not in toll_station_name:
                toll_station_name = toll_station_name.replace('收费站', '主线收费站')

            if high_link.link_label.highway_updir == 1:
                toll_station_name = toll_station_name + '(上行)'
            elif high_link.link_label.highway_updir == 2:
                toll_station_name = toll_station_name + '(下行)'
            elif high_link.link_label.highway_updir == 3 or  high_link.link_label.highway_updir == 5:
                toll_station_name = toll_station_name + '(内环)'
            elif high_link.link_label.highway_updir == 4 or  high_link.link_label.highway_updir == 6:
                toll_station_name = toll_station_name + '(外环)'

            elif high_link.link_label.highway_updir == 7:
                toll_station_name = toll_station_name + '(入城)'
            elif high_link.link_label.highway_updir == 8:
                toll_station_name = toll_station_name + '(出城)'


            highway_links[high_link_id].link_label.point_poi_name = toll_station_name
            highway_links[high_link_id].link_label.point_poi_type = 1 # 收费站.

            highway_links[high_link_id].link_label.area_poi_toll = toll_station_name

            (search_code1, toll_next_links, search_len1) = mm.straight_path(dtiplus_link, 1000., highway_links, True, False) # 下游1公里.
            if search_code1 == 1 or search_code1 == 3:
                for k in range(len(toll_next_links)):
                    if toll_next_links[k].link_id in highway_links.keys():
                        highway_links[toll_next_links[k].link_id].link_label.area_poi_toll = toll_station_name


            (search_code2, toll_pre_links, search_len2) = mm.straight_path(dtiplus_link, 2000., highway_links, False, False) # 上游2公里.

            if search_code2 == 2 or search_code == 4:
                for k in range(len(toll_pre_links)):
                    if toll_pre_links[k].link_id in highway_links.keys():
                        highway_links[toll_pre_links[k].link_id].link_label.area_poi_toll = toll_station_name


            continue

        # 主线外的收费站.
        (check_out_code, out_link) = check_out_high_link(dtiplus_link, highway_links)
        if check_out_code == 0: # 说明找到了出口路段.

            (derive_result, list_links_in_path, toll_station, poi_match_link) = mm.path_derive(out_link, \
                                                                                            dict_toll_match_infos, 5000., dict_highway_name, highway_links, True)

            if derive_result == True:

                for k in range(len(list_links_in_path)):
                    link_in_path = list_links_in_path[k]
                    copy_highway_name(link_in_path, high_link)

                    if link_in_path.link_id not in dict_added_links.keys():
                        dict_added_links[link_in_path.link_id] = link_in_path

                    if link_in_path.link_label.trip_type == 0:
                        link_in_path.link_label.trip_type = 6  # 出口匝道.

                    if link_in_path.link_label.trip_from_code == '':
                        link_in_path.link_label.trip_from_code = high_link.link_label.trip_code
                    else:
                        link_in_path.link_label.trip_from_code = '' # 上下行出口匝道的并线部分，不赋值.

                    link_in_path.link_label.area_poi_toll = toll_station.toll_station_name + '(出口)'
                    link_in_path.link_label.highway_name_degree3 = toll_station.toll_station_name + '(出口)'


                high_link.link_label.point_poi_name = toll_station.toll_station_name
                high_link.link_label.point_poi_type = 1 # 收费站.

                poi_match_link.link_label.point_poi_name = toll_station.toll_station_name + '(出口)'
                poi_match_link.link_label.trip_type = 8  # 出口收费站所在路段.
                poi_match_link.link_label.area_poi_toll = toll_station.toll_station_name + '(出口)'
                copy_highway_name(poi_match_link, high_link)
                poi_match_link.link_label.highway_name_degree3 = toll_station.toll_station_name + '(出口)'

                if poi_match_link.link_id not in dict_added_links.keys():
                    dict_added_links[poi_match_link.link_id] = poi_match_link

                # 直线搜索出口收费站的下游.
                (search_code, toll_next_links, search_len) = mm.straight_path(poi_match_link, 1000., highway_links, True)

                if search_code == 1 or search_code == 3:
                    for k in range(len(toll_next_links)):
                        toll_next_link = toll_next_links[k]
                        copy_highway_name(toll_next_link, high_link)

                        if toll_next_link.link_id not in dict_added_links.keys():
                            dict_added_links[toll_next_link.link_id] = toll_next_link

                        toll_next_link.link_label.trip_type = 10  # 出口收费站下游匝道.
                        toll_next_link.link_label.area_poi_toll = toll_station.toll_station_name + '(出口)'
                        toll_next_link.link_label.highway_name_degree3 = toll_station.toll_station_name + '(出口)'

            else:
                logging.error('out link: ' + out_link.link_id + ' can not find toll station on next links.')


        # 注意，有的路段既是入口路段，又是出口路段.
        (check_in_code, in_link) = check_in_high_link(dtiplus_link, highway_links)
        if check_in_code == 0: # 说明找到了入口路段.

            (derive_result, list_links_in_path, toll_station, poi_match_link) = mm.path_derive(in_link, \
                                                                                            dict_toll_match_infos, 5000., dict_highway_name, highway_links, False)

            if derive_result == True:

                for k in range(len(list_links_in_path)):
                    link_in_path = list_links_in_path[k]
                    copy_highway_name(link_in_path, high_link)

                    if link_in_path.link_id not in dict_added_links.keys():
                        dict_added_links[link_in_path.link_id] = link_in_path

                    if link_in_path.link_label.trip_type == 0:
                        link_in_path.link_label.trip_type = 5  # 入口匝道.

                    if link_in_path.link_label.trip_to_code == '':
                        link_in_path.link_label.trip_to_code = high_link.link_label.trip_code
                    else:
                        link_in_path.link_label.trip_to_code = ''  # 上下行出口匝道的并线部分，不赋值.

                    link_in_path.link_label.area_poi_toll = toll_station.toll_station_name + '(入口)'
                    link_in_path.link_label.highway_name_degree3 = toll_station.toll_station_name + '(入口)'

                high_link.link_label.point_poi_name = toll_station.toll_station_name
                high_link.link_label.point_poi_type = 1  # 收费站.

                poi_match_link.link_label.point_poi_name = toll_station.toll_station_name + '(入口)'
                poi_match_link.link_label.trip_type = 9  # 入口收费站所在路段.
                poi_match_link.link_label.area_poi_toll = toll_station.toll_station_name + '(入口)'
                copy_highway_name(poi_match_link, high_link)
                poi_match_link.link_label.highway_name_degree3 = toll_station.toll_station_name + '(入口)'

                if poi_match_link.link_id not in dict_added_links.keys():
                    dict_added_links[poi_match_link.link_id] = poi_match_link

                # 直线搜索入口收费站的上游.
                (search_code, toll_pre_links, search_len) = mm.straight_path(poi_match_link, 2000., highway_links, False)

                if search_code == 2 or search_code == 4:
                    for k in range(len(toll_pre_links)):
                        toll_pre_link = toll_pre_links[k]
                        copy_highway_name(toll_pre_link, high_link)

                        if toll_pre_link.link_id not in dict_added_links.keys():
                            dict_added_links[toll_pre_link.link_id] = toll_pre_link

                        toll_pre_link.link_label.trip_type = 11  # 入口收费站上游匝道.
                        toll_pre_link.link_label.area_poi_toll = toll_station.toll_station_name + '(入口)'
                        toll_pre_link.link_label.highway_name_degree3 = toll_station.toll_station_name + '(入口)'
            else:
                logging.error('in link: ' + in_link.link_id + ' can not find toll station on pre links.')


    return dict_added_links


# 基于city_code来解码还原出 原来的省份、城市、区县名称.
def decode_city_code(dict_links, city_encode_path):

    line_count = 0
    dict_city_codes = {}
    dict_pre_city_encodes = {}

    with open(city_encode_path, 'r') as f:
        for line in f:

            line_count = line_count + 1
            if line_count == 1:
                continue

            items = line.strip('\n').replace('\"', '').split(',')

            city_code_id = items[3]

            if city_code_id not in dict_city_codes.keys():
                city_encode = city_encode_obj()

                city_encode.province_name = items[0]
                city_encode.city_name = items[1]
                city_encode.county_name = items[2]
                dict_city_codes[city_code_id] = city_encode

                if items[4] != '': # 说明city_code改过了.

                    pre_city_code_id = items[4]
                    pre_city_encode = city_encode_obj()

                    pre_city_encode.province_name = items[0]
                    pre_city_encode.city_name = items[1]
                    pre_city_encode.county_name = items[2]

                    pre_city_encode.change_city_encode = city_code_id
                    dict_pre_city_encodes[pre_city_code_id] = pre_city_encode

    f.close()

    for link_id in sorted(dict_links.keys()):
        link = dict_links[link_id]

        if link.link_label.city_code in dict_city_codes.keys():
            city_encode = dict_city_codes[link.link_label.city_code]

            link.link_label.area_poi_province = city_encode.province_name
            link.link_label.area_poi_city = city_encode.city_name
            link.link_label.area_poi_county = city_encode.county_name
        else:

            # 区县经过了改名.
            if link.link_label.city_code in dict_pre_city_encodes.keys():
                pre_city_encode = dict_pre_city_encodes[link.link_label.city_code]

                link.link_label.area_poi_province = pre_city_encode.province_name
                link.link_label.area_poi_city = pre_city_encode.city_name
                link.link_label.area_poi_county = pre_city_encode.county_name

                # logging.info('change ' + link.link_label.link_id + ' from ' +  link.link_label.city_code + ' to ' + pre_city_encode.change_city_encode)
                link.link_label.city_code = pre_city_encode.change_city_encode

            else:
                logging.error('can not find ' + link.link_label.link_id + ' \'s city_code: ' +  link.link_label.city_code)


# 寻找出入区域范围的路段.
def find_in_out_links(dict_links):

    dict_links_by_trip = {}

    for link_id in sorted(dict_links.keys()):

        link = dict_links[link_id]
        trip_key = link.link_label.highway_name_identify + '_' + '{:d}'.format(link.link_label.highway_updir)

        if trip_key not in dict_links_by_trip.keys():
            trip = {}
            trip[link.link_label.trip_index] = link
            dict_links_by_trip[trip_key] = trip
        else:
            trip = dict_links_by_trip[trip_key]
            trip[link.link_label.trip_index] = link


    for trip_key in sorted(dict_links_by_trip.keys()):
        trip = dict_links_by_trip[trip_key]

        for j in range(len(trip) - 1):
            pre_link = trip[j + 1]
            next_link = trip[j + 2]

            if pre_link.link_label.area_poi_zoo != next_link.link_label.area_poi_zoo:
               pre_link.link_label.cross_zoo = pre_link.link_label.area_poi_zoo + '>' + next_link.link_label.area_poi_zoo

            if pre_link.link_label.area_poi_security != next_link.link_label.area_poi_security:
                pre_link.link_label.cross_security = pre_link.link_label.area_poi_security + '>' + next_link.link_label.area_poi_security

            if pre_link.link_label.area_poi_province != next_link.link_label.area_poi_province:
                pre_link.link_label.cross_province = pre_link.link_label.area_poi_province + '>' + next_link.link_label.area_poi_province

            if pre_link.link_label.area_poi_city != next_link.link_label.area_poi_city:
                pre_link.link_label.cross_city = pre_link.link_label.area_poi_city + '>' + next_link.link_label.area_poi_city

            if pre_link.link_label.area_poi_county != next_link.link_label.area_poi_county:
                pre_link.link_label.cross_county = pre_link.link_label.area_poi_county + '>' + next_link.link_label.area_poi_county


# 全体道路增加上下行标记.
def add_high_code_updir(dict_links):
    for link_id in sorted(dict_links.keys()):
        link = dict_links[link_id]

        link.link_label.trip_code = link.link_label.trip_code + '_{:d}'.format(link.link_label.highway_updir)

# test
def print_map_indexer(output_path, dict_links_by_grid):

    output = open(output_path, 'w')

    for grid_key in sorted(dict_links_by_grid.keys()):
        link_list = dict_links_by_grid[grid_key]

        sss = set(link_list)

        output.write(grid_key + ', ')
        for link_id in sss:

            output.write(link_id + ' ')

        output.write('\n')


