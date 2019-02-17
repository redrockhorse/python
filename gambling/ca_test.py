# -*- coding: utf8 -*-
#encoding=utf-8
#By @mahy
#email:kkkkbj@163.com
#元胞自动机测试
import PIL.Image as Image
import matplotlib.pyplot as plt
import numpy as np

'''
newim = Image.new('RGB',(100,100))
for y in range(1,100):
    for x in range(1,100):
        if (x+y)%7==0:
            newim.putpixel((x, y ), (255, 0, 0))
        else:
            newim.putpixel((x, y), (0, 255, 0))
#newim.show()

a = np.array([0.313660827978, 0.365348418405, 0.423733120134,
              0.365348418405, 0.439599930621, 0.525083754405,
              0.423733120134, 0.525083754405, 0.651536351379]).reshape(3,3)
a = np.array([1, 0, 0,
              1, 1, 1,
              1, 1, 0]).reshape(3,3)
a = np.array([[1, 0, 0],
              [1, 1, 1],
              [1, 1, 0]])
# 这是颜色的标注
# 主要使用imshow来显示图片，这里暂时不适用图片来显示，采用色块的方式演示。
plt.imshow(a, interpolation='nearest', cmap='bone', origin='lower')
plt.colorbar(shrink=.90)  # 这是颜色深度的标注，shrink表示压缩比例

plt.xticks(())
plt.yticks(())
plt.show()
'''
'''
N = 33
x = np.random.randn(N)
y = np.random.randn(N)
print(x)
print(y)
plt.scatter(x, y,alpha=0.5,marker='s',)
plt.grid(True)
plt.xlabel('X axis')
plt.ylabel('Y axis')
plt.show()
'''
x=[]
y=[]
v=[]
for i in range(33):
    x.append(i)
for j in range(100):
    y.append(j)
for k in range(3300):
    v.append(k)

height = np.max(y) + 1
width = np.max(x) + 1
arr = np.zeros((height, width))
for i in range(len(x)):
    for j in range(len(y)):
        arr[y[j], x[i]] = v[i*33+j-1]
plt.matshow(arr, cmap='hot')
plt.colorbar()
plt.show()