# -*- coding: utf8 -*-
#encoding=utf-8
#By @mahy
#email:kkkkbj@163.com
#安联数据处理

import json
import math
def gps_coord_02tobd(gps_cx_02, gps_cy_02):
    x_pi = 3.14159265358979324 * 3000.0 / 180.0
    z = math.sqrt(gps_cx_02 * gps_cx_02 + gps_cy_02 * gps_cy_02) + 0.00002 * math.sin(gps_cy_02 * x_pi)
    theta = math.atan2(gps_cy_02, gps_cx_02) + 0.000003 * math.cos(gps_cx_02 * x_pi)
    gps_cx_bd = z * math.cos(theta) + 0.0065
    gps_cy_bd = z * math.sin(theta) + 0.006
    return (gps_cx_bd, gps_cy_bd)

result={}
result['data']=[]
with open('/Users/hongyanma/Desktop/awpdata/data.txt','r') as inputfile:
    i=0
    for line in inputfile:
        if i==0:
            pass
        else:
            arr=line.replace('\n','').split(',')
            coords = gps_coord_02tobd(float(arr[4]), float(arr[5]))
            #result['data'].append([arr[4],arr[5]])
            result['data'].append(['%.6f' % coords[0], '%.6f' % coords[1]])
        i+=1

with open('/Users/hongyanma/Desktop/awpdata/awp_2017_gps.json','w') as outputfile:
    json.dump(result,outputfile)


