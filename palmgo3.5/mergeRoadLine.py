# -*- coding: utf8 -*-
#encoding=utf-8
#By @mahy
#email:kkkkbj@163.com
#合并路链，成为一条长线
import sqlite3
conn = sqlite3.connect('E:\\ctfo\\ctfodayfile\\201802\\20180222\\chinaroad\\cr.db')
c = conn.cursor()
sf = "E:\\ctfo\\ctfodayfile\\201802\\20180222\\chinaroad\\locfile.txt"
def createLinkTable():
    c.execute('''CREATE TABLE LINK
           (ID INTEGER PRIMARY KEY AUTOINCREMENT,
           SPOINT           VARCHAR    NOT NULL,
           EPOINT           VARCHAR    NOT NULL,
           LINK         TEXT);''')

def initTable(inFile):
    fa = eval(open(inFile).read())
    #print(len(fa))
    print(fa[3][0])
    print(fa[3][-1])
    for i in range(len(fa)):
        linkstr = "["
        for j in range(len(fa[i])):
            linkstr += "["
            linkstr += str(fa[i][j][0])+","
            linkstr += str(fa[i][j][1])
            linkstr += "]"
            if j<len(fa[i])-1:
                linkstr +=","
        linkstr += "]"
        #print(linkstr)
        spstr = str(fa[i][0][0])+","+str(fa[i][0][1])
        epstr = str(fa[i][-1][0])+","+str(fa[i][-1][1])
        c.execute("INSERT INTO LINK (SPOINT,EPOINT,LINK)  VALUES('"+spstr+"','"+epstr+"','"+linkstr+"')")
    conn.commit()
    print('insert down!!!')


def fetchData():
    cursor = c.execute("SELECT ID,SPOINT,EPOINT,LINK  from LINK ORDER BY ID ASC" )
    #cursor = c.execute("SELECT count(*) from LINK " )
    values = cursor.fetchone()
    print(values)
    if values[1] == values[2]:
        print('sss')
    for row in values:
        print(row)


def mergeData():
    #要返回的路线，应为3维数组
    roads = []
    while(True):
        #一条路
        tmproad =[]
        #取一个点作为开始
        cursor = c.execute("SELECT ID,SPOINT,EPOINT,LINK  from LINK ORDER BY ID ASC" )
        values = cursor.fetchone()
        if values is None or len(values) < 1:
            print('There is no data in table!!! Done!')
            print(roads)
            file=open('E:\\ctfo\\ctfodayfile\\201802\\20180222\\chinaroad\\data.txt','w+')
            file.write(str(roads));
            file.close()
            return roads
        bid = pid= id = values[0]
        spstr = values[1]
        epstr = values[2]
        link = eval(values[3])
        if len(link)<3 and spstr == epstr:
            tmproad.append(link[0])
        else:
            for p in link:
                tmproad.append(p)
        c.execute("DELETE  from LINK WHERE ID="+str(id)+"" )
        conn.commit()
        #print(tmproad)
        usedpoint = {}
        #usedpoint[id]=True

        while(True):
            tmpspstr_p = str(tmproad[0][0])+","+str(tmproad[0][1])
            tmpepstr_p = str(tmproad[-1][0])+","+str(tmproad[-1][1])
            tmpspstr_b = str(tmproad[0][0])+","+str(tmproad[0][1])
            tmpepstr_b = str(tmproad[-1][0])+","+str(tmproad[-1][1])
            cflag_p = True #向前拓扑标志
            cflag_b = True #向后拓扑标志
            #向前拓扑
            #print("SELECT ID,SPOINT,EPOINT,LINK  from LINK WHERE EPOINT='"+tmpspstr_p+"' AND ID IS NOT "+str(pid)+" ORDER BY ID ASC" )
            cursor = c.execute("SELECT ID,SPOINT,EPOINT,LINK  from LINK WHERE EPOINT='"+tmpspstr_p+"' AND ID IS NOT "+str(pid)+" ORDER BY ID ASC" )
            values = cursor.fetchone()
            if values is not None and len(values) > 1:
                pid = values[0]
                #if pid  not in usedpoint:
                cflag_p = False
                spstr = values[1]
                epstr = values[2]
                link = eval(values[3])
                if len(link)<3 and spstr == epstr:
                    #tmproad.insert(0,link[0])
                    pass
                else:
                    for i in range(len(link)-1):
                        tmproad.insert(0,link[len(link)-i-2])
                #usedpoint[pid] = True
                c.execute("DELETE  from LINK WHERE ID="+str(pid)+"" )
                #conn.commit()
            #向后拓扑
            #print("SELECT ID,SPOINT,EPOINT,LINK  from LINK WHERE SPOINT='"+tmpepstr_b+"' AND ID != '"+str(bid)+"' ORDER BY ID ASC")
            cursor = c.execute("SELECT ID,SPOINT,EPOINT,LINK  from LINK WHERE SPOINT='"+tmpepstr_b+"' AND ID != '"+str(bid)+"' ORDER BY ID ASC" )
            values = cursor.fetchone()
            if values is not None and len(values) > 1:
                bid = values[0]
                #if bid  not in usedpoint:
                cflag_b = False
                spstr = values[1]
                epstr = values[2]
                link = eval(values[3])
                if len(link)<3 and spstr == epstr:
                    #tmproad.append(link[0])
                    pass
                else:
                    for i in range(len(link)-1):
                        tmproad.append(link[i+1])
                #usedpoint[bid] = True
                c.execute("DELETE  from LINK WHERE ID="+str(bid)+"" )
            #conn.commit()
            if cflag_p and cflag_b:
                break
        if len(tmproad)>1:
            print(tmproad)
            roads.append(tmproad)



import  time
if __name__ == "__main__":
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    createLinkTable()
    initTable(sf)
    #fetchData()
    mergeData()
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    c.close()
    conn.close()
    exit()




