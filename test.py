__author__ = 'mahone'

import numpy as np

def getNameByOneHotCode(oneHot,dictArray):
    oneHotArray = np.array(oneHot)
    _positon =np.argmax(oneHotArray)
    name = dictArray[_positon]
    return name

if __name__ == '__main__':
    oneHot = [0,0,1,0,0,0,0,0,0]
    dict ={}
    dict['a']=0
    dict['b']=1
    dict['c']=2
    dict['d']=3
    dict['e']=4
    dict['f']=5
    dict['g']=6
    dict['h']=7
    dictArray=['a','b','c','d','e','f','g','h','f']
    name = getNameByOneHotCode(oneHot,dictArray)
    print(name)