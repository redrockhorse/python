# -*- coding:utf-8 -*-
# @Time : 2020/8/26 下午1:42
# @Author: kkkkibj@163.com
# @File : deal_huizhou_oftenjam_data.py
# 处理惠州常发拥堵点数据
import csv
import json

months = ['201907', '201908', '201909', '201910', '201911', '201912', '202001', '202002', '202003', '202004', '202005',
          '202006', '202007']

result = {'zxq': {}, 'highway': {}}
basedir = '/Users/hongyanma/Downloads/'
prefix = 'JamRoutinueIndex'
postfix = '.csv'
for i in range(13):
    filename = basedir + prefix + months[i] + postfix
    if months[i] not in result['zxq']:
        result['zxq'][months[i]] = []
    if months[i] not in result['highway']:
        result['highway'][months[i]] = []
    # print(months[i])
    with open(filename, 'r', encoding='gbk') as f:
        reader = csv.reader(f)
        # column = [row[0] for row in reader]
        # print(column)
        # if len(column) < 60:
        #     print(months[i])
        for row in reader:
            # print(row)
            if row[-1] == '中心区':
                result['zxq'][months[i]].append([row[1],row[2]])
            if row[-1] == '高速':
                result['highway'][months[i]].append([row[1], row[2]])
print(result)

with open(basedir+'ofenjam30.json','w') as of:
    json.dump(result,of)
