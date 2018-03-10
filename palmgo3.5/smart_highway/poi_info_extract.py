## -*- coding: utf8 -*-
#!/usr/bin/python
import logging # 日志类.
logging.basicConfig(level = logging.INFO)

import midmif_supporter
import gis_supporter
import const_param as cp
# 生成POI文件列表.

# 处理POI的类.

class poi_map_obj:

    dict_trips = {}
    pre_mif_lines = []

    trip_name_index = 0
    trip_updir_index = 0
    poi_name_index = 0
    poi_type_index = 0

    def __init__(self, tn_idx, tu_idx, pn_idx, pt_idx):
        self.trip_name_index = tn_idx
        self.trip_updir_index = tu_idx

        self.poi_name_index = pn_idx
        self.poi_type_index = pt_idx

    # 处理POI重名的情况.
    # 如果POI重名，则在后边加[1][2][3]……
    def add_name_to_dict(self, dict_names, name, coord, poi_type):

        if poi_type != '3':
            if name == '':
                name = 'blank'

            add_index = 1
            while True:
                if name not in dict_names.keys():
                    dict_names[name] = coord
                    final_name = name
                    return final_name

                else:
                    name = 'blank[' + '{:d}'.format(add_index) + ']'
                    add_index = add_index + 1
                    continue

        else: # 收费站 不区分上下行；所以将坐标直接放到后边就行.

            if name not in dict_names.keys():
                dict_names[name] = coord
                final_name = name
                return final_name
            else:
                src_coord = dict_names[name]
                dst_coord = src_coord + ';' + coord
                dict_names[name] = dst_coord
                final_name = name
                return final_name


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

            trip_key1 = ''
            trip_key2 = ''
            trip_key = ''

            if poi_type == '8': # 枢纽先不处理.
                continue
            elif poi_type == '3': # 收费站不区分上下行 (2个都写到一起吧).
                if trip_updir == '1' or trip_updir == '2':
                    trip_key = trip_name + ',' + '12' + ',' + poi_type

                elif trip_updir == '3' or trip_updir == '4':
                    trip_key = trip_name + ',' + '34' + ',' + poi_type

                elif trip_updir == '5' or trip_updir == '6':
                    trip_key = trip_name + ',' + '56' + ',' + poi_type

                elif trip_updir == '7' or trip_updir == '8':
                    trip_key = trip_name + ',' + '78' + ',' + poi_type


            elif poi_type == '9' or poi_type == '15': #桥隧要往两边分.

                if trip_updir == '12':
                    trip_key1 = trip_name + ',' + '1' + ',' + poi_type
                    trip_key2 = trip_name + ',' + '2' + ',' + poi_type

                elif trip_updir == '34':
                    trip_key1 = trip_name + ',' + '3' + ',' + poi_type
                    trip_key2 = trip_name + ',' + '4' + ',' + poi_type

                elif trip_updir == '56':
                    trip_key1 = trip_name + ',' + '5' + ',' + poi_type
                    trip_key2 = trip_name + ',' + '6' + ',' + poi_type

                elif trip_updir == '78':
                    trip_key1 = trip_name + ',' + '7' + ',' + poi_type
                    trip_key2 = trip_name + ',' + '8' + ',' + poi_type

                else:

                    if trip_updir == '1' or trip_updir == '2' or trip_updir == '3' or trip_updir == '4' \
                            or trip_updir == '5' or trip_updir == '6' or trip_updir == '7' or trip_updir == '8':
                        trip_key = trip_name + ',' + trip_updir + ',' + poi_type
                    else:
                        logging.error('unexpected trip_updir = ' + trip_updir + ', from mid_line = ' + mid_line)

            else:
                if trip_updir == '1' or trip_updir == '2' or trip_updir == '3' or trip_updir == '4' \
                        or trip_updir == '5' or trip_updir == '6' or trip_updir == '7' or trip_updir == '8':
                    trip_key = trip_name + ',' + trip_updir + ',' + poi_type
                else:
                    logging.error('unexpected trip_updir = ' + trip_updir + ', from mid_line = ' + mid_line)


            if trip_key1 != '':

                final_name = ''

                if trip_key1 not in self.dict_trips.keys():
                    trip = {}
                    final_name = self.add_name_to_dict(trip, poi_name, mif_coord_list[0], poi_type)  # 处理POI重名的情况.
                    self.dict_trips[trip_key1] = trip
                else:
                    trip = self.dict_trips[trip_key1]
                    final_name = self.add_name_to_dict(trip, poi_name, mif_coord_list[0], poi_type)  # 处理POI重名的情况.

                if final_name != poi_name:
                    logging.error('error: name changed, poi_name = ' + poi_name + ', final name = ' + final_name)


            if trip_key2 != '':
                final_name = ''

                if trip_key2 not in self.dict_trips.keys():
                    trip = {}
                    final_name = self.add_name_to_dict(trip, poi_name, mif_coord_list[0], poi_type)  # 处理POI重名的情况.
                    self.dict_trips[trip_key2] = trip
                else:
                    trip = self.dict_trips[trip_key2]
                    final_name = self.add_name_to_dict(trip, poi_name, mif_coord_list[0], poi_type)  # 处理POI重名的情况.

                if final_name != poi_name:
                    logging.error('error: name changed, poi_name = ' + poi_name + ', final name = ' + final_name)



            if trip_key != '':
                final_name = ''

                if trip_key not in self.dict_trips.keys():
                    trip = {}
                    final_name = self.add_name_to_dict(trip, poi_name, mif_coord_list[0], poi_type)  # 处理POI重名的情况.
                    self.dict_trips[trip_key] = trip
                else:
                    trip = self.dict_trips[trip_key]
                    final_name = self.add_name_to_dict(trip, poi_name, mif_coord_list[0], poi_type)  # 处理POI重名的情况.

                if final_name != poi_name:
                    logging.error('error: name changed, poi_name = ' + poi_name + ', final name = ' + final_name)



    # 打印POI信息.

    def print_poi_info(self, output_path):

        output = open(output_path, 'w')

        for trip_key in sorted(self.dict_trips.keys()):
            trip = self.dict_trips[trip_key]
            output.write(trip_key + ',' + '{:d}'.format(len(trip)) + ',')

            for poi_name in sorted(trip.keys()):
                output.write(poi_name + '|' + trip[poi_name] + ',')

            output.write('\n')

        output.close()


# test main.
poi_map = poi_map_obj(4, 9, 6, 8)
poi_map.create_map_obj(cp.poi_mid_path, cp.poi_mif_path)

poi_map.print_poi_info(cp.poi_list_path)

print('操作完成@@')









