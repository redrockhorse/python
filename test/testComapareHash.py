# Hash值对比
from functools import reduce
def cmpHash(hash1, hash2):
    n = 0
    # hash长度不同则返回-1代表传参出错
    if len(hash1)!=len(hash2):
        return -1
    # 遍历判断
    for i in range(len(hash1)):
        # 不相等则n计数+1，n最终为相似度
        a = int(hash1[i],16)
        b = int(hash2[i],16)
        c = list(bin(a ^ b)[2:])
        d = reduce(lambda x, y: int(x)+int(y), c)
        n = n + int(d)
    #print(n)
    return n

h1 = '0001a1fffffdc740'
h2 = '0001a17fffc5e500'
h3 = '0040a07ffff0e200'
h4 = '3c7c0200fefe7c00'

cmpHash(h1, h2)
cmpHash(h1, h3)
cmpHash('0001a1fffffdc740', '0073217fffff4400')
'''
print(bin(int('1',16)))
print(bin(int('f',16)))

a=int('1',16)
b=int('f',16)
print(bin(a^b)[2:])
c = list(bin(a^b)[2:])
print(c)
import  numpy as np
print(reduce(lambda x, y: int(x)+int(y), c))
'''