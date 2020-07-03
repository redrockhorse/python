__author__ = 'mahy'
# -*- coding: utf8 -*-
# 分析联赛信息
import pymysql
from collections import Counter
import numpy as np
from flask import Flask
import json
app = Flask(__name__)


conn = pymysql.connect(host='127.0.0.1', user='root', passwd='Qd@#$mo658', db='jc', port=3306, charset='utf8',
                       cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()


def getP():
    dic = {}
    sql = "select a.hname,a.tw/b.t as p from (select hname,count(1) as tw from tb_okooo_league_odds where win <>'-' and hg+0 > ag+0  group by hname) a,(select hname,count(1) as t from tb_okooo_league_odds where win <>'-'   group by hname) b where a.hname=b.hname;"
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        dic[row['hname']] = row['p']
    return dic


def getB():
    dic = {}
    sql = "select  hname,avg(win) as b from tb_okooo_league_odds where win <>'-' group by hname order by avg(win) asc;"
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        dic[row['hname']] = row['b']
    return dic

def getScore(hg,ag):
    if hg+0>ag+0:
        return ((hg-ag)*0.1-0.1)*3
    if hg+0 == ag+0:
        return 1
    if hg+0 < ag+0:
        return (hg - ag) * 0.1 + 0.1

def getAnalysisStrength(season,round):
    sql = "select hname,aname,round,season,hg,ag,case when hg>ag then win when hg=ag then draw when hg<ag then lost end b,win,draw,lost from tb_okooo_league_odds where lg='德甲' and hg<>''  and win <> '-' and season='"+season+"' and round+0<"+str(round)+" order by season,round+0,gametime asc;"  # and hname='多特蒙德'
    cursor.execute(sql)
    results = cursor.fetchall()
    last_round = ''
    last_season = ''
    strength_dic ={}
    for row in results:
        #print(row)
        hname = row['hname']
        aname = row['aname']
        season = row['season']
        hg = int(row['hg'])
        ag = int(row['ag'])
        if hname+'_'+season not in strength_dic:
            strength_dic[hname + '_' + season] = 0
        if aname+'_'+season not in strength_dic:
            strength_dic[aname + '_' + season] = 0
        sd = strength_dic[hname + '_' + season] - strength_dic[aname + '_' + season]
        weight = 1
        if sd >= 10:
            weight = 0.8
        if sd <= -10:
            weight = 1.2
        gd = hg-ag
        if gd > 0:
            strength_dic[hname + '_' + season] += 3 * weight
            strength_dic[aname + '_' + season] += 0
        if gd == 0:
            strength_dic[hname + '_' + season] += 1 * weight
            strength_dic[aname + '_' + season] += 1 * (2-weight)
        if gd < 0:
            strength_dic[hname + '_' + season] += 0
            strength_dic[aname + '_' + season] += 3*(2-weight)
    #print(strength_dic)
    #strength_dic = sorted(strength_dic.items(), key=lambda item: item[1], reverse=True)
    tmp_dic = {}
    #print(strength_dic)
    for key in strength_dic:
        tmp_dic[key] = strength_dic[key]
    tmp_list = sorted(tmp_dic.items(), key=lambda item: item[1], reverse=True)
    print(tmp_list)

    '''
    for key in strength_dic:
        if key.find('_19/20') != -1:
            #print(key,strength_dic[key])
            tmp_dic[key] = strength_dic[key]
    tmp_list = sorted(tmp_dic.items(), key=lambda item: item[1], reverse=True)
    print(tmp_list)

    tmp_dic = {}
    for key in strength_dic:
        if key.find('_18/19') != -1:
            # print(key,strength_dic[key])
            tmp_dic[key] = strength_dic[key]
    tmp_list = sorted(tmp_dic.items(), key=lambda item: item[1], reverse=True)
    print(tmp_list)
    '''






def getGListByLg():
    sql = "select hname,aname,hg-ag,case when hg>ag then win when hg=ag then draw when hg<ag then lost end b,win,draw,lost from tb_okooo_league_odds where lg='德甲' and (hname='莱比锡' or aname ='沃尔夫斯堡') and win <> '-' order by season,round+0,gametime asc;"#and hname='多特蒙德'
    cursor.execute(sql)
    results = cursor.fetchall()
    hdic = {}
    adic = {}
    tarr = []
    cold_value_arr =[]
    r_value_arr = []
    sigma = 1.4570050325206478
    mu = 2.8225
    for row in results:
        print(row)
        max_v = max(row['win'],row['draw'],row['lost'])
        min_v = min(row['win'], row['draw'], row['lost'])
        cold_score = 0
        cold_value = (float(row['b']) - float(min_v))/(float(max_v) - float(min_v))*float(row['b'])
        x = abs(float(min_v) - float(row['b']))
        if x >= 0.5 * sigma and x < sigma:
            cold_score = 1
            # print(row['win'], row['draw'], row['lost'], row['hg-ag'])
        if x >=  sigma:
            cold_score = 3
            #print(row['win'], row['draw'], row['lost'], row['hg-ag'])

        tarr.append(cold_score)
        cold_value_arr.append(cold_value)
        r_value_arr.append(float(row['b']))
        # print(row['hname'],row['aname'],cold_score,row['win'],row['draw'],row['lost'],row['hg-ag'])
        # print(row['hname'], row['aname'], cold_score, cold_value,row['win'],row['draw'],row['lost'],)
    # print(np.mean(cold_value_arr)*Counter(tarr)[3]/Counter(tarr)[0])
    print(Counter(tarr))
    print(np.mean(r_value_arr))
    print(np.median(r_value_arr))
    counts = np.bincount(r_value_arr)
    # 返回众数
    print(np.argmax(counts))
    print(np.std(r_value_arr,ddof=1))
        # hname = row['hname']
        # aname = row['aname']
        # hg = row['hg']
        # ag = row['ag']
        # s = getScore(hg,ag)
        # if hname not in hdic:
        #     hdic[hname] = 0
        # if aname not in adic:
        #     adic[aname] = 0
        # hdic[hname] = hdic[hname]+(row['hg']-row['ag'])*row['win']/row['lost']

@app.route('/')
def index():
    return "Hello, World!"

if __name__ == '__main__':
    # pdic = getP()
    # bdic = getB()
    # kdic = {}
    # for hname in pdic:
    #     p = pdic[hname]
    #     b = bdic[hname]
    #     kdic[hname] = (b * float(p) - 1 + float(p)) / b
    # kdic = sorted(kdic.items(), key=lambda item: item[1], reverse=True)
    #print(kdic)
    #getGListByLg()
    total =39
    curr = 9
    getAnalysisStrength('16/17', curr)
    getAnalysisStrength('16/17', total)
    getAnalysisStrength('17/18',curr)
    getAnalysisStrength('17/18', total)
    getAnalysisStrength('18/19', curr)
    getAnalysisStrength('18/19', total)
    getAnalysisStrength('19/20', curr)
    getGListByLg()
    #app.run(host="0.0.0.0", port=5000, debug=True)

