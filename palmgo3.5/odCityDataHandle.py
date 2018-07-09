# -*- coding: utf8 -*-
#encoding=utf-8
# coding=utf-8
#By @mahy
#email:kkkkbj@163.com
#处理od数据

'''
数据格式
20171012,6404#6404,1499,3184
20171012,4309,1488,1667
20171012,3202#3205#3100,1483,1498
'''


import sqlite3
conn = sqlite3.connect('/Users/hongyanma/Desktop/20171012/20171012/cityod.db')
c = conn.cursor()
def createTab():
    c.execute('''CREATE TABLE CITYOD
           (OID TEXT    NOT NULL,
           CID TEXT,
           DID TEXT    NOT NULL,
           CARCOUNT        INT,
           SUMCOUNT        INT,
           ODTIME         TEXT);''')

def formatTime(str):
     #print(str)
     a = str.split('-')
     y=a[0]
     m=a[1]
     d=a[2].split()[0]
     if int(m)<10:
         m='0'+m
     if int(d)<10:
         d = '0'+d
     H = a[2].split()[1].split(":")[0]
     M = a[2].split()[1].split(":")[1]
     S = a[2].split()[1].split(":")[2]
     if int(H)<10:
         H='0'+H
     if int(M)<10:
         M='0'+M
     if int(S)<10:
         S='0'+S
     return y+"-"+m+"-"+d+" "+H+":"+M+":"+S

def putDataInToTB():
    f_dir ="/Users/hongyanma/Desktop/20171012/20171012/000000_0"
    print(f_dir)
    rf = open(f_dir,'r')
    i =0
    for line in rf:
        data_array = line.split(',')
        odtime = data_array[0]
        ocd_array = data_array[1].split('#')
        ocd_length = len(ocd_array)
        if ocd_length == 3:
            oid=ocd_array[0]
            cid = ocd_array[1]
            did = ocd_array[2]
        elif ocd_length == 2:
            oid = ocd_array[0]
            cid = ''
            did = ocd_array[1]
        elif ocd_length == 1:
            oid = ocd_array[0]
            cid = ocd_array[0]
            did = ocd_array[0]
        else:
            print('citycode error !!!')
            continue
        carcount = data_array[2]
        sumcount = data_array[3]

        if i>-1:
            #endtime = formatTime(data_array[8])
            #startime = formatTime(data_array[7])
            c.execute("INSERT INTO CITYOD (OID,CID,DID,CARCOUNT,SUMCOUNT,ODTIME) VALUES('"+oid+"','"+cid+"','"+did+"',"+carcount+","+sumcount+",'"+odtime+"')")
        i=i+1
        #print(i)
        if i%500 ==0:
            conn.commit()
    print('filecount:',i)
    conn.commit()
import datetime

''' 
def handleData():
    cursor = c.execute("SELECT count(*)  from OD")
    for row in cursor:
       print("db count = ", row[0])
    # cursor = c.execute("SELECT STARTLON,STARTLAT,ENDLON,ENDLAT,STARTTIME  from OD order by STARTTIME ASC")
    # for row in cursor:
    #    print("db count = ", row[4])
    d1 = datetime.datetime(2018,1,22,0,0,0)
    dtmp = d1
    for i in range(7*24):
        d2 = dtmp +datetime.timedelta(hours=1)
        sql_time = d2.strftime("%Y-%m-%d %H:%M:%S")
        #print(sql_time)
        #print(dtmp.strftime("%Y-%m-%d %H:%M:%S"))
        file_time = dtmp.strftime("%Y%m%d%H")
        #print(file_time)
        cursor = c.execute("SELECT STARTLON,STARTLAT,ENDLON,ENDLAT,STARTTIME  from OD where STARTTIME>='"+dtmp.strftime("%Y-%m-%d %H:%M:%S")+"' and STARTTIME<'"+sql_time+"'" )
        wf = open("/Users/hongyanma/Downloads/2018_gdhd_od/"+file_time+".json","w+")
        json_str ="{\"data\":["
        j = 0
        values = cursor.fetchall()
        for row in values:
           j=j+1
           #print("db count = ", row[4])
           if j == len(values):
               json_str = json_str+"[["+str(row[0])+","+str(row[1])+"],["+str(row[2])+","+str(row[3])+"]]"
           else:
               json_str = json_str+"[["+str(row[0])+","+str(row[1])+"],["+str(row[2])+","+str(row[3])+"]],"

        json_str = json_str+"]}"
        wf.write(json_str)
        wf.close()

        dtmp = d2
     
def handleData():
    cursor = c.execute("SELECT count(*)  from OD")
    for row in cursor:
       print("db count = ", row[0])
    # cursor = c.execute("SELECT STARTLON,STARTLAT,ENDLON,ENDLAT,STARTTIME  from OD order by STARTTIME ASC")
    # for row in cursor:
    #    print("db count = ", row[4])
    d1 = datetime.datetime(2018,1,22,0,0,0)
    dtmp = d1
    for i in range(7*24):
        d2 = dtmp +datetime.timedelta(hours=1)
        sql_time = d2.strftime("%Y-%m-%d %H:%M:%S")
        #print(sql_time)
        #print(dtmp.strftime("%Y-%m-%d %H:%M:%S"))
        file_time = dtmp.strftime("%Y%m%d%H")
        #print(file_time)
        cursor = c.execute("SELECT STARTLON,STARTLAT,ENDLON,ENDLAT,STARTTIME  from OD where STARTTIME>='"+dtmp.strftime("%Y-%m-%d %H:%M:%S")+"' and STARTTIME<'"+sql_time+"'" )
        wf = open("/Users/hongyanma/Downloads/2018_gdhd_od/"+file_time+".json","w+")
        json_str ="{\"data\":["
        j = 0
        values = cursor.fetchall()
        for row in values:
           j=j+1
           #print("db count = ", row[4])
           if j == len(values):
               json_str = json_str+"[["+str(row[0])+","+str(row[1])+"],["+str(row[2])+","+str(row[3])+"]]"
           else:
               json_str = json_str+"[["+str(row[0])+","+str(row[1])+"],["+str(row[2])+","+str(row[3])+"]],"

        json_str = json_str+"]}"
        wf.write(json_str)
        wf.close()

        dtmp = d2
'''

import collections
import json
import requests
import  os
from urllib.request import urlopen, quote
def handleData():

    citycodeDic = collections.OrderedDict()
    citycodefile = open('/Users/hongyanma/Desktop/20171012/20171012/citycode.txt','r',encoding='utf-8')
    citycodejson = open('/Users/hongyanma/Desktop/20171012/20171012/citycode.json', 'w',encoding='utf-8')
    i=0
    for line in citycodefile:
        if i>0:
            larray = line.split(',')
            print(larray[2])
            #citycodeDic[larray[4]] = larray[2]
            url = 'http://api.map.baidu.com/geocoder/v2/'
            output = 'json'
            ak = '1XjLLEhZhQNUzd93EjU5nOGQ'
            add =  quote(larray[2].encode('utf8'))  # 由于本文城市变量为中文，为防止乱码，先用quote进行编码
            uri = url + '?' + 'address=' + add + '&output=' + output + '&ak=' + ak
            req = urlopen(uri)
            res = req.read().decode()
            temp = json.loads(res)  # 对json数据进行解析
            citycodeDic[larray[4].replace('\n','')] = [larray[2],[temp["result"]["location"]["lng"],temp["result"]["location"]["lat"]]]
            #print(res)
        i+=1
    citycodeJson = json.dump(citycodeDic,citycodejson,ensure_ascii=False,indent=4)
    #print(citycodeJson)
    #return

    print('start press od data!!!')

    odic = collections.OrderedDict()
    cdic = collections.OrderedDict()
    ddic = collections.OrderedDict()
    allDict = collections.OrderedDict()
    olist = {}
    olist["data"]=[]
    clist = {}
    clist["data"] = []
    dlist = {}
    dlist["data"] = []
    chinaof = open('/Users/hongyanma/Desktop/20171012/20171012/o_china.json', 'w')
    cursor = c.execute("SELECT OID,SUM(SUMCOUNT)  from CITYOD group by OID order by SUM(SUMCOUNT) desc")
    for row in cursor:
        # print('-------------------------')
        # print("citycode: ", row[0])
        # print("count: ", row[1])
        # print('-------------------------')
        odic[row[0]]=row[1]
        if row[0] in citycodeDic.keys():
            olist["data"].append({"name": citycodeDic[row[0]][0],"value": citycodeDic[row[0]][1],"count":row[1]})
        i+=i
    json.dump(olist,chinaof,ensure_ascii=False,indent=4)
    #print(oddicJson)
    #return

    chinaoc = open('/Users/hongyanma/Desktop/20171012/20171012/c_china.json', 'w')
    cursor = c.execute("SELECT CID,SUM(SUMCOUNT)  from CITYOD group by CID order by SUM(SUMCOUNT) desc")
    for row in cursor:
        # print('-------------------------')
        # print("citycode: ", row[0])
        # print("count: ", row[1])
        # print('-------------------------')
        if len(row[0])>0:
            cdic[row[0]] = row[1]
            if row[0] in citycodeDic.keys():
                clist["data"].append({"name": citycodeDic[row[0]][0], "value": citycodeDic[row[0]][1], "count": row[1]})
    #cdicJson = json.dumps(cdic)
    json.dump(clist, chinaoc, ensure_ascii=False, indent=4)
    #print(cdicJson)

    chinaod = open('/Users/hongyanma/Desktop/20171012/20171012/d_china.json', 'w')
    cursor = c.execute("SELECT DID,SUM(SUMCOUNT)  from CITYOD group by DID order by SUM(SUMCOUNT) desc")
    for row in cursor:
        # print('-------------------------')
        # print("citycode: ", row[0])
        # print("count: ", row[1])
        # print('-------------------------')
        ddic[row[0]] = row[1]
        if row[0] in citycodeDic.keys():
            dlist["data"].append({"name": citycodeDic[row[0]][0],"value": citycodeDic[row[0]][1],"count":row[1]})

    json.dump(dlist, chinaod, ensure_ascii=False, indent=4)
    #print(ddicJson)


    o2ddic = collections.OrderedDict()
    cityo2d = open('/Users/hongyanma/Desktop/20171012/20171012/o_city.json', 'w')
    for key in odic:
        ddic.setdefault(key, 0)
        cdic.setdefault(key, 0)
        allDict[key] = odic[key]+ddic[key]+cdic[key]
        #print("SELECT DID,SUMCOUNT  from CITYOD where OID="+key+"  order by SUMCOUNT desc")
        if key in citycodeDic.keys():
            ocityname = citycodeDic[key][0]
            ocitycoord = citycodeDic[key][1]
            o2ddic[ocityname] = []
            cursor = c.execute("SELECT DID,sum(SUMCOUNT)  from CITYOD where OID=%s and DID !=OID group by DID order by sum(SUMCOUNT) desc LIMIT 15" %key)
            for row in cursor:
                # print('-------------------------')
                # print("citycode: ", row[0])
                # print("count: ", row[1])
                if row[0] in citycodeDic.keys():
                    o2ddic[ocityname].append({"fromName": ocityname,"toName": citycodeDic[row[0]][0],"coords": [ocitycoord,citycodeDic[row[0]][1]],"count":row[1]})
    o2ddicJson = json.dump(o2ddic,cityo2d, ensure_ascii=False, indent=4)
    #print(o2ddicJson)

    d2odic=collections.OrderedDict()
    cityd2o = open('/Users/hongyanma/Desktop/20171012/20171012/d_city.json', 'w')
    for key in ddic:
        #print(SELECT OID,SUMCOUNT  from CITYOD where DID=%s order by SUMCOUNT desc)
        if key in citycodeDic.keys():
            dcityname = citycodeDic[key][0]
            dcitycoord = citycodeDic[key][1]
            d2odic[dcityname] = []
            #cursor = c.execute("SELECT OID,SUMCOUNT  from CITYOD where DID=%s and OID !=DID order by SUMCOUNT desc LIMIT 15" %key)
            cursor = c.execute("SELECT OID,SUM(SUMCOUNT)  from CITYOD where DID=%s and OID !=DID group by OID order by SUM(SUMCOUNT) desc LIMIT 15" % key)
            for row in cursor:
                # print('-------------------------')
                # print("citycode: ", row[0])
                # print("count: ", row[1])
                if row[0] in citycodeDic.keys():
                    d2odic[dcityname].append({"fromName": citycodeDic[row[0]][0],"toName": dcityname,"coords": [citycodeDic[row[0]][1],dcitycoord],"count":row[1]})
    d2odicJson = json.dump(d2odic,cityd2o, ensure_ascii=False, indent=4)
    #print(d2odicJson)

    cityc2od= open('/Users/hongyanma/Desktop/20171012/20171012/c_city.json', 'w')
    c2oddic = collections.OrderedDict()
    for key in cdic:
        if key in citycodeDic.keys():
            ccityname = citycodeDic[key][0]
            ccitycoord = citycodeDic[key][1]
            c2oddic[ccityname] = []
            cursor = c.execute("SELECT OID,DID,SUMCOUNT  from CITYOD where CID=%s and SUMCOUNT>100 order by SUMCOUNT desc LIMIT 12" %key)
            ocdid = 0
            for row in cursor:
                # print('-------------------------')
                # print("oid: ", row[0])
                # print("did: ", row[1])
                # print("count: ", row[2])
                if row[0] in citycodeDic.keys() and row[1] in citycodeDic.keys():
                    c2oddic[ccityname].append({"fromName": citycodeDic[row[0]][0],"toName": ccityname,"coords": [citycodeDic[row[0]][1],ccitycoord],"count": row[1],"ocdid":ocdid})
                    c2oddic[ccityname].append({"fromName": ccityname ,"toName": citycodeDic[row[1]][0],"coords":[ccitycoord,citycodeDic[row[1]][1]],"count": row[1],"ocdid":ocdid})
                    ocdid+=1
    c2oddicJson = json.dump(c2oddic,cityc2od, ensure_ascii=False, indent=4)
    #print(c2oddicJson)

    #print(sorted(allDict.items(), key=lambda d: d[1],reverse=True))
    allchina = open('/Users/hongyanma/Desktop/20171012/20171012/all_china.json', 'w')
    allList = sorted(allDict.items(), key=lambda d: d[1],reverse=True)
    allListResult = {}
    allListResult["data"] = []
    ocddic = collections.OrderedDict()
    for v in allList:
        #ocddic[v[0]]=v[1]
        if v[0] in citycodeDic.keys():
            allListResult["data"].append({"name": citycodeDic[v[0]][0],"value": citycodeDic[v[0]][1],"count":v[1]});
    ocddicJson = json.dump(allListResult,allchina, ensure_ascii=False, indent=4)
    print(ocddicJson)


    ''' 
    cursor = c.execute("SELECT DID,SUMCOUNT  from CITYOD where OID=?  order by SUMCOUNT desc")
    for row in cursor:
        print('-------------------------')
        print("citycode: ", row[0])
        print("count: ", row[1])

    cursor = c.execute("SELECT OID,SUMCOUNT  from CITYOD where DID=?  order by SUMCOUNT desc")
    for row in cursor:
        print('-------------------------')
        print("citycode: ", row[0])
        print("count: ", row[1])

    cursor = c.execute("SELECT OID,DID,SUMCOUNT  from CITYOD where CID=?  order by SUMCOUNT desc")
    for row in cursor:
        print('-------------------------')
        print("citycode: ", row[0])
        print("count: ", row[1])
    '''

def checkData():
    cursor = c.execute("SELECT *  from CITYOD where OID='3100' order by SUMCOUNT desc")
    for row in cursor:
        print('-------------------------')
        print(row[0],row[1],row[2],row[3],row[4],row[5])
        #print("count: ", row[1])

def handleZsjData():
    citycodeDic = collections.OrderedDict()
    citycodejson = open('/Users/hongyanma/Desktop/20171012/20171012/citycode.json', 'r', encoding='utf-8')
    citycodeDic = json.load(citycodejson)
    #print(citycodeDic)
    '''
    guangzhouoresult = {}
    guangzhouoresult['data']=[]
    guangzhouo = open('/Users/hongyanma/Desktop/20171012/20171012/o_guangzhou.json', 'w')
    cursor = c.execute("SELECT DID,sum(SUMCOUNT)  from CITYOD where OID='4401' and DID <>'4401'  group by DID order by sum(SUMCOUNT)   desc")
    for row in cursor:
        #print('-------------------------')
        #print(row[0],row[1])
        if row[0] in citycodeDic.keys():
            guangzhouoresult['data'].append({
                "fromName": citycodeDic['4401'][0],
                "toName": citycodeDic[row[0]][0],
                "coords": [citycodeDic['4401'][1],citycodeDic[row[0]][1]],
                "count": row[1]
            })


    guangzhoudresult = {}
    guangzhoudresult['data']=[]
    guangzhoud = open('/Users/hongyanma/Desktop/20171012/20171012/d_guangzhou.json', 'w')
    cursor = c.execute("SELECT OID,sum(SUMCOUNT)  from CITYOD where DID='4401' and OID <>'4401'  group by OID order by sum(SUMCOUNT)   desc")
    for row in cursor:
        #print('-------------------------')
        #print(row[0],row[1])
        if row[0] in citycodeDic.keys():
            guangzhoudresult['data'].append({
                "fromName": citycodeDic[row[0]][0],
                "toName":  citycodeDic['4401'][0],
                "coords": [citycodeDic[row[0]][1],citycodeDic['4401'][1]],
                "count": row[1]
            })
    json.dump(guangzhouoresult, guangzhouo, ensure_ascii=False, indent=4)
    json.dump(guangzhoudresult,guangzhoud, ensure_ascii=False, indent=4)
    #print(guangzhoudresult)
    '''
    #广州','深圳','佛山','东莞','惠州','中山','珠海','江门','肇庆
    zsjcitylist =['4401','4403','4406','4419','4413','4420','4404','4407','4412']
    #广州市','韶关市','深圳市','珠海市','汕头市','佛山市','江门市','湛江市','茂名市','肇庆市','惠州市','梅州市','汕尾市','河源市','阳江市','清远市','东莞市','中山市','潮州市','揭阳市','云浮市
    gdcitynames =['广州市','韶关市','深圳市','珠海市','汕头市','佛山市','江门市','湛江市','茂名市','肇庆市','惠州市','梅州市','汕尾市','河源市','阳江市','清远市','东莞市','中山市','潮州市','揭阳市','云浮市']
    gdpcitylist =[]
    for key in citycodeDic:
       if citycodeDic[key][0]  in gdcitynames:
           #print(citycodeDic[key][0])
           gdpcitylist.append(key)
    #print(gdpcitylist)

    zsjresult = {}
    zsjresult['data']=[]
    zsjod = open('/Users/hongyanma/Desktop/20171012/20171012/od_zsj.json', 'w')
    tmp = []
    for c0 in zsjcitylist:
        tmp.append(c0)
        for c1 in zsjcitylist:
            if c0 != c1 and c1 not in tmp:
                cursor = c.execute("SELECT sum(SUMCOUNT)  from CITYOD where (OID="+c0+" and DID ="+c1+") or  (OID="+c0+" and DID ="+c1+") ")
                #print(cursor)
                for row in cursor:
                    zsjresult['data'].append({
                        "fromName": citycodeDic[c0][0],
                        "toName": citycodeDic[c1][0],
                        "coords": [citycodeDic[c0][1], citycodeDic[c1][1]],
                        "count": row[0]
                    })
    print(zsjresult)
    #guangzhoud = open('/Users/hongyanma/Desktop/20171012/20171012/d_guangzhou.json', 'w')

    gdresult = {}
    gdresult['data'] = []
    gdod = open('/Users/hongyanma/Desktop/20171012/20171012/od_gd.json', 'w')
    tmp = []
    for c0 in gdpcitylist:
        tmp.append(c0)
        for c1 in gdpcitylist:
            if c0 != c1 and c1 not in tmp:
                cursor = c.execute("SELECT sum(SUMCOUNT)  from CITYOD where (OID=" + c0 + " and DID =" + c1 + ") or  (OID=" + c0 + " and DID =" + c1 + ") ")
                # print(cursor)
                for row in cursor:
                    gdresult['data'].append({
                        "fromName": citycodeDic[c0][0],
                        "toName": citycodeDic[c1][0],
                        "coords": [citycodeDic[c0][1], citycodeDic[c1][1]],
                        "count": row[0]
                    })
    print(gdresult)
    json.dump(zsjresult, zsjod, ensure_ascii=False, indent=4)
    json.dump(gdresult, gdod, ensure_ascii=False, indent=4)


        



if __name__ =="__main__":
    #createTab()
    #putDataInToTB()
    # putDataInToTB('20180123')
    # putDataInToTB('20180124')
    # putDataInToTB('20180125')
    # putDataInToTB('20180126')
    # putDataInToTB('20180127')
    # putDataInToTB('20180128')
    # print(os.sys.path)
    #handleData()
    #checkData()
    handleZsjData()
    print("done!!!")
    #cursor.close()

    conn.close()
