#!/usr/bin/python  
#encoding=utf-8  
__author__ = 'mahy'
from BeautifulSoup import BeautifulSoup
import urllib2
import sys
import re
import MySQLdb
import datetime
import time
conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='root',db='jc',port=3306,charset='utf8')#
cur = conn.cursor()
reload(sys)
sys.setdefaultencoding('utf8')
date_pattern = re.compile(r'\d*-\d*-\d*')
time_pattern = re.compile(r'\d*:\d*')
num_pattern= re.compile(r'\d*')
score_pattern= re.compile(r'\d*-\d*')
def getGameList(url):
    resContent  = urllib2.urlopen(url).read()
    soup = BeautifulSoup(resContent)
    baseInfo_list=soup.findAll("div",attrs={"class": "touzhu_1"})
    n = len(baseInfo_list)
    for i in range(n):
        getGameBaseInfo(baseInfo_list[i]['data-mid'])

def getGameBaseInfo(mid):
    time.sleep(1)
    exc_url='http://www.okooo.com/soccer/match/'+mid+'/history/'
    print exc_url
    req = urllib2.Request(exc_url)
    req.add_header('Host','www.okooo.com')
    req.add_header('Referer','http://www.okooo.com/jingcai/')
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36')
    req.add_header('Cookie','FirstURL=www.okooo.com/; FirstOKURL=http://www.okooo.com/jingcai/; First_Source=www.okooo.com; pgv_pvi=1297987712; PHPSESSID=c121eb6d1393141538968660f29b335cd3d50e02; userCustomLottery=SSQ%2CSportteryNWDL%2CSportteryScore%2CSportteryWDL%2CSportterySoccerMix%2CToTo%2CSuperLotto%2CWDL; IMUserID=18564539; IMUserName=13633473448; UWord=d451d8cd981f00b204e9800998ecf84827e; LastUrl=; Hm_lvt_5ffc07c2ca2eda4cc1c4d8e50804c94b=1477483622,1477568686,1477696697,1477717587; Hm_lpvt_5ffc07c2ca2eda4cc1c4d8e50804c94b=1477717615; showCustomMenu=2; __utma=56961525.76133388.1431060652.1477712069.1477717545.33; __utmb=56961525.10.7.1477717614276; __utmc=56961525; __utmz=56961525.1477717545.33.27.utmcsr=baidu|utmccn=(organic)|utmcmd=organic')
    resContent_exc  = urllib2.urlopen(req).read()
    soup_exc = BeautifulSoup(resContent_exc,fromEncoding='gb18030')
    hname=soup_exc.findAll("div",attrs={"class": "qpai_zi"})
    aname=soup_exc.findAll("div",attrs={"class": "qpai_zi_1"})
    ptime_div=soup_exc.findAll("div",attrs={"class": "qbx_2"})
    vs_div=soup_exc.findAll("div",attrs={"class": "vs"})
    vs_span=vs_div[0].findAll('span')
    hscore_str=''
    ascore_str=''
    gameresult=None
    score_dif=None
    if(vs_span != None and len(vs_span)>1):
        hscore_str=vs_span[0].string
        ascore_str=vs_span[1].string
        hscore=int(hscore_str)
        ascore=int(ascore_str)
        gameresult = reduce(lambda x,y : 3 if x > y  else 1 if x==y else 0,[hscore,ascore])
        score_dif = hscore-ascore
    score=hscore_str+'-'+ascore_str
    ptime='20'+ptime_div[0].findAll('p')[0].string
    datestr=date_pattern.search(ptime).group()
    timestr=time_pattern.search(ptime).group()
    ptime=datestr+' '+timestr
    lg_div=soup_exc.findAll("div",attrs={"class": "qbx_1"})
    lg=lg_div[0].findAll('a')[0].string
    lg_round = None
    if(len(lg_div[0].findAll('span'))>1):
        lg_round=lg_div[0].findAll('span')[-1].string
    hname= hname[0].string
    aname= aname[0].string
    ranking_div=soup_exc.findAll("div",attrs={"class": "shuj"})
    ht_ranking_info=''
    ht_ranking_point='0'
    ht_ranking='0'
    h_ranking_info=''
    h_ranking_point='0'
    h_ranking='0'
    at_ranking_info=''
    at_ranking_point='0'
    at_ranking='0'
    a_ranking_info=''
    a_ranking_point='0'
    a_ranking='0'

    if(len(ranking_div)>0):
        ranking_table=ranking_div[0].findAll("table")
        if(len(ranking_table)>1):
            trs=ranking_table[0].findAll("tr")
            if(len(trs)>1):
                tds=trs[0].findAll("td")
                if(len(tds)>3):
                    ht_ranking_info=tds[1].string
                    ht_ranking_point=num_pattern.search(tds[2].string).group()
                    ht_ranking=num_pattern.search(tds[3].string).group()
                    ht_ranking_point=ht_ranking_point if ht_ranking_point  else '0'
                    ht_ranking=ht_ranking if ht_ranking  else '0'
                tds=trs[1].findAll("td")
                if(len(tds)>3):
                    h_ranking_info=tds[1].string
                    h_ranking_point=num_pattern.search(tds[2].string).group()
                    h_ranking=num_pattern.search(tds[3].string).group()
                    h_ranking_point=h_ranking_point if h_ranking_point  else '0'
                    h_ranking=h_ranking if h_ranking  else '0'

            trs=ranking_table[1].findAll("tr")
            if(len(trs)>1):
                tds=trs[0].findAll("td")
                if(len(tds)>3):
                    at_ranking_info=tds[1].string
                    at_ranking_point=num_pattern.search(tds[2].string).group()
                    at_ranking=num_pattern.search(tds[3].string).group()
                    at_ranking_point=at_ranking_point if at_ranking_point  else '0'
                    at_ranking=at_ranking if at_ranking  else '0'

                tds=trs[1].findAll("td")
                if(len(tds)>3):
                    a_ranking_info=tds[1].string
                    a_ranking_point=num_pattern.search(tds[2].string).group()
                    a_ranking=num_pattern.search(tds[3].string).group()
                    a_ranking_point=a_ranking_point if a_ranking_point  else '0'
                    a_ranking=a_ranking if a_ranking  else '0'
    half_score =None
    half_score_div=soup_exc.findAll("div",attrs={"class": "jifen_dashi"})
    if(len(half_score_div)>0):
        half_score_p=half_score_div[0].findAll("p")
        if(len(half_score_p)>0):
            half_score= score_pattern.search(half_score_p[0].string).group()

    if(hname!=None):
        print '================================================='
        print lg
        print lg_round
        print ptime
        print hname+' vs '+ aname
        print ht_ranking_info+'|'+ht_ranking_point+'|'+ht_ranking
        print h_ranking_info+'|'+h_ranking_point+'|'+h_ranking
        print at_ranking_info+'|'+at_ranking_point+'|'+at_ranking
        print a_ranking_info+'|'+a_ranking_point+'|'+a_ranking
        print hscore_str+' - '+ ascore_str
        print half_score
        print gameresult
        print '================================================='

        delete_sql='delete from td_okooo_gamebaseinfo where ptime="'+ptime+'" and lg="'+lg+'" and hname="'+hname+'" and aname="'+aname+'"'
        sql="INSERT INTO `td_okooo_gamebaseinfo` (`ptime`,`lg`,`lg_round`,`hname`,`aname`,`ht_ranking_info`,`ht_ranking_point`,`ht_ranking`,`h_ranking_info`,`h_ranking_point`,`h_ranking`,`at_ranking_info`,`at_ranking_point`,`at_ranking`,`a_ranking_info`,`a_ranking_point`,`a_ranking`,`gameresult`,`score`,`score_dif`)  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        cur.execute(delete_sql)
        cur.execute(sql,(ptime,lg,lg_round,hname,aname,ht_ranking_info,ht_ranking_point,ht_ranking,h_ranking_info,h_ranking_point,h_ranking,at_ranking_info,at_ranking_point,at_ranking,a_ranking_info,a_ranking_point,a_ranking,gameresult,score,score_dif))
        conn.commit()
if __name__=="__main__":
    print 'start-time:'
    print datetime.datetime.now()
    url='http://www.okooo.com/jingcai/'
    sqlmin='select min(ptime) from td_okooo_gamebaseinfo'
    datestr = ''
    '''
    cur.execute(sqlmin)
    results = cur.fetchall()
    if(len(results)>0):
        if(len(results[0])>0):
            row=results[0]
            if(len(row)>0):
                mindate=row[0]
                hisdate = mindate - datetime.timedelta(days=2)
    '''
    mindate = datetime.datetime.strptime('2013-05-05', "%Y-%m-%d").date()
    for i in range(1800):
        hisdate = mindate - datetime.timedelta(days=i)
        url='http://www.okooo.com/jingcai/'+ hisdate.strftime("%Y-%m-%d")+'/'
        print url
        getGameList(url)
    print 'en-time:'
    print datetime.datetime.now()
    cur.close()
    conn.close()
