#!/usr/bin/python
#encoding=utf-8
#lbp feature extraction
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
    tmparr = np.zeros(33,dtype=np.int)
    tmparr[int(row['v1'])-1] = 1
    tmparr[int(row['v2'])-1] = 1
    tmparr[int(row['v3'])-1] = 1
    tmparr[int(row['v4'])-1] = 1
    tmparr[int(row['v5'])-1] = 1
    tmparr[int(row['v6'])-1] = 1
    rs = np.append(rs,tmparr)
shape = rs.reshape(-1,33).shape
matrix = rs.reshape(-1,33)

def origin_LBP(matrix):
    h,w = matrix.shape
    dst = np.zeros(matrix.shape, dtype=matrix.dtype)
    print(h)
    print(w)
    for i in range(1, h - 1):
        for j in range(1, w - 1):
            code = 0
            code |= (matrix[i - 1][j - 1] > 0) << (np.uint8)(7)
            code |= (matrix[i - 1][j] > 0) << (np.uint8)(6)
            code |= (matrix[i - 1][j + 1] > 0) << (np.uint8)(5)
            code |= (matrix[i][j + 1] > 0) << (np.uint8)(4)
            code |= (matrix[i + 1][j + 1] > 0) << (np.uint8)(3)
            code |= (matrix[i + 1][j] > 0) << (np.uint8)(2)
            code |= (matrix[i + 1][j - 1] > 0) << (np.uint8)(1)
            code |= (matrix[i][j - 1] > 0) << (np.uint8)(0)
            dst[i - 1][j - 1] = code
    return dst

from collections import Counter
if __name__ == '__main__':
    lbpMatrix = origin_LBP(matrix)
    print(lbpMatrix.shape)
    print(lbpMatrix[2404])
    preResult = []
    for i in range(lbpMatrix.shape[1] - 2):
        print('---------------------------')
        print(i + 2)
        print(Counter(lbpMatrix[:, i]).most_common(2))
        binstr = bin(int(Counter(lbpMatrix[:, i]).most_common(2)[1][0])).replace('0b', '')
        for l in range(8 - len(binstr)):
            binstr = '0' + binstr
        print(binstr)
        if binstr[4:5] == '1':
            print(i + 3)
            preResult.append(i + 3)
        if binstr[5:6] == '1':
            print(i + 2)
            preResult.append(i + 2)
        if binstr[6:7] == '1':
            print(i + 1)
            preResult.append(i + 1)
        print(binstr[4:5])
        print(binstr[5:6])
        print(binstr[6:7])
        print('---------------------------')
    print(preResult)
