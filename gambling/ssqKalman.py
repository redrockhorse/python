#!/usr/bin/python
#encoding=utf-8
#kalman
__author__ = 'mahy'

import pymysql
import numpy as np
from PIL import Image
import matplotlib.pyplot as pyplot
conn=pymysql.connect(host='127.0.0.1',user='root',passwd='Qd@#$mo658',db='jc',port=3306,charset='utf8', cursorclass = pymysql.cursors.DictCursor)
cursor = conn.cursor()

sql="select *  from jc.td_ptl_ssq_data   order by pdate asc"
cursor.execute(sql)
result = cursor.fetchall()

rs = []
for row in result:
    print(row)
    tmparr = np.zeros(40,dtype=np.int)
    tmparr[int(row['v1'])-1] = 1
    tmparr[int(row['v2'])-1] = 1
    tmparr[int(row['v3'])-1] = 1
    tmparr[int(row['v4'])-1] = 1
    tmparr[int(row['v5'])-1] = 1
    tmparr[int(row['v6'])-1] = 1
    rs = np.append(rs,tmparr)
shape = rs.reshape(-1,40).shape
matrix = rs.reshape(-1,40)
print(matrix[2410])
def origin_LBP(matrix):
    h,w = matrix.shape
    #dst = np.zeros(matrix.shape, dtype=matrix.dtype)
    dst = []
    print(h)
    print(w)
    for i in range(0, h - 1):
        code = 0
        for j in range(0, w - 1):
            #code |= (matrix[i][j] > 0) << (np.uint32)(31)
            if matrix[i][j]>0:
                print(i)
                print(j)
                code = code +  np.power(2,j)
        dst.append(code)
    return dst
from collections import Counter
if __name__ == '__main__':
    lbpMatrix = origin_LBP(matrix)
    print(lbpMatrix)
    print(np.mean(lbpMatrix))
    print(np.median(lbpMatrix))
    print(Counter(lbpMatrix).most_common(10))
    print(bin(Counter(lbpMatrix).most_common(10)[0][0]))
    #print(lbpMatrix.shape)
    #print(np.power(2,35))