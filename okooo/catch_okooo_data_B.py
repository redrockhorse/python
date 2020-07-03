__author__ = 'mahy'
# -*- coding: utf8 -*-
from BeautifulSoup import BeautifulSoup
import urllib2
import sys
import re
import MySQLdb
import time
import datetime
conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='root',db='jc',port=3306,charset='utf8')
cur = conn.cursor()
#reload(sys)
sys.setdefaultencoding('utf8')
pattern = re.compile(r'\d*-\d*-\d*')
def getBaseInfo(url):
    resContent  = urllib2.urlopen(url).read()
    soup = BeautifulSoup(resContent)
    baseInfo_list=soup.findAll("div",attrs={"class": "touzhu_1"})
    n = len(baseInfo_list)
    for i in range(n):
        getExchanges(baseInfo_list[i]['data-mid'])

def getExchanges(mid):
    exc_url='http://www.okooo.com/soccer/match/'+mid+'/exchanges/'
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
    ptime=pattern.match(ptime).group()
    lg_div=soup_exc.findAll("div",attrs={"class": "qbx_1"})
    lg=lg_div[0].findAll('a')[0].string
    tables = soup_exc.findAll('table',attrs={"class": "noBberBottom"})
    hname= hname[0].string
    aname= aname[0].string
    print '================================================='
    print lg
    print pattern.match(ptime).group()
    print hname+' vs '+ aname
    print hscore_str+' - '+ ascore_str
    print gameresult
    print '================================================='
    tab = tables[0]
    dataList =[([0] * 13) for i in range(5)]
    l=0
    for tr in tab.findAll('tr'):
        l+=1
        c=0
        for td in tr.findAll('td'):
            c+=1
            dataList[l-1][c-1]=td.string
    sql="INSERT INTO `td_ptl_okooo_data` (`pdate`,`lg`,`hname`,`aname`,`buyers_bf_price_3`,`buyers_bf_newlist_3`,`seller_bf_price_3`,`seller_bf_newlist_3`,`deal_bf_price_3`,`deal_bf_volume_3`,`deal_bf_profit_3`,`sl_odds_3`,`sl_savecount_3`,`sl_profit_3`,`sl_opularity_3`,`sl_percent_3`,`buyers_bf_price_1`,`buyers_bf_newlist_1`,`seller_bf_price_1`,`seller_bf_newlist_1`,`deal_bf_price_1`,`deal_bf_volume_1`,`deal_bf_profit_1`,`sl_odds_1`,`sl_savecount_1`,`sl_profit_1`,`sl_opularity_1`,`sl_percent_1`,`buyers_bf_price_0`,`buyers_bf_newlist_0`,`seller_bf_price_0`,`seller_bf_newlist_0`,`deal_bf_price_0`,`deal_bf_volume_0`,`deal_bf_profit_0`,`sl_odds_0`,`sl_savecount_0`,`sl_profit_0`,`sl_opularity_0`,`sl_percent_0`,`gameresult`,`score`,`score_dif`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    delete_sql='delete from td_ptl_okooo_data where pdate="'+ptime+'" and lg="'+lg+'" and hname="'+hname+'" and aname="'+aname+'"'
    print delete_sql
    cur.execute(delete_sql)
    conn.commit()
    cur.execute(sql,(ptime,lg,hname,aname,dataList[2][1],dataList[2][2],dataList[2][3],dataList[2][4],dataList[2][5],dataList[2][6],dataList[2][7],dataList[2][8],dataList[2][9],dataList[2][10],dataList[2][11],dataList[2][12],dataList[3][1],dataList[3][2],dataList[3][3],dataList[3][4],dataList[3][5],dataList[3][6],dataList[3][7],dataList[3][8],dataList[3][9],dataList[3][10],dataList[3][11],dataList[3][12],dataList[4][1],dataList[4][2],dataList[4][3],dataList[4][4],dataList[4][5],dataList[4][6],dataList[4][7],dataList[4][8],dataList[4][9],dataList[4][10],dataList[4][11],dataList[4][12],gameresult,score,score_dif))
    conn.commit()



if __name__=="__main__":
    url='http://www.okooo.com/jingcai/'
    getBaseInfo(url)
    cur.close()
    conn.close()
    '''
    tstr = raw_input("begin date:")
    daynumstr = raw_input("Days:")
    if daynumstr != None:
	    daynum = int(daynumstr)
    stamp = time.strptime(tstr, "%Y%m%d")
    t = datetime.date.fromtimestamp(int(time.mktime(stamp)))
    for y in xrange(0,daynum):
        datestr = t+datetime.timedelta(days=y)
        url='http://www.okooo.com/jingcai/'+datestr.strftime("%Y-%m-%d")+'/'
        print url
        getBaseInfo(url)
    cur.close()
    conn.close()
'''
