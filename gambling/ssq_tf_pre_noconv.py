# -*- coding:utf-8 -*-
# @Time : 2020/4/24 下午4:43
# @Author: kkkkibj@163.com
# @File : ssq_tf_pre.py

import tensorflow as tf
import numpy as np
import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root', passwd='Qd@#$mo658', db='jc', port=3306, charset='utf8',
                       cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()
cursor_lt = conn.cursor()

sql = "select *  from jc.td_ptl_ssq_data where pdate>'2018-02-27'  order by pdate asc"
cursor.execute(sql)
result = cursor.fetchall()
rs = []
data = []
for row in result:
    rowdata = []
    rowdata.append(int(row['v1']))
    rowdata.append(int(row['v2']))
    rowdata.append(int(row['v3']))
    rowdata.append(int(row['v4']))
    rowdata.append(int(row['v5']))
    rowdata.append(int(row['v6']))
    rowdata.append(int(row['v7']))
    #print(rowdata)
    data.append(rowdata)
print(data)


inputs = tf.keras.Input(shape=(7,), name='mnist_input')
h1 = tf.keras.layers.Dense(64, activation='relu')(inputs)
h1 = tf.keras.layers.Dense(64, activation='relu')(h1)
outputs = tf.keras.layers.Dense(7, activation='softmax')(h1)
model = tf.keras.Model(inputs, outputs)
model.compile(optimizer=tf.keras.optimizers.Adam(0.001), loss=tf.keras.losses.categorical_crossentropy,
               metrics=[tf.keras.metrics.categorical_accuracy])

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
print(len(train_x))
print(len(train_y))
train_x = np.array(train_x)
train_y = np.array(train_y)
print(train_x.shape)
print(train_y.shape)
print(train_y[0])

model.fit(train_x, train_y, batch_size=64, epochs=57, validation_split=0.1)