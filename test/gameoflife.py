# -*- coding:utf-8 -*-
#@Time : 2020/2/7 下午4:53
#@Author: kkkkibj@163.com
#@File : gameoflife.py

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#生命游戏
'''
Game of life World
author: Pleiades
'''

import pygame
from sys import exit
import numpy as np
import matplotlib.pyplot as plt

fps = 300
generator_times = 0
dst = np.zeros((400,400))
screem = pygame.display.set_mode((400,400))
pygame.display.set_caption('巴拉巴拉小魔仙')
fclock = pygame.time.Clock()

def blit(dst,src,rec):
    '''
    帮助成为初代对象，用途：把src的填进dst中，位置为rec，用法同pygame中的blit。

    '''
    shape = height,width = src.shape
    dst[rec[0]:rec[0]+height,rec[1]:rec[1]+width] = src
    return dst

s = np.eye(52)
s += s[:,::-1]
s = blit(dst,s,(200-26,200-26))

'''
生命游戏规则来源：百度 https://baike.baidu.com/item/%E7%94%9F%E5%91%BD%E6%B8%B8%E6%88%8F/2926434?fr=aladdin
1． 如果一个细胞周围有3个细胞为生（一个细胞周围共有8个细胞），则该细胞为生（即该细胞若原先为死，则转为生，若原先为生，则保持不变） 。
2． 如果一个细胞周围有2个细胞为生，则该细胞的生死状态保持不变；
3． 在其它情况下，该细胞为死（即该细胞若原先为生，则转为死，若原先为死，则保持不变）。
'''

def gen_next(s):
    s2 = np.zeros((400,400))
    for i in range(1,399):
        for j in range(1,399):
            arround = np.array([[s[i-1,j-1],s[i-1,j],s[i-1,j+1]],
                            [s[i,j-1],0,s[i,j+1]],
                            [s[i+1,j-1],s[i+1,j],s[i+1,j+1]]])
            if arround.sum() == 3:s2[i,j] = 1
            elif s[i,j] == 0 and arround.sum() == 2:s2[i,j] = 0
            elif s[i,j] == 1 and arround.sum() == 2:s2[i,j] = 1
            else :s2[i,j] = 0
    return s2

while True:
    fclock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:exit()
        else:pass

    s  = gen_next(s)
    body = pygame.surfarray.make_surface(s*255)
    screem.fill((0,0,0))
    screem.blit(body,(0,0))
    pygame.display.update()
    generator_times += 1
    if generator_times %10 == 0:print('第 %s 代...'%generator_times)
    screem_array =  pygame.surfarray.array2d(screem)[200-40:200+40,200-40:200+40]
    plt.imsave('%s.jpg'%generator_times,screem_array)
