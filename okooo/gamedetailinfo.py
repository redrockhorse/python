#!/usr/bin/python
#encoding=utf-8
__author__ = 'mahy'
from pyquery import PyQuery as pq
from lxml import etree
import httplib2
import re
import MySQLdb
import time
import datetime


conn_g=MySQLdb.connect(host='127.0.0.1',user='root',passwd='Ke_Xing3508',db='jc',port=3306,charset='utf8')
cur_g = conn_g.cursor()



def collectingData(urldate):
    conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='Ke_Xing3508',db='jc',port=3306,charset='utf8')
    cur = conn.cursor()
    pattern = re.compile(r'\d*')
    v_source = pq(url="http://trade.500.com/jczq/?date="+urldate+"&playtype=both")
    print "http://trade.500.com/jczq/?date="+urldate+"&playtype=both"
    n = v_source('.bet_table').children('tr').length
    for i in range(n-1):
        pdate = v_source('.bet_table').children('tr').eq(i).attr('pdate')
        lg = v_source('.bet_table').children('tr').eq(i).attr('lg')
        homesxname = v_source('.bet_table').children('tr').eq(i).attr('homesxname')
        awaysxname = v_source('.bet_table').children('tr').eq(i).attr('awaysxname')
        score = v_source('.bet_table').children('tr').eq(i).children('td').eq(4).children('a').text()
        rq = v_source('.bet_table').children('tr').eq(i).attr('rq')
        win_rq = v_source('.bet_table').children('tr').eq(i).children('td').eq(7).children('div').eq(1).children(
            'span').eq(0).attr('data-sp')
        draw_rq = v_source('.bet_table').children('tr').eq(i).children('td').eq(7).children('div').eq(1).children(
            'span').eq(1).attr('data-sp')
        lost_rq = v_source('.bet_table').children('tr').eq(i).children('td').eq(7).children('div').eq(1).children(
            'span').eq(2).attr('data-sp')
        win = v_source('.bet_table').children('tr').eq(i).children('td').eq(7).children('div').children('span').eq(
            0).attr('data-sp')
        draw = v_source('.bet_table').children('tr').eq(i).children('td').eq(7).children('div').children('span').eq(
            1).attr('data-sp')
        lost = v_source('.bet_table').children('tr').eq(i).children('td').eq(7).children('div').children('span').eq(
            2).attr('data-sp')
        shujuurl = v_source('.bet_table').children('tr').eq(i).children('td').eq(8).children('a').eq(0).attr('href')
        leftteamorder = v_source('.bet_table').children('tr').eq(i).children('td').eq(3).children(
            'span').text().replace('[', '').replace(']', '')
        rightteamorder = v_source('.bet_table').children('tr').eq(i).children('td').eq(5).children(
            'span').text().replace('[', '').replace(']', '')

        http = httplib2.Http()
        response, content = http.request(shujuurl, 'GET')
        print shujuurl
        tree = etree.HTML(content)
        jiaozhan = tree.xpath(u'//span[@class="f16"]/em')
        ta_score = tree.xpath(u'//div[@class="team_a"]//span[@class="ying"]')
        tb_score = tree.xpath(u'//div[@class="team_b"]//span[@class="ying"]')

        yazhiurl = v_source('.bet_table').children('tr').eq(i).children('td').eq(8).children('a').eq(1).attr('href')

        response_yazhi, content_yazhi = http.request(yazhiurl, 'GET')
        print yazhiurl
        tree_yazhi = etree.HTML(content_yazhi)
        jishi_l=tree_yazhi.xpath(u'//tr[@id="5"]/td[3]//td[1]')
        jishi_m=tree_yazhi.xpath(u'//tr[@id="5"]/td[3]//td[2]')
        jishi_r=tree_yazhi.xpath(u'//tr[@id="5"]/td[3]//td[3]')
        chupan_l=tree_yazhi.xpath(u'//tr[@id="5"]/td[5]//td[1]')
        chupan_m=tree_yazhi.xpath(u'//tr[@id="5"]/td[5]//td[2]')
        chupan_r=tree_yazhi.xpath(u'//tr[@id="5"]/td[5]//td[3]')



        chupan_l_val=None
        chupan_m_val=None
        chupan_r_val=None
        if(len(chupan_l)>0):
            print chupan_l[0].text
            print chupan_m[0].text
            print chupan_r[0].text
            chupan_l_val=chupan_l[0].text
            chupan_m_val=chupan_m[0].text
            chupan_r_val=chupan_r[0].text
        jishi_l_val=None
        jishi_m_val=None
        jishi_r_val=None
        if(len(jishi_l)>0):
            print jishi_l[0].text
            print jishi_m[0].text
            print jishi_r[0].text
            p=re.search(r'\d+\.\d+', jishi_l[0].text)
            jishi_l_val=eval(p.group())
            jishi_m_val=jishi_m[0].text
            p=re.search(r'\d+\.\d+', jishi_r[0].text)
            jishi_r_val=eval(p.group())
        d_score = None
        pwin =None
        plost =None
        pdraw =None
        if(len(ta_score)>0 and len(tb_score)>0):
            if(ta_score[0].text and tb_score[0].text):
                d_score = float(ta_score[0].text) - float(tb_score[0].text)
                pwin = 44.8 + (0.53 * d_score)
                plost = 24.5 - (0.39 * d_score)
                pdraw = 100 - pwin - plost


        print "============================================================================================"
        print "基本信息：".decode('utf-8'), pdate, lg, homesxname, awaysxname
        print "基本赔率: ".decode('utf-8'), win, draw, lost
        print "积分赔率: ".decode('utf-8'), round(90 / pwin, 2), round(90 / pdraw, 2), round(90 / plost, 2)
        print "让(".decode('utf-8') + rq + ")赔率: ".decode('utf-8'), win_rq, draw_rq, lost_rq
        print "赛   果: ".decode('utf-8'), score
        print "赛前排名: ".decode('utf-8'), leftteamorder, rightteamorder
        if(len(jiaozhan)>2):
            print "对战往绩: ".decode('utf-8'), jiaozhan[0].text, jiaozhan[1].text, jiaozhan[2].text
        print "积分对比: ".decode('utf-8'), ta_score[0].text, tb_score[0].text
        print "============================================================================================"
        jiaozhanscore=None
        if(len(jiaozhan)>2):
            jiaozhanscore = int(pattern.match(jiaozhan[0].text).group()) * 3 + int(
            pattern.match(jiaozhan[1].text).group()) - int(pattern.match(jiaozhan[2].text).group())
        sarray = score.split(':')
        resulenum = None
        if(len(sarray)>1):
            hscore=sarray[0] if sarray[0]  else None
            ascore=sarray[1] if sarray[1]  else None
            if(hscore and ascore):
                resulenum = int(sarray[0]) - int(sarray[1])
        dorder = None
        if(rightteamorder and leftteamorder):
            dorder = int(rightteamorder) - int(leftteamorder)


        print "*********************************************************************************************"
        print win, draw, lost, win_rq, draw_rq, lost_rq, jiaozhanscore, dorder, d_score, resulenum
        print "*********************************************************************************************"
        sql="INSERT INTO tb_rate_power_rs(`pdate`,`lg`,`homesxname`,`awaysxname`, `win`,`draw`,`lost`,`win_rq`,`draw_rq`,`lost_rq`,`jiaozhanscore`,`dorder`,`d_score`,`resulenum`,`chupan_l`,`chupan_m`,`chupan_r`,`jishi_l`,`jishi_m`,`jishi_r`,`score`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        delete_sql='delete from tb_rate_power_rs where pdate="'+pdate+'" and lg="'+lg+'" and homesxname="'+homesxname+'"'
        cur.execute(delete_sql)
        cur.execute(sql,(pdate,lg,homesxname,awaysxname,win,draw,lost, win_rq, draw_rq, lost_rq, jiaozhanscore, dorder, d_score, resulenum,chupan_l_val,chupan_m_val,chupan_r_val,jishi_l_val,jishi_m_val,jishi_r_val,score))
        conn.commit()
    cur.close()
    conn.close()




daynum = 3
for y in xrange(0,daynum):
    datestr = datetime.datetime.now()-datetime.timedelta(days=y)
    collectingData(datestr.strftime("%Y-%m-%d"))
    time.sleep(1)



