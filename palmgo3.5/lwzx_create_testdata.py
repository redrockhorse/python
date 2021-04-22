# -*- coding:utf-8 -*-
# @Time : 2020/9/27 下午3:33
# @Author: kkkkibj@163.com
# @File : lwzx_create_testdata.py
# 监测预警平台创建测试数据
import requests
import pymongo
import pymysql
import psycopg2
import time
import random
import threading

# mysql 链接
mqconn = pymysql.connect(host='192.168.220.246', user='lwzx2020', passwd='lwzx2020', db='lwzx_yjjc', port=3306,
                         charset='utf8',
                         cursorclass=pymysql.cursors.DictCursor)
mqcursor = mqconn.cursor()
# postgresql链接
pgconn = psycopg2.connect(database="lwzx2020", user="postgres", password="123456", host="192.168.220.246", port="5432")
pgcursor = pgconn.cursor()

# mongodb链接
client = pymongo.MongoClient(host='192.168.220.246', port=27017)

tmpDic = {}


# 根据主题树，获取图层列表
def subscribeInfo():
    rs = requests.get('http://192.168.220.248:8009/lwzxrest/api/yjjc/subject/infosubscribe')
    rs.encoding = rs.apparent_encoding
    result = rs.json()
    layerList = []
    for children in result['body']['dataList'][0]['children']:
        for sc in children['children']:
            if sc['seriesType'] == 'layer':
                if sc['id'] not in tmpDic:
                    layerList.append(sc)
                    tmpDic[sc['id']] = 1
    return layerList


def getTaskIdByLayerId(layerId):
    sql = 'select tskId from subject_layer where layerId = %s limit 1'
    mqcursor.execute(sql, list([layerId]))
    result = mqcursor.fetchall()
    rs = {}
    for row in result:
        rs = row
    return rs


def getGids(geoLayerId):  # 根据图层id从postgresql中获取地图属性，只选收费站和省,
    if 'lwzx_furniture' == geoLayerId:
        sql = 'select gid,fsssname,lxbm,lxmc from public.' + geoLayerId + ' where kind =\'230209\';'
    if 'lwzx_region_border' == geoLayerId:
        sql = 'select gid,adminshe00 from public.' + geoLayerId + ' where adminxian=\'0\' and adminshi=\'0\';'
    pgcursor.execute(sql, list([geoLayerId]))
    result = pgcursor.fetchall()
    rs = []
    for row in result:
        # print(list(row))
        rs.append(list(row))
    return rs


def createTestData(gids, collection, optime): #生成测试数据
    for gid in gids:
        jamIndex = random.random()  # 生成随机数作为拥堵指数
        avgspeed = (1 - jamIndex) * 120 - random.randint(0, 9)
        if avgspeed < 0:
            avgspeed = 0
        flownum = jamIndex * 100 - avgspeed * 0.1 * jamIndex
        if flownum < 0:
            flownum = 0
        flownum = int(flownum)
        jamLen = 3 * jamIndex
        duration = int(jamIndex * 10)
        title = gid[1]
        subtitle = ''
        if len(gid) > 3:
            if gid[3] is not None:
                subtitle = gid[2] + '_' + gid[3]
            else:
                subtitle = gid[2]
        des = '拥堵' + '%.2f' % jamLen + '公里,' + '平均时速' + '%.2f' % avgspeed + 'km/h,' + '累计拥堵' + str(
            duration) + '分钟'
        data = {'gid': str(gid[0]), 'flownum': flownum, 'jamindex': jamIndex, 'avgspeed': avgspeed,
                'jamlen': jamLen, 'duration': duration, 'title': title, 'subtitle': subtitle, 'des': des,
                'optime': optime}
        # print(data)
        collection.remove({'gid': str(gid[0]), 'optime': optime})
        collection.insert([data])


def main():
    layerList = subscribeInfo()
    print(layerList)
    # print(time.mktime(time.strptime("2020-09-20 00:00", "%Y-%m-%d %H:%M")))
    # startTime = time.mktime(time.strptime("2020-09-20 00:00", "%Y-%m-%d %H:%M"))  # 开始时间设为2020-09-20
    # print(time.strftime("%Y-%m-%d %H:%M", time.localtime(startTime + 300)))
    # endTime = startTime
    endTime = int(time.time() / 300) * 300
    print(time.strftime("%Y-%m-%d %H:%M", time.localtime(endTime)))
    n = 1
    # while endTime < time.time():
    while n > 0:
        optime = time.strftime("%Y%m%d%H%M", time.localtime(endTime))
        print(optime)
        for layer in layerList:
            if layer['seriesType'] == 'layer' and (layer['attr']['geoLayerId'] == 'lwzx_furniture' or layer['attr'][
                'geoLayerId'] == 'lwzx_region_border'):
                geolayer = layer['attr']['geoLayerId']
                layerId = layer['id']
                tskId = getTaskIdByLayerId(layerId)['tskId']
                print(geolayer, layerId, tskId)
                db = client['db_' + tskId]
                collection = db['layer_' + layerId]
                gids = getGids(geolayer)
                # print(len(gids))
                # thread1 = createTestData(gids, collection, optime)
                # thread1.start()
                t = threading.Thread(target=createTestData, args=(gids, collection, optime))
                t.start()
        endTime = endTime - 300
        n = n - 1


if __name__ == '__main__':
    main()
