#!/usr/bin/python
#encoding=utf-8
__author__ = 'mahy'
'''
在澳客网抓取比赛基本信息
'''
from lxml import etree
import httplib2
import re
import random
import time
import MySQLdb
import datetime

conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='Qd@#$mo658',db='jc',port=3306,charset='utf8')
cur = conn.cursor()
num_pattern= re.compile(r'\d*')

def getGameList(datastr):
    url = "http://www.okooo.com/jingcai/"+datastr+"/"
    http = httplib2.Http()
    response, content = http.request(url, 'GET',headers = {
        'Host': 'www.okooo.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Referer': 'http://www.okooo.com/',
       # 'Cookie': 'pgv_pvi=1297987712; FirstURL=www.okooo.com/; FirstOKURL=http%3A//www.okooo.com/jingcai/; First_Source=www.okooo.com; Last_Source=http%3A//www.okooo.com/User/partner/PartnerLogin.php; userCustomLottery=SportteryWDL%2CSportteryScore%2CSportteryNWDL%2CSportterySoccerMix%2CWDL%2CScore%2CTotalGoals; PHPSESSID=6d7f438b142b6a96bbadd8202e03ef9c349e5d0d; OKSID=90ce4f063ce7b001f1068cc879db39942efa7b54; M_UserName=%2213633473448%22; M_UserID=18564539; M_Ukey=de52cd817a93ed1ed03e143104707ef2; OkTouchAutoUuid=e351c2cc54fccfa1640fd8ac6886d082; OkTouchMsIndex=7; DRUPAL_LOGGED_IN=Y; IMUserID=18564539; IMUserName=13633473448; OkAutoUuid=4e081ac6d8fe7c3117d1745b5cd2a2f1; OkMsIndex=7; isInvitePurview=0; UWord=220950c35d78e9edfb5d9acdedddc46066c; _ga=GA1.2.76133388.1431060652; LastUrl=; Hm_lvt_5ffc07c2ca2eda4cc1c4d8e50804c94b=1491836117,1491884815,1492247525,1492248799; Hm_lpvt_5ffc07c2ca2eda4cc1c4d8e50804c94b=1492251441; showCustomMenu=2; __utma=56961525.76133388.1431060652.1491884741.1492247508.90; __utmb=56961525.53.8.1492251441307; __utmc=56961525; __utmz=56961525.1488543216.65.35.utmcsr=baidu|utmccn=(organic)|utmcmd=organic',
       #'Cookie':cookie,
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    })

    tree = etree.HTML(content)
    gamelist = tree.xpath(u'//div[@class="touzhu_1"]')

    for g in gamelist:
        time.sleep(random.randint(3, 10))
        #id = datastr.replace('-','')+g.get('data-morder')
        morder = g.get('data-morder')
        okid = g.get('data-mid')
        try:
            getGameBaseInfo(okid,morder)
        except Exception:
            print("error",okid,morder)
        continue

def getGameBaseInfo(okid, morder):
    # id=id
    okid = okid
    gametime = None
    lg = None
    hmname = None
    ayname = None
    season = None
    gamerule = None
    round = None
    field = None
    weather = None
    temperature = None
    h_t_w = None
    h_t_d = None
    h_t_l = None
    h_t_s = None
    h_t_o = None
    h_h_w = None
    h_h_d = None
    h_h_l = None
    h_h_s = None
    h_h_o = None
    a_t_w = None
    a_t_d = None
    a_t_l = None
    a_t_s = None
    a_t_o = None
    a_a_w = None
    a_a_d = None
    a_a_l = None
    a_a_s = None
    a_a_o = None
    hscore = None
    ascore = None
    h_hs = None
    h_as = None
    url = 'http://www.okooo.com/soccer/match/' + okid + '/history/'
    http = httplib2.Http()
    response, content = http.request(url, 'GET', headers={
        'Host': 'www.okooo.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Referer': 'http://www.okooo.com/',
        # 'Cookie': 'pgv_pvi=1297987712; FirstURL=www.okooo.com/; FirstOKURL=http%3A//www.okooo.com/jingcai/; First_Source=www.okooo.com; Last_Source=http%3A//www.okooo.com/User/partner/PartnerLogin.php; userCustomLottery=SportteryWDL%2CSportteryScore%2CSportteryNWDL%2CSportterySoccerMix%2CWDL%2CScore%2CTotalGoals; PHPSESSID=6d7f438b142b6a96bbadd8202e03ef9c349e5d0d; OKSID=90ce4f063ce7b001f1068cc879db39942efa7b54; M_UserName=%2213633473448%22; M_UserID=18564539; M_Ukey=de52cd817a93ed1ed03e143104707ef2; OkTouchAutoUuid=e351c2cc54fccfa1640fd8ac6886d082; OkTouchMsIndex=7; DRUPAL_LOGGED_IN=Y; IMUserID=18564539; IMUserName=13633473448; OkAutoUuid=4e081ac6d8fe7c3117d1745b5cd2a2f1; OkMsIndex=7; isInvitePurview=0; UWord=220950c35d78e9edfb5d9acdedddc46066c; _ga=GA1.2.76133388.1431060652; LastUrl=; Hm_lvt_5ffc07c2ca2eda4cc1c4d8e50804c94b=1491836117,1491884815,1492247525,1492248799; Hm_lpvt_5ffc07c2ca2eda4cc1c4d8e50804c94b=1492251441; showCustomMenu=2; __utma=56961525.76133388.1431060652.1491884741.1492247508.90; __utmb=56961525.53.8.1492251441307; __utmc=56961525; __utmz=56961525.1488543216.65.35.utmcsr=baidu|utmccn=(organic)|utmcmd=organic',
        # 'Cookie':cookie,
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    })
    tree = etree.HTML(content)
    lunci_div = tree.xpath(u'//div[@id="lunci"]')
    span = lunci_div[0].xpath(u'div/p')
    a1 = span[0].xpath(u'span/a')
    lg = a1[0].text
    season = a1[1].text
    if len(span) > 1:
        a2 = span[1].xpath(u'span/a')
        gamerule = a2[0].text
    span1 = lunci_div[0].xpath(u'div/span[1]')
    round = span1[0].text

    qbx_2_div = tree.xpath(u'//div[@class="qbx_2"]')
    qbx_2_p = qbx_2_div[0].xpath(u'p')
    gametime = qbx_2_p[0].text.replace(u'\xa0', u' ')
    field = qbx_2_p[1].text
    weather = qbx_2_p[2].text
    qbx_2_span = qbx_2_p[2].xpath(u'span')
    temperature = qbx_2_span[0].text
    hnamediv = tree.xpath(u'//div[@class="qpai_zi"]')
    hmname = hnamediv[0].text
    anamediv = tree.xpath(u'//div[@class="qpai_zi_1"]')
    ayname = anamediv[0].text

    shuju_div = tree.xpath(u'//div[@class="shuj"]')
    shuju_tb = shuju_div[0].xpath(u'table')
    h_tb = shuju_tb[0]
    h_tr1 = h_tb.xpath(u'tr[1]')
    h_td = h_tr1[0].xpath(u'td')
    htwdl = re.findall(r"\d+\.?\d*", h_td[1].text)
    if len(htwdl) == 3:
        h_t_w = htwdl[0]
        h_t_d = htwdl[1]
        h_t_l = htwdl[2]
    h_t_s_a = re.findall(r"\d+\.?\d*", h_td[2].text)
    if len(h_t_s_a) > 0:
        h_t_s = h_t_s_a[0]
    h_t_o_a = re.findall(r"\d+\.?\d*", h_td[3].text)
    if len(h_t_o_a) > 0:
        h_t_o = h_t_o_a[0]

    h_tr2 = h_tb.xpath(u'tr[2]')
    h_td2 = h_tr2[0].xpath(u'td')
    hhwdl = re.findall(r"\d+\.?\d*", h_td2[1].text)
    if len(hhwdl) == 3:
        h_h_w = hhwdl[0]
        h_h_d = hhwdl[1]
        h_h_l = hhwdl[2]
    h_h_s_a = re.findall(r"\d+\.?\d*", h_td2[2].text)
    if len(h_h_s_a) > 0:
        h_h_s = h_h_s_a[0]
    h_h_o_a = re.findall(r"\d+\.?\d*", h_td2[3].text)
    if len(h_h_o_a) > 0:
        h_h_o = h_h_o_a[0]

    shuju_tb = shuju_div[0].xpath(u'table')
    a_tb = shuju_tb[1]
    a_tr1 = a_tb.xpath(u'tr[1]')
    a_td = a_tr1[0].xpath(u'td')
    atwdl = re.findall(r"\d+\.?\d*", a_td[1].text)
    if len(atwdl) == 3:
        a_t_w = atwdl[0]
        a_t_d = atwdl[1]
        a_t_l = atwdl[2]
    a_t_s_a = re.findall(r"\d+\.?\d*", a_td[2].text)
    if len(a_t_s_a) > 0:
        a_t_s = a_t_s_a[0]
    a_t_o_a = re.findall(r"\d+\.?\d*", a_td[3].text)
    if len(a_t_o_a) > 0:
        a_t_o = a_t_o_a[0]

    a_tr2 = a_tb.xpath(u'tr[2]')
    a_td2 = a_tr2[0].xpath(u'td')
    aawdl = re.findall(r"\d+\.?\d*", a_td2[1].text)
    if len(aawdl) == 3:
        a_a_w = aawdl[0]
        a_a_d = aawdl[1]
        a_a_l = aawdl[2]
    a_a_s_a = re.findall(r"\d+\.?\d*", a_td2[2].text)
    if len(a_a_s_a) > 0:
        a_a_s = a_a_s_a[0]
    a_a_o_a = re.findall(r"\d+\.?\d*", a_td2[3].text)
    if len(a_a_o_a) > 0:
        a_a_o = a_a_o_a[0]

    vs_div = tree.xpath(u'//div[@class="vs"]')
    vs_span = vs_div[0].xpath(u'span')
    if len(vs_span) > 1:
        hscore = vs_span[0].text
        ascore = vs_span[1].text
    jifen_dashi_div = tree.xpath(u'//div[@class="jifen_dashi"]')
    if len(jifen_dashi_div) > 0:
        jifen_p = jifen_dashi_div[0].xpath(u'p')
        if len(jifen_p) > 0:
            halfsocre = re.findall(r"\d+\.?\d*", jifen_p[0].text)
            if len(halfsocre) > 1:
                h_hs = halfsocre[0]
                h_as = halfsocre[1]
    gametime = '20' + gametime
    id = gametime.split(' ')[0].replace('-', '') + morder
    print(id, okid, gametime, lg, hmname, ayname, season, gamerule, round, field, weather, temperature, h_t_w, h_t_d,
          h_t_l, h_t_s, h_t_o, h_h_w, h_h_d, h_h_l, h_h_s, h_h_o, a_t_w, a_t_d, a_t_l, a_t_s, a_t_o, a_a_w, a_a_d,
          a_a_l, a_a_s, a_a_o, hscore, ascore, h_hs, h_as)
    delete_sql = 'delete from td_ok_gamebaseinfo where Id="' + id + '"'
    sql = "INSERT INTO `td_ok_gamebaseinfo` (`id`,`okid`,`gametime`,`lg`,`hmname`,`ayname`,`season`,`gamerule`,`round`,`field`,`weather`,`temperature`,`h_t_w`,`h_t_d`,`h_t_l`,`h_t_s`,`h_t_o`,`h_h_w`,`h_h_d`,`h_h_l`,`h_h_s`,`h_h_o`,`a_t_w`,`a_t_d`,`a_t_l`,`a_t_s`,`a_t_o`,`a_a_w`,`a_a_d`,`a_a_l`,`a_a_s`,`a_a_o`,`hscore`,`ascore`,`h_hs`,`h_as`)  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    cur.execute(delete_sql)
    cur.execute(sql, (
    id, okid, gametime, lg, hmname, ayname, season, gamerule, round, field, weather, temperature, h_t_w, h_t_d, h_t_l,
    h_t_s, h_t_o, h_h_w, h_h_d, h_h_l, h_h_s, h_h_o, a_t_w, a_t_d, a_t_l, a_t_s, a_t_o, a_a_w, a_a_d, a_a_l, a_a_s,
    a_a_o, hscore, ascore, h_hs, h_as))
    conn.commit()



if __name__=="__main__":
    sqlmin='select min(gametime) from td_ok_gamebaseinfo'
    #datastr = '2017-08-11'
    #getGameList(datastr)
    cur.execute(sqlmin)
    results = cur.fetchall()
    if(len(results)>0):
        if(len(results[0])>0):
            row=results[0]
            if(len(row)>0):
                mindate=row[0]
                if mindate != None:
                    for i in range(366):
                        hisdate = mindate - datetime.timedelta(days=i)
                        getGameList(hisdate.strftime("%Y-%m-%d"))
                else:
                    for i in range(366):
                        datestr = datetime.datetime.now()-datetime.timedelta(days=i)
                        getGameList(datestr.strftime("%Y-%m-%d"))
    cur.close()
    conn.close()