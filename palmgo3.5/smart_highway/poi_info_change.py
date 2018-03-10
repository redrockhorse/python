## -*- coding: utf8 -*-
#!/usr/bin/python
import logging # 日志类.
logging.basicConfig(level = logging.INFO)

import midmif_supporter
import gis_supporter
import const_param as cp

# 主要目的是将POI的信息进行最初步的转换：
# 1 - 只遴选出 2（服务区） 3 （收费站） 8 （枢纽） 9 （桥） 15 （隧道）的信息.
# 2 - 将 8 （枢纽中）除了 “枢纽” “立交桥” 字样，且带“大桥”字样的 POI点合并到 9 （桥）中，注意排重.


class poi_info_obj:

    mid_line = ''
    coord_str = ''  # 坐标.

    trip_name = ''
    trip_updir = ''
    poi_name = ''
    poi_type = ''

    if_print = True
    if_created = False


    def __init__(self):
        mid_line = ''
        coord_str = ''  # 坐标.

        trip_name = ''
        trip_updir = ''
        poi_name = ''
        poi_type = ''

        if_print = True # 是不是最后打印出来.
        if_created = False # 是后续创造出来的.



# 处理POI的类.

class poi_map_obj:

    dict_trips = {}
    pre_mif_lines = []

    trip_name_index = 0
    trip_updir_index = 0
    poi_name_index = 0
    poi_type_index = 0


    dict_pois = {}


    def __init__(self, tn_idx, tu_idx, pn_idx, pt_idx):
        self.trip_name_index = tn_idx
        self.trip_updir_index = tu_idx

        self.poi_name_index = pn_idx
        self.poi_type_index = pt_idx

    # 创建POI地图对象.

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

            mid_items = mid_line.replace('\"', '').split(',')

            trip_name = mid_items[self.trip_name_index]
            trip_updir = mid_items[self.trip_updir_index]
            poi_name = mid_items[self.poi_name_index]
            poi_type = mid_items[self.poi_type_index]

            if poi_type != '8' and poi_type != '9' and poi_type != '2' and poi_type != '3' and poi_type != '15':
                continue

            poi = poi_info_obj()
            poi.mid_line = mid_line
            poi.coord_str = mif_coord_list[0]

            poi.trip_name = trip_name
            poi.trip_updir = trip_updir
            poi.poi_name = poi_name
            poi.poi_type = poi_type
            poi.if_print = True
            poi.if_created = False

            poi_key = poi.trip_name + '|' + poi.trip_updir + '|' +  poi.poi_type + '|' + poi.coord_str

            if poi_key not in self.dict_pois.keys():
                self.dict_pois[poi_key] = poi

        #  将 9 中带立交桥的 移植到 8中.

        for poi_key in sorted(self.dict_pois.keys()):
            poi = self.dict_pois[poi_key]

            if poi.poi_type == '9' and ('小桥' in poi.poi_name or '无名' in poi.poi_name \
                                                or '通道' in poi.poi_name or '分离' in poi.poi_name \
                                        or '排水沟' in poi.poi_name or '干沟' in poi.poi_name \
                                        or '天桥' in poi.poi_name or '+' in poi.poi_name\
                                        or '中桥' == poi.poi_name or '跨线桥' == poi.poi_name \
                                                or '互通跨线桥' == poi.poi_name or '大桥' == poi.poi_name) :
                poi.if_print = False  # 将这种删除

            if poi.poi_type == '9' and ('立交桥' in poi.poi_name or '互通' in poi.poi_name or '枢纽' in poi.poi_name):
                poi.if_print = False # 将这种删除.

                create_poi_key = poi.trip_name + '|' + poi.trip_updir + '|' +  '8' + '|' + poi.coord_str

                if create_poi_key not in self.dict_pois.keys():
                    create_poi = poi_info_obj()

                    create_poi_items = poi.mid_line.split(',')
                    create_poi_items[self.poi_type_index] = '8'

                    create_mid_line = ''
                    for k in range(len(create_poi_items) - 1):
                        create_mid_line = create_mid_line + create_poi_items[k] + ','
                    create_mid_line = create_mid_line + create_poi_items[len(create_poi_items) - 1]

                    create_poi.mid_line = create_mid_line
                    create_poi.coord_str = poi.coord_str
                    create_poi.trip_name = poi.trip_name
                    create_poi.trip_updir = poi.trip_updir
                    create_poi.poi_name = poi.poi_name
                    create_poi.poi_type = '8'
                    create_poi.if_print = True
                    create_poi.if_created = True

                    self.dict_pois[create_poi_key] = create_poi

        # 将 8 中 带’大桥‘的POI移植到9中.
        for poi_key in sorted(self.dict_pois.keys()):
            poi = self.dict_pois[poi_key]

            if poi.poi_type == '8' and ('大桥' in poi.poi_name or '中桥' in poi.poi_name) \
                and (poi.poi_name != '大桥' and poi.poi_name != '中桥') \
                    and ('无名' not in poi.poi_name and '通道' not in poi.poi_name and '分离' not in poi.poi_name):

                create_poi_key = poi.trip_name + '|' + poi.trip_updir + '|' + '9' + '|' + poi.coord_str

                if create_poi_key not in self.dict_pois.keys():
                    create_poi = poi_info_obj()

                    create_poi_items = poi.mid_line.split(',')
                    create_poi_items[self.poi_type_index] = '9'

                    create_mid_line = ''
                    for k in range(len(create_poi_items) - 1):
                        create_mid_line = create_mid_line + create_poi_items[k] + ','
                    create_mid_line = create_mid_line + create_poi_items[len(create_poi_items) - 1]

                    create_poi.mid_line = create_mid_line
                    create_poi.coord_str = poi.coord_str
                    create_poi.trip_name = poi.trip_name
                    create_poi.trip_updir = poi.trip_updir
                    create_poi.poi_name = poi.poi_name
                    create_poi.poi_type = '9'
                    create_poi.if_print = True
                    create_poi.if_created = True

                    self.dict_pois[create_poi_key] = create_poi


    # 打印POI信息.

    def print_poi_info(self, out_mid_path, out_mif_path):

        output_mid = open(out_mid_path, 'w')
        output_mif = open(out_mif_path, 'w')

        for k in range(len(self.pre_mif_lines)):
            output_mif.write(self.pre_mif_lines[k])

        for poi_key in sorted(self.dict_pois.keys()):
            poi = self.dict_pois[poi_key]

            if poi.if_print == False:
                continue

            output_mid.write(poi.mid_line + '\n')
            output_mif.write('Point ' + poi.coord_str + '\n')
            output_mif.write('\tSymbol (35,0,10)\n')

        output_mid.close()
        output_mif.close()





# test main.
poi_map = poi_map_obj(4, 9, 6, 8)
poi_map.create_map_obj(cp.poi_src_mid_path, cp.poi_src_mif_path)

poi_map.print_poi_info(cp.poi_mid_path, cp.poi_mif_path)

print('操作完成@@')
