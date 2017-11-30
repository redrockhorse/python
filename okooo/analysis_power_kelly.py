# -*- coding: utf8 -*-
from __future__ import division

__author__ = 'mahy'
import MySQLdb
import xlwt
import math
import time


conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='root',db='jc',port=3306,charset='utf8')
cur = conn.cursor()
excelfile = xlwt.Workbook()
sheet1 = excelfile.add_sheet(u'sheet1',cell_overwrite_ok=True)
style_default = xlwt.XFStyle()
sqlstr=" select pdate,lg,homesxname,awaysxname,win,draw,lost,jishi_m from tb_rate_power_rs where pdate='2017-04-09'  and resulenum is null and jishi_m is not null and lg is not null and win is not null order by gametime asc;"
#sqlstr=" select pdate,lg,homesxname,awaysxname,win,draw,lost,jishi_m from tb_rate_power_rs where pdate>'2017-03-17' and pdate<'2017-03-20' and lg='日职'  and jishi_m is not null and lg is not null and win is not null;"

cur.execute(sqlstr)
result = cur.fetchall()
l=0

columnames =["时间".decode('utf-8'),'联赛'.decode('utf-8'),'球队'.decode('utf-8'),"3","1","0","亚盘盘口".decode('utf-8'),'亚盘胜'.decode('utf-8'),'亚盘平'.decode('utf-8'),'亚盘负'.decode('utf-8'),'欧赔胜'.decode('utf-8'),'欧赔平'.decode('utf-8'),'欧赔负'.decode('utf-8'),'胜概率'.decode('utf-8'),'平概率'.decode('utf-8'),'负概率'.decode('utf-8'),'胜凯利'.decode('utf-8'),'平凯利'.decode('utf-8'),'负凯利'.decode('utf-8')]
for i in range(0,len(columnames)):
    sheet1.write(0,i,columnames[i],style_default)
for vals in result:
    l+=1
    pdate = vals[0]
    lg = vals[1]
    homesxname = vals[2]
    awaysxname = vals[3]
    win = vals[4]
    draw = vals[5]
    lost = vals[6]
    jishi_m = vals[7]
    lglike = ''
    ypWin=0.0
    ypDraw=0.0
    ypLost=0.0
    upWin=0.0
    upDraw=0.0
    upLost=0.0
    gmwin = 0.0
    gmdraw = 0.0
    gmlost = 0.0

    for c in lg:
        lglike+=c+'%'
    ysql = "select a.r310,count(*) from  (select case when resulenum>0 then '3' when resulenum=0 then '1'  when resulenum<0 then '0' end r310 from tb_rate_power_rs  where lg like   '"+lglike+"' and resulenum is not null and jishi_m='"+jishi_m+"') a group by a.r310;"

    if win>lost:
        uMax=float(lost)+0.05
        uMin=float(lost)-0.05
        usql ="  select a.r310,count(*) from  (select case  when resulenum>0 then '3'  when resulenum=0 then '1' when resulenum<0 then '0' end r310 from tb_rate_power_rs  where lg like  '"+lglike+"'  and resulenum is not null  and lost>"+str(uMin)+" and lost<"+str(uMax)+") a group by a.r310;"
    else:
        uMax=float(win)+0.05
        uMin=float(win)-0.05
        usql ="  select a.r310,count(*) from  (select case  when resulenum>0 then '3'  when resulenum=0 then '1' when resulenum<0 then '0' end r310 from tb_rate_power_rs  where lg like  '"+lglike+"'  and resulenum is not null  and win>"+str(uMin)+" and win<"+str(uMax)+") a group by a.r310;"

    ywin =0
    ydraw=0
    ylost=0
    cur.execute(ysql)
    yresult = cur.fetchall()
    for yval in yresult:
       if yval[0] == '0':
           ylost = yval[1]
       if yval[0] == '1':
           ydraw = yval[1]
       if yval[0] == '3':
           ywin = yval[1]
    ytotal = ywin+ydraw+ylost
    if ytotal != 0:
        ypWin = ywin/ytotal*1.00
        ypDraw = ydraw/ytotal*1.00
        ypLost = ylost/ytotal*1.00

    uwin =0
    udraw=0
    ulost=0
    cur.execute(usql)
    uresult = cur.fetchall()
    for uval in uresult:
       if uval[0] == '0':
           ulost = uval[1]
       if uval[0] == '1':
           udraw = uval[1]
       if uval[0] == '3':
           uwin = uval[1]
    utotal = uwin+udraw+ulost
    if utotal != 0:
        upWin = uwin/utotal
        upDraw = udraw/utotal
        upLost = ulost/utotal
    gmwin=math.sqrt(ypWin*upWin)
    gmdraw=math.sqrt(ypDraw*upDraw)
    gmlost=math.sqrt(ypLost*upLost)
    klwin=(gmwin*(float(win)-1)-1+gmwin)/(float(win)-1)
    kldraw=(gmdraw*(float(draw)-1)-1+gmdraw)/(float(draw)-1)
    kllost=(gmlost*(float(lost)-1)-1+gmlost)/(float(lost)-1)
    sheet1.write(l,0,pdate)
    sheet1.write(l,1,lg)
    sheet1.write(l,2,homesxname+"vs"+awaysxname)
    sheet1.write(l,3,win)
    sheet1.write(l,4,draw)
    sheet1.write(l,5,lost)
    sheet1.write(l,6,jishi_m)
    sheet1.write(l,7,ypWin)
    sheet1.write(l,8,ypDraw)
    sheet1.write(l,9,ypLost)
    sheet1.write(l,10,upWin)
    sheet1.write(l,11,upDraw)
    sheet1.write(l,12,upLost)
    sheet1.write(l,13,gmwin)
    sheet1.write(l,14,gmdraw)
    sheet1.write(l,15,gmlost)
    sheet1.write(l,16,klwin)
    sheet1.write(l,17,kldraw)
    sheet1.write(l,18,kllost)
    print ypWin,ypDraw,ypLost,upWin,upDraw,upLost,gmwin,gmdraw,gmlost,klwin
    print '-----------------------------------------'
fliename='kelly_'+time.strftime('%Y-%m-%d')
defatul_f = r'E:\1579\excel'       # ???��??
#f = raw_input(u'????????????��???????????????')
f=''
f_name = r'\%s.xls' % fliename
filepath = [defatul_f+f_name, f+f_name][f != '']
excelfile.save(filepath)
cur.close()
conn.close()
