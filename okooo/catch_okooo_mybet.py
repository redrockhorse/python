#encoding=utf-8
#!/usr/bin/python
__author__ = 'mahy'
from pyquery import PyQuery as pq
from lxml import etree
import httplib2
import re
import MySQLdb
import time
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf8')

conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='root',db='jc',port=3306,charset='utf8')
cur = conn.cursor()
num_pattern= re.compile(r'\d+\.?\d*')
cookie ='pgv_pvi=1297987712; FirstURL=www.okooo.com/; FirstOKURL=http%3A//www.okooo.com/jingcai/; First_Source=www.okooo.com; Last_Source=http%3A//www.okooo.com/User/partner/PartnerLogin.php; userCustomLottery=SportteryWDL%2CSportteryScore%2CSportteryNWDL%2CSportterySoccerMix%2CWDL%2CScore%2CTotalGoals; M_UserName=%2213633473448%22; M_UserID=18564539; M_Ukey=de52cd817a93ed1ed03e143104707ef2; OkTouchAutoUuid=e351c2cc54fccfa1640fd8ac6886d082; OkTouchMsIndex=7; _ga=GA1.2.76133388.1431060652; PHPSESSID=b468dea13b2933028222fcd6488add09c355d016; DRUPAL_LOGGED_IN=Y; IMUserID=18564539; IMUserName=13633473448; OkAutoUuid=5b89a43ed03f89cd9bb04130ef5086e6; OkMsIndex=2; isInvitePurview=0; UWord=226950c35d98e9edfb5d9acdedddc46566c; LastUrl=; Hm_lvt_5ffc07c2ca2eda4cc1c4d8e50804c94b=1492430148,1492432380,1492515960,1492907890; Hm_lpvt_5ffc07c2ca2eda4cc1c4d8e50804c94b=1492907912; showCustomMenu=2; __utma=56961525.76133388.1431060652.1492515960.1492907865.98; __utmb=56961525.15.8.1492907911908; __utmc=56961525; __utmz=56961525.1488543216.65.35.utmcsr=baidu|utmccn=(organic)|utmcmd=organic';
#url='http://www.okooo.com/Buy/UserBetList.php?UserID=18564539&Style=&Type=Store&LotteryStyle=JC&OwnerType=all&GoodsStatus=all&StartDate=2017-04-01&EndDate=2017-05-01&page=2'
url='http://www.okooo.com/Buy/UserBetList.php?UserID=18564539&Style=&Type=Store&LotteryStyle=JC&OwnerType=all&GoodsStatus=all&StartDate=2017-04-01&EndDate=2017-04-31&page=1'

http = httplib2.Http()
response, content = http.request(url, 'GET',headers = {
        'Host': 'www.okooo.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Referer': 'http://www.okooo.com/Buy/UserBetList.php?UserID=18564539&Style=&Type=Store&LotteryStyle=JC&OwnerType=all&GoodsStatus=all&StartDate=2017-02-01&EndDate=2017-02-01&FieldType=BuyTime',
       # 'Cookie': 'pgv_pvi=1297987712; FirstURL=www.okooo.com/; FirstOKURL=http%3A//www.okooo.com/jingcai/; First_Source=www.okooo.com; Last_Source=http%3A//www.okooo.com/User/partner/PartnerLogin.php; userCustomLottery=SportteryWDL%2CSportteryScore%2CSportteryNWDL%2CSportterySoccerMix%2CWDL%2CScore%2CTotalGoals; PHPSESSID=6d7f438b142b6a96bbadd8202e03ef9c349e5d0d; OKSID=90ce4f063ce7b001f1068cc879db39942efa7b54; M_UserName=%2213633473448%22; M_UserID=18564539; M_Ukey=de52cd817a93ed1ed03e143104707ef2; OkTouchAutoUuid=e351c2cc54fccfa1640fd8ac6886d082; OkTouchMsIndex=7; DRUPAL_LOGGED_IN=Y; IMUserID=18564539; IMUserName=13633473448; OkAutoUuid=4e081ac6d8fe7c3117d1745b5cd2a2f1; OkMsIndex=7; isInvitePurview=0; UWord=220950c35d78e9edfb5d9acdedddc46066c; _ga=GA1.2.76133388.1431060652; LastUrl=; Hm_lvt_5ffc07c2ca2eda4cc1c4d8e50804c94b=1491836117,1491884815,1492247525,1492248799; Hm_lpvt_5ffc07c2ca2eda4cc1c4d8e50804c94b=1492251441; showCustomMenu=2; __utma=56961525.76133388.1431060652.1491884741.1492247508.90; __utmb=56961525.53.8.1492251441307; __utmc=56961525; __utmz=56961525.1488543216.65.35.utmcsr=baidu|utmccn=(organic)|utmcmd=organic',
        'Cookie':cookie,
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    })
#print content
tree = etree.HTML(content)
user_buy_list = tree.xpath(u'//table[@id="user_buy_list"]/tr')
#print user_buy_list
for i in range(1,len(user_buy_list)):
    gtype=user_buy_list[i][0]
    gtype=gtype.text

    bettime=user_buy_list[i][1]
    bettime='2017-'+bettime.text

    betmoney=user_buy_list[i][3]
    betmoney=betmoney.text

    betstat=user_buy_list[i][4][0]
    betstat=betstat.text

    betflag=user_buy_list[i][5][0]
    betflag=betflag.text

    winmoney=user_buy_list[i][6]
    winmoney=winmoney.text.strip();

    durl=user_buy_list[i][7][0]
    durl=durl.values()[0]
    orderid=durl.split("/p")
    orderid = orderid[1].replace("/","")
    durl='http://www.okooo.com'+durl
    print durl
    dresponse, dcontent = http.request(durl, 'GET',headers = {
        'Host': 'www.okooo.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Referer': 'http://www.okooo.com/Buy/UserBetList.php?UserID=18564539&Style=&Type=Store&LotteryStyle=JC&OwnerType=all&GoodsStatus=all&StartDate=2017-04-01&EndDate=2017-05-01&FieldType=BuyTime',
       #'Cookie': 'pgv_pvi=1297987712; FirstURL=www.okooo.com/; FirstOKURL=http%3A//www.okooo.com/jingcai/; First_Source=www.okooo.com; Last_Source=http%3A//www.okooo.com/User/partner/PartnerLogin.php; userCustomLottery=SportteryWDL%2CSportteryScore%2CSportteryNWDL%2CSportterySoccerMix%2CWDL%2CScore%2CTotalGoals; PHPSESSID=6d7f438b142b6a96bbadd8202e03ef9c349e5d0d; OKSID=90ce4f063ce7b001f1068cc879db39942efa7b54; M_UserName=%2213633473448%22; M_UserID=18564539; M_Ukey=de52cd817a93ed1ed03e143104707ef2; OkTouchAutoUuid=e351c2cc54fccfa1640fd8ac6886d082; OkTouchMsIndex=7; DRUPAL_LOGGED_IN=Y; IMUserID=18564539; IMUserName=13633473448; OkAutoUuid=4e081ac6d8fe7c3117d1745b5cd2a2f1; OkMsIndex=7; isInvitePurview=0; UWord=220950c35d78e9edfb5d9acdedddc46066c; _ga=GA1.2.76133388.1431060652; LastUrl=; Hm_lvt_5ffc07c2ca2eda4cc1c4d8e50804c94b=1491836117,1491884815,1492247525,1492248799; Hm_lpvt_5ffc07c2ca2eda4cc1c4d8e50804c94b=1492251441; showCustomMenu=2; __utma=56961525.76133388.1431060652.1491884741.1492247508.90; __utmb=56961525.53.8.1492251441307; __utmc=56961525; __utmz=56961525.1488543216.65.35.utmcsr=baidu|utmccn=(organic)|utmcmd=organic',
        'Cookie':cookie,
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    })
    dtree = etree.HTML(dcontent.decode('gbk'))
    OpenType=dtree.xpath(u'//div[@id="OpenType"]/span')
    betnum=OpenType[1].text
    betmd=OpenType[2].text
    #betnum_n=num_pattern.search(betnum).group()
    #betnum_n=num_pattern.findall(betnum);
    #betmd_n=num_pattern.search(betmd).group()
    #betmd_n=num_pattern.findall(betmd);
    #print durl.values()[0]
    #print '\n'.join(['%s:%s' % item for item in durl.items()])
    #betnum_n=betnum.decode('gbk').replace("鲁隆".decode("gbk"),"");
    #betmd_n=betmd.decode('gbk').replace("麓庐".decode("gbk"),"");
    #betnum_n=betnum.decode('gbk').replace("鲁隆","");
    #betmd_n=betmd.decode('gbk').replace("麓庐","").replace("碌楼鹿脴","1");
    betnum_n=betnum
    betmd_n=betmd
    mtable=dtree.xpath(u'//table[@class="mtable"]/tr')
    for i in range(1,len(mtable)-1):
        if len(mtable[i]) == 3 and len(mtable[i+1])==2 and len(mtable[i+2])==2:
            gametime=mtable[i][1]
            gametime='2017-'+gametime.text
            homesxname=mtable[i][2][0][0]
            homesxname=homesxname.text
            awaysxname=mtable[i][2][2][0]
            awaysxname=awaysxname.text
            result=mtable[i][2][1]
            result=result.text

            mybet=mtable[i+1][0][0][0]
            mybet=mybet.text.strip()
            mybetcode=mybet
            betrq=''
            if mybet.find("-1") != -1:
                betrq='-1'
            if mybet.find("+1") != -1:
                betrq='+1'
            if homesxname.find(mybet[0:2]) != -1 :
                mybetcode=betrq+'主胜'.decode('utf-8')
            if awaysxname.find(mybet[0:2]) != -1:
                mybetcode=betrq+'客胜'.decode('utf-8')
            print orderid,gtype,bettime,betmoney,betstat,betflag,winmoney,durl,betnum_n,betmd_n,gametime,homesxname,awaysxname,result,mybet,mybetcode;
            sql="INSERT INTO tb_okooo_mybet(`orderid`,`gtype`,`bettime`,`betmoney`,`betstat`,`betflag`,`winmoney`,`durl`,`betnum`,`betmd`,`gametime`,`homesxname`,`awaysxname`,`result`,`mybet`,`mybetcode`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            delete_sql='delete from tb_okooo_mybet where orderid="'+orderid+'" and homesxname="'+homesxname+'"  and mybetcode="'+mybetcode+'"'
            cur.execute(delete_sql)
            cur.execute(sql,(orderid,gtype,bettime,betmoney,betstat,betflag,winmoney,durl,betnum_n,betmd_n,gametime,homesxname,awaysxname,result,mybet,mybetcode))
            conn.commit()

            mybet=mtable[i+2][0][0][0]
            mybet=mybet.text.strip()
            mybetcode=mybet
            betrq=''
            if mybet.find("-1") != -1:
                betrq='-1'
            if mybet.find("+1") != -1:
                betrq='+1'
            if homesxname.find(mybet[0:2]) != -1 :
                mybetcode=betrq+'主胜'.decode('utf-8')
            if awaysxname.find(mybet[0:2]) != -1:
                mybetcode=betrq+'客胜'.decode('utf-8')
            print orderid,gtype,bettime,betmoney,betstat,betflag,winmoney,durl,betnum_n,betmd_n,gametime,homesxname,awaysxname,result,mybet,mybetcode;
            sql="INSERT INTO tb_okooo_mybet(`orderid`,`gtype`,`bettime`,`betmoney`,`betstat`,`betflag`,`winmoney`,`durl`,`betnum`,`betmd`,`gametime`,`homesxname`,`awaysxname`,`result`,`mybet`,`mybetcode`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            delete_sql='delete from tb_okooo_mybet where orderid="'+orderid+'" and homesxname="'+homesxname+'"  and mybetcode="'+mybetcode+'"'
            cur.execute(delete_sql)
            cur.execute(sql,(orderid,gtype,bettime,betmoney,betstat,betflag,winmoney,durl,betnum_n,betmd_n,gametime,homesxname,awaysxname,result,mybet,mybetcode))
            conn.commit()
        elif len(mtable[i]) == 2:
            print '~~~~~~~'
        else:
            gametime=mtable[i][1]
            gametime='2017-'+gametime.text
            homesxname=mtable[i][2][0][0]
            homesxname=homesxname.text
            awaysxname=mtable[i][2][2][0]
            awaysxname=awaysxname.text
            result=mtable[i][2][1]
            result=result.text
            mybet=mtable[i][3][0][0]
            mybet=mybet.text.strip()
            mybetcode=mybet
            betrq=''
            if mybet.find("-1") != -1:
                betrq='-1'
            if mybet.find("+1") != -1:
                betrq='+1'
            if homesxname.find(mybet[0:2]) != -1 :
                mybetcode=betrq+'主胜'.decode('utf-8')
            if awaysxname.find(mybet[0:2]) != -1:
                mybetcode=betrq+'客胜'.decode('utf-8')
            print orderid,gtype,bettime,betmoney,betstat,betflag,winmoney,durl,betnum_n,betmd_n,gametime,homesxname,awaysxname,result,mybet,mybetcode;
            sql="INSERT INTO tb_okooo_mybet(`orderid`,`gtype`,`bettime`,`betmoney`,`betstat`,`betflag`,`winmoney`,`durl`,`betnum`,`betmd`,`gametime`,`homesxname`,`awaysxname`,`result`,`mybet`,`mybetcode`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            delete_sql='delete from tb_okooo_mybet where orderid="'+orderid+'" and homesxname="'+homesxname+'"  and mybetcode="'+mybetcode+'"'
            cur.execute(delete_sql)
            cur.execute(sql,(orderid,gtype,bettime,betmoney,betstat,betflag,winmoney,durl,betnum_n,betmd_n,gametime,homesxname,awaysxname,result,mybet,mybetcode))
            conn.commit()
cur.close()
conn.close()