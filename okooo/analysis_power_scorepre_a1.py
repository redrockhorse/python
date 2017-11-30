# -*- coding: utf8 -*-
from __future__ import division

__author__ = 'mahy'
import MySQLdb



#conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='root',db='jc',port=3306,charset='utf8')
conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='Qd@#$mo658',db='jc',port=3316,charset='utf8')
cur = conn.cursor()
#sqlstr="select lg,homesxname,awaysxname,gametime from tb_rate_power_rs where lg = '英超' and gametime>'2016-08-10' order by gametime asc;"
#sqlstr="select lg,homesxname,awaysxname,gametime from tb_rate_power_rs where lg = '西甲' and gametime>'2016-08-18' order by gametime asc;"
#sqlstr="select lg,homesxname,awaysxname,gametime from tb_rate_power_rs where lg = '德乙' and gametime>'2016-08-04' order by gametime asc;"
sqlstr="select lg,homesxname,awaysxname,gametime from tb_rate_power_rs_a1 where gametime>'2011-01-01' order by gametime desc;"
cur.execute(sqlstr)
result = cur.fetchall()
for vals in result:
    #sqltmp="select h.hv-a.av,h.*,a.* from (select avg(hscore-ascore) as hv,STDDEV_SAMP(hscore-ascore) from tb_rate_power_rs  where lg = '"+vals[0]+"'  and homesxname = '"+vals[1]+"' and pdate>'2016-08-10' and gametime<'"+vals[3].strftime("%Y-%m-%d %H:%M:%S")+"'  and resulenum is not null) h, (select avg(ascore-hscore) as av,STDDEV_SAMP(hscore-ascore) from tb_rate_power_rs where lg = '"+vals[0]+"'    and awaysxname = '"+vals[2]+"'  and pdate>'2016-08-10' and  gametime<'"+vals[3].strftime("%Y-%m-%d %H:%M:%S")+"'   and resulenum is not null) a ;"
    sqltmp="select h.hw,h.hl,h.hwstd,h.hlstd,a.aw,a.al,a.awstd,a.alstd  from (select avg(hscore) as hw,avg(ascore) as hl,STDDEV_SAMP(hscore) as hwstd,STDDEV_SAMP(ascore) as hlstd from tb_rate_power_rs_a1 where homesxname = '"+vals[1]+"' and lg = '"+vals[0]+"'  and   datediff('"+vals[3].strftime("%Y-%m-%d %H:%M:%S")+"',gametime)<120  and datediff('"+vals[3].strftime("%Y-%m-%d %H:%M:%S")+"',gametime)>0 order by gametime desc limit 6) h,  (select avg(hscore) as aw,avg(ascore) as al,STDDEV_SAMP(hscore) as awstd,STDDEV_SAMP(ascore) as alstd  from tb_rate_power_rs_a1 where awaysxname = '"+vals[2]+"' and lg = '"+vals[0]+"'  and   datediff('"+vals[3].strftime("%Y-%m-%d %H:%M:%S")+"',gametime)<120  and datediff('"+vals[3].strftime("%Y-%m-%d %H:%M:%S")+"',gametime)>0  order by gametime desc limit 6) a;"
    #print(sqltmp)
    cur.execute(sqltmp)
    rtmp = cur.fetchone()
    print rtmp

    hw='0'
    if rtmp[0] is not None:
        hw='%0.2f'%rtmp[0]
    hl='0'
    if rtmp[1] is not None:
        hl='%0.2f'%rtmp[1]

    hwstd='0'
    if rtmp[2] is not None:
        hwstd='%0.2f'%rtmp[2]
    hlstd='0'
    if rtmp[3] is not None:
        hlstd='%0.2f'%rtmp[3]

    aw='0'
    if rtmp[4] is not None:
        aw='%0.2f'%rtmp[4]
    al='0'
    if rtmp[5] is not None:
        al='%0.2f'%rtmp[5]

    awstd='0'
    if rtmp[6] is not None:
        awstd='%0.2f'%rtmp[6]
    alstd='0'
    if rtmp[7] is not None:
        alstd='%0.2f'%rtmp[7]

    updatesql ="update tb_rate_power_rs_a1 set hw=%s,hl=%s,hwstd=%s,hlstd=%s,aw=%s,al=%s,awstd=%s,alstd=%s  where gametime='"+vals[3].strftime("%Y-%m-%d %H:%M:%S")+"' and lg= '"+vals[0]+"' and homesxname='"+vals[1]+"' and awaysxname='"+vals[2]+"';"

    print(updatesql)
    cur.execute(updatesql,(hw,hl,hwstd,hlstd,aw,al,awstd,alstd))
    conn.commit()
cur.close()
conn.close()
