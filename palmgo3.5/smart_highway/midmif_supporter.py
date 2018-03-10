## -*- coding: utf8 -*-
#!/usr/bin/python
# 日志类.
import logging
logging.basicConfig(level = logging.INFO)

import string

# mid/mif全局对象.

# 文件对象.
global mid_file
global mif_file

#行List对象.
global mid_lines
global mif_lines

# 当前读到的行号.
global mid_cur_line_num
global mif_cur_line_num

global pre_mif_lines

def load_mid_file(mid_path):
    global mid_file
    global mid_lines
    global mid_cur_line_num
    global pre_mif_lines

    try:
        mid_file = open(mid_path, 'r', encoding='gbk', errors='ignore')
        mid_lines = mid_file.readlines()
        mid_file.close()
        mid_cur_line_num = 0

        logging.info('load mid file ok: ' + mid_path)

    except Exception as err:
        logging.error('load mid file failed: ' + mid_path)
        logging.error(err)

def load_mif_file(mif_path):

    global mif_file
    global mif_lines
    global mif_cur_line_num
    global pre_mif_lines

    try:
        mif_file = open(mif_path, 'r')
        mif_lines = mif_file.readlines()
        mif_file.close()
        mif_cur_line_num = 0
        pre_mif_lines = []

        logging.info('load mif file ok: ' + mif_path)
    except Exception as err:
        logging.error('load mif file failed: ' + mif_path)
        logging.error(err)

# 获取Mif文件在Pre Lines的分割行号.
def read_pre_mif_lines():
    global mif_lines
    global mif_cur_line_num
    global pre_mif_lines

    end_str = 'Data'

    for line in mif_lines:
        mif_cur_line_num = mif_cur_line_num + 1
        pre_mif_lines.append(line)

        if end_str in line:
            break


    # 读取空行.
    for line in mif_lines[mif_cur_line_num:]:

        if line[:-1] != '':
           break
        else:
            mif_cur_line_num = mif_cur_line_num + 1


#是否读取完文件.
def read_all_links():

    global mid_lines
    global mid_cur_line_num

    if mid_cur_line_num == len(mid_lines):
        return True
    else:
        return False


def read_one_link_info():

    global mid_lines
    global mif_lines

    global mid_cur_line_num
    global mif_cur_line_num

    mid_line_str = mid_lines[mid_cur_line_num][:-1]
    mid_cur_line_num = mid_cur_line_num + 1

    mif_line_list = []
    mif_line_str = mif_lines[mif_cur_line_num][:-1]
    lab_str = mif_line_str[0:4]

    if lab_str == 'Line':
        items = mif_line_str.split(' ')

        mif_line_list.append(items[1] + ' ' + items[2])
        mif_line_list.append(items[3] + ' ' + items[4])

        # 读取pen.
        mif_cur_line_num = mif_cur_line_num + 2
        return (mid_line_str, mif_line_list)

    elif lab_str == 'Plin':

        items = mif_line_str.split(' ')
        line_size = int(items[1])

        bgn_line_num = mif_cur_line_num + 1
        end_line_num =  mif_cur_line_num + line_size + 1

        for coord_byte in mif_lines[bgn_line_num:end_line_num]:
            coord_str = coord_byte
            mif_line_list.append(coord_str[:-1])    # 去掉/n

        # 读取pen.
        mif_cur_line_num = mif_cur_line_num + line_size + 2
        return (mid_line_str, mif_line_list)

    elif lab_str == 'Poin':
        items = mif_line_str.split(' ')
        mif_line_list.append(items[1] + ' ' + items[2])

        # 读取pen.
        mif_cur_line_num = mif_cur_line_num + 2
        return (mid_line_str, mif_line_list)

    else:
        logging.error('read error mif line:')
        logging.error(mif_line_str)

# test main.

# mid_path = 'D:\\VC_Data\\lichengzhuang-XUYINGYING\\FCD_1000_17Q2_SN_FC1NR1all-Name.MID'
# mif_path = 'D:\\VC_Data\\lichengzhuang-XUYINGYING\\FCD_1000_17Q2_SN_FC1NR1all-Name.MIF'
#
# load_mid_file(mid_path)
# load_mif_file(mif_path)
#
# read_pre_mif_lines()
#
# print('mid line count: ')
# print(len(mid_lines))
#
# print('mif line count: ')
# print(len(mif_lines))
#
#
# link_index = 1
# while read_all_links() == False:
#     (mid_line, mif_coord_list) = read_one_link_info()
#
#     #print(link_index)
#     link_index = link_index + 1
#
#     # print(mid_line)
#     # print(mif_coord_list)
#
#
# print('total read links: ')
# print(link_index)



