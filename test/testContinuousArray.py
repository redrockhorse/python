# -*- coding: utf8 -*-
#encoding=utf-8
#By @mahy
#email:kkkkbj@163.com


#arr = [1,2,3,5,7,8,11]

#arr  = [1,3,5,7]
arr = [90,96,97,98,552,553,554,555,556,557,558,598]
def countInterrupted(array):
    interruptePoint = []
    for i in range(len(array)-1):
        if array[i+1] - array[i]>1:
            interruptePoint.append([array[i],array[i+1]])
    n = len(interruptePoint)
    print(interruptePoint)
    for j in range(n):
        if n%2 == (j+1)%2:
            tmp = interruptePoint[j]
            p = array.index(tmp[0])+1
            for  a  in range(tmp[0]+1,tmp[1]):
                array.insert(p,a)
                p+=1
    return  array


def fillInterrupted(array):
    interruptePoint = []
    for i in range(len(array)-1):
        if array[i+1] - array[i]>1:
            interruptePoint.append([array[i],array[i+1]])
    n = len(interruptePoint)
    for j in range(n):
        if n%2 == (j+1)%2:
            tmp = interruptePoint[j]
            p = array.index(tmp[0])+1
            for  a  in range(tmp[0]+1,tmp[1]):
                array.insert(p,a)
                p+=1
    return  array


if __name__=='__main__':
    ab = countInterrupted(arr)
    print(ab)
