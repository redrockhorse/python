# -*- coding: utf8 -*-
#encoding=utf-8
# coding=utf-8
#By @mahy
#email:kkkkbj@163.com
#处理od数据


import sqlite3
conn = sqlite3.connect('/Users/hongyanma/Downloads/2018_gdhd_od/od.db')
c = conn.cursor()
def createTab():
    c.execute('''CREATE TABLE OD
           (CARID TEXT    NOT NULL,
           STARTLON           REAL    NOT NULL,
           STARTLAT           REAL     NOT NULL,
           ENDLON           REAL    NOT NULL,
           ENDLAT           REAL     NOT NULL,
           USETIME        INT,
           DISTANCE         REAL,
           STARTTIME         TEXT,
           ENDTIME         TEXT);''')

def formatTime(str):
     #print(str)
     a = str.split('-')
     y=a[0]
     m=a[1]
     d=a[2].split()[0]
     if int(m)<10:
         m='0'+m
     if int(d)<10:
         d = '0'+d
     H = a[2].split()[1].split(":")[0]
     M = a[2].split()[1].split(":")[1]
     S = a[2].split()[1].split(":")[2]
     if int(H)<10:
         H='0'+H
     if int(M)<10:
         M='0'+M
     if int(S)<10:
         S='0'+S
     return y+"-"+m+"-"+d+" "+H+":"+M+":"+S

def putDataInToTB(filename):
    f_dir ="/Users/hongyanma/Downloads/2018_gdhd_od/"+filename+".txt"
    print(f_dir)
    rf = open(f_dir,'r')
    i =0
    for line in rf:
        data_array = line.split(',')
        # carId = data_array[0]
        # start = [data_array[1],data_array[2]]
        # end = [data_array[3],data_array[4]]
        # usetime = data_array[5]
        # distance = data_array[6]
        if i >0:
            endtime = formatTime(data_array[8])
            startime = formatTime(data_array[7])
            c.execute("INSERT INTO OD (CARID,STARTLON,STARTLAT,ENDLON,ENDLAT,USETIME,DISTANCE,STARTTIME,ENDTIME) VALUES('"+data_array[0]+"',"+data_array[1]+","+data_array[2]+","+data_array[3]+","+data_array[4]+","+data_array[5]+","+ data_array[6]+",'"+startime+"','"+endtime+"')")
        i=i+1
        #print(i)
        if i%500 ==0:
            conn.commit()
    print('filecount:',i)
    conn.commit()
import datetime
def handleData():
    cursor = c.execute("SELECT count(*)  from OD")
    for row in cursor:
       print("db count = ", row[0])
    # cursor = c.execute("SELECT STARTLON,STARTLAT,ENDLON,ENDLAT,STARTTIME  from OD order by STARTTIME ASC")
    # for row in cursor:
    #    print("db count = ", row[4])
    d1 = datetime.datetime(2018,1,22,0,0,0)
    dtmp = d1
    for i in range(7*24):
        d2 = dtmp +datetime.timedelta(hours=1)
        sql_time = d2.strftime("%Y-%m-%d %H:%M:%S")
        #print(sql_time)
        #print(dtmp.strftime("%Y-%m-%d %H:%M:%S"))
        file_time = dtmp.strftime("%Y%m%d%H")
        #print(file_time)
        cursor = c.execute("SELECT STARTLON,STARTLAT,ENDLON,ENDLAT,STARTTIME  from OD where STARTTIME>='"+dtmp.strftime("%Y-%m-%d %H:%M:%S")+"' and STARTTIME<'"+sql_time+"'" )
        wf = open("/Users/hongyanma/Downloads/2018_gdhd_od/"+file_time+".json","w+")
        json_str ="{\"data\":["
        j = 0
        values = cursor.fetchall()
        for row in values:
           j=j+1
           #print("db count = ", row[4])
           if j == len(values):
               json_str = json_str+"[["+str(row[0])+","+str(row[1])+"],["+str(row[2])+","+str(row[3])+"]]"
           else:
               json_str = json_str+"[["+str(row[0])+","+str(row[1])+"],["+str(row[2])+","+str(row[3])+"]],"

        json_str = json_str+"]}"
        wf.write(json_str)
        wf.close()

        dtmp = d2




if __name__ =="__main__":
    #createTab()
    putDataInToTB('all')
    # putDataInToTB('20180123')
    # putDataInToTB('20180124')
    # putDataInToTB('20180125')
    # putDataInToTB('20180126')
    # putDataInToTB('20180127')
    # putDataInToTB('20180128')
    handleData()
    #cursor.close()
    conn.close()
