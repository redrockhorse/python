#!/usr/bin/python
#encoding=utf-8
__author__ = 'mahy'

'''
在澳客网抓取比赛赔率信息
'''
from lxml import etree
import httplib2
from urllib import urlencode
import re
import json
import random
from  datetime  import  *
import time
import pymysql

url = "http://www.okooo.com/I/?method=ok.soccer.odds.GetProcess"
conn=pymysql.connect(host='127.0.0.1',user='root',passwd='Qd@#$mo658',db='jc',port=3306,charset='utf8')
cur = conn.cursor()
num_pattern= re.compile(r'\d*')
cookie = '__utma=56961525.85067690.1476523374.1492249589.1502600208.3; __utmz=56961525.1476523374.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); Hm_lvt_5ffc07c2ca2eda4cc1c4d8e50804c94b=1502600209; _ga=GA1.2.85067690.1476523374; LastUrl=; __utmb=56961525.28.8.1502600642401; __utmc=56961525; Hm_lpvt_5ffc07c2ca2eda4cc1c4d8e50804c94b=1502600642; PHPSESSID=19703e76c26596ac69c7617b8890b98d6a3f5b73; pm=; LStatus=N; LoginStr=%7B%22welcome%22%3A%22%u60A8%u597D%uFF0C%u6B22%u8FCE%u60A8%22%2C%22login%22%3A%22%u767B%u5F55%22%2C%22register%22%3A%22%u6CE8%u518C%22%2C%22TrustLoginArr%22%3A%7B%22alipay%22%3A%7B%22LoginCn%22%3A%22%u652F%u4ED8%u5B9D%22%7D%2C%22tenpay%22%3A%7B%22LoginCn%22%3A%22%u8D22%u4ED8%u901A%22%7D%2C%22qq%22%3A%7B%22LoginCn%22%3A%22QQ%u767B%u5F55%22%7D%2C%22weibo%22%3A%7B%22LoginCn%22%3A%22%u65B0%u6D6A%u5FAE%u535A%22%7D%2C%22renren%22%3A%7B%22LoginCn%22%3A%22%u4EBA%u4EBA%u7F51%22%7D%2C%22baidu%22%3A%7B%22LoginCn%22%3A%22%u767E%u5EA6%22%7D%2C%22weixin%22%3A%7B%22LoginCn%22%3A%22%u5FAE%u4FE1%u767B%u5F55%22%7D%2C%22snda%22%3A%7B%22LoginCn%22%3A%22%u76DB%u5927%u767B%u5F55%22%7D%7D%2C%22userlevel%22%3A%22%22%2C%22flog%22%3A%22hidden%22%2C%22UserInfo%22%3A%22%22%2C%22loginSession%22%3A%22___GlobalSession%22%7D; FirstURL=www.okooo.com/; FirstOKURL=http%3A//www.okooo.com/jingcai/; First_Source=www.okooo.com'
def getOdds():
    sql ='select Id,okid,gametime from td_ok_gamebaseinfo order by gametime desc'
    cur.execute(sql)
    results = cur.fetchall()
    if(len(results)>0):
        if(len(results[0])>0):
            for row in results:
                if(len(row)>0):
                    time.sleep(random.randint(3, 10))
                    Id=row[0]
                    okid = row[1]
                    gametime = row[2]
                    #try:
                    fetchOdd(okid,'24',gametime,Id)
                    fetchOdd(okid,'2',gametime,Id)
                    fetchOdd(okid,'14',gametime,Id)
                    fetchOdd(okid,'84',gametime,Id)
                    fetchOdd(okid,'19',gametime,Id)
                    fetchOdd(okid,'82',gametime,Id)
                    #except Exception:
                    print("odd error",okid,id)
                    #continue


'''
provider_id：99家平均 24,竞彩官方 2，威廉希尔 14，澳门彩票 84，必发 19，立博 82，
'''
def fetchOdd(okid,provider_id,gametime,Id):
    request_param ={'match_id':okid,'betting_type_id':"1",'provider_id':provider_id}
    http = httplib2.Http()
    response, content = http.request(url, 'POST',urlencode(request_param),headers = {
        'Host': 'www.okooo.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Referer': 'http://www.okooo.com/soccer/match/'+okid+'/odds/',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie':cookie,
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    })
    s = json.loads(content)
    if s.get('code') ==1 and s.get('msg')=='succ':
        data = s.get('data')
        for i in data:
            w = i.get('o').get('h')
            d = i.get('o').get('d')
            l = i.get('o').get('a')
            t = i.get('t')
            tmp = str(gametime.year)+'/'+t
            timeTuple = datetime.strptime(tmp, '%Y/%m/%d %H:%M')
            if datetime.now() > timeTuple:
                t = tmp
            else:
                t = str(gametime.year-1)+'/'+t
            m = i.get('m')
            b = i.get('b')
            print(Id,okid,gametime,provider_id,w,d,l,t,m,b)
            delete_sql = 'delete from td_ok_odds where Id="' + Id + '" and t="'+t+'"'
            sql = "INSERT INTO `td_ok_odds` (`Id`,`okid`,`gametime`,`provider_id`,`w`,`d`,`l`,`t`,`m`,`b`)  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            cur.execute(delete_sql)
            cur.execute(sql, (Id,okid,gametime,provider_id,w,d,l,t,m,b))
            conn.commit()

if __name__=='__main__':
    getOdds()
    cur.close()
    conn.close()