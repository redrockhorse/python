# -*- coding: utf8 -*-
# !/usr/bin/python
import random
'''
v1=[1,2,8,9,10,5,6,7]
v2=[4,10,12,11,13]
v3=[17,18,19,20]
v4=[20,22,17,19,23]
v5=[23,29,21,22]
v6=[31,32,33]
v7=[7,5,13,6,15]
'''
#print(random.randint)#v1': '11', 'v2': '18', 'v3': '20', 'v4': '23', 'v5': '31', 'v6': '32', 'v7': '15',
#'v1': '03', 'v2': '15', 'v3': '17', 'v4': '23', 'v5': '27', 'v6': '30',
def ssq():
    lastnum = [2,4,5,8,11,30]
    '''
    20181125 v1-5x3120 v2-10x v3-10x v4-812x v5-7x31 v6-5x51
    v1 = [1, 2, 8, 9, 10, 5, 6, 7]
    v2 = [4, 10, 12, 11, 13]
    v3 = [17, 18, 19, 20]
    v4 = [20, 22, 17, 19, 23]
    v5 = [23, 29, 21, 22]
    v6 = [31, 32, 33]
    v7 = [7, 5, 13, 6, 15]
    '''
    v1 = [4, 5 ,6, 2, 3, 1, 2, 8,9,10]
    v2 = [9, 10, 12, 4, 13,3,14,16,15,2]
    v3 = [17, 18, 19, 10,20,8,9,21,7,22]
    v4 = [20, 22, 17, 19, 23,18,16,24]
    v5 = [26,25,27,23,29,22,30,21,20,24]
    v6 = [31, 32, 33,30,29,28,27,26]
    v7 = [7, 5, 13, 6, 15,1,14,10,3]
    x1=0
    x2=0
    x3=0
    x4=0
    x5=0
    x6=0
    x7=0
    i=0
    while i<5:
        samenum =0
        random.shuffle(v1)
        random.shuffle(v2)
        random.shuffle(v3)
        random.shuffle(v4)
        random.shuffle(v5)
        random.shuffle(v6)
        random.shuffle(v7)
        x1=v1[0]
        for t in v2:
            if t>x1:
                x2=t
                break
        for t in v3:
            if t>x2:
                x3=t
                break
        for t in v4:
            if t>x3:
                x4=t
                break
        for t in v5:
            if t>x4:
                x5=t
                break
        for t in v6:
            if t>x5:
                x6=t
                break
        x7=v7[0]
        redarr =[x1,x2,x3,x4,x5,x6]
        c=[x for x in redarr if x in lastnum]
        if len(c)>1:
            continue
        #print(str(v1[0])+','+str(v2[0])+','+str(v3[0])+','+str(v4[0])+','+str(v5[0])+','+str(v6[0])+'-'+str(v7[i]))
        print(str(x1) + ',' + str(x2) + ',' + str(x3) + ',' + str(x4) + ',' + str(x5) + ',' + str(x6) + '-' + str(x7))
        #print(str(x1) + ',' + str(x2) + ',' + str(x3) + ',' + str(x4) + ',' + str(x5) + ',' + str(x6) + '-5' )
        i+=1



def ssq_ly():
    lastnum=[11,14,16,18,24,33]
    '''
    20181125 v1-5x3120 v2-10x v3-10x v4-812x v5-7x31 v6-5x51
    v1 = [1, 2, 8, 9, 10, 5, 6, 7]
    v2 = [4, 10, 12, 11, 13]
    v3 = [17, 18, 19, 20]
    v4 = [20, 22, 17, 19, 23]
    v5 = [23, 29, 21, 22]
    v6 = [31, 32, 33]
    v7 = [7, 5, 13, 6, 15]
    '''
    v1 = [4, 5 ,6, 2, 3, 1, 2, 8,9,10]
    v2 = [9, 10, 12, 4, 13,3,14,16,15,2]
    v3 = [17, 18, 19, 10,20,8,9,21,7,22]
    v4 = [20, 22, 17, 19, 23,18,16,24]
    v5 = [26,25,27,23,29,22,30,21,20,24]
    v6 = [31, 32, 33,30,29,28,27,26]
    v7 = [7, 5, 13, 6, 15,1,14,10,3]
    x1=0
    x2=0
    x3=0
    x4=0
    x5=0
    x6=0
    x7=0
    i=0
    while i<10:
        samenum =0
        random.shuffle(v1)
        random.shuffle(v2)
        random.shuffle(v3)
        random.shuffle(v4)
        random.shuffle(v5)
        random.shuffle(v6)
        random.shuffle(v7)
        x1=v1[0]
        if x1%2 ==0:
            continue
        for t in v2:
            if t>x1 and t%2==0:
                x2=t
                break
        for t in v3:
            if t>x2 and t%2==0:
                x3=t
                break
        for t in v4:
            if t>x3 and t%2==0:
                x4=t
                break
        for t in v5:
            if t>x4 and t%2==0:
                x5=t
                break
        for t in v6:
            if t>x5 and t%2==0:
                x6=t
                break
        #x7=v7[0]
        x7 = 12
        redarr =[x1,x2,x3,x4,x5,x6]
        c=[x for x in redarr if x in lastnum]
        if len(c)>1:
            continue
        #print(str(v1[0])+','+str(v2[0])+','+str(v3[0])+','+str(v4[0])+','+str(v5[0])+','+str(v6[0])+'-'+str(v7[i]))
        print(str(x1) + ',' + str(x2) + ',' + str(x3) + ',' + str(x4) + ',' + str(x5) + ',' + str(x6) + '-' + str(x7))
        i+=1

#v1': '01', 'v2': '11', 'v3': '26', 'v4': '33', 'v5': '35', 'v6': '02', 'v7': '10'
def lt():
    lastnum = [3,9,15,18,26]
    lastnum_h = [6, 12]
    v1=[11,12,4,5,6]
    v2=[14,15,16,17,9]
    v3=[25,21,24,15,19]
    v4=[29,30,32,24,26]
    v5=[35,34,33,28,32]
    v6=[1,4,5,3,6]
    v7=[12,11,10,9,8]
    x1=0
    x2=0
    x3=0
    x4=0
    x5=0
    x6=0
    x7=0
    i = 0
    while i < 5:
        samenum = 0
        samenum_h = 0
        random.shuffle(v1)
        random.shuffle(v2)
        random.shuffle(v3)
        random.shuffle(v4)
        random.shuffle(v5)
        random.shuffle(v6)
        random.shuffle(v7)
        x1=v1[0]
        for t in v2:
            if t>x1:
                x2=t
                break
        for t in v3:
            if t>x2:
                x3=t
                break
        for t in v4:
            if t>x3:
                x4=t
                break
        for t in v5:
            if t>x4:
                x5=t
                break
        x6=v6[0]
        for t in v7:
            if t>x6:
                x7=t
                break
        redarr = [x1, x2, x3, x4, x5]
        bluearr=[x6,x7]
        c = [x for x in redarr if x in lastnum]
        if len(c) > 1:
            continue
        c = [x for x in bluearr if x in lastnum_h]
        if len(c) > 1:
            continue
        #print(str(v1[0])+','+str(v2[0])+','+str(v3[0])+','+str(v4[0])+','+str(v5[0])+','+str(v6[0])+'-'+str(v7[i]))
        print(str(x1) + ',' + str(x2) + ',' + str(x3) + ',' + str(x4) + ',' + str(x5) + '-' + str(x6) + ',' + str(x7))
        i+=1
from collections import Counter
def spsnum():
    red_arr =['06','10','16','20','27','32','10','11','13','21','27','31','01','06','07','11','13','15','04','19','20','22','28','33','01','02','09','10','15','22']
    print(Counter(red_arr).most_common())
#lt()
print('-----------------------')
#ssq_ly()
ssq()
#spsnum()
