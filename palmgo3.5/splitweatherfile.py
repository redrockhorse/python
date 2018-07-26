# -*- coding: utf8 -*-
#encoding=utf-8
#By @mahy
#email:kkkkbj@163.com
#分割天气数据
outfile=None
with open('E:\\desktop\\weatherhis.txt','r') as infile:
    i=0
    j=0
    for line in infile:
        if i%3240==0:
            if outfile != None:
                outfile.close()
            j+=1
            outfile=open('E:\\desktop\\a\\weatherhis'+str(j)+'.txt','w')
        outfile.write(line)
        i+=1

