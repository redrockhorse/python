# -*- coding:utf-8 -*-
#@Time : 2020/1/21 上午9:39
#@Author: kkkkibj@163.com
#@File : springpredata.py


with open('/Users/hongyanma/Desktop/springpre2019.txt','r') as f:
    datearr = []
    valuearr = []
    line = f.readline()
    while line:
        #print(line)
        darr = line.split(',')
        # print(darr[0])
        datestr = darr[0]
        mdarr = datestr.split('/')
        # if int(mdarr[2]) < 10:
        #     md = mdarr[1]+'月0'+mdarr[2]+'日'
        # else:
        #     md = mdarr[1] + '月' + mdarr[2] + '日'
        md = mdarr[1] + '月' + mdarr[2] + '日'
        valuearr.append(float(darr[1]))
        # print(md)
        datearr.append(md)
        line = f.readline()
    print(datearr)
    print(valuearr)
