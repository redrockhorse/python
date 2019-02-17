# -*- coding: utf8 -*-
#!/bin/python
__author__ = 'mahy'
'''
路网热力图过滤山东部分
'''
import  json
import math
def gps_coord_02tobd(coord):
    gps_cx_02 = float(coord[0])
    gps_cy_02 = float(coord[1])
    x_pi = 3.14159265358979324 * 3000.0 / 180.0
    z = math.sqrt(gps_cx_02 * gps_cx_02 + gps_cy_02 * gps_cy_02) + 0.00002 * math.sin(gps_cy_02 * x_pi)
    theta = math.atan2(gps_cy_02, gps_cx_02) + 0.000003 * math.cos(gps_cx_02 * x_pi)
    gps_cx_bd = z * math.cos(theta) + 0.0065
    gps_cy_bd = z * math.sin(theta) + 0.006
    return ["%.6f" % gps_cx_bd, "%.6f" % gps_cy_bd]
resdata ={}
resdata['data']=[]
inputObj ={}
with open("/Users/hongyanma/Desktop/goodsLinkHotMap.json",'r') as inputfile:
    inputObj=json.load(inputfile)
print(inputObj)
nw = [114.764152, 34.323916];
se = [122.711785, 38.283489];
data= inputObj['data']
for v in data:
    x=v['pline'][0][0]
    y=v['pline'][0][1]
    if x > nw[0] and x < se[0] and y > nw[1] and y < se[1]:
        resdata['data'].append(v)

with open("/Users/hongyanma/Desktop/result/shandonglinkhp.json", 'w') as outputfile:
    json.dump(resdata, outputfile, ensure_ascii=False)
'''
for datastr in ['20171015','20171016','20171017','20171018','20171019','20171020','20171021','20171022']:
    with open("/Users/hongyanma/Desktop/result/"+datastr+".txt",'r') as inputfile:
        #i=0
        for line in inputfile:
            #print(line)
            #print(i)
            #i+=1
            arr = line.split(';')
            value=arr[1]
            roadcode=arr[2]
            roadname=arr[3]
            roadlinkstr = arr[4]
            #print(list(map(lambda x:x.split(','),roadlinkstr.replace('\n','').split("|"))))
            roadlinkarr=list(map(lambda x:gps_coord_02tobd(x.split(',')),roadlinkstr.replace('\n','').split("|")))
            resdata['data'].append({
                'roadcode':roadcode,
                'roadname': roadname,
                'count':value,
                'link':roadlinkarr
            })
        print(resdata)
    with open("/Users/hongyanma/Desktop/result/"+datastr+".json",'w') as outputfile:
        json.dump(resdata,outputfile,ensure_ascii=False)
'''
