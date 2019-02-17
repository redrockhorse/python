#-*-codeing :utf-8-*-
import numpy as np
import random
import math
from PIL import Image
import matplotlib
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt

# 元胞空间
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['font.family']='sans-serif'
# 解决负号'-'显示为方块的问题
matplotlib.rcParams['axes.unicode_minus'] = False
p = np.zeros((24,2))

# 元胞空间
test =np.ones((102,102))*255
# 出口定位
test[18:30,1:2] = 50
p[0,0:2] = [18,1]
p[1,:] = [29,1]
test[44:56,1:2] = 50
p[2,:] = [44,1]
p[3,:] = [55,1]
test[70:82,1:2] = 50
p[4,:] = [70,1]
p[5,:] = [81,1]
test[1:2,18:30,] = 50
p[6,:] = [1,18]
p[7,:] = [1,29]
test[1:2,44:56] = 50
p[8,:] = [1,44]
p[9,:] = [1,55]
test[1:2,70:82] = 50
p[10,:] = [1,70]
p[11,:] = [1,81]
test[18:30,99:100] = 50
p[12,:] = [18,100]
p[13,:] = [29,100]
test[44:56,100:101] = 50
p[14,:] = [44,100]
p[15,:] = [55,100]
test[70:82,100:101] = 50
p[16,:] = [70,100]
p[17,:] = [81,100]

test[100:101,18:30] = 50
p[18,:] = [100,18]
p[19,:] = [100,29]
test[100:101,44:56] = 50
p[20,:] = [100,44]
p[21,:] = [100,55]
test[99:100,70:82] = 50
p[22,:] = [100,70]
p[23,:] = [100,81]
# 商城定位
test[81:93,10:45] = 144
test[83:93,55:85] = 144
test[82:92,11:44] = 255
test[84:92,56:83] = 255

test[55:70,10:45] = 144
test[55:70,55:85] = 144
test[56:69,11:44] = 255
test[56:69,56:84] = 255

test[55:65,10:20] = 30
test[55:65,10:20] = 30


test[30:45,10:45] = 144
test[30:45,55:85] = 144
test[31:44,11:44] = 255
test[31:44,56:84] = 255

test[8:20,10:45] = 144
test[8:20,55:85] = 144
test[9:19,11:44] = 255
test[9:19,56:84] = 255
# 距离存储
ll = np.zeros((102,102))*1000
for i in range(1,101):
    for j in range(1,101):
        flag = 0
        if i == 1 or j == 1 or i == 100 or j == 100:
            for k in range(0, 24,2):
                if i >= p[k][0] and i <= p[k+1][0] and j >= p[k][1] and j <= p[k+1][1]:
                    ll[i, j] = 0
                    flag = 1
                    break
        if flag==0 and ll[i,j]!=2000:
            max = 999
            for k in range(0, 24):
                x = math.fabs(p[k][0]-i)
                y = math.fabs(p[k][1]-j)
                if max> math.sqrt(x**2+y**2):
                    max = math.sqrt(x**2+y**2)
            ll[i,j] =max

#人群模拟
i = 0
while i<500:
     a = random.randint(1, 101)
     b = random.randint(1, 101)
     if test[a, b] != 0 and test[a, b]!=30 and test[a, b]!= 144:
         test[a, b] = 0
         i += 1

# 运动方向
dirr = [[0, 1],
       [0, -1],
       [-1, -1],
       [1, -1],
       [1, 0],
       [-1, 0],
       [-1, 1],
       [1, 1]]
people =[]
ci=30

sim = test.copy()
while ci>0:
    re =0 # 记录时间间隔的人群疏散量
    for i in range(1,101):
        for j in range(1,101):
            if ll[i, j] == 0 and sim[i, j] == 0:
                re += 1
                sim[i, j] = 255
                continue
            # 人群运动
            if sim[i, j] == 0:
                next_x = 0
                next_y = 0
                min_s = 999
                for k in range(0, 8):
                    x = i+dirr[k][0]
                    y = j+dirr[k][1]
                    if sim[x,y] != 0:
                        if ll[x,y] < min_s:
                            min_s = ll[x, y]
                            next_x = x
                            next_y = y
                if min_s < 999:
                    sim[next_x, next_y] = 0
                    sim[i, j] = 255
    people.append(re)
    ci -= 1

image1 = Image.fromarray(sim)
Image._show(image1)
acpeople = np.cumsum(people)
plt.plot(acpeople,'-o')
plt.title('疏散人口总量与时间的关系')
plt.xlabel('时间间隔')
plt.ylabel('疏散人口总理')
plt.show()

image = Image.fromarray(test)
image.resize((2200,2020))
Image._show(image)