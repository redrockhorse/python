#!/usr/bin/python
# encoding=utf-8
# lbp feature extraction
__author__ = 'mahy'
import pymysql
import numpy as np
import tensorflow as tf

conn = pymysql.connect(host='127.0.0.1', user='root', passwd='Qd@#$mo658', db='jc', port=3306, charset='utf8',
                       cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()

rs = []
max_arr = []
min_arr = []
avg_arr = []
sql = "select max(v1),max(v2),max(v3),max(v4),max(v5),max(v6),max(v7) from td_ptl_ssq_data"
cursor.execute(sql)
result = cursor.fetchall()
for row in result:
    max_arr.append(int(row['max(v1)']))
    max_arr.append(int(row['max(v2)']))
    max_arr.append(int(row['max(v3)']))
    max_arr.append(int(row['max(v4)']))
    max_arr.append(int(row['max(v5)']))
    max_arr.append(int(row['max(v6)']))
    max_arr.append(int(row['max(v7)']))
print(max_arr)

sql = "select min(v1),min(v2),min(v3),min(v4),min(v5),min(v6),min(v7) from td_ptl_ssq_data"
cursor.execute(sql)
result = cursor.fetchall()
for row in result:
    min_arr.append(int(row['min(v1)']))
    min_arr.append(int(row['min(v2)']))
    min_arr.append(int(row['min(v3)']))
    min_arr.append(int(row['min(v4)']))
    min_arr.append(int(row['min(v5)']))
    min_arr.append(int(row['min(v6)']))
    min_arr.append(int(row['min(v7)']))
print(min_arr)

sql = "select avg(v1),avg(v2),avg(v3),avg(v4),avg(v5),avg(v6),avg(v7) from td_ptl_ssq_data"
cursor.execute(sql)
result = cursor.fetchall()
for row in result:
    avg_arr.append(float(row['avg(v1)']))
    avg_arr.append(float(row['avg(v2)']))
    avg_arr.append(float(row['avg(v3)']))
    avg_arr.append(float(row['avg(v4)']))
    avg_arr.append(float(row['avg(v5)']))
    avg_arr.append(float(row['avg(v6)']))
    avg_arr.append(float(row['avg(v7)']))
print(avg_arr)

sql = "select *  from jc.td_ptl_ssq_data   order by pdate asc"
cursor.execute(sql)
result = cursor.fetchall()
for row in result:
    tmp = []
    tmp.append((int(row['v1']) - avg_arr[0]) / (max_arr[0] - min_arr[0]))
    tmp.append((int(row['v2']) - avg_arr[1]) / (max_arr[1] - min_arr[1]))
    tmp.append((int(row['v3']) - avg_arr[2]) / (max_arr[2] - min_arr[2]))
    tmp.append((int(row['v4']) - avg_arr[3]) / (max_arr[3] - min_arr[3]))
    tmp.append((int(row['v5']) - avg_arr[4]) / (max_arr[4] - min_arr[4]))
    tmp.append((int(row['v6']) - avg_arr[5]) / (max_arr[5] - min_arr[5]))
    tmp.append((int(row['v7']) - avg_arr[6]) / (max_arr[6] - min_arr[6]))
    rs.append(tmp)
print(rs)

data = np.array(rs)

n = len(data)
train_x = []
train_y = []
start = 0
end = 6
while end < n:
    train_x.append(data[start:end])
    train_y.append(data[end])
    start += 1
    end += 1

train_x = np.array(train_x)
train_y = np.array(train_y)

# 定义输入的是一个为长度为784的张量
inputs = tf.keras.Input(shape=(42,), name='digits')
# 第1层包含64个节点，采用relu激活函数
x = tf.keras.layers.Dense(64, activation='relu', name='dense_1')(inputs)
# 第2层包含64个节点，采用relu激活函数
x = tf.keras.layers.Dense(64, activation='relu', name='dense_2')(x)
# 输出层采用softmax函数进行处理，得到最终的预测结果
outputs = tf.keras.layers.Dense(7, activation='softmax', name='predictions')(x)
# 实例化模型
model = tf.keras.Model(inputs=inputs, outputs=outputs)

train_x = train_x.reshape(len(train_x), 42)
model.summary()
print(train_y.shape)
# train_y = tf.reshape(train_y,[train_y.shape[0],1,train_y.shape[1]])
# print(train_y)
print(train_y)
train_y = tf.expand_dims(train_y, axis=2)
print(train_y.shape)
model.compile(optimizer=tf.keras.optimizers.Adam(0.001), loss=tf.keras.losses.categorical_crossentropy)
model.fit(train_x, train_y,
          batch_size=64,
          epochs=157)

test_x = []
test_x.append(data[n - 6:])
test_x = np.array(test_x)
test_x = test_x.reshape(1, 42)
result = model.predict(test_x, batch_size=1)
print(test_x)
print(result)

v1 = result[0][0] * (max_arr[0] - min_arr[0]) + avg_arr[0]
v2 = result[0][1] * (max_arr[1] - min_arr[1]) + avg_arr[1]
v3 = result[0][2] * (max_arr[2] - min_arr[2]) + avg_arr[2]
v4 = result[0][3] * (max_arr[3] - min_arr[3]) + avg_arr[3]
v5 = result[0][4] * (max_arr[4] - min_arr[4]) + avg_arr[4]
v6 = result[0][5] * (max_arr[5] - min_arr[5]) + avg_arr[5]
v7 = result[0][6] * (max_arr[6] - min_arr[6]) + avg_arr[6]
print(str(int(v1)) + ',' + str(int(v2)) + ',' + str(int(v3)) + ',' + str(int(v4)) + ',' + str(int(v5)) + ',' + str(
    int(v6)) + '-' + str(int(v7)))

'''
x_train = train_x.reshape((-1, 6, 7, 1))
model = tf.keras.Sequential()
model.add(.layers.Conv2D(input_shape=(x_train.shape[1], x_train.shape[2], x_train.shape[3]),
                                 filters=32, kernel_size=(3, 3), strides=(1, 1), padding='valid',
                                 activation='relu'))
model.add(tf.keras.layers.MaxPool2D(pool_size=(2, 2)))
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(32, activation='relu'))
# 分类层
model.add(tf.keras.layers.Dense(7, activation='softmax'))
model.compile(optimizer=tf.keras.optimizers.Adam(0.001),
              loss=tf.keras.losses.categorical_crossentropy,
              metrics=[tf.keras.metrics.categorical_accuracy])
history = model.fit(x_train, train_y, batch_size=64, epochs=157, validation_split=0.1)

test_x = []
test_x.append(data[n - 6:])
test_x = np.array(test_x).reshape((-1, 6, 7, 1))
result = model.predict(test_x, batch_size=1)
print(test_x)
print(result)

v1= result[0][0]*(max_arr[0]-min_arr[0])+min_arr[0]
v2= result[0][1]*(max_arr[1]-min_arr[1])+min_arr[1]
v3= result[0][2]*(max_arr[2]-min_arr[2])+min_arr[2]
v4= result[0][3]*(max_arr[3]-min_arr[3])+min_arr[3]
v5= result[0][4]*(max_arr[4]-min_arr[4])+min_arr[4]
v6= result[0][5]*(max_arr[5]-min_arr[5])+min_arr[5]
v7= result[0][6]*(max_arr[6]-min_arr[6])+min_arr[6]
print(str(int(v1))+','+str(int(v2))+','+str(int(v3))+','+str(int(v4))+','+str(int(v5))+','+str(int(v6))+'-'+str(int(v7)))
'''
