__author__ = 'Thinkpad'
import time
a = [[1,2],[3,4],[5,6]]
c1 = [x[0] for x in a]
c2 = [x[1] for x in a]

a1=[1.333,2.1]
a2=[1.333,2]
print(a1==a2)
print(max(c1))
print(max(c2))
print(max(1,2))
print('start-time',time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
i=0
++i
print(i)
i+=1
print(i)

if True:
    pass
if 1==1:
    print(111)
