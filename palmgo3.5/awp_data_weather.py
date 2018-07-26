# -*- coding: utf8 -*-
#encoding=utf-8
#By @mahy
#email:kkkkbj@163.com
#安联数据增加天气信息

import pymysql
import json
import math
import requests
import sys
import datetime
import numpy as np
import decimal

conn=pymysql.connect(host='127.0.0.1',user='root',passwd='root',db='palmgo',port=3306,charset='utf8', cursorclass = pymysql.cursors.DictCursor)
cursor = conn.cursor()
monthlist = ['201701','201702','201703','201704','201705','201706','201707','201708','201709','201710','201711','201712','201801','201802','201803','201804']
#arealistweb={"54511":"北京","60198":"昌平","71141":"朝阳","60205":"大兴","71445":"东城","60206":"房山","71142":"丰台","60207":"怀柔","71144":"海淀","60247":"密云","60246":"门头沟","60204":"平谷","60202":"顺义","71143":"石景山","71071":"通州","71446":"西城","60199":"延庆","58362":"上海","71072":"宝山","60005":"崇明","71448":"长宁","60298":"奉贤","71447":"黄浦","71451":"虹口","60010":"嘉定","60006":"金山","71449":"静安","60008":"闵行","60299":"南汇","71146":"浦东","71450":"普陀","60007":"青浦","60009":"松江","71147":"徐汇","71452":"杨浦"}
'''
for key in arealistweb:
    name=arealistweb[key]
    if name+'区' in arealist:
        arealist[name+'区']=key
'''
#print(arealist)
arealist={'浦东新区': '71146', '萧山区': '60175', '平谷区': '60204', '丰城市': '60502', '昆山市': '60037', '朝阳区': '71141', '越城区': '3580', '密云县': '60247', '大兴区': '60205', '宝山区': '71072', '长宁区': '71448', '海淀区': '71144', '崇明县': '60005', '云岩区': '71412', '普陀区': '71450', '海盐县': '60121', '乐清市': '60180', '丰台区': '71142', '安岳县': '61088', '昌平区': '60198', '延庆县': '60199', '东城区': '71445', '兴隆县': '60275', '涿州市': '60523', '西城区': '71446', '闸北区': '79346', '怀柔区': '60207', '闵行区': '60008', '金山区': '60006', '嘉善县': '60194', '青浦区': '60007', '中山市市辖区': '59485', '固安县': '70189', '黄浦区': '71447', '香河县': '60111', '嘉定区': '60010', '鼓楼区': '71799', '奉贤区': '60298', '通州区': '71071', '门头沟区': '60246', '西乡塘区': '72066', '岳麓区': '71952', '长乐市': '60396', '秀洲区': '71859', '石景山区': '71143', '房山区': '60206', '徐汇区': '71147', '怀来县': '70197', '顺义区': '60202', '彭水苗族土家族自治县': '60978', '武侯区': '71988', '三河市': '60522', '静安区': '71449', '松江区': '60009', '虹口区': '71451', '杨浦区': '71452'}

'''
for key in arealist:
    if arealist[key] =='':
        print(key)
r = requests.get(url='http://tianqi.2345.com/t/wea_history/js/201807/60198_201807.js')
result = r.text
jsonstr=result.split('=')[1].replace(';','').replace(',{}','').replace('\'','"').replace('{','{"').replace(':','":').replace(',',',"').replace('"{','{')
weather=json.loads(jsonstr)
print(weather)
'''


for m in monthlist:
    print(m)
    for a in arealist:
        #url='http://tianqi.2345.com/t/wea_history/js/201807/60198_201807.js'
        r = requests.get(url='http://tianqi.2345.com/t/wea_history/js/'+m+'/'+arealist[a]+'_'+m+'.js')
        #print(r.status_code)
        if r.status_code ==200:
            result = r.text
            jsonstr=result.split('=')[1].replace(';','').replace(',{}','').replace('\'','"').replace('{','{"').replace(':','":').replace(',',',"').replace('"{','{')
            '''
            print('--------------------------------------------------------')
            print('http://tianqi.2345.com/t/wea_history/js/'+m+'/'+arealist[a]+'_'+m+'.js')
            print(jsonstr)
            print('--------------------------------------------------------')
            '''
            weatherobj=json.loads(jsonstr)
            weatherlist=weatherobj['tqInfo']
            #print(weatherlist)
            for tq in weatherlist:
                aqi=''
                aqiInfo=''
                aqiLevel=''
                if 'aqi' in tq:
                    aqi=tq['aqi']
                if 'aqiInfo' in tq:
                    aqiInfo=tq['aqiInfo']
                if 'aqiLevel' in tq:
                    aqiLevel=tq['aqiLevel']
                update_sql="update td_awp_source_data set bWendu=%s,yWendu=%s,tianqi=%s,fengxiang=%s,fengli=%s,aqi=%s,aqiInfo=%s,aqiLevel=%s where Case_Time>=%s and Case_Time<=%s and district=%s and tianqi is null"
                cursor.execute(update_sql,(tq['bWendu'],tq['yWendu'],tq['tianqi'],tq['fengxiang'],tq['fengli'],aqi,aqiInfo,aqiLevel,tq['ymd']+' 00:00:00',tq['ymd']+' 23:59:59',a))
            conn.commit()


