# -*- coding: utf8 -*-
__author__ = 'mahongyan'
import os
import re
def isfloat(float_number):
    value = re.compile(r'^[-+]?[0-9]+\.[0-9]+$')
    result = value.match(float_number)
    return  result

def raster(distance,infile,outfile):
    gpsfile = open(infile,'r')
    jsonfile = open(outfile,'w')
    x0=int(73.48625*1000000)
    y0=int(18.083528*1000000)
    xm=int((int(135.301167*1000000)-x0)/distance)
    ym=int((int(53.685851*1000000)-y0)/distance)
    dic ={}
    jsonstr ='{"data":['

    for line in gpsfile:
        gps = line.split(",")
        if len(gps)>1 and isfloat(gps[0]) and isfloat(gps[1]):
            x=int((float(gps[0])*1000000-x0)/distance)
            y=int((float(gps[1])*1000000-y0)/distance)
            if x<xm and y<ym:
                if str(x)+"_"+str(y) in dic:
                    dic[str(x)+"_"+str(y)]+=1
                    #print str(x)+"_"+str(y)
                    #print dic[str(x)+"_"+str(y)]
                else:
                    dic[str(x)+"_"+str(y)]=1
        else:
            print(gps[0],gps[1])
    for gpsstr in dic:
        if dic[gpsstr] > 4:
            arr=gpsstr.split("_")
            lon=(int(arr[0])*distance+distance*0.5+x0)/1000000
            lat=(int(arr[1])*distance+distance*0.5+y0)/1000000
            if lon>73.48625 and lat>18.083528:
                arrstr ="["+str(lon)+","+str(lat)+","+str(dic[gpsstr])+"],"
                jsonstr=jsonstr+arrstr
    jsonstr=jsonstr+"]}"
    jsonfile.write(jsonstr)
    jsonfile.close()
    gpsfile.close()
if __name__ == '__main__':
    distance=int(0.00027*1000000)
    #infile="E:\\ctfo\\ctfodayfile\\201706\\gps\\UGC.txt"
    #outfile="E:\\ctfo\\ctfodayfile\\201706\\gps\\UGC.json"
    #raster(distance,infile,outfile)
    rootdir = 'E:\\ctfo\\ctfodayfile\\201706\\'
    files = os.listdir(rootdir)
    for f in files:
        infile=rootdir+"\\"+f
        outfile=rootdir+"\\res\\"+f
        raster(distance,infile,outfile)








