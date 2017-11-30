#!/usr/bin/python  
#encoding=utf-8  
__author__ = 'mahy'
import MySQLdb
import time
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf8')
conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='Ke_Xing3508',db='jc',port=3306,charset='utf8')
cur = conn.cursor()
def alfunc(arr_r,arr_b,vnum,ps):
    sql_v1="select * from td_ptl_lt_data where v"+'%d' %ps+"='"+vnum+"';"
    print sql_v1
    cur.execute(sql_v1)
    v1_result = cur.fetchall()
    for v1_rs in v1_result:
        sql_tmp="select * from td_ptl_lt_data where pdate>'"+v1_rs[1].strftime('%Y-%m-%d')+"' order by pdate asc limit 1;"
        cur.execute(sql_tmp)
        v_tmp =  cur.fetchall()
        for v in v_tmp:
            if(ps < 7):
                arr_r[int(v[2])]+=1
                arr_r[int(v[3])]+=1
                arr_r[int(v[4])]+=1
                arr_r[int(v[5])]+=1
                arr_r[int(v[6])]+=1
            else:
                arr_b[int(v[7])]+=1
                arr_b[int(v[8])]+=1
if __name__ == '__main__':
    sql="select * from td_ptl_lt_data order by pdate desc limit 1;"
    cur.execute(sql)
    all_results = cur.fetchall()
    for rs in all_results:
        v1 = rs[2]
        v2 = rs[3]
        v3 = rs[4]
        v4 = rs[5]
        v5 = rs[6]
        v6 = rs[7]
        v7 = rs[8]
        pnum = rs[9]
    print "上期号码:".decode('utf-8'),rs[1],pnum,v1,v2,v3,v4,v5,v6,v7
    note = "上期号码".decode('utf-8')+ rs[1].strftime("%Y-%m-%d") + ':  '+v1+','+v2+','+v3+','+v4+','+v5+'-'+v6+','+v7
    #t = datetime.date.fromtimestamp(int(time.mktime(rs[1])))
    pre_pdate = None
    if(rs[1].weekday() == 3):
        datestr = rs[1]+datetime.timedelta(days=4)
        pre_pdate = datestr.strftime("%Y-%m-%d")
    else:
        datestr = rs[1]+datetime.timedelta(days=3)
        pre_pdate = datestr.strftime("%Y-%m-%d")
    arr_r = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    arr_b = [0,0,0,0,0,0,0,0,0,0,0,0,0]
    alfunc(arr_r,arr_b,v1,1)
    alfunc(arr_r,arr_b,v2,2)
    alfunc(arr_r,arr_b,v3,3)
    alfunc(arr_r,arr_b,v4,4)
    alfunc(arr_r,arr_b,v5,5)
    alfunc(arr_r,arr_b,v6,6)
    alfunc(arr_r,arr_b,v7,7)
    print arr_r
    print arr_b
    dic_r = {}
    dic_b = {}
    for i in range(0,len(arr_r)):
        i_str='%d' %i
        if(dic_r.has_key(arr_r[i])):
            dic_r[arr_r[i]]=i_str+'-'+dic_r[arr_r[i]]
        else:
            dic_r[arr_r[i]]=i_str

    for i in range(0,len(arr_b)):
        i_str='%d' %i
        if(dic_b.has_key(arr_b[i])):
            dic_b[arr_b[i]]=i_str+','+dic_b[arr_b[i]]
        else:
            dic_b[arr_b[i]]=i_str
    print '--------------------------------------------------------------------------------------------------------'
    n_r=sorted(dic_r.keys(),reverse=True)
    print "推荐红球:".decode('utf-8'),dic_r[n_r[0]],dic_r[n_r[1]],dic_r[n_r[2]],dic_r[n_r[3]],dic_r[n_r[4]],dic_r[n_r[5]],dic_r[n_r[6]]
    red = dic_r[n_r[0]]+','+dic_r[n_r[1]]+','+dic_r[n_r[2]]+','+dic_r[n_r[3]]+','+dic_r[n_r[4]]+','+dic_r[n_r[5]]+','+dic_r[n_r[6]]+','+dic_r[n_r[7]]+','+dic_r[n_r[8]]
    n_b=sorted(dic_b.keys(),reverse=True)
    print "推荐蓝球:".decode('utf-8'),dic_b[n_b[0]],dic_b[n_b[1]]
    blue = dic_b[n_b[0]]+','+dic_b[n_b[1]]+','+dic_b[n_b[2]]+','+dic_b[n_b[3]]
    pre_sql = sql="INSERT INTO `td_ptl_lt_pre` (`pdate`,`red`,`blue`,`note`) VALUES (%s,%s,%s,%s);"
    delete_sql='delete from td_ptl_lt_pre where pdate="'+pre_pdate+'"'
    cur.execute(delete_sql)
    cur.execute(sql,(pre_pdate,red,blue,note))
    conn.commit()
    cur.close()
    conn.close()
