#!/usr/bin/python
#encoding=utf-8
#lbp feature extraction
__author__ = 'mahy'


import random
#print(random.uniform(0.8,1.1))
l =[]
for i in range(1,36):
    l.append(i)
print(l)



b = []
for i in range(1,13):
    b.append(i)
print(b)

#print(random.sample(l,4))
#print(random.sample(r,2))

n=3
for i in range(n):
    lr = random.sample(l,5) #[13:36]
    br = sorted(random.sample(b,2))
    red = sorted(lr)
    result = ''
    for num in red :
        if num <10:
            result += '0'+str(num)+','
        else:
            result += str(num) + ','
    if br[0] < 10:
        result +='-'+'0'+str(br[0])
    else:
        result += '-'  + str(br[0])

    if br[1] < 10:
        result +=','+'0'+str(br[1])
    else:
        result += ','  + str(br[1])
    print(result)

