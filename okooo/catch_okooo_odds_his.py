#!/usr/bin/python  
#encoding=utf-8  
__author__ = 'mahy'
from BeautifulSoup import BeautifulSoup
import urllib2
import sys
import re
import MySQLdb
import datetime
conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='root',db='jc',port=3306,charset='utf8')
cur = conn.cursor()
reload(sys)
sys.setdefaultencoding('utf8')
date_pattern = re.compile(r'\d*-\d*-\d*')
time_pattern = re.compile(r'\d*:\d*')
num_pattern= re.compile(r'\d*')
score_pattern= re.compile(r'\d*-\d*')
def getGameList(url):
    print url
   # resContent  = urllib2.urlopen(url).read()
    req = urllib2.Request(url)
    req.add_header('Host','www.okooo.com')
    req.add_header('Referer','http://www.okooo.com/jingcai/')
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36')
    req.add_header('Cookie','FirstURL=www.okooo.com/; FirstOKURL=http://www.okooo.com/jingcai/; First_Source=www.okooo.com; pgv_pvi=1297987712; PHPSESSID=c121eb6d1393141538968660f29b335cd3d50e02; userCustomLottery=SSQ%2CSportteryNWDL%2CSportteryScore%2CSportteryWDL%2CSportterySoccerMix%2CToTo%2CSuperLotto%2CWDL; IMUserID=18564539; IMUserName=13633473448; UWord=d451d8cd981f00b204e9800998ecf84827e; LastUrl=; Hm_lvt_5ffc07c2ca2eda4cc1c4d8e50804c94b=1477483622,1477568686,1477696697,1477717587; Hm_lpvt_5ffc07c2ca2eda4cc1c4d8e50804c94b=1477717615; showCustomMenu=2; __utma=56961525.76133388.1431060652.1477712069.1477717545.33; __utmb=56961525.10.7.1477717614276; __utmc=56961525; __utmz=56961525.1477717545.33.27.utmcsr=baidu|utmccn=(organic)|utmcmd=organic')
    resContent  = urllib2.urlopen(req).read()
    soup = BeautifulSoup(resContent)
    baseInfo_list=soup.findAll("div",attrs={"class": "touzhu_1"})
    n = len(baseInfo_list)
    for i in range(n):
        getGameBaseInfo(baseInfo_list[i]['data-mid'])

def getGameBaseInfo(mid):
    exc_url='http://www.okooo.com/soccer/match/'+mid+'/odds/'
    odds_url='http://www.okooo.com/soccer/match/'+mid+'/odds/ajax/?page=0&trnum=0&companytype=BaijiaBooks&type=1'
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
    vs_span = None
    if(vs_div != None and len(vs_div)>0):
        vs_span=vs_div[0].findAll('span')
    oid=mid
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

    half_score =None
    half_score_div=soup_exc.findAll("div",attrs={"class": "jifen_dashi"})
    if(len(half_score_div)>0):
        half_score_p=half_score_div[0].findAll("p")
        if(len(half_score_p)>0):
            half_score= score_pattern.search(half_score_p[0].string).group()

    req = urllib2.Request(odds_url)
    req.add_header('Host','www.okooo.com')
    req.add_header('Referer',exc_url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36')
    req.add_header('Cookie','FirstURL=www.okooo.com/; FirstOKURL=http://www.okooo.com/jingcai/; First_Source=www.okooo.com; pgv_pvi=1297987712; PHPSESSID=c121eb6d1393141538968660f29b335cd3d50e02; userCustomLottery=SSQ%2CSportteryNWDL%2CSportteryScore%2CSportteryWDL%2CSportterySoccerMix%2CToTo%2CSuperLotto%2CWDL; IMUserID=18564539; IMUserName=13633473448; UWord=d451d8cd981f00b204e9800998ecf84827e; LastUrl=; Hm_lvt_5ffc07c2ca2eda4cc1c4d8e50804c94b=1477483622,1477568686,1477696697,1477717587; Hm_lpvt_5ffc07c2ca2eda4cc1c4d8e50804c94b=1477717615; showCustomMenu=2; __utma=56961525.76133388.1431060652.1477712069.1477717545.33; __utmb=56961525.10.7.1477717614276; __utmc=56961525; __utmz=56961525.1477717545.33.27.utmcsr=baidu|utmccn=(organic)|utmcmd=organic')
    resContent_odds  = urllib2.urlopen(req).read()
    soup_odds = BeautifulSoup(resContent_odds,fromEncoding='gb18030')
    trs=soup_odds.findAll("tr")
    cpname=None
    iwin=None
    idraw=None
    ilost=None
    lwin=None
    ldraw=None
    llost=None
    roi=None
    hscore=None
    ascore=None
    for tr in trs:
        spans = tr.findAll("span")
       # print spans
        #print len(spans)
        if len(spans)> 15:
            cpname=spans[1].string
            iwin=spans[2].string
            idraw=spans[3].string
            ilost=spans[4].string
            lwin=spans[5].string
            ldraw=spans[6].string
            llost=spans[7].string
            roi=spans[14].string
            print '================================================='
            print lg
            print lg_round
            print ptime
            print hname+' vs '+ aname
            print hscore_str+' - '+ ascore_str
            print half_score
            print gameresult
            print oid
            print cpname, iwin,idraw,ilost,lwin,ldraw,llost,roi
            print '================================================='
            delete_sql='delete from td_okooo_odds where ptime="'+ptime+'" and lg="'+lg+'" and hname="'+hname+'" and aname="'+aname+'" and oid='+oid+' and cpname="'+cpname+'"'
            sql="INSERT INTO `td_okooo_odds` (`oid`,`ptime`,`lg`,`hname`,`aname`,`gameresult`,`hscore`,`ascore`,`score_dif`,`cpname`,`iwin`,`idraw`,`ilost`,`lwin`,`ldraw`,`llost`,`roi`)  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            print delete_sql
            cur.execute(delete_sql)
            cur.execute(sql,(oid,ptime,lg,hname,aname,gameresult,hscore,ascore,score_dif,cpname,iwin,idraw,ilost,lwin,ldraw,llost,roi))
            conn.commit()

if __name__=="__main__":
    print 'start-time:'
    print datetime.datetime.now()
    url='http://www.okooo.com/jingcai/'
    sqlmin='select min(ptime) from td_okooo_odds'
    datestr = ''
    cur.execute(sqlmin)
    results = cur.fetchall()
    if(len(results)>0):
        if(len(results[0])>0):
            row=results[0]
            if(len(row)>0 and row[0] != None):
                mindate=row[0]
                print mindate
                for n in range(1,100):
                    hisdate = mindate - datetime.timedelta(days=n)
                    url1=url+ hisdate.strftime("%Y-%m-%d")+'/'
                    getGameList(url1)
    #getGameList(url1)
    print 'en-time:'
    print datetime.datetime.now()
    cur.close()
    conn.close()