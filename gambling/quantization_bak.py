# -*- coding: utf-8 -*-
# encoding=utf-8
__author__ = 'mahy'
import numpy as np
import pymysql

'''
量化
'''
conn_g = pymysql.connect(host='127.0.0.1', user='root', passwd='Qd@#$mo658', db='jc', port=3318, charset='utf8')
cur_g = conn_g.cursor()
#g_sql = "select gametime,lg,homesxname,awaysxname,hscore,ascore,win,draw,lost,rq,win_rq,draw_rq,lost_rq from tb_rate_power_rs where resulenum is not null  and lg != '友谊赛' and lg != '球会友谊' and lg != '公开赛' order by  gametime asc; "
g_sql = "select gametime,lg,homesxname,awaysxname,hscore,ascore,win,draw,lost,rq,win_rq,draw_rq,lost_rq from tb_rate_power_rs where  lg != '友谊赛' and lg != '球会友谊' and lg != '公开赛' order by  gametime asc; "
t_group = {}
g_group = {}
split_days = 60.00
fatigue_w = 5.00
pre_w = 1.00
lg_w_group = {'意甲': 1, '法甲': 1, '西甲': 1, '英超': 1, '德甲': 1, '欧冠': 1, '欧冠杯': 1, '欧洲杯': 1, '世界杯': 1, '世外北美': 1, '世外非洲': 1,
              '世外南美': 1, '世外欧洲': 1, '世外亚洲': 1, '亚洲杯': 1}
ha_w = 1.00
g_list = []

u_l_d = 10.00
upper_w = 0.8
lower_w = 1.2

output_file = open("E:\\1579\\\lianghua\\ouguan20171124_2.txt", "w+")


class TInfo:
    tname = ''
    new_season = False
    p = 0.0
    fatigue = 0.0
    round_n = 1

    def __init__(self, tname, new_season, p, fatigue, round_n):
        self.tname = tname
        self.new_season = new_season
        self.p = p
        self.fatigue = fatigue
        self.round_n = round_n


class GInfo:
    gtime = ''
    lg = ''
    ht = None
    at = None
    hscore = 0
    ascore = 0
    w = 0.0
    d = 0.0
    l = 0.0
    r = 1
    wr = 0.0
    dr = 0.0
    lr = 0.0

    def __init__(self, gtime, lg, ht, at, hscore, ascore, w, d, l, r, wr, dr, lr):
        self.gtime = gtime
        self.lg = lg
        self.ht = ht
        self.at = at
        self.hscore = hscore
        self.ascore = ascore
        self.w = w
        self.d = d
        self.l = l
        self.r = r
        self.wr = wr
        self.dr = dr
        self.lr = lr

    def output(self):
        # print(self.gtime, self.lg, self.ht.tname, self.at.tname,self.ht.p,self.at.p,self.ht.fatigue,self.at.fatigue,self.hscore,self.ascore, self.w, self.d, self.l, self.r, self.wr, self.dr, self.lr)
        line = self.gtime.strftime(
            "%Y-%m-%d %H:%M:%S") + "," + self.lg + "," + self.ht.tname + "," + self.at.tname + "," + str(
            self.ht.p) + "," + str(self.at.p) + "," + str(self.ht.fatigue) + "," + str(self.at.fatigue) + "," + str(
            self.hscore) + "," + str(self.ascore) + "," + str(self.ht.round_n) + "," + str(self.at.round_n) + "," + str(
            self.w) + "," + str(self.d) + "," + str(self.l) + "," + str(self.r) + "," + str(self.wr) + "," + str(
            self.dr) + "," + str(self.lr)
        print(line)
        output_file.write(line + '\n')


def init():
    cur_g.execute(g_sql)
    result = cur_g.fetchall()
    for vals in result:
        gtime = vals[0]  # str2datetime
        lg = vals[1]
        hname = vals[2]
        aname = vals[3]
        hscore = vals[4]
        ascore = vals[5]
        w = vals[6]
        d = vals[7]
        l = vals[8]
        r = vals[9]
        wr = vals[10]
        dr = vals[11]
        lr = vals[12]

        ht = None
        htupdate = None
        at = None
        atupdate = None
        h_d_days = 0
        a_d_days = 0

        ht = TInfo(hname, True, 0.0, 0.0, 1)
        htupdate = TInfo(hname, True, 0.0, 0.0, 1)
        if hname in g_group:
            prev_g = g_group[hname]
            h_d_days = (gtime - prev_g.gtime).days
            ht_tmp = g_group[hname].ht if g_group[hname].ht.tname == hname else g_group[hname].at
            if h_d_days < split_days and ht_tmp.round_n < 60:
                ht = ht_tmp
                if ht.tname != hname:
                    print("----------------------------------------------------")
                    print(hname)
                    print(g_group[hname].ht.tname)
                    print(g_group[hname].at.tname)
                    print("----------------------------------------------------")
                    ht = None
                ht.new_season = False
                htupdate.new_season = False
                htupdate.round_n = ht.round_n + 1

        at = TInfo(aname, True, 0.0, 0.0, 1)
        atupdate = TInfo(aname, True, 0.0, 0.0, 1)
        if aname in g_group:
            prev_g = g_group[aname]
            a_d_days = (gtime - prev_g.gtime).days
            at_tmp = g_group[aname].at if g_group[aname].at.tname == aname else g_group[aname].ht
            if a_d_days < split_days and at_tmp.round_n < 60:
                at = at_tmp
                if at.tname != aname:
                    print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
                    print(aname)
                    print(g_group[aname].at.tname)
                    print(g_group[aname].ht.tname)
                    print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
                    at = None
                at.new_season = False
                atupdate.new_season = False
                atupdate.round_n = at.round_n + 1


        # out put
        g_info = GInfo(gtime, lg, ht, at, hscore, ascore, w, d, l, r, wr, dr, lr)

        # update
        g_info.output()
        if lg in lg_w_group:
            pass
        else:
            lg_w_group[lg] = 0.8
        hp = 0
        ap = 0
        new_season = ht.new_season or at.new_season
        if hscore > ascore:
            hp = 3 * lg_w_group[lg]
            ap = 0
        elif hscore == ascore:
            hp = 1 * lg_w_group[lg]
            ap = 1 * lg_w_group[lg]
        else:
            hp = 0
            ap = 3 * lg_w_group[lg]
        if new_season:
            pass
        else:
            if ht.p - at.p > u_l_d:
                hp = hp * upper_w
                ap = ap * lower_w
            if at.p - ht.p > u_l_d:
                hp = hp * lower_w
                ap = ap * upper_w
        htupdate.p = ht.p + hp
        atupdate.p = at.p + ap

        hf = 0
        af = 0
        hf = 0.7 - np.tanh(h_d_days / fatigue_w)
        af = 0.7 - np.tanh(a_d_days / fatigue_w)
        if ht.fatigue + hf < 0:
            htupdate.fatigue = 0
        else:
            htupdate.fatigue = ht.fatigue + hf
        if at.fatigue + af < 0:
            atupdate.fatigue = 0
        else:
            atupdate.fatigue = at.fatigue + af
        g_info_new = GInfo(gtime, lg, htupdate, atupdate, hscore, ascore, w, d, l, r, wr, dr, lr)
        g_group[hname] = g_info_new
        g_group[aname] = g_info_new


if __name__ == "__main__":
    init()
    cur_g.close()
    conn_g.close()
