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
ltdata = []
sql = "select *  from jc.td_ptl_ssq_data where pdate>'2018-02-27'  order by pdate asc"
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
    rowdata[int(row['v6']) - 1] = 1
    rowdata[int(row['v7']) + 32] = 1
    # print(row['pdate'])

    sql_lt = "select *  from jc.td_ptl_lt_data where pdate>'2018-02-27' and pdate > '" + row['pdate'].strftime(
        '%Y-%m-%d') + "'  order by pdate asc limit 1"
    cursor_lt.execute(sql_lt)
    result_lt = cursor_lt.fetchall()
    rs_lt = []
    for row_lt in result_lt:
        rowdata_lt = np.zeros(64)
        print(row_lt)
        rowdata_lt[int(row_lt['v1']) - 1] = 1
        rowdata_lt[int(row_lt['v2']) - 1] = 1
        rowdata_lt[int(row_lt['v3']) - 1] = 1
        rowdata_lt[int(row_lt['v4']) - 1] = 1
        rowdata_lt[int(row_lt['v5']) - 1] = 1
        rowdata_lt[int(row_lt['v6']) + 34] = 1
        rowdata_lt[int(row_lt['v7']) + 34] = 1
        # print(rowdata.tolist())
        data.append(rowdata.tolist())
        ltdata.append(rowdata_lt.tolist())
# print(np.array(data).shape)
# print(len(data))
# print(ltdata)
# print(len(ltdata))
print(len(data))
print(len(ltdata))
splitnum = int(len(data) * 0.9)
train_x = np.array(data[0:splitnum])
train_y = np.array(ltdata[0:splitnum])
val_x = np.array(data[splitnum:])
val_y = np.array(ltdata[splitnum:])
print(val_x.shape)

# model = tf.keras.Sequential()
# model.add(tf.keras.layers.Dense(64, activation='relu'))
# model.add(tf.keras.layers.Dense(64, activation='relu'))
# model.add(tf.keras.layers.Dense(64, activation='softmax'))
# model.compile(optimizer=tf.keras.optimizers.Adam(0.001), loss=tf.keras.losses.categorical_crossentropy,
#               metrics=[tf.keras.metrics.categorical_accuracy])


inputs = tf.keras.Input(shape=(64,), name='mnist_input')
h1 = tf.keras.layers.Dense(64, activation='relu')(inputs)
h1 = tf.keras.layers.Dense(64, activation='relu')(h1)
outputs = tf.keras.layers.Dense(64, activation='softmax')(h1)
model = tf.keras.Model(inputs, outputs)
model.compile(optimizer=tf.keras.optimizers.Adam(0.001), loss=tf.keras.losses.categorical_crossentropy,
               metrics=[tf.keras.metrics.categorical_accuracy])

dataset = tf.data.Dataset.from_tensor_slices((train_x, train_y))
dataset = dataset.batch(32)
dataset = dataset.repeat()
val_dataset = tf.data.Dataset.from_tensor_slices((val_x, val_y))
val_dataset = val_dataset.batch(32)
val_dataset = val_dataset.repeat()

model.fit(dataset, epochs=10, steps_per_epoch=30,
          validation_data=val_dataset, validation_steps=3)
model.summary()
tf.keras.utils.plot_model(model, 'lt_model.png')
tf.keras.utils.plot_model(model, 'lt_model_info.png', show_shapes=True)

# predict

sql = "select *  from jc.td_ptl_ssq_data  order by pdate desc limit 1"
cursor.execute(sql)
result = cursor.fetchall()
rs = []
testdata = []
for row in result:
    rowdata = np.zeros(64)
    print(row)
    rowdata[int(row['v1']) - 1] = 1
    rowdata[int(row['v2']) - 1] = 1
    rowdata[int(row['v3']) - 1] = 1
    rowdata[int(row['v4']) - 1] = 1
    rowdata[int(row['v5']) - 1] = 1
    rowdata[int(row['v6']) - 1] = 1
    rowdata[int(row['v7']) + 32] = 1
    testdata.append(rowdata.tolist())
test_x = np.array(testdata)
result = model.predict(test_x, batch_size=1)
print(result)
print(result.shape)
i = 0
for item in result[0]:
    i += 1
    #print(item)
    if item > 0:
        if i<= 35:
            print(str(i) + " : " + str(item))
        else:
            print(str(i-35) + " : " + str(item))
print(len(np.argsort(result[0][0:35])))
redball = np.argsort(result[0][0:35])
redball = np.argsort(result[0][0:35])
print(redball)
for i in range(5):
    print(redball[35-i-1]+1)

blueball = np.argsort(result[0][35:47])
print(blueball)
for i in range(2):
    print(blueball[12-i-1]+1)
'''
cursor_lt = conn.cursor()
sql_lt = "select *  from jc.td_ptl_lt_data where pdate>'2019-02-27' and pnum='"+"19023"+"'  order by pdate asc limit 1"
cursor_lt.execute(sql_lt)
result_lt = cursor_lt.fetchall()
rs_lt = []
ltdata = []
for row_lt in result_lt:
    rowdata_lt = np.zeros(49)
    print(row_lt)
    rowdata_lt[int(row_lt['v1']) - 1] = 1
    rowdata_lt[int(row_lt['v2']) - 1] = 1
    rowdata_lt[int(row_lt['v3']) - 1] = 1
    rowdata_lt[int(row_lt['v4']) - 1] = 1
    rowdata_lt[int(row_lt['v5']) - 1] = 1
    rowdata_lt[int(row_lt['v6']) + 34] = 1
    rowdata_lt[int(row_lt['v7']) + 34] = 1
    # print(rowdata.tolist())
    ltdata.append(rowdata_lt.tolist())
print(ltdata)
print(len(ltdata))
'''
# layer = tf.keras.layers.Dense(100)

# x = tf.matmul([[1]], [[2, 3]])

'''
x = tf.matmul([[1, 2], [3, 4], [5, 6]], [[2], [1]])
print(x)
print(x.shape)
print(x.dtype)
print(tf.reshape(x,[1,-1]))
'''

# layer = tf.keras.layers.Dense(10, input_shape=(None, 5))
# print(layer)

'''
model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(32, activation='relu'))
model.add(tf.keras.layers.Dense(32, activation='relu'))
model.add(tf.keras.layers.Dense(10, activation='softmax'))
model.compile(optimizer=tf.keras.optimizers.Adam(0.001),
             loss=tf.keras.losses.categorical_crossentropy,
             metrics=[tf.keras.metrics.categorical_accuracy])
'''
