# -*- coding: utf8 -*-
# !/usr/bin/python
# 根据周几进行分析

import pymysql
import sys
import datetime
import numpy as np
import decimal
from collections import Counter

conn=pymysql.connect(host='127.0.0.1',user='root',passwd='Qd@#$mo658',db='jc',port=3306,charset='utf8', cursorclass = pymysql.cursors.DictCursor)
cursor = conn.cursor()

from collections import Counter
def counter(arr):
    return Counter(arr).most_common(3)

sql="select * from td_ptl_lt_data order by pdate asc"#td_ptl_ssq_data,td_ptl_lt_data
cursor.execute(sql)
v1_result = cursor.fetchall()
dic ={}
v1=[]
v2=[]
v3=[]
v4=[]
v5=[]
v6=[]
v7=[]
for row in v1_result:
    print(row)
    v1.append(row['v1'])
    v2.append(row['v2'])
    v3.append(row['v3'])
    v4.append(row['v4'])
    v5.append(row['v5'])
    v6.append(row['v6'])
    v7.append(row['v7'])

l=len(v1)
import collections
v1d=collections.OrderedDict()
v2d=collections.OrderedDict()
v3d=collections.OrderedDict()
v4d=collections.OrderedDict()
v5d=collections.OrderedDict()
v6d=collections.OrderedDict()
v7d=collections.OrderedDict()

n=200
i=1
#print(Counter(v1).most_common())
for v in Counter(v1).most_common():
    v1d[v[0]]=v[1]/l*1.00
for v in Counter(v2).most_common():
    v2d[v[0]]=v[1]/l*1.00
for v in Counter(v3).most_common():
    v3d[v[0]]=v[1]/l*1.00
for v in Counter(v4).most_common():
    v4d[v[0]]=v[1]/l*1.00
for v in Counter(v5).most_common():
    v5d[v[0]]=v[1]/l*1.00
for v in Counter(v6).most_common():
    v6d[v[0]]=v[1]/l*1.00
for v in Counter(v7).most_common():
    v7d[v[0]]=v[1]/l*1.00
#print(v1d['01'])


v1p=[]
v2p=[]
v3p=[]
v4p=[]
v5p=[]
v6p=[]
v7p=[]
i=0
while i<l:
    v1p.append(v1.count(v1[i]) / l * 1.00)
    v2p.append(v2.count(v2[i]) / l * 1.00)
    v3p.append(v3.count(v3[i]) / l * 1.00)
    v4p.append(v4.count(v4[i]) / l * 1.00)
    v5p.append(v5.count(v5[i]) / l * 1.00)
    v6p.append(v6.count(v6[i]) / l * 1.00)
    v7p.append(v7.count(v7[i]) / l * 1.00)
    i += 1
import numpy as np
a = np.array(v2p)
print(a.max())
print(a.min())
print(a.mean())
print(a.std())
print('-----------------')
print(len(v1p))
print('-----------------')
v1t=v1p[l-n:l]
v2t=v2p[l-n:l]
v3t=v3p[l-n:l]
v4t=v4p[l-n:l]
v5t=v5p[l-n:l]
v6t=v6p[l-n:l]
v7t=v7p[l-n:l]
tarr =[]
tatt =[]
for t in range(n):
    tarr.append([v1t[t] / np.array(v1p).mean(),v2t[t] / np.array(v2p).mean(),v3t[t] / np.array(v3p).mean(),v4t[t] / np.array(v4p).mean(),v5t[t] / np.array(v5p).mean(),v6t[t] / np.array(v6p).mean(),v7t[t] / np.array(v7p).mean()])
    '''
    print('----------------------------')
    print(v1t[t] / np.array(v1p).mean())
    print(v2t[t] / np.array(v2p).mean())
    print(v3t[t] / np.array(v3p).mean())
    print(v4t[t] / np.array(v4p).mean())
    print(v5t[t] / np.array(v5p).mean())
    print(v6t[t] / np.array(v6p).mean())
    print(v7t[t] / np.array(v7p).mean())
    print('----------------------------')
    '''
    tatt.append('%.2f' % (v7t[t] / np.array(v7p).mean()))
print('****************************')
print(tarr)
print(Counter(tatt).most_common(3))
print(np.array(v1p).mean(),np.array(v2p).mean(),np.array(v3p).mean(),np.array(v4p).mean(),np.array(v5p).mean(),np.array(v6p).mean(),np.array(v7p).mean())
#print(np.array(v1p).mean()*1.46,np.array(v2p).mean()*1.29,np.array(v3p).mean()*0.82,np.array(v4p).mean()*1.69,np.array(v5p).mean()*1.37,np.array(v6p).mean()*1.38,np.array(v7p).mean()*1.28)
#print(v1d)#03
#print(v2d)#07
#print(v3d)#12,26
#print(v4d)#29
#print(v5d)#34
#print(v6d)#01
#print(v7d)#10,11
print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
print(v1d)#03
print(v2d)#07
print(v3d)#12,26
print(v4d)#29
print(v5d)#34
print(v6d)#01
print(v7d)#10,11
print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')

v1m=np.array(v1p).mean()
v2m=np.array(v2p).mean()
v3m=np.array(v3p).mean()
v4m=np.array(v4p).mean()
v5m=np.array(v5p).mean()
v6m=np.array(v6p).mean()
v7m=np.array(v7p).mean()

tmpc =[]
for c in range(l):
    s=''
    if v1p[c]>v1m:
        s+='1'
    else:
        s+='0'
    if v2p[c]>v2m:
        s+='1'
    else:
        s+='0'

    if v3p[c]>v3m:
        s+='1'
    else:
        s+='0'
    if v4p[c]>v4m:
        s+='1'
    else:
        s+='0'
    if v5p[c]>v5m:
        s+='1'
    else:
        s+='0'
    if v6p[c]>v6m:
        s+='1'
    else:
        s+='0'
    if v7p[c] > v7m:
        s += '1'
    else:
        s += '0'
    tmpc.append(s)
#print(tmpc)

print(Counter(tmpc).most_common(10))

tmpc =[]
for c in range(l):
    s=''
    if v1p[c]/v1m>1.2:
        s+='1'
    elif v1p[c]/v1m<0.5:
        s+='0'
    else:
        s+='x'

    if v2p[c]/v2m>1.2:
        s+='1'
    elif v2p[c]/v2m<0.5:
        s+='0'
    else:
        s+='x'

    if v3p[c]/v3m>1.2:
        s+='1'
    elif v3p[c]/v3m<0.5:
        s+='0'
    else:
        s+='x'

    if v4p[c]/v4m>1.2:
        s+='1'
    elif v4p[c]/v4m<0.5:
        s+='0'
    else:
        s+='x'


    if v5p[c]/v5m>1.2:
        s+='1'
    elif v5p[c]/v5m<0.5:
        s+='0'
    else:
        s+='x'

    if v6p[c]/v6m>1.2:
        s+='1'
    elif v6p[c]/v6m<0.5:
        s+='0'
    else:
        s+='x'

    if v7p[c]/v7m>1.2:
        s+='1'
    elif v7p[c]/v7m<0.5:
        s+='0'
    else:
        s+='x'
    tmpc.append(s)
#print(tmpc)

print(Counter(tmpc).most_common(10))

'''
for t in range(n-1):
    #print(t)
    #print(v1p[t])
    if t>0:
        print(str(v1p[t]-v1p[t-1])+','+str(v1p[t+1]-v1p[t]))

print('======================')

print(v1d['14'])
print(v1d['04'])
'''

print(tarr[len(tarr)-3:len(tarr)])


