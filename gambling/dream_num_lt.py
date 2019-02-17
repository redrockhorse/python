# -*- coding: utf8 -*-
# !/usr/bin/python
import random

#arr=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35]
#print(len(arr))

# lastnum = [9,18,29,31,33]
# i = 0
# while i < 5:
#     tmp = []
#     while len(tmp)<5:
#         x=random.randint(1,35)
#         if x not in tmp:
#             tmp.append(x)
#     c = [x for x in tmp if x in lastnum]
#     if len(c) > 1 or sum(tmp) != 45:
#         continue
#     i+=1
#     #print(tmp)
#     #print(sum(tmp))
#     print(str(tmp[0])+","+str(tmp[1])+","+str(tmp[2])+","+str(tmp[3])+","+str(tmp[4])+"-4,5")

def tj():
    sarr = [['02','03','06','15','25','30','02'],['03','05','06','17','26','33','08'],['07','17','19','20','21','29','11'],['03','08','16','17','21','29','06'],['01','03','07','08','25','26','14'],['03','12','13','25','26','31','03'],['03','05','11','15','20','23','09'],
            ['11','13','16','21','22','23','02'],['01','05','09','20','28','32','12'],['06','07','12','16','22','25','07'],['07','08','09','15','22','27','12'],['02','05','09','15','24','25','11'],['03','08','10','19','26','33','03'],['02','04','12','14','19','25','06']]
    i=0
    rarr =[]
    while i<5:
        #x = random.randint(0, 5)
        y = random.randint(0, 13)
        t=sarr[y][0]
        iarr =[t]
        #print(i)

        while len(iarr)<6:
            #x = random.randint(0, 5)
            y = random.randint(0, 13)
            #print(x,y)
            t = sarr[y][len(iarr)-1]
            print(iarr)
            #print(t,iarr[-1])
            if t>iarr[-1]:
                iarr.append(t)
        #print(iarr)
        rarr.append(iarr)
        i += 1
    print(rarr)



tj()