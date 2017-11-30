# -*- coding: utf8 -*-
#encoding=utf-8
__author__ = 'mahy'

import csv

#csvfile = open('e:\\ctfo\\20170720_2204.csv','rb')
with open('e:\\ctfo\\20170720_2204_3.csv',encoding='utf-8') as csvfile:
#with open('e:\\ctfo\\testcode.csv') as csvfile:
    csv_reader = csv.reader(csvfile)
    #rows = [row for row in csv_reader]
    #for row in csv_reader:
    for i,rows in enumerate(csv_reader):
        print(i)
        print(rows)
        if i>50:
            exit(-1)
