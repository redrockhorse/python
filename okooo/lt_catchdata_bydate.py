#!/usr/bin/python  
#encoding=utf-8  
__author__ = 'mahy'
from BeautifulSoup import BeautifulSoup
import urllib2
import MySQLdb
conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='Ke_Xing3508',db='jc',port=3306,charset='utf8')
cur = conn.cursor()

url = 'http://www.lottery.gov.cn/historykj/history.jspx?_ltype=dlt'
print url
req = urllib2.Request(url)
req.add_header('Host','www.lottery.gov.cn')
req.add_header('Referer','http://www.lottery.gov.cn/historykj/history.jspx?_ltype=dlt')
req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36')
req.add_header('Cookie','BIGipServerserver_pool=270012588.20480.0000; JSESSIONID=AB4018B049AE62B7DBA50DE7FFAD029C; Hm_lvt_8929ffae85e1c07a7ded061329fbf441=1478322456; Hm_lpvt_8929ffae85e1c07a7ded061329fbf441=1478322531')
resContent_exc  = urllib2.urlopen(req).read()
soup_exc = BeautifulSoup(resContent_exc,fromEncoding='gb18030')
table = soup_exc.findAll("tbody")
trs = table[0].findAll("tr")
tr=trs[0]
tds = tr.findAll("td")
pdate = tds[len(tds)-1].string
pnum = tds[0].string
v1 = tds[1].string
v2 = tds[2].string
v3 = tds[3].string
v4 = tds[4].string
v5 = tds[5].string
v6 = tds[6].string
v7 = tds[7].string
sql="INSERT INTO `td_ptl_lt_data` (`pdate`,`pnum`,`v1`,`v2`,`v3`,`v4`,`v5`,`v6`,`v7`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
delete_sql='delete from td_ptl_lt_data where pdate="'+pdate+'"'
print sql
cur.execute(delete_sql)
cur.execute(sql,(pdate,pnum,v1,v2,v3,v4,v5,v6,v7))
conn.commit()
cur.close()
conn.close()
