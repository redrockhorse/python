# -*- coding:utf-8 -*-
# @Time : 2020/3/19 下午12:40
# @Author: kkkkibj@163.com
# @File : threading_test.py
import threading
import time

def sub_mothed(a,t):
    print(t,a)

def test(a,t):
    if t==1:
        time.sleep(5)
    print(str(t)+'x:'+str(a))
    sub_mothed(a, t)
    a=1


a = 0
t = threading.Thread(target=test, args=(a,1))
t.start()
a=1
t = threading.Thread(target=test, args=(a,2))
t.start()
print(a)
