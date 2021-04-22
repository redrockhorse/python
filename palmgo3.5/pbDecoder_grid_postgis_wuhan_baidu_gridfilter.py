# -*- coding:utf-8 -*-
# @Time : 2020/7/20 上午11:38
# @Author: kkkkibj@163.com
# @File : pbDecoder.py
# 解析pb gps文件

import zipfile
import json
import os
import GPS_pb2
import coordinateSystemTransform
import struct
import pymysql

grid = [0.09, 0.09]


def getThreeJson(hour):
    for i in range(0, 24):
        print(i)
        hour = str(i)
        dic = {}
        with open('/Users/hongyanma/Downloads/pb/wuhan/t_' + hour + '.json', 'r') as outf:
            dic = json.load(outf)
            data = dic['data']
            # a = sorted(data, key=lambda x: (float(x[0]), float(x[1])))
            # tmp = a[::30]
            # rs['data'] = tmp
            for j in range(3):
                rs = {}
                rs['data'] = data[j::3]
                with open('/Users/hongyanma/Downloads/pb/wuhan/t_' + hour + '_' + str(j) + '.json', 'w') as wf:
                    json.dump(rs, wf)


def thinning():
    for i in range(0, 7):
        print(i)
        hour = str(i)
        dic = {}
        rs = {}
        rs['data'] = []
        with open('/Users/hongyanma/Downloads/pb/wuhan/wh_' + hour + '.json', 'r') as outf:
            dic = json.load(outf)
            data = dic['data']
            a = sorted(data, key=lambda x: (float(x[0]), float(x[1])))
            tmp = a[::5]
            rs['data'] = tmp
            with open('/Users/hongyanma/Downloads/pb/wuhan/t_' + hour + '.json', 'w') as wf:
                json.dump(rs, wf)


if __name__ == '__main__':
    print('start')

    with open('/Users/hongyanma/Downloads/pb/wuhan/d_18.json', 'r') as outf:
        dic = json.load(outf)
        data = dic['data']
        # a = sorted(data, key=lambda x: (float(x[0]), float(x[1])))
        # tmp = a[::30]
        # rs['data'] = tmp
        for j in range(24):
            rs = {}
            rs['data'] = data[j::24]
            with open('/Users/hongyanma/Downloads/pb/wuhan/d_18_' + str(j) + '.json', 'w') as wf:
                json.dump(rs, wf)


# rs = {}
# with open('/Users/hongyanma/Downloads/pb/wuhan/wh_18.json', 'r') as outf:
#     dic = json.load(outf)
#     data = dic['data']
#     a = sorted(data, key=lambda x: (float(x[0]), float(x[1])))
#     tmp = a[::10]
#     rs['data'] = tmp
#     with open('/Users/hongyanma/Downloads/pb/wuhan/d_18.json', 'w') as wf:
#         json.dump(rs, wf)


# for i in range(0, 7):
#     print(i)
#     hour = str(i)
#     dic = {}
#     with open('/Users/hongyanma/Downloads/pb/wuhan/t_' + hour + '.json', 'r') as outf:
#         dic = json.load(outf)
#         data = dic['data']
#         # a = sorted(data, key=lambda x: (float(x[0]), float(x[1])))
#         # tmp = a[::30]
#         # rs['data'] = tmp
#         for j in range(3):
#             rs = {}
#             rs['data'] = data[j::3]
#             with open('/Users/hongyanma/Downloads/pb/wuhan/t_' + hour + '_' + str(j) + '.json', 'w') as wf:
#                 json.dump(rs, wf)
#
# for i in range(0, 7):
#     print(i)
#     hour = str(i)
#     dic = {}
#     rs = {}
#     rs['data'] =[]
#     with open('/Users/hongyanma/Downloads/pb/wuhan/wh_'+hour+'.json','r') as outf:
#         dic = json.load(outf)
#         data = dic['data']
#         a = sorted(data, key=lambda x: (float(x[0]), float(x[1])))
#         tmp = a[::5]
#         rs['data'] = tmp
#         with open('/Users/hongyanma/Downloads/pb/wuhan/t_'+hour+'.json', 'w') as wf:
#             json.dump(rs, wf)

# result = {}
# result['data'] = []
# with open('/Users/hongyanma/Downloads/pb/wuhan/wh_0.json', 'r') as outf:
#     dic = json.load(outf)
#     data = dic['data']
#     print(data)
#     a = sorted(data, key=lambda x: (float(x[0]), float(x[1])))
#     a0 = [float(a[0][0]), float(a[0][1])]
#     result['data'].append(a0)
#     for i in range(1, len(a)):
#         an = [int((float(a[i][0]) - float(a[i - 1][0])) * 1000000), int((float(a[i][1]) - float(a[i - 1][1])) * 1000000)]
#         result['data'].append(an)
#         # a0 = an
#     with open('/Users/hongyanma/Downloads/pb/wuhan/t_0.json', 'w') as wf:
#         json.dump(result, wf)
