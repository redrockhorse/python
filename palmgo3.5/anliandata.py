# -*- coding: utf8 -*-
#encoding=utf-8
#By @mahy
#email:kkkkbj@163.com
#安联数据处理
import xlrd
import json
workbook = xlrd.open_workbook(r'E:\desktop\data_anlian.xlsx')
print(workbook.sheet_names()) # [u'sheet1', u'sheet2']
sheet1=workbook.sheet_by_index(0)
rownum=sheet1.nrows
cols = sheet1.col_values(2)
rs={}
rs['data']={}
for r in range(rownum):
    tcell = sheet1.cell(r,2).value
    loncell = sheet1.cell(r,5).value
    latcell =sheet1.cell(r,6).value
    timestr=xlrd.xldate_as_tuple(tcell,workbook.datemode)[3]
    if timestr not in rs['data']:
        rs['data'][timestr]=[]
    rs['data'][timestr].append([loncell,latcell,1])
    #print(timestr[3])
fileout = open('E:\desktop\data_anlian.json','w')
json.dump(rs,fileout)