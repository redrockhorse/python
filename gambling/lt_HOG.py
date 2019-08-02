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

sql="select *  from jc.td_ptl_lt_data   order by pdate asc"
cursor.execute(sql)
result = cursor.fetchall()

import cmath
def getItemValue(matrix,x,y):
    return matrix[y][x]

def dX(matrix,x,y):
    return getItemValue(matrix,x+1,y) - getItemValue(matrix,x,y)

def dY(matrix,x,y):
    return getItemValue(matrix,x,y+1) - getItemValue(matrix,x,y)

def delta(matrix,x,y):
    return cmath.sqrt(dX(matrix,x,y)**2+dY(matrix,x,y)**2)

def theta(matrix,x,y):
    cmath.atan()

rs = []
for row in result:
    print(row)
    tmparr = np.zeros(35,dtype=np.int)
    tmparr[int(row['v1'])-1] = 1
    tmparr[int(row['v2'])-1] = 1
    tmparr[int(row['v3'])-1] = 1
    tmparr[int(row['v4'])-1] = 1
    tmparr[int(row['v5'])-1] = 1
    #tmparr[int(row['v6'])-1] = 1
    rs = np.append(rs,tmparr)
shape = rs.reshape(-1,35).shape
matrix = rs.reshape(-1,35)

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

def seedFilling(matrix):
    h, w = matrix.shape
    newim = Image.new("RGB", (w, h), (255, 0, 0))
    for i in range(h):
        for j in range(w):
            if matrix[i][j] == 1:
                newim.putpixel((j, i), (255, 0, 0))
            else:
                newim.putpixel((j, i), (255, 255, 255))
    newim.show()
    newim.save("save.png", "png")


# def createTestPng(matrix):
#     h, w = matrix.shape
#     newim = Image.new("RGBA", (w, h), (255, 0, 0, 0))
#     for i in range(h):
#         for j in range(w):
#             op = 0
#             if j%5 == 0:
#                 op = 255
#             newim.putpixel((j, i), (255, 0, 0, op))
#     newim.show()
#     newim.save("src.png", "png")

def createTestPng(matrix):
    h, w = matrix.shape
    newim = Image.new("RGB", (w, h), (255, 0, 0))
    for i in range(h):
        for j in range(w):
            if j%5 == 0:
                newim.putpixel((j, i), (255, 0, 0))
            else:
                newim.putpixel((j, i), (255, 255, 255))
    newim.show()
    newim.save("src.png", "png")

from collections import Counter

import PIL.Image as Image

if __name__ == '__main__':
    #lbpMatrix = origin_LBP(matrix)
    seedFilling(matrix)
    #createTestPng(matrix)