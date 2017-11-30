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
sqlstr="select lg,homesxname,awaysxname,gametime from tb_rate_power_rs_al where gametime>'2011-01-01' and gametime<'2016-11-28' order by gametime desc;"
cur.execute(sqlstr)
result = cur.fetchall()
for vals in result:
    #sqltmp="select h.hv-a.av,h.*,a.* from (select avg(hscore-ascore) as hv,STDDEV_SAMP(hscore-ascore) from tb_rate_power_rs  where lg = '"+vals[0]+"'  and homesxname = '"+vals[1]+"' and pdate>'2016-08-10' and gametime<'"+vals[3].strftime("%Y-%m-%d %H:%M:%S")+"'  and resulenum is not null) h, (select avg(ascore-hscore) as av,STDDEV_SAMP(hscore-ascore) from tb_rate_power_rs where lg = '"+vals[0]+"'    and awaysxname = '"+vals[2]+"'  and pdate>'2016-08-10' and  gametime<'"+vals[3].strftime("%Y-%m-%d %H:%M:%S")+"'   and resulenum is not null) a ;"
    sqltmp="select h.hw+a.al,h.hl+a.aw  from (select avg(hscore) as hw,avg(ascore) as hl from tb_rate_power_rs_al where homesxname = '"+vals[1]+"' and lg = '"+vals[0]+"'  and   datediff('"+vals[3].strftime("%Y-%m-%d %H:%M:%S")+"',gametime)<120  and datediff('"+vals[3].strftime("%Y-%m-%d %H:%M:%S")+"',gametime)>0 order by gametime desc limit 6) h,  (select avg(hscore) as al,avg(ascore) as aw from tb_rate_power_rs_al where awaysxname = '"+vals[2]+"' and lg = '"+vals[0]+"'  and   datediff('"+vals[3].strftime("%Y-%m-%d %H:%M:%S")+"',gametime)<120  and datediff('"+vals[3].strftime("%Y-%m-%d %H:%M:%S")+"',gametime)>0  order by gametime desc limit 6) a;"
    #print(sqltmp)
    cur.execute(sqltmp)
    rtmp = cur.fetchone()
    print rtmp

    hp='0'
    if rtmp[0] is not None:
        hp='%0.2f'%rtmp[0]
    ap='0'
    if rtmp[1] is not None:
        ap='%0.2f'%rtmp[1]
    updatesql ="update tb_rate_power_rs_al set hp='"+hp+"',ap='"+ap+"',hpf='"+hp+"',apf='"+ap+"' where gametime='"+vals[3].strftime("%Y-%m-%d %H:%M:%S")+"' and lg= '"+vals[0]+"' and homesxname='"+vals[1]+"' and awaysxname='"+vals[2]+"';"
    print(updatesql)
    cur.execute(updatesql)
    conn.commit()
cur.close()
conn.close()
