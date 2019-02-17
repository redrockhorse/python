# -*- coding: utf8 -*-
#encoding=utf-8
#By @mahy
#email:kkkkbj@163.com
#17q2道路拓扑，完成朱老师选址项目
import sqlite3
basedir='/Users/hongyanma/Desktop/nr1'
conn = sqlite3.connect(basedir+'/nr1.db')
c = conn.cursor()
midfilepath = basedir+'/17q2nr11.MID'
miffilepath = basedir+'/17q2nr11_BD.MIF'
def createLinkTable():
    c.execute('''CREATE TABLE TB_MIF
           (LINKID VARCHAR PRIMARY KEY,
           LINK         TEXT);''')
    c.execute('''CREATE TABLE TB_MID
               (LINKID VARCHAR PRIMARY KEY,
               FJCID           VARCHAR    NOT NULL,
               TJCID           VARCHAR    NOT NULL,
               NAMECODE        VARCHAR    NOT NULL,   
               PROVINCENAME    VARCHAR    NOT NULL,
               CITYNAME        VARCHAR    NOT NULL);''')

import  time
def initData():
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    midarr =[]
    mifarr =[]

    with open(midfilepath,'r') as midfile:
        line = midfile.readline()
        while line:
            tmp=line.split(',')
            LINKID=tmp[1].strip('"')
            FJCID=tmp[2].strip('"')
            TJCID=tmp[3].strip('"')
            NAMECODE=tmp[4]
            PROVINCENAME=tmp[22]
            CITYNAME = tmp[24]
            midarr.append([LINKID,FJCID,TJCID,NAMECODE,PROVINCENAME,CITYNAME])
            line = midfile.readline()
            #break
        #print(len(midarr))


    with open(miffilepath, 'r') as miffile:
        line = miffile.readline()
        while line:
            if line.find('PLine') != -1:
                pointsnum = line.split(' ')[1].strip('\n')
                #print(pointsnum)
                linestr =''
                for n in range(int(pointsnum)):
                    pointsline = miffile.readline().strip('\n').split(' ')
                    linestr += pointsline[0]+','+pointsline[1]+';'
                mifarr.append(linestr)
            elif line.find('Line') != -1:
                pointsline = line.strip('\n').split(' ')
                #print(pointsline)
                mifarr.append(pointsline[1]+','+pointsline[2]+';'+pointsline[3]+','+pointsline[4]+';')
            line = miffile.readline()
        #print(len(mifarr))

    for i in range(len(mifarr)):
        c.execute("INSERT INTO TB_MIF (LINKID,LINK)  VALUES('" + midarr[i][0] + "','" + mifarr[i]  + "')")
        c.execute("INSERT INTO TB_MID (LINKID,FJCID,TJCID,NAMECODE,PROVINCENAME,CITYNAME)  VALUES('" + midarr[i][0] + "','" + midarr[i][1] + "','" + midarr[i][2] +"','" + midarr[i][3] +"','" + midarr[i][4] +"','" + midarr[i][5] +"')")
        if i%100==0:
            conn.commit()
    conn.commit()
    print('done!!!')
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    #c.execute("INSERT INTO LINK (SPOINT,EPOINT,LINK)  VALUES('" + spstr + "','" + epstr + "','" + linkstr + "')")
    #conn.commit()

def fetchData():
    roadnamearr=[]
    lablepoints=[]
    #cursor = c.execute("SELECT LINKID,FJCID,TJCID,NAMECODE,PROVINCENAME,CITYNAME  from TB_MID WHERE PROVINCENAME ='山东省'" )
    cursor = c.execute("SELECT  NAMECODE from TB_MID WHERE PROVINCENAME ='山东省' or PROVINCENAME ='江苏省' group by NAMECODE")
    #cursor = c.execute("SELECT count(*) from LINK " )
    values = cursor.fetchall()
    #print(values)

    for row in values:
        if row[0].find('S')!=-1 or row[0].find('G')!=-1:
            #print(row[0])
            roadnamearr.append(row[0])
    print(len(roadnamearr))
    for i in range(len(roadnamearr)):
        cursor = c.execute("SELECT  LINKID from TB_MID WHERE NAMECODE='"+roadnamearr[i]+"'")
        values = cursor.fetchone()
        #print(values[0])
        cursor = c.execute("SELECT  LINK from TB_MIF WHERE LINKID='" + values[0] + "'")
        link = cursor.fetchone()
        #print(link[0])
        point=link[0].split(';')[0].split(',')
        lablepoints.append(point)
    print(lablepoints)

if __name__ =='__main__':
    #createLinkTable()
    #initData()
    #print('sss')
    fetchData()

