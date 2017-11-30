#!/usr/bin/python
#encoding=utf-8
__author__ = 'mahy'
import sys
reload(sys)
sys.setdefaultencoding('utf8')
def strsamenum(a,b):
    res = []
    for x in a:
        if x in b and x !=' ':
            #print x
            res.append(x)
    return len(res)
def writeresult(linestr):
    w500f = open('D:\\UltraEdit\\500.txt', 'r')
    for line_5 in w500f:
        line_5str = line_5.strip()
        #print "r: "+line_5str
        num = strsamenum(line_5str.decode('gbk'),linestr.decode('gbk'))
        if num>1 and num<3:
           # print line_5,line
            #print line_5.strip(),line.strip()
            rs2.write(line_5str+"|"+linestr+"\n")
        elif num>=3:
            #print line_5str+"|"+line
            rs3.write(line_5str+"|"+linestr+"\n")
        else:
            print

okooo = open('D:\\UltraEdit\\okooo.txt','r')

rs2 = open('D:\\UltraEdit\\rs2.txt', 'w+')
rs3 = open('D:\\UltraEdit\\rs3.txt', 'w+')
for line in okooo:
    linestr=line.strip()
    writeresult(linestr)
    #print "l: "+linestr
okooo.close()
#w500f.close()
rs2.close()
rs3.close()


