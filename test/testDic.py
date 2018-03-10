__author__ = 'mahy'

dic = {}
class link:
    def __init__(self,lable):
        self.lable = lable

class linkLable:
    def __init__(self,name):
        self.name = name



def changeDicFunc(dic,name):
    for linkId in dic:
        link = dic[linkId]
        link.lable.name

from collections import Iterator
if __name__=="__main__":
    l1 = [1,2,3,4,5]
    l2 = l1.copy()
    l1.reverse()
    print(l1)
    print(l2)
    print(l2[-1])
    print(6 in l2)

