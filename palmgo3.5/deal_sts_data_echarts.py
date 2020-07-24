# -*- coding:utf-8 -*-
# @Time : 2020/7/2 下午7:00
# @Author: kkkkibj@163.com
# @File : deal_sts_data.py
# 处理中科院空气污染数据
import json

area_arr = ['bj', 'hb', 'tj']
date_arr = ['20180415', '20180416', '20180417', '20180418', '20180419']
type_arr = ['Emission_CO', 'Emission_NOX', 'Emission_PM', 'Emission_SO2', 'Emission_VOC']
data_dir = '/Users/hongyanma/Downloads/sts_result'
# td_ptl_air_pollution










if __name__ == '__main__':
    gbdic = {}
    with open('/Users/hongyanma/Desktop/gb.csv','r') as infile:
        line = infile.readline()
        while line:
            line = infile.readline()
            if line:
                line = line.replace('\n','')
                # print(line)
                dataarr = line.split(',')
                datestr = dataarr[0].split('_')[0]
                timeid = dataarr[0].split('_')[1]
                if datestr not in gbdic:
                    gbdic[datestr] = {}
                gbdic[datestr][timeid] = dataarr[1:]
    print(gbdic)

    typesdic = {}
    with open('/Users/hongyanma/Desktop/types.csv','r') as infile:
        line = infile.readline()
        while line:
            line = infile.readline()
            if line:
                line = line.replace('\n','')
                # print(line)
                dataarr = line.split(',')
                datestr = dataarr[0].split('_')[0]
                timeid = dataarr[0].split('_')[1]
                typestr = dataarr[1].split('_')[1]
                if datestr not in typesdic:
                    typesdic[datestr] = {}
                if typestr not in typesdic[datestr]:
                    typesdic[datestr][typestr] = []
                typesdic[datestr][typestr].append(dataarr[2])
    print(typesdic)

    dwdic = {}
    with open('/Users/hongyanma/Desktop/dw.csv','r') as infile:
        line = infile.readline()
        while line:
            line = infile.readline()
            if line:
                line = line.replace('\n','')
                # print(line)
                dataarr = line.split(',')
                datestr = dataarr[0].split('_')[0]
                timeid = dataarr[0].split('_')[1]
                if datestr not in dwdic:
                    dwdic[datestr] = {}
                dwdic[datestr][timeid] = dataarr[1:]
    print(dwdic)

    with open('/Users/hongyanma/Desktop/gb.json','w') as outfile:
        json.dump(gbdic,outfile)
    with open('/Users/hongyanma/Desktop/dw.json','w') as outfile:
        json.dump(dwdic,outfile)
    with open('/Users/hongyanma/Desktop/types.json','w') as outfile:
        json.dump(typesdic,outfile)