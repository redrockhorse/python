# -*- coding: utf8 -*-
from __future__ import division

__author__ = 'mahy'
import MySQLdb



#conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='root',db='jc',port=3306,charset='utf8')
conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='Qd@#$mo658',db='jc',port=3316,charset='utf8')
cur = conn.cursor()
#sqlstr="select lg,homesxname,awaysxname,gametime from tb_rate_power_rs where lg = '英超' and gametime>'2016-08-10' order by gametime asc;"
#sqlstr="select lg,homesxname,awaysxname,gametime from tb_rate_power_rs where lg = '西甲' and gametime>'2016-08-18' order by gametime asc;"
sqlstr="select lg,homesxname,awaysxname,gametime from tb_rate_power_rs where  gametime>'2017-05-11 22:00:00' and gametime<'2017-05-12 18:00:00' order by gametime asc;"
cur.execute(sqlstr)
result = cur.fetchall()
for vals in result:
   # sqltmp="select h.hv-a.av,h.*,a.* from (select avg(hscore-ascore) as hv,STDDEV_SAMP(hscore-ascore) from tb_rate_power_rs  where lg = '"+vals[0]+"'  and homesxname = '"+vals[1]+"' and pdate>'2016-08-10' and gametime<'"+vals[3].strftime("%Y-%m-%d %H:%M:%S")+"'  and resulenum is not null) h, (select avg(ascore-hscore) as av,STDDEV_SAMP(hscore-ascore) from tb_rate_power_rs where lg = '"+vals[0]+"'    and awaysxname = '"+vals[2]+"'  and pdate>'2016-08-10' and  gametime<'"+vals[3].strftime("%Y-%m-%d %H:%M:%S")+"'   and resulenum is not null) a ;"
    sqltmp="select h.hv-a.av,h.*,a.* from (select avg(hscore-ascore) as hv,STDDEV_SAMP(hscore-ascore) from tb_rate_power_rs  where  homesxname = '"+vals[1]+"' and pdate>'2016-08-10' and gametime<'"+vals[3].strftime("%Y-%m-%d %H:%M:%S")+"'  and resulenum is not null) h, (select avg(ascore-hscore) as av,STDDEV_SAMP(hscore-ascore) from tb_rate_power_rs where lg = '"+vals[0]+"'    and awaysxname = '"+vals[2]+"'  and pdate>'2016-08-10' and  gametime<'"+vals[3].strftime("%Y-%m-%d %H:%M:%S")+"'   and resulenum is not null) a ;"
   # print(sqltmp)
    cur.execute(sqltmp)
    rtmp = cur.fetchall()
    for valtmp in rtmp:
        dv='0'
        hv='0'
        hstq='0'
        av='0'
        astq='0'
        if valtmp[0] is not None:
            dv='%0.2f'%valtmp[0]
        if valtmp[1] is not None:
            hv='%0.2f'%valtmp[1]
        if valtmp[2] is not None:
            hstq='%0.2f'%valtmp[2]
        if valtmp[3] is not None:
            av='%0.2f'%valtmp[3]
        if valtmp[4] is not None:
            astq='%0.2f'%valtmp[4]
        updatesql ="update tb_rate_power_rs set dv='"+dv+"',hv='"+hv+"',hstq='"+hstq+"',av='"+av+"',astq='"+astq+"' where gametime='"+vals[3].strftime("%Y-%m-%d %H:%M:%S")+"' and lg= '"+vals[0]+"' and homesxname='"+vals[1]+"' and awaysxname='"+vals[2]+"';"
        print(updatesql)
       # cur.execute(updatesql)
conn.commit()
cur.close()
conn.close()
