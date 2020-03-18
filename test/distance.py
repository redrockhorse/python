import json
import requests
import math
import pymysql
conn = pymysql.connect(host='127.0.0.1', user='root', passwd='123456', db='datacapture', port=3786, charset='utf8',
                       cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()


headers = {'Accept': 'application/json, text/javascript, */*; q=0.01'
,'Accept-Encoding': 'gzip, deflate'
,'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
,'Cache-Control': 'no-cache'
,'Connection': 'keep-alive'
,'Host': 'testqxsj.txffp.com'
,'Origin': 'http://127.0.0.1:2500'
,'Pragma': 'no-cache'
,'Referer': 'http://127.0.0.1:2500/layerdata/collectPage?tbfid=79b22d4324614ce5a9f44ab570d7a1f2'
,'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 扁率
def wgs84togcj02(lng, lat):
    """
    WGS84转GCJ02(火星坐标系)
    :param lng:WGS84坐标系的经度
    :param lat:WGS84坐标系的纬度
    :return:
    """
    if out_of_china(lng, lat):  # 判断是否在国内
        return lng, lat
    dlat = transformlat(lng - 105.0, lat - 35.0)
    dlng = transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [mglng, mglat]

def gcj02towgs84(lng, lat):
    """
    GCJ02(火星坐标系)转GPS84
    :param lng:火星坐标系的经度
    :param lat:火星坐标系纬度
    :return:
    """
    if out_of_china(lng, lat):
        return lng, lat
    dlat = transformlat(lng - 105.0, lat - 35.0)
    dlng = transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [lng * 2 - mglng, lat * 2 - mglat]

def transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
        0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 *
            math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 *
            math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret

def transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
        0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 *
            math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 *
            math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret

def out_of_china(lng, lat):
    """
    判断是否在国内，不在国内不做偏移
    :param lng:
    :param lat:
    :return:
    """
    if lng < 72.004 or lng > 137.8347:
        return True
    if lat < 0.8293 or lat > 55.8271:
        return True
    return False

def handleUpdateLogDic():
    dic ={}
    infile = '/Users/hongyanma/Desktop/updateerror.log'
    with open(infile, 'r') as f:
        line = f.readline()
        while line:
            lineobj = json.loads(line.replace("'", "\""))
            linedata = lineobj['content']['data']
            if linedata['id'] not in dic:
                dic[linedata['id']] =1
            line = f.readline()
    return dic

def handleUpdateLog():
    infile = '/Users/hongyanma/Desktop/updateerror.log'
    outfile = '/Users/hongyanma/Desktop/aaa.log'
    with open(infile,'r') as f,open(outfile,'w+') as outf:
        line = f.readline()
        print(line)
        csystem = '84'
        i =0
        while line:
           lineobj = json.loads(line.replace("'","\""))
           linedata = lineobj['content']['data']
           if linedata['corrdinate'] == 'WGS84':
               csystem = '84'
           else:
               csystem = '02'
           if linedata['state'] =='1' or linedata['state'] =='2':
               param ={"Coordinate_Systems": csystem, 'attribute': 'true', 'dianinterval': 1000, 'lng': linedata['x'], 'lat': linedata['y']}
               r = requests.get("http://testqxsj.txffp.com/API/diantoexamine.do", headers=headers, params=param)
                   #print(r.json())
               result = r.json()
               rstr =''
               if result and 'code' in result and result['code']==200:
                    data = result['data']
                    if data['distance'] is not None:
                        print(linedata['id']+','+str(data['distance'])+','+linedata['state']+','+linedata['x']+','+linedata['y']+','+csystem)
                        #rstr=line+','+str(data['distance'])
                    else:
                        print(line +',' + '>1000'+','+linedata['state']+','+linedata['x']+','+linedata['y']+','+csystem)
                        rstr = line +',' + '>1000'
               else:
                    #print(result)
                    #print('error:'+linedata['id']+','+linedata['state']+','+linedata['x']+','+linedata['y']+','+csystem)
                    print(linedata['id'] + ',' + '2000' + ',' + linedata['state'] + ',' + linedata['x'] + ',' +linedata['y'] + ',' + csystem)
                    rstr = line+',error'
           line = f.readline()
           i=i+1
        print(i)
       #outf.write(rstr + '\n')

def getDistance(x,y,csystem,flag):
    param = {"Coordinate_Systems": csystem, 'attribute': 'true', 'dianinterval': 1000, 'lng': x,
             'lat': y}
    r = requests.get("http://testqxsj.txffp.com/API/diantoexamine.do", headers=headers, params=param)
    result = r.json()
    if result and 'code' in result and result['code'] == 200:
        data = result['data']
        return data['distance']
    else:
        #print('id',)
        print(param)
        print('distance  error!'+str(flag))
        return 2000


def recoverData():
    nowfile = '/Users/hongyanma/Desktop/now.json'
    recoverfile = '/Users/hongyanma/Desktop/recover.json'
    dic = handleUpdateLogDic()
    nowJson = {"msg": "", "msgcode": 200, "body": []}
    recoverJson =  {"msg": "", "msgcode": 200, "body": []}
    for id in dic:
        sql = "select  * from layer_video where id='" + id + "' and (state = 1 or state=2);"
        cursor.execute(sql)
        sqlresult = cursor.fetchall()
        csystem = '84'
        if len(sqlresult) > 0:
            #print(sqlresult)
            if sqlresult[0]['corrdinate'] == 'WGS84':
                csystem = '84'
            else:
                csystem = '02'
            x = float(sqlresult[0]['x'])
            y = float(sqlresult[0]['y'])
            recoord = gcj02towgs84(x, y)#还原的坐标

            nowDis = getDistance(x, y, csystem,1)
            hisDis = getDistance(recoord[0], recoord[1], csystem,0)
            if nowDis-hisDis>3 and nowDis>10:
                nowJson['body'].append({'id': sqlresult[0]['id'], 'corrdinate': sqlresult[0]['corrdinate'], 'x': sqlresult[0]['x'], 'y': sqlresult[0]['y']})
                recoverJson['body'].append({'id': sqlresult[0]['id'], 'corrdinate': sqlresult[0]['corrdinate'], 'x': round(recoord[0],6), 'y': round(recoord[1],6)})
                print(sqlresult)
    with open(nowfile,'w') as nf,open(recoverfile,'w') as rf:
        json.dump(nowJson,nf)
        json.dump(recoverJson, rf)
    print('done !!!')

def genarationSql():
    with open('/Users/hongyanma/Desktop/now.json','r') as f,open('/Users/hongyanma/Desktop/recover.json','r') as fr:
        jobject = json.load(f)
        jro = json.load(fr)
        #print(jobject)
        data = jobject['body']
        datar = jro['body']
        rdic ={}
        for i in range(len(datar)):
            rdic[datar[i]['id']]=datar[i]
        print(len(data))
        updatesql =''
        for i in range(len(data)):
            id = data[i]['id']
            udate = rdic[id]
            updatesql = 'update layer_video_bak set x=\''+str(udate['x'])+'\',y=\''+str(udate['y'])+'\' where id=\''+id+'\' and x=\''+str(data[i]['x'])+'\' and y=\''+ str(data[i]['y'])+'\';'
            # updatesql = 'update layer_video set x=\'' + str(udate['x']) + '\',y=\'' + str(
            #     udate['y']) + '\' where id=\'' + id + '\' and x=\'' + str(data[i]['x']) + '\' and y=\'' + str(
            #     data[i]['y']) + '\' and operid=\'shanxi_layer1\';'
            print(updatesql)
        ids ='('
        for i in range(len(data)):
            id = data[i]['id']
            ids = ids + '\''+id+'\','
        ids = ids+')'
        print(ids)
        print(len(ids.split(',')))

#数据库所有数据检测距离
def checkDataPoint(dic):
    csystem = '84'
    for id in dic:
        sql = "select  * from layer_video where state in (1,2) and  id='"+id+"';"
        cursor.execute(sql)
        sqlresult = cursor.fetchall()
        #print(sql)
        #print(sqlresult)
        if len(sqlresult) > 0:
            if sqlresult[0]['corrdinate'] == 'WGS84':
                csystem = '84'
            else:
                csystem = '02'
            x = float(sqlresult[0]['x'])
            y = float(sqlresult[0]['y'])
            nowDis = getDistance(x, y, csystem, 1)
            #print(nowDis)
            #if nowDis > 30 :
            print(sqlresult[0]['id'],nowDis)

def analyPointDis():
    rdics ={}
    sql = "select  * from layer_video where state in (1,2)  and distance = 'null';"
    cursor.execute(sql)
    sqlresult = cursor.fetchall()
    print('total',len(sqlresult))
    for i in range(len(sqlresult)):
        if i%100 == 0:
            print(i)

        item = sqlresult[i]
        province = item['0af3a34c76e4437a8e915ae343eb082f']
        #print(item)
        if item['corrdinate'] == 'WGS84':
            csystem = '84'
        else:
            csystem = '02'
        x = float(item['x'])
        y = float(item['y'])
        nowDis = getDistance(x, y, csystem, 1)
        updatesql = "update layer_video set distance='"+str(nowDis)+"' where id='"+item['id']+"';"
        cursor.execute(updatesql)
        conn.commit()

        if province in rdics:
            if 'gt3' not in rdics[province]:
                rdics[province]['gt3'] = 0
            if 'lt3' not in rdics[province]:
                rdics[province]['lt3'] = 0
            if nowDis >3:
                rdics[province]['gt3'] = rdics[province]['gt3'] + 1
            else:
                rdics[province]['lt3'] = rdics[province]['lt3'] + 1
    print(rdics)

def countByProvince():
    rdics ={}
    sql = "select  * from layer_video where state in (1,2)"
    cursor.execute(sql)
    sqlresult = cursor.fetchall()
    print('total',len(sqlresult))
    for i in range(len(sqlresult)):
        if i%100 == 0:
            print(i)
        item = sqlresult[i]
        province = item['dataarea']
        #print(item)
        nowDis = item['distance']
        if province in rdics:
            if 'gt3' not in rdics[province]:
                rdics[province]['gt3'] = 0
            if 'lt3' not in rdics[province]:
                rdics[province]['lt3'] = 0
        else:
            rdics[province] = {}
            rdics[province]['gt3'] = 0
            rdics[province]['lt3'] = 0
        if float(nowDis) >10:
            rdics[province]['gt3'] = rdics[province]['gt3'] + 1
        else:
            rdics[province]['lt3'] = rdics[province]['lt3'] + 1
    print(rdics)
    return rdics


if __name__ == '__main__':
    #recoverData()
    #genarationSql()
    #dic = handleUpdateLogDic()
    #checkDataPoint(dic)
    provinceDic ={}
    with open('/Users/hongyanma/Desktop/provincecode.txt') as f:
        line = f.readline()
        while line:
            print(line[0:2])
            print(line[2:-1])
            provinceDic[line[0:2]+'0000']=line[2:-1]
            line = f.readline()
    rdic = countByProvince()
    for id in rdic:
        l = provinceDic[id]+','+str(rdic[id]['gt3'])+','+str(rdic[id]['lt3'])
        print(l)




