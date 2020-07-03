# -*- coding:utf-8 -*-
# @Time : 2020/4/26 上午10:23
# @Author: kkkkibj@163.com
# @File : beihang_sensor_data_csv2json.py
# 将北航的的传感器数据cvs转换为json

import json
'''
with open('/Users/hongyanma/Desktop/data_event.csv', 'r') as inputfile:
    result = {}
    dataset = []
    line = inputfile.readline().replace('\n', '')
    while line:
        # print(line)
        arr = line.split(',')
        dataset.append(arr)
        line = inputfile.readline().replace('\n', '')
    print(dataset)
    result['dataset'] = dataset
    with open('/Users/hongyanma/Desktop/data_event.json', 'w+') as outputfile:
        json.dump(result, outputfile)
'''

with open('/Users/hongyanma/Desktop/data_min.csv', 'r') as inputfile:
    result = {}
    dataset = []
    line = inputfile.readline().replace('\n', '')
    while line:
        # print(line)
        arr = line.split(',')
        dataset.append(arr)
        line = inputfile.readline().replace('\n', '')
    print(dataset)
    result['dataset'] = dataset
    with open('/Users/hongyanma/Desktop/data_min.json', 'w+') as outputfile:
        json.dump(result, outputfile)
