import json
import requests
import math
import pymysql
conn = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='datacapture', port=3306, charset='utf8',
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


#调用接口计算到道路的距离，如果匹配不到道路，则返回2000米
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


#计算点到路的距离并更新到数据库中
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



#分省统计 距离道路大于3米的点数量
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
        if float(nowDis) >3:
            rdics[province]['gt3'] = rdics[province]['gt3'] + 1
        else:
            rdics[province]['lt3'] = rdics[province]['lt3'] + 1
    print(rdics)
    return rdics



if __name__ == '__main__':
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




