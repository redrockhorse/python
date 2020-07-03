# -*- coding:utf-8 -*-
# @Time : 2020/5/29 下午1:22
# @Author: kkkkibj@163.com
# @File : test_kelly.py

win = 4.6
draw = 3.9
lost = 1.49

gmwin = 4 / 11
gmdraw = 1 / 11
gmlost = 6 / 11

klwin = (win * gmwin - (1 - gmwin)) / win
kldraw = (draw * gmdraw - (1 - gmdraw)) / draw
kllost = (lost * gmlost - (1 - gmlost)) / lost
print(klwin,kldraw,kllost)
