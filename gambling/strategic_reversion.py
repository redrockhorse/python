# -*- coding: utf8 -*-
# !/usr/bin/python
# 策略复盘
__author__ = 'mahy'

import pymysql
import sys
import datetime
import numpy as np
import decimal

conn=pymysql.connect(host='127.0.0.1',user='root',passwd='Qd@#$mo658',db='jc',port=3306,charset='utf8', cursorclass = pymysql.cursors.DictCursor)
cursor = conn.cursor()



#复盘主题方法
def replay():
    print('sss')
    games =[]
    sql= "select gametime,lg,homesxname,awaysxname,win,draw,lost,win_rq,draw_rq,lost_rq,rq,chupan_l,ypbegin,chupan_r,jishi_l,ypbegin,jishi_r,hscore,ascore from  jc.tb_rate_power_rs where lg like '%世%界%' and gametime>'2018-01-01 00:00:00' and resulenum is not null  order by gametime asc;"
    cursor.execute(sql)
    results = cursor.fetchall()
    money_begin=money_left = 10000
    #money_left = 1000
    money_ret =0
    money_wave = []
    money_wave.append(money_begin)
    lastgame = None
    for row in results:
        if lastgame == None:
            op, money_buy, money_ret = strategy(row, money_begin)
            money_left = money_begin-money_buy
            #money_wave.append(money_begin-money_buy)
        else:
            time_dif = row['gametime']-lastgame['gametime']
            #print(time_dif.days)
            if (time_dif.total_seconds()/60/60)>6:#结算
                money_left = money_left+money_ret
                money_wave.append(money_left)

                op, money_buy, money_ret = strategy(row, money_left)
                money_left = money_left - money_buy

            else:
                op, money_buy_s, money_ret_s = strategy(row, money_left)
                money_ret = money_ret+money_ret_s
                money_left = money_left - money_buy_s
        lastgame = row
    print(money_wave)






#策略 输入比赛信息，总金额，输出押注选项（胜负平，让球胜负平，）/押注金额，中奖金额
def strategy(game,money):
    oplist =['win','draw','lost','win_rq','draw_rq','lost_rq']
    opvlist = [game['win'],game['draw'],game['lost'],game['win_rq'],game['draw_rq'],game['lost_rq']]
    #oplist =['win','draw','lost']
    #opvlist = [game['win'],game['draw'],game['lost']]
    op=''
    money_buy =0
    money_ret =0
    zhong_flag = False

    if money > 2:
        #最大最小赔率法

        ''' '''
        myop = max(opvlist)
        myopindex = opvlist.index(myop)
        op = oplist[myopindex]
        money_buy = 200


        '''
         凯利值法
        
        ret_rate = decimal.Decimal(0.89)
        kylist = []
        #win_ky = (0.89-(1-0.89/game['win']))/game['win']
        for key in opvlist:
            kylist.append((ret_rate-(1-ret_rate/key))/key)
        myky = max(kylist)
        mykyindex = kylist.index(myky)
        op = oplist[mykyindex]
        myop  = opvlist[mykyindex]
        if myky<=0:
            return op, money_buy, money_ret
        money_buy = int(money*myky/2)*2
        '''


        rq_num = int(game['hscore']) - int(game['ascore']) + int(game['rq'])
        if rq_num>0:
            rs_rq = "win_rq"
        elif rq_num<0:
            rs_rq = "lost_rq"
        else:
            rs_rq = "draw_rq"

        num = int(game['hscore']) - int(game['ascore'])
        if num>0:
            rs = "win"
        elif num<0:
            rs = "lost"
        else:
            rs= "draw"

        if op == rs or op == rs_rq:
            zhong_flag = True
            money_ret = money_buy * myop
        #money_ret = 200 * maxop
    else:#钱数少于0进入破产清算流程
        pass
    print(game)
    print(money,op,money_buy,money_ret,rs,rs_rq,zhong_flag)
    return op,money_buy,money_ret






if __name__ == "__main__":
    replay()
    #print(sys.path)