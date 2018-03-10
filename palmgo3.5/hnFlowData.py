# -*- coding: utf8 -*-
#encoding=utf-8
#By @mahy
#email:kkkkbj@163.com
import  numpy as np
#rd = np.random.normal(3, 2, 24*60 )
#print(rd)
import datetime
import random
import json

sdt = datetime.datetime.strptime('20180310000000', "%Y%m%d%H%M%S")
#print(sdt)
ynow = 3
yhis = 2.8
mt = 20180310133000
dic = {}
dic["msgcode"]="200"
data = []
for i in range(24*12):
    nt =  sdt + datetime.timedelta( minutes=i*5)
    y1 = 3-abs((i-150)/70.00*random.random())
    data.append({"xdata":nt.strftime("%Y%m%d%H%M%S"),"ydata":round(y1*1000,0)})
   # print(nt.strftime("%Y%m%d%H%M%S"))
    #print(y1)
dic["data"]=data
python_to_json = json.dumps(dic,ensure_ascii=False)
#print(python_to_json)

def getVule(r):
    x = 3
    if r>0.95:
        x=1
    elif r<=0.95 and r>0.87:
        x=2
    return x


dic1={}
dic1["msgcode"]="200"
datac = []
for l in range(24*12):
    datal = []
    for i in range(248):
        r = random.random()
        if l==0:
            pass
        else:
            if datac[l-1][i] == 1:
                r = r*1.5
            if datac[l-1][i] == 2:
                r = r*1.5
        datal.append(getVule(r))
    datac.append(datal)
dic1["data"]=datac
python_to_json = json.dumps(dic1,ensure_ascii=False)
fw = open('E:\\hnstd.json','w')
fw.write(python_to_json)
fw.close()
#print(python_to_json)


