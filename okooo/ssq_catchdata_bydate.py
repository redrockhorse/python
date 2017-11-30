__author__ = 'Thinkpad'
from BeautifulSoup import BeautifulSoup
import urllib2
import MySQLdb
conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='Ke_Xing3508',db='jc',port=3306,charset='utf8')
cur = conn.cursor()

url = 'http://kaijiang.zhcw.com/zhcw/html/ssq/list_1.html'
req = urllib2.Request(url)
req.add_header('Host','kaijiang.zhcw.com')
req.add_header('Referer','http://www.zhcw.com/ssq/kaijiangshuju/index.shtml?type=0')
req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36')
req.add_header('Cookie','JSESSIONID=abcLZEBRKynNe7HO3GYGv; _gat=1; QhGG_75da_saltkey=vl5SLPSM; QhGG_75da_lastvisit=1478313040; tmc=1.101746250.85712658.1478316506110.1478316506110.1478316506110; tma=101746250.85712658.1478316506110.1478316506110.1478316506110.1; tmd=1.101746250.85712658.1478316506110.; fingerprint=8f5482e560a7de1b02bb2eee14eb660a; bfd_s=223256514.741757190237870.1478316506353; QhGG_75da_sid=mRe7sZ; QhGG_75da_lastact=1478316642%09sync.php%09; bfd_g=b56c782bcb75035d00002a9c00bd0c50551de962; Hm_lvt_692bd5f9c07d3ebd0063062fb0d7622f=1478316493; Hm_lpvt_692bd5f9c07d3ebd0063062fb0d7622f=1478316567; _ga=GA1.2.549514814.1478316493')
resContent_exc  = urllib2.urlopen(req).read()
soup_exc = BeautifulSoup(resContent_exc,fromEncoding='gb18030')
table = soup_exc.findAll("table",attrs={"class": "wqhgt"})
trs = table[0].findAll("tr")
tds = trs[2].findAll("td")
pdate = tds[0].string
pnum = tds[1].string
ems = tds[2].findAll("em")
v1 = ems[0].string
v2 = ems[1].string
v3 = ems[2].string
v4 = ems[3].string
v5 = ems[4].string
v6 = ems[5].string
v7 = ems[6].string
sql="INSERT INTO `td_ptl_ssq_data` (`pdate`,`pnum`,`v1`,`v2`,`v3`,`v4`,`v5`,`v6`,`v7`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
delete_sql='delete from td_ptl_ssq_data where pdate="'+pdate+'"'
print sql
cur.execute(delete_sql)
conn.commit()
cur.execute(sql,(pdate,pnum,v1,v2,v3,v4,v5,v6,v7))
conn.commit()
cur.close()
conn.close()

#for em in ems:
#    print em.string
