# -*- coding: utf8 -*-
from __future__ import division
__author__ = 'mahy'

import pymysql
import  numpy as np
import sys


conn_g=pymysql.connect(host='127.0.0.1',user='root',passwd='Qd@#$mo658',db='jc',port=3306,charset='utf8')
cur_g = conn_g.cursor()

last_game_time = {}
fatigue_degree = {}
points = {}
#意甲,法甲,西甲,英超,德甲,欧冠,欧冠杯
lg_dic={'意甲':1,'法甲':1,'西甲':1,'英超':1,'德甲':1,'欧冠':1,'欧冠杯':1}
#g_sql ="select gametime,lg,homesxname,awaysxname,hscore,ascore from tb_rate_power_rs where resulenum is not null and (homesxname in  ('安德莱','拜  仁','巴塞尔','曼  联','贝西克','波尔图','多  特','热  刺','卡拉巴','切尔西','里斯本','奥林匹','马竞技','罗  马','曼  城','费耶诺','摩纳哥','莱比锡','莫陆军','本菲卡','莫斯巴','马里博','那不勒','矿  工','日尔曼','凯尔特','塞维利','利物浦','希腊人','皇  马','尤  文','巴  萨') or awaysxname in  ('安德莱','拜  仁','巴塞尔','曼  联','贝西克','波尔图','多  特','热  刺','卡拉巴','切尔西','里斯本','奥林匹','马竞技','罗  马','曼  城','费耶诺','摩纳哥','莱比锡','莫陆军','本菲卡','莫斯巴','马里博','那不勒','矿  工','日尔曼','凯尔特','塞维利','利物浦','希腊人','皇  马','尤  文','巴  萨')) and lg != '友谊赛' order by  gametime asc; "
g_sql ="select gametime,lg,homesxname,awaysxname,hscore,ascore from jc.t500 where resulenum is not null  and lg != '友谊赛' order by  gametime asc; "

cur_g.execute(g_sql)
result = cur_g.fetchall()
output_file = open("E:\\1579\\ouguan20171123_2.txt","w+")
for vals in result:
    lgweight =0.8
    if vals[1] in lg_dic:
        lgweight =1
    sweight = 1
    hp = 0
    ap = 0
    h_fatigue  = 0
    a_fatigue  = 0
    h_new_season = False
    a_new_season = False
    if vals[2] in last_game_time or vals[3] in last_game_time:
        #处理时间，看两次间隔是否大于60天
        if vals[2] in last_game_time:
            h_l_t = last_game_time[vals[2]]
            h_tmp = (vals[0]-h_l_t).days
            if h_tmp>60.0:
                h_new_season = True
            else:
                if h_tmp>10.0:
                    h_fatigue = 0
                else:
                    if vals[2] in fatigue_degree:
                        if fatigue_degree[vals[2]] == 0.0:
                            h_fatigue = 1-np.tanh(h_tmp/5.00)
                        else:
                            h_fatigue = fatigue_degree[vals[2]]-np.tanh(h_tmp/5.00)
                        if h_fatigue < 0:
                            h_fatigue = 0
        if vals[3] in last_game_time:
            a_l_t = last_game_time[vals[3]]
            a_tmp = (vals[0]-a_l_t).days
            if a_tmp>60.0:
                a_new_season = True
            else:
                if a_tmp>10.0:
                    a_fatigue = 0
                else:
                    if vals[3] in fatigue_degree:
                        if fatigue_degree[vals[3]] == 0:
                            a_fatigue = 1-np.tanh(a_tmp/5.00)
                        else:
                            a_fatigue = fatigue_degree[vals[3]] - np.tanh(a_tmp/5.00)
                        if a_fatigue < 0:
                            a_fatigue = 0

        #@todo
        if vals[4] > vals[5]:#3
            hp=3*lgweight
            ap=0
        elif vals[4] < vals[5]:#0
            hp=0
            ap=3*lgweight
        else:#1
            hp=lgweight
            ap=lgweight
        if h_new_season is not True and a_new_season is not True:
            h_h_p = 0
            a_h_p = 0
            if vals[2] in points:
                h_h_p = points[vals[2]]
            if vals[3] in points:
                a_h_p = points[vals[3]]
            if h_h_p - a_h_p > 10:
                hp = hp*0.8
                ap = ap*1.2
            if a_h_p - h_h_p >10:
                hp = hp*1.2
                ap = ap*0.8
    else:
        if vals[4] > vals[5]:
            hp=3*lgweight
            ap=0
        elif vals[4] < vals[5]:
            hp=0
            ap=3*lgweight
        else:
            hp=lgweight
            ap=lgweight
    last_game_time[vals[2]]=vals[0]
    last_game_time[vals[3]]=vals[0]
    fatigue_degree[vals[2]]=h_fatigue
    fatigue_degree[vals[3]]=a_fatigue
    if vals[2] in points and h_new_season is not True:
        points[vals[2]]+=hp
    else:
        points[vals[2]] = hp
    if vals[3] in points and a_new_season is not True:
        points[vals[3]]+=ap
    else:
        points[vals[3]]=ap
    #print(vals[0],vals[1],vals[2],vals[3],points[vals[2]]-hp,points[vals[3]]-ap,h_fatigue,a_fatigue,vals[4],vals[5])
    line = vals[0].strftime("%Y-%m-%d %H:%M:%S")+','+vals[1]+','+vals[2]+','+vals[3]+','+str(points[vals[2]]-hp)+','+str(points[vals[3]]-ap)+','+str(h_fatigue)+','+str(a_fatigue)+','+str(vals[4])+','+str(vals[5])
    updatesql='update jc.t500 set h_points='+str('%.2f' %(points[vals[2]]-hp))+', a_points='+str('%.2f' %(points[vals[3]]-ap))+', h_fatigue='+str('%.2f' % h_fatigue)+', a_fatigue='+str('%.2f' %a_fatigue)+' where gametime="'+vals[0].strftime("%Y-%m-%d %H:%M:%S")+'" and lg="'+vals[1]+'" and homesxname="'+vals[2]+'" and awaysxname="'+vals[3]+'"'
    cur_g.execute(updatesql)
    conn_g.commit()
    #print(line)
    #output_file.write(line+'\n')



cur_g.close()
conn_g.close()