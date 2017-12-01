## -*- coding: utf8 -*-
#!/usr/bin/python
# 日志类.
import logging
logging.basicConfig(level = logging.INFO)


import midmif_supporter
import gis_supporter

# node 对象.
class node_obj:
    def __init__(self):
        pass

# link对象.
class link_obj:

    link_id = ''            # linkid.
    bro_link_id = ''        # 共线的对向linkid.

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

    def __init__(self):
        self.node_coord_list = []
        self.pre_links = []
        self.next_links = []


# 地图对象.
class map_obj:

    link_dict = {}
    fnode_topo_dict = {}
    tnode_topo_dict = {}

    # 创建link对象.
    def create_up_link_obj(self, mid_line, mif_coord_list):

        mid_items = mid_line.split(',')
        up_dir = int(mid_items[6])

        up_link = link_obj()
        up_link.link_id = mid_items[1].strip('\"') + '1'

        if up_link == 1:
            up_link.bro_link_id = mid_items[1].strip('\"') + '0'
        else:
            up_link.bro_link_id = ''

        up_link.len = float(mid_items[5])

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

        mid_items = mid_line.split(',')
        up_dir = int(mid_items[6])

        down_link = link_obj()

        down_link.link_id = mid_items[1].strip('\"') + '0'

        if up_dir == 1:
            down_link.bro_link_id = mid_items[1].strip('\"') + '1'
        else:
            down_link.bro_link_id = ''

        down_link.len = float(mid_items[5])

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
            up_dir = int(mid_items[6])

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



# # test main.
#
# mid_path = 'D:\\VC_Data\\Map\\1100\\16q2\\FCD_1100_16Q2.MID.txt'
# mif_path = 'D:\\VC_Data\\Map\\1100\\16q2\\FCD_1100_16Q2.MIF.txt'
#
#
# dti_plus = map_obj()
#
# dti_plus.create_map_obj(mid_path, mif_path)
# dti_plus.create_topo()
#
# #print(dti_plus.fnode_topo_dict)
#
#
# # 打印上下游关系.
#
# output = open('D:\\VC_Data\\Map\\1100\\16q2\\ts.txt', 'w')
#
#
# for link_obj in dti_plus.link_dict.values():
#
#     # print('linkid: ')
#     # print(link_obj.link_id)
#     #
#
#     output.write('linkid: ')
#     output.write(link_obj.link_id)
#     output.write('; next links: ')
#
#
#
#     #print('next links: ')
#     # print(len(link_obj.next_links))
#     next_link_vec = []
#     for next_link in link_obj.next_links:
#         #print(next_link.link_id)
#         next_link_vec.append(next_link.link_id)
#
#     next_link_list_str = "| ".join(next_link_vec)
#     output.write(next_link_list_str)
#
#
#
#     #print('pre links: ')
#
#     output.write('; pre links: ')
#     pre_link_vec = []
#     for pre_link in link_obj.pre_links:
#         # print(pre_link.link_id)
#         pre_link_vec.append(pre_link.link_id)
#
#     pre_link_list_str = "| ".join(pre_link_vec)
#     output.write(pre_link_list_str)
#
#     output.write('\r\n')
#
# output.close()










