#!/usr/bin/python
# encoding=utf-8
# 历史事件转换为json
import json
import xlrd
from collections import Counter

__author__ = 'kkkkibj@163.com'
# event_inter_his.xlsx
# infile = '/Users/hongyanma/Downloads/event_history.txt'
# excelFile = '/Users/hongyanma/Downloads/event_inter_his.xlsx'  # 原始数据文件，要保存为utf-8编码
excelFile = '/Users/hongyanma/Downloads/his_event_inter.xlsx'  # 原始数据文件，要保存为utf-8编码
outfile = '/Users/hongyanma/Downloads/event_history.json'
outfile_types = '/Users/hongyanma/Downloads/event_types_history.json'

with open(outfile, 'w') as outputFile, open(outfile_types, 'w') as outFileTypes:
    data = xlrd.open_workbook(excelFile)
    table = data.sheet_by_index(0)
    result = {}
    result_arr = []
    row = 0
    event_types = []
    result_types = {}
    for rowNum in range(table.nrows):
        row = rowNum
        if rowNum > 0:
            rowVale = table.row_values(rowNum)
            event_types.append(int(rowVale[14]))
            type_key = int(rowVale[14])
            coord = [float(rowVale[8].split(';')[1].split(',')[0]), float(rowVale[8].split(';')[1].split(',')[1])]
            obj = {"coord": coord, "elevation": int(rowVale[20])}
            result_arr.append(obj)
            if type_key not in result_types:
                result_types[type_key] = []
            result_types[type_key].append(obj)

    print("---------------")
    result["data"] = [result_arr]
    print(result)
    orderDic = Counter(event_types).most_common()
    print(orderDic)
    json.dump(result,outputFile)
    result["data"] = result_types
    json.dump(result, outFileTypes)
    print('共' + str(row) + '行', '执行完毕')
