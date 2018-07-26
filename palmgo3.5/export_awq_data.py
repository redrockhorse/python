# -*- coding: utf8 -*-
#encoding=utf-8
#By @mahy
#email:kkkkbj@163.com
#导出安联数据
import pymysql
import json
import math

def gps_coord_02tobd(gps_cx_02, gps_cy_02):
    x_pi = 3.14159265358979324 * 3000.0 / 180.0
    z = math.sqrt(gps_cx_02 * gps_cx_02 + gps_cy_02 * gps_cy_02) + 0.00002 * math.sin(gps_cy_02 * x_pi)
    theta = math.atan2(gps_cy_02, gps_cx_02) + 0.000003 * math.cos(gps_cx_02 * x_pi)
    gps_cx_bd = z * math.cos(theta) + 0.0065
    gps_cy_bd = z * math.sin(theta) + 0.006
    return (gps_cx_bd, gps_cy_bd)
conn=pymysql.connect(host='127.0.0.1',user='root',passwd='root',db='palmgo',port=3306,charset='utf8', cursorclass = pymysql.cursors.DictCursor)
cursor = conn.cursor()
def exportWeatherData():
    result={}
    result['data']={}
    #sql="select DATE_FORMAT(wtime,'%Y%m%d') as wtime,bWendu, yWendu,tianqi, aqiInfo from td_weather_his_data where city='上海市'"
    sql="select DATE_FORMAT(wtime,'%Y%m%d') as wtime,city,bWendu, yWendu,tianqi, aqiInfo from td_weather_his_data where DATE_FORMAT(wtime,'%Y%m')='201805' and city in ('北京市','东城区','丰台区','大兴区','密云县','平谷区','延庆县','怀柔区','房山区','昌平区','朝阳区','海淀区','石景山区','西城区','通州区','门头沟区','顺义区')"
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        result['data'][row['wtime']+'_'+row['city']]={}
        result['data'][row['wtime']+'_'+row['city']]['bWendu']=row['bWendu']
        result['data'][row['wtime']+'_'+row['city']]['yWendu']=row['yWendu']
        result['data'][row['wtime']+'_'+row['city']]['tianqi']=row['tianqi']
        result['data'][row['wtime']+'_'+row['city']]['aqiInfo']=row['aqiInfo']
    with open('e:\\desktop\\bj_pre_5_weather.json','w') as outfile:
        json.dump(result,outfile,ensure_ascii=False)

def exportAwpData():
    result={}
    result['data']={}
    sql="select DATE_FORMAT(Case_Time,'%Y%m%d') as Case_Time,Longitude,Latitude, district,street,tianqi from td_awp_source_data where city='北京市' and DATE_FORMAT(Case_Time,'%Y%m')='201705' and Case_Time>='2017-05-08 00:00:00'  and Case_Time<='2017-05-14 23:59:59'"
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        if row['Case_Time'] not in result['data']:
            result['data'][row['Case_Time']]=[]
        coords = gps_coord_02tobd(float(row['Longitude']), float(row['Latitude']))
        result['data'][row['Case_Time']].append(['%.6f' % coords[0],'%.6f' % coords[1],row['district'],row['street'],row['tianqi']])
    with open('e:\\desktop\\bj_awp_pre_5.json','w') as outfile:
        print(result)
        json.dump(result,outfile,ensure_ascii=False)

def exportAwpPreData():
    result={}
    result['data']={}
    sql="select DATE_FORMAT(Case_Time,'%Y%m%d') as Case_Time,Longitude,Latitude, district,street,tianqi from td_awp_source_data where city='北京市' and DATE_FORMAT(Case_Time,'%Y%m')='201705'"
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        if row['Case_Time'] not in result['data']:
            result['data'][row['Case_Time']]=[]
        coords = gps_coord_02tobd(float(row['Longitude']), float(row['Latitude']))
        result['data'][row['Case_Time']].append(['%.6f' % coords[0],'%.6f' % coords[1],row['district'],row['street'],row['tianqi']])
    with open('e:\\desktop\\bj_awp_pre_5.json','w') as outfile:
        print(result)
        json.dump(result,outfile,ensure_ascii=False)

import requests
def getDistrictCenter():
    rt={}
    sql="select district from td_awp_source_data where city='北京市' group by district"
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        url='http://api.map.baidu.com/geocoder/'
        print(url)
        r = requests.get(url='http://api.map.baidu.com/geocoder/v2/',params={'ak': '1XjLLEhZhQNUzd93EjU5nOGQ','output': 'json','address':row['district'],'city':'北京市'})
        result = r.json()
        print(result)
        location=result['result']['location']
        rt[row['district']]=[location['lng'],location['lat']]
    print(rt)




if __name__=='__main__':
    exportAwpData()
    #getDistrictCenter()
    #exportWeatherData()

