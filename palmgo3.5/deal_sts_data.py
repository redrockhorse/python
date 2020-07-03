# -*- coding:utf-8 -*-
# @Time : 2020/7/2 下午7:00
# @Author: kkkkibj@163.com
# @File : deal_sts_data.py
# 处理中科院空气污染数据
import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root', passwd='123456', db='datacapture', port=3786, charset='utf8',
                       cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()

area_arr = ['bj', 'hb', 'tj']
date_arr = ['20180415', '20180416', '20180417', '20180418', '20180419']
type_arr = ['Emission_CO', 'Emission_NOX', 'Emission_PM', 'Emission_SO2', 'Emission_VOC']
data_dir = '/Users/hongyanma/Downloads/sts_result'
# td_ptl_air_pollution
for area in area_arr:
    for type in type_arr:
        for datestr in date_arr:
            for i in range(1, 256):
                filepath = data_dir + '/' + area + '/' + type + '/' + 'Track_FCD_' + datestr
                tr = str(i)
                while len(tr) < 3:
                    tr = '0' + tr
                # print(tr)
                filepath = filepath + '/' + 'FCD_' + datestr + '_' + tr + '.txt'
                with open(filepath, 'r') as f:
                    linestr = f.readline()
                    while linestr:
                        linestr = f.readline()
                        print(area + ',' + type + ',' + datestr + ',' + tr + ',' + linestr.replace('\n', ''))
                        if len(linestr.replace('\n', '').split(',')) > 1:
                            linkid = linestr.replace('\n', '').split(',')[0]
                            val = linestr.replace('\n', '').split(',')[1]
                            insert_sql = "INSERT INTO `datacapture`.`td_ptl_air_pollution` (`area`,`ptype`,`datestr`,`timeid`,`linkid`,`val`) VALUES (%s,%s, %s,%s,%s,%s);"
                            cursor.execute(insert_sql, (area, type, datestr, tr, linkid, val))
                        else:
                            print(linestr)
                conn.commit()
