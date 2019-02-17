import PIL.Image as Image
import random

import pymysql
import json
import matplotlib.pyplot as plt

def findNearestPoint(p0,data):
    if p0 in data:
        data.remove(p0)
    l=28
    i=0
    lt=27
    dic={}
    pr=None
    while lt < 28 and i<len(data):
        p = data[i]
        lt = pow((pow((p[0] - p0[0]), 2) + pow((p[1] - p0[1]), 2)), 0.5)
        if l > lt and lt<2:
            l = lt
            dic[l]=p
            pr=p
        i+=1
    if None != pr:
        data.remove(pr)
    #print(p0,pr,l)
    return pr,data

import numpy as np
import tensorflow as tf
def convolution(data,n):
    print('convolution')
    #print(data)
    a=np.zeros([33,33])
    #print(a)
    for i in range(6*33*n,6*33*(n+1)):
        y=data[i][0]-1
        x=data[i][1]%33
        a[x][y]=1
    ck=np.mat('1.0,1.0,1.0;1.0 -7.0 1.0;1.0 1.0 1.0')#卷积核
    #r=np.convolve(a,ck,'full')
    input = tf.convert_to_tensor(a)
    input = tf.expand_dims(input, 0)
    input = tf.expand_dims(input, -1)
    print(input)
    ft=tf.convert_to_tensor(ck)
    ft = tf.expand_dims(ft,-1)
    ft = tf.expand_dims(ft,-1)
    print(ft)
    r = tf.nn.conv2d(input, ft, strides=[1,1,1,1], padding='SAME')
    #print(r)
    r=tf.reshape(r,(33, 33))
    sess = tf.Session()
    rt=sess.run(r)
    eigenvalues, eigenvectors = sess.run(tf.self_adjoint_eig(r))#tf求特征值和特征向量
    print(eigenvalues)
    print(eigenvectors)

    newim = Image.new("RGBA", (33 , 33), (255, 0, 0, 0))
    for i in range(32):
        for j in range(32):
            op=0
            if rt[i][j]==1:
                op=125
            if rt[i][j]==2:
                op = 200
            if rt[i][j]>2:
                op=255
            newim.putpixel((j+1, i+1), (255, 0, 0, op))

    newim.show()
    #print(rt[0])

if __name__=="__main__":
    rdata = {}
    with open('/Users/hongyanma/gitspace/python/python/okooo/ssq_png.json', 'r') as inputfile:
        rdata = json.load(inputfile)
    data = rdata['data']
    print(len(data)/6/33)
    convolution(data,5)
    '''
    result =[]
    while len(data)>0:
        c = []
        p0 = data[0]
        c.append(p0)
        p,data=findNearestPoint(p0,data)
        while p != None:
            c.append(p)
            p, data = findNearestPoint(p, data)
        result.append(c)
        #print(c)
    print(result)
    for line in result:
        x=[]
        y=[]
        y0=0
        if len(line)>5:
            for i in range(len(line)):
                if i==0:
                    y0=line[i][1]
                x.append(line[i][0])
                y.append(line[i][1]-y0)

            print(x)
            print(y)
            plt.plot(x, y)
            #plt.scatter(x, y)
    plt.show()
    '''
    '''
    import numpy as np

    x = np.linspace(0, 2 * np.pi, 100)
    y1, y2 = np.sin(x), np.cos(x)

    plt.plot(x, y1)
    plt.plot(x, y2)

    plt.title('line chart')
    plt.xlabel('x')
    plt.ylabel('y')

    plt.show()
    '''




'''
conn=pymysql.connect(host='127.0.0.1',user='root',passwd='Qd@#$mo658',db='jc',port=3306,charset='utf8', cursorclass = pymysql.cursors.DictCursor)
cursor = conn.cursor()
sql="select * from td_ptl_ssq_data order by pdate asc"#td_ptl_ssq_data,td_ptl_lt_data
cursor.execute(sql)

tab=[]

v1_result = cursor.fetchall()
for row in v1_result:
    r=[]
    r.append(int(row['v1']))
    r.append(int(row['v2']))
    r.append(int(row['v3']))
    r.append(int(row['v4']))
    r.append(int(row['v5']))
    r.append(int(row['v6']))
    r.append(int(row['v7']))
    tab.append(r)

gridSize = 10
imageWidth = 49
imageHeight = len(tab)
num=6
print(imageHeight)
result={}
result['data']=[]
newim=Image.new("RGBA",(imageWidth*gridSize,imageHeight*gridSize),(255,0,0,0))
for i in range(imageHeight):
    for j in range(num):
        #x = random.randint(0, imageWidth-1)
        x=tab[i][j]
        result['data'].append([x, i])
        for cw in range(gridSize):
            for ch in range(gridSize):
                newim.putpixel((x*gridSize+cw, i*gridSize+ch), (255, 0, 0,255))

with open('./ssq_png.json','w') as outfile:
    json.dump(result,outfile)

newim.show()
'''