# -*- coding: utf-8 -*-
#encoding=utf-8
__author__ = 'mahy'
#天气影响路链 weather influence road links
#from xml.dom.minidom import parse
import xml.dom.minidom
#import numpy as np
import re
import time


weatherregionflie="./data/weatherregion/2017070815_prec.kml"
#E:\ctfo\tensorflow\palm\data\weatherregion\2017070815_prec.kml
midfile="./data/link/map_link.MID"
miffile="./data/link/map_link.MIF"
region_mif = "./data/test/reg_2017070815_prec.mif"
region_mid = "./data/test/reg_2017070815_prec.mid"
wl_mif = "./data/test/2017070815_prec.mif"
wl_mid = "./data/test/2017070815_prec.mid"
'''
def createRegionFileByWeatherFile(f):
    region_mif_file = open(region_mif,'w')
    region_mid_file = open(region_mid,'w')
    DOMTree = xml.dom.minidom.parse(f)
    collection = DOMTree.documentElement
    placemarks = collection.getElementsByTagName("Placemark")
    region_mif_header = 'Version 450'+'\n'+'Charset "WindowsSimpChinese"'+'\n'+'Delimiter ","'+'\n'+'CoordSys Earth Projection 1, 0'\
    +'\n'+'Columns 6'+'\n'+'  ID Integer'+'\n'+'  NAME Char(50)'+'\n'+'  CLASS Integer'+'\n'+'  other Integer'+'\n'+'  ns Integer'+'\n'+'  ne Integer'\
    +'\n'+'Data'+'\n'
    i=0
    mifline=''
    midline=''
    for pm in placemarks:
        i=i+1
        rname = pm.getElementsByTagName("name")[0]
        visibility=rname.childNodes[0].data.split(' to ')
        print(visibility[0]+'-'+visibility[1])
        region=pm.getElementsByTagName("coordinates")[0]
        path=region.childNodes[0].data
        pointnum=path.count(",0 ")
        path=path.replace('\n','')
        path=path.replace(',0 ','\n')
        path=path.replace(' ','')
        path=path.replace(',',' ')
        #startpoint = path.split('\n')[0]+'\n'#mapInfo中的Region起点须与终点相同
        path='Region 1\n'+str(pointnum)+'\n'+path+'\n'#+startpoint+
        mifline=mifline+path
        print(path)
        #print(pointnum)
        midline=midline+'\n'+str(i)+',"'+rname.childNodes[0].data+'",'+str(i)+',0,'+visibility[0]+','+visibility[1]
    region_mid_file.write(midline)
    region_mid_file.close()
    mifline=region_mif_header+mifline
    region_mif_file.write(mifline)
    region_mif_file.close()
'''
def createRegionFileByWeatherFile_1(f):
    region_mif_file = open(region_mif,'w')
    region_mid_file = open(region_mid,'w')
    DOMTree = xml.dom.minidom.parse(f)
    collection = DOMTree.documentElement
    placemarks = collection.getElementsByTagName("Placemark")
    region_mif_header = 'Version 450'+'\n'+'Charset "WindowsSimpChinese"'+'\n'+'Delimiter ","'+'\n'+'CoordSys Earth Projection 1, 0'\
    +'\n'+'Columns 6'+'\n'+'  ID Integer'+'\n'+'  NAME Char(50)'+'\n'+'  CLASS Integer'+'\n'+'  other Integer'+'\n'+'  ns Integer'+'\n'+'  ne Integer'\
    +'\n'+'Data'+'\n'
    i=0
    mifline=''
    midline=''
    for pm in placemarks:
        rname = pm.getElementsByTagName("name")[0]
        visibility=rname.childNodes[0].data.split(' to ')
        print(visibility[0]+'-'+visibility[1])
        if visibility[0] != '-100' or visibility[1]!='20':
            i=i+1
            region=pm.getElementsByTagName("coordinates")[0]
            path=region.childNodes[0].data
            pointnum=path.count(",0 ")
            path=path.replace('\n','')
            path=path.replace(',0 ','\n')
            path=path.replace(' ','')
            path=path.replace(',',' ')
            #startpoint = path.split('\n')[0]+'\n'#mapInfo中的Region起点须与终点相同
            path='Region 1\n'+str(pointnum)+'\n'+path+'\n'#+startpoint+
            mifline=mifline+path
            print(path)
            #print(pointnum)
            midline=midline+'\n'+str(i)+',"'+rname.childNodes[0].data+'",'+str(i)+',0,'+visibility[0]+','+visibility[1]
            break
    region_mid_file.write(midline)
    region_mid_file.close()
    mifline=region_mif_header+mifline
    region_mif_file.write(mifline)
    region_mif_file.close()
'''
天气影响区域类
@name:-100 to 20
@path:二维数组，区域边界线
@path_length:整型,区域边界线上的点数量
@isLinkIn(link):判断路链是否在此区域内，返回True or False，采用射线法,判断路链上的三个点,首中尾
'''
class WeatherRegion:
    name = ''
    path = []
    path_length=0
    id=0
    def __init__(self,name,path,path_length,id):
        self.name=name
        self.path=path
        self.path_length=path_length
        self.id = id

    def isLinkIn(self,link):
        hp=link[0]
        mp=link[int(len(link)/2)]
        tp=link[len(link)-1]
        #判断3个点是否都在大矩形内，如果都不在，返回FLASE
        if self.isPointInRect(hp) or self.isPointInRect(mp) or self.isPointInRect(tp):
            pass
        else:
            return  False

        #射线法及顶点处理
        if self.isPointInPolygon(hp) or self.isPointInPolygon(mp) or self.isPointInPolygon(tp):
            return True
        else:
            return False

    def getSouthWest(self):
        c1 = [x[0] for x in self.path]
        c2 = [x[1] for x in self.path]
        return [min(c1),min(c2)]

    def getNorthEast(self):
        c1 = [x[0] for x in self.path]
        c2 = [x[1] for x in self.path]
        return [max(c1),max(c2)]

    def isPointInRect(self,point):
        sw = self.getSouthWest() #西南脚点
        ne = self.getNorthEast() #东北脚点
        #print(point)
        return point[0]>= sw[0] and point[0] <= ne[0] and point[1] >= sw[1] and point[1] <= ne[1]

    def isPointInPolygon(self,point):
        intersectCount = 0
        boundOrVertex = True
        precision = 2e-10
        p1 = self.path[0]
        for i in range(1,self.path_length):
            if p1 == point:
                return True
            p2 = self.path[i]
            if point[1]<min(p1[1],p2[1]) or point[1]>max(p1[1],p2[1]):
                p1 = p2
                continue
            if point[1]>min(p1[1],p2[1]) or point[1]<max(p1[1],p2[1]):
                if point[0] <= max(p1[0], p2[0]):
                    if p1[1] == p2[1] and point[0] >=min(p1[0], p2[0]):
                        return boundOrVertex
                    if p1[0] == p2[0]:
                        if p1[0] == point[0]:
                            return boundOrVertex
                        else:
                            intersectCount+=1
                    else:
                        xinters = (point[1] - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1]) + p1[0]
                        if abs(point[0] - xinters) < precision :
                            return boundOrVertex
                        if point[0] < xinters:
                            intersectCount+=1
            else:
                if point[1] == p2[1] and point[0] <= p2[0]:
                    p3 = self.path[(i+1) % self.path_length]
                    if point[1] >= min(p1[1], p3[1]) and point[1] <= max(p1[1], p3[1]):
                        intersectCount+=1
                    else:
                        intersectCount += 2
            p1 = p2#next ray left point

        if intersectCount % 2 == 0:#偶数在多边形外
           return False
        else: #奇数在多边形内
           return True





def getRegionFromWeatherFile(weatherFile):
    regions = []
    DOMTree = xml.dom.minidom.parse(weatherFile)
    collection = DOMTree.documentElement
    placemarks = collection.getElementsByTagName("Placemark")
    n=1
    for pm in placemarks:
        rname = pm.getElementsByTagName("name")[0]
        visibility=rname.childNodes[0].data.split(' to ')
        if visibility[0] != '-100' or visibility[1]!='20':
            region=pm.getElementsByTagName("coordinates")[0]
            path=region.childNodes[0].data
            pointnum=path.count(",0 ")
            path=path.replace('\n','')
            temp_arr = path.split(',0 ')
            bound = []
            for i in range(0,pointnum):
                temp_point = temp_arr[i].replace(' ','').split(',')
                lng = float(temp_point[0])
                lat = float(temp_point[1])
                bound.append([lng,lat])
            region=WeatherRegion(rname.childNodes[0].data,bound,pointnum,n)
            #region.isLinkIn([])
            regions.append(region)
            n+=1
            #break
    return regions


def createWeatherLink():
    print('start-time',time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    regions = getRegionFromWeatherFile(weatherregionflie)
    linkmidfile=open(midfile,'r')
    linkmiffile=open(miffile,'r')
    line_num = len(linkmidfile.readlines())
    linkmidfile.close()
    links = []
    templink =[]
    dataflag = False
    i = 0
    name_array = ['' for n in range(line_num)]
    print(line_num)
    print(len(name_array))
    print('---------------------------------------------------')
    for link in linkmiffile:
        if link.find('Data'):
            dataflag = True
        if dataflag:
            if link.find('Pline') != -1 or link.find('Line') != -1:
                if len(templink) > 0:
                    if regions[25].isLinkIn(templink):
                        name_array[i]=regions[25].name
                        '''
                        print("*********************************")
                        print(regions[25].getSouthWest())
                        print(regions[25].getNorthEast())
                        print(templink[0])
                        print(templink[len(templink)-1])
                        print("*********************************")
                        '''
                        print('name:'+regions[25].name)
                    '''
                    for r in regions:
                        if r.isLinkIn(templink):
                            name_array[i]=r.name
                            print('name:'+r.name)
                            break
                    '''
                templink =[]
                if i % 10000==0:
                    print(i)
                i+=1
            else:
                tmppoint = link.split(' ')
                value = re.compile(r'^[-+]?[0-9]+\.[0-9]+$')
                result = value.match(tmppoint[0])
                if result:
                    templink.append([float(tmppoint[0]),float(tmppoint[1])])
    print('--------------------------------------------------------')
    print(i)
    print('--------------------------------------------------------')
    #print(name_array)
    linkmiffile.close()
    linkmidfile=open(midfile,'r')
    region_mid_file=open(wl_mid,'w+')
    n = 0
    for line in linkmidfile:
        name = name_array[n]
        line = line.replace('\n','')
        if name == "":
            region_mid_file.write(line+','+','+'\n')
        else:
            tmparr = name.split(' to ')
            region_mid_file.write(line+','+tmparr[0]+','+tmparr[1]+'\n')
        n+=1
    region_mid_file.close()
    print('end-time',time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))

if __name__ == '__main__':
    #createRegionFileByWeatherFile_1(weatherregionflie)
    createWeatherLink()








