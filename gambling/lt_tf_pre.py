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

sql = "select *  from jc.td_ptl_lt_data where pdate>'2018-02-27'  order by pdate asc"
cursor.execute(sql)
result = cursor.fetchall()
rs = []
data = []
for row in result:
    rowdata = np.zeros(64)
    # print(row)
    rowdata[int(row['v1']) - 1] = 1
    rowdata[int(row['v2']) - 1] = 1
    rowdata[int(row['v3']) - 1] = 1
    rowdata[int(row['v4']) - 1] = 1
    rowdata[int(row['v5']) - 1] = 1
    rowdata[int(row['v6']) + 34] = 1
    rowdata[int(row['v7']) + 34] = 1
    data.append(rowdata.tolist())

print(len(data))
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

x_train = train_x.reshape((-1, 6, 64, 1))
model = tf.keras.Sequential()
model.add(tf.keras.layers.Conv2D(input_shape=(x_train.shape[1], x_train.shape[2], x_train.shape[3]),
                                 filters=32, kernel_size=(3, 3), strides=(1, 1), padding='valid',
                                 activation='relu'))
model.add(tf.keras.layers.MaxPool2D(pool_size=(2, 2)))
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(32, activation='relu'))
# 分类层
model.add(tf.keras.layers.Dense(64, activation='softmax'))
model.compile(optimizer=tf.keras.optimizers.Adam(0.001),
              loss=tf.keras.losses.categorical_crossentropy,
              metrics=[tf.keras.metrics.categorical_accuracy])
history = model.fit(x_train, train_y, batch_size=64, epochs=577, validation_split=0.1)
print(history.history['loss'][-1])
test_x = []
test_x.append(data[n - 6:])
test_x = np.array(test_x).reshape((-1, 6, 64, 1))
result = model.predict(test_x, batch_size=1)
# result = model.predict(test_x, batch_size=1)

redball = np.argsort(result[0][0:35])
print(redball)
luckarr = ""
for i in range(5):
    print(redball[35 - i - 1] + 1)
    luckarr += str(redball[35 - i - 1] + 1) + ","

blueball = np.argsort(result[0][35:47])
print(blueball)
bluenum = ''
for i in range(2):
    print(blueball[12 - i - 1] + 1)
    bluenum = bluenum + ',' + str(blueball[12 - i - 1] + 1)

print(luckarr + "-" + str(bluenum))
