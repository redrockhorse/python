# -*- coding: utf8 -*-
# !/usr/bin/python
# 抓取北京交通事件.python 版本2.5
__author__ = 'mahy'

import requests

data = 20180213
def getData(dateStr):
    url = 'http://hmrc.palmgo.cn/visual-offline/operIndex/kindHeap.do?kind=citycode&daystr='+dateStr+'&_=1521104024551'
    sess = requests.Session()
    res = sess.get(url)
    print(res)
import sys
print(sys.path)
getData('20180213')


