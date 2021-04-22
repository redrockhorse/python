# -*- coding:utf-8 -*-
# @Time : 2020/9/8 上午9:41
# @Author: kkkkibj@163.com
# @File : huizhou_link_csv2json.py
# 惠州路网 csv 转  json


import csv
import json
result = {}
result['data'] = {}
result['data']['highway'] = []
result['data']['center'] = []
result['data']['other'] = []
with open('/Users/hongyanma/Downloads/huizhou_group_check_sort_addcolum.csv', 'r', encoding='gbk') as csvf:
    data = csv.reader(csvf)
    i = 0
    for item in data:
        if i > 0:
            print(item)
            if item[12] == '高速':
                result['data']['highway'].append({'key': item[0], 'lseq': item[11]})
            elif item[12] == '中心区':
                result['data']['center'].append({'key': item[0], 'lseq': item[11]})
            else:
                result['data']['other'].append({'key': item[0], 'lseq': item[11]})
        i += 1
print(result)

with open('/Users/hongyanma/Downloads/huizhou_group_check_sort_addcolum.json','w') as jsonf:
    json.dump(result, jsonf)
