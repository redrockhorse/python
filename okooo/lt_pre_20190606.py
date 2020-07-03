#!/usr/bin/python
#encoding=utf-8
__author__ = 'mahy'

import pymysql
import numpy as np
from PIL import Image
import matplotlib.pyplot as pyplot
conn=pymysql.connect(host='127.0.0.1',user='root',passwd='Qd@#$mo658',db='jc',port=3306,charset='utf8', cursorclass = pymysql.cursors.DictCursor)
cursor = conn.cursor()

sql="select *  from jc.td_ptl_lt_data   order by pdate asc"
cursor.execute(sql)
result = cursor.fetchall()

def drawImg(sq,arr):
    newim = Image.new("RGBA", (sp[1], sp[0]), (255, 0, 0, 0))
    for y in range(sp[0]):
        for x in range(sp[1]):
            op = 0
            if arr[y][x] == 0:
                op = 125
            newim.putpixel((x, y), (255, 0, 0, op))
    newim.show()

rs = []
for row in result:
    print(row)
    tmparr = np.zeros(35,dtype=np.int)
    tmparr[int(row['v1'])-1] = 1
    tmparr[int(row['v2'])-1] = 1
    tmparr[int(row['v3'])-1] = 1
    tmparr[int(row['v4'])-1] = 1
    tmparr[int(row['v5'])-1] = 1
    rs = np.append(rs,tmparr)
sp = rs.reshape(-1,35).shape
arr = rs.reshape(-1,35)
print(sp)
'''
newim = Image.new("RGBA", (sp[1] , sp[0]), (255, 0, 0, 0))
for y in range(sp[0]):
    for x in range(sp[1]):
        op = 0
        if arr[y][x] == 0:
            op = 125
        newim.putpixel((x, y), (255, 0, 0, op))
newim.show()
'''

ziprs =[]
for y in range(sp[0]):
    line = []
    for i in range(7):#
        t =0
        for j in range(5):
            t += arr[y][5*i+j]
        line.append(t)
    ziprs = np.append(ziprs, line)
#print(ziprs.reshape(-1,11).shape)
zsp = ziprs.reshape(-1,7).shape
zarr = ziprs.reshape(-1,7)
newim = Image.new("RGBA", (zsp[1] , zsp[0]), (255, 0, 0, 0))


'''
for y in range(zsp[0]):
    for x in range(zsp[1]):
        op = 0
        if zarr[y][x] == 3:
            op = 255
        if zarr[y][x] == 2:
            op = 175
        if zarr[y][x] == 1:
            op = 75
        newim.putpixel((x, y), (255, 0, 0, op))
newim.show()
'''

zzrs =[]
for i in range(607):
    line = []
    for x in range(zsp[1]):
        t = 0
        for j in range(3):
            t+=zarr[i*3+j][x]
        line.append(t)
    #print(line)
    zzrs = np.append(zzrs, line)
zsp = zzrs.reshape(-1,7).shape
zzarr = zzrs.reshape(-1,7)
#print(zsp)

alDic = {}
n =6
for i in range(607):
    if i>3:
        key = str(zzarr[i-3][n])+'_'+str(zzarr[i-2][n])+'_'+str(zzarr[i-1][n])
        if key not in alDic:
            alDic[key] =[]
        alDic[key].append(zzarr[i][n])
#print(alDic)
#print(alDic[str(zzarr[607-3][n])+'_'+str(zzarr[607-2][n])+'_'+str(zzarr[607-1][n])])
from collections import Counter
print(Counter(alDic[str(zzarr[607-3][n])+'_'+str(zzarr[607-2][n])+'_'+str(zzarr[607-1][n])]).most_common())
#2,3,1,2,2,3,3
#6-10,31-35,26-30 多
#11-15，少

'''
for y in range(zsp[0]):
    for x in range(zsp[1]):
        op = int(255*zzarr[y][x]/6)
        newim.putpixel((x, y), (255, 0, 0, op))
newim.show()
'''