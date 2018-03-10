## -*- coding: utf8 -*-
#!/usr/bin/python
# 日志类.
import logging
logging.basicConfig(level = logging.INFO)

import midmif_supporter
import gis_supporter

import const_param as cp

# 处理里程桩数据的类.
class map_obj:

    dict_trips = {}

    pre_mif_lines = []

    link_index = 0
    len_index = 0
    df_index = 0

    def __init__(self, lk_idx, len_idx, df_idx):
        self.link_index = lk_idx
        self.len_index = len_idx
        self.df_index = df_idx


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

            mid_items = mid_line.replace('\"', '').split(',')

            bgn_stake = mid_items[4]
            end_stake = mid_items[5]

            if bgn_stake == '0' and end_stake == '0':
                continue

            up_dir = int(mid_items[self.df_index])
            if up_dir != 2 and up_dir != 3:
                continue

            trip_id = mid_items[2]
            trip_name = mid_items[3]
            trip_updir = mid_items[6]

            city_code = mid_items[11]

            trip_key = trip_id + ',' + trip_name + ',' + trip_updir

            # 整形.
            bgn_new_stake = int(float(bgn_stake) * 1000)
            end_new_stake = int(float(end_stake) * 1000)

            bgn_new_coord = ''
            end_new_coord = ''

            if up_dir == 2:
                bgn_new_coord = mif_coord_list[0] + '|' + city_code
                end_new_coord = mif_coord_list[len(mif_coord_list) - 1] + '|' + city_code

            elif up_dir == 3:
                bgn_new_coord = mif_coord_list[len(mif_coord_list) - 1] + '|' + city_code
                end_new_coord = mif_coord_list[0] + '|' + city_code

            if trip_key in self.dict_trips.keys():
                trip = self.dict_trips[trip_key]

                trip[bgn_new_stake] = bgn_new_coord
                trip[end_new_stake] = end_new_coord

            else:
                trip = {}

                trip[bgn_new_stake] = bgn_new_coord
                trip[end_new_stake] = end_new_coord

                self.dict_trips[trip_key] = trip


            logging.info('total read line: %d ' % line_count)
            logging.info('total create link: %d' % link_count)

    # 打印成新的Point 结果.
    def print_stake_point(self, mid_path, mif_path):

        mid_file = open(mid_path, 'w')
        mif_file = open(mif_path, 'w')

        # 打印Mif文件头.

        mif_file.write('Version   300\n')
        mif_file.write('Charset \"WindowsSimpChinese\"\n')
        mif_file.write('Delimiter \",\"\n')
        mif_file.write('CoordSys Earth Projection 1, 104\n')
        mif_file.write('Columns 4\n')
        mif_file.write('TripId Char(50)\n')
        mif_file.write('Trip_Name Char(50)\n')
        mif_file.write('Trip_SXX Integer\n')
        mif_file.write('Trip_Stake Float\n')
        mif_file.write('Data\n\n')

        for trip_key in sorted(self.dict_trips.keys()):
            trip = self.dict_trips[trip_key]
            trip_items = trip_key.split(',')

            for stake_num in sorted(trip.keys()):
                mid_file.write('\"' + trip_items[0] + '\",\"' + trip_items[1] + '\",\"' + trip_items[2] + '\",' + '{:.3f}'.format(float(stake_num) / 1000.) + '\n')

                all_info =  trip[stake_num] # 去掉后边加的 CityCode信息.
                all_items = all_info.split('|')
                coord_info = all_items[0]

                mif_file.write('Point ' + coord_info + '\n')
                mif_file.write('\tSymbol (35,0,10)\n')


        mid_file.close()
        mif_file.close()

    # 按照简单文件格式打印.
    def print_stake_simple(self, output_path):

        output = open(output_path, 'w')

        for trip_key in sorted(self.dict_trips.keys()):
            trip = self.dict_trips[trip_key]
            trip_items = trip_key.split(',')

            output.write(trip_items[0] + ',' + trip_items[1] + ',' + trip_items[2] + ',' + '{:d}'.format(len(trip)) + ',')

            for stake_num in sorted(trip.keys()):
                output.write('{:.3f}'.format(float(stake_num) / 1000) + '|' + trip[stake_num] + ',')

            output.write('\n')

        output.close()


# 基于 GSLD文件 生成里程桩的Point文件.

def read_gsdl_files(mid_path, mif_path, output_mid_path, output_mif_path):
    gsdl_map = map_obj(0, 6, 1)
    gsdl_map.create_map_obj(mid_path, mif_path)

    gsdl_map.print_stake_point(output_mid_path, output_mif_path)
    gsdl_map.print_stake_simple(cp.stake_list_path)


# test main.
read_gsdl_files(cp.stake_mid_path, cp.stake_mif_path, cp.stake_point_mid_path, cp.stake_point_mif_path)

print('## 操作完成@@')
