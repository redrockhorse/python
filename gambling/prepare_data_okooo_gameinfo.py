# -*- coding: utf8 -*-
# !/usr/bin/python
# 准备分析数据，从okooo网拿到的联赛数据
__author__ = 'mahy'
import pymysql
import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
conn = None
cursor = None
conn = pymysql.connect(host='127.0.0.1', user='root', passwd='Qd@#$mo658', db='jc', port=3306, charset='utf8',
                       cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()


def writeFile():
    sql = "select hname,aname,win,draw,lost,lg,case when hg>ag then 3 when hg < ag then 0 else 1 end result ,hg,ag from tb_okooo_league_odds where hg != '' and ag !='' and win!='-' order by lg,season,round+0,gametime asc;"
    cursor.execute(sql)
    results = cursor.fetchall()
    with open('/Users/hongyanma/okooo/okoodata.csv','w') as outputfile:
        for row in results:
            content = ','.join((row['hname'],row['aname'],row['win'],row['draw'],row['lost'],row['lg'],str(row['result']),row['hg'],row['ag']))
            outputfile.write(content+'\n')
    print('write file done !')



def dealDataWithOneHotEncode(usecols):
    t1 = np.loadtxt("/Users/hongyanma/okooo/okoodata.csv", dtype=np.chararray,delimiter=",", usecols=usecols)
    t2 = np.unique(t1.flatten())
    t2_len = len(t2)
    oneHotArr = np.eye(t2_len)
    # print(t2)
    # print(t2_len)
    # print(oneHotArr)
    return t2,oneHotArr

'''
def build_model():
    model = keras.Sequential([
      keras.layers.Dense(512, activation=tf.nn.sigmoid,
                       input_shape=(train_data.shape[1],)),
      keras.layers.Dense(512, activation=tf.nn.sigmoid),
      keras.layers.Dense(1)
    ])
    # optimizer = tf.train.RMSPropOptimizer(0.001)
    optimizer = tf.train.AdamOptimizer()
    # model.compile(loss='mse',
    #             optimizer=optimizer,
    #             metrics=['mae'])
    model.compile(loss='mse',
                  optimizer=optimizer,
                  metrics=['mae'])
    return model
'''

def build_model():
    model = keras.Sequential([
      keras.layers.Dense(512, activation=tf.nn.sigmoid,
                       input_shape=(train_data.shape[1],)),
      keras.layers.Dense(512, activation=tf.nn.sigmoid),
      keras.layers.Dense(1)
    ])
    # optimizer = tf.train.RMSPropOptimizer(0.001)
    optimizer = tf.train.AdamOptimizer()
    # model.compile(loss='mse',
    #             optimizer=optimizer,
    #             metrics=['mae'])
    model.compile(loss='mse',
                  optimizer=optimizer,
                  metrics=['mae'])
    return model

class PrintDot(keras.callbacks.Callback):
  def on_epoch_end(self,epoch,logs):
    if epoch % 100 == 0: print('')
    print('.', end='')


def plot_history(history):
    # print(history)
    plt.figure()
    plt.xlabel('Epoch')
    plt.ylabel('Mean Abs Error [1000$]')
    # print(history.history['mean_absolute_error'])
    # print(history.history['val_mean_absolute_error'])
    print(history.history)
    plt.plot(history.epoch, np.array(history.history['mean_absolute_error']),
           label='Train Loss')
    # plt.plot(history.epoch, np.array(history.history['val_mean_absolute_error']),
    #        label = 'Val loss')
    plt.legend()
    plt.ylim([0, 5])
    plt.show()

    # plt.plot()
    # plt.plot(history.history['val_acc'])
    # plt.title('model accuracy')
    # plt.ylabel('accuracy')
    # plt.xlabel('epoch')
    # plt.legend(['train', 'test'], loc='upper left')
    # plt.show()
    # # summarize history for loss
    # plt.plot(history.history['loss'])
    # plt.plot(history.history['val_loss'])
    # plt.title('model loss')
    # plt.ylabel('loss')
    # plt.xlabel('epoch')
    # plt.legend(['train', 'test'], loc='upper left')
    # plt.show()



EPOCHS = 30

if __name__ == '__main__':
    #writeFile()
    nameArr, nameOneHotArr = dealDataWithOneHotEncode((0,1))
    lgArr, lgOneHotArr = dealDataWithOneHotEncode((5))
    # itemindex = np.argwhere(lgArr == '德甲')
    # lgIndex = itemindex[0][0]
    # lgOneHot = lgOneHotArr[lgIndex]
    # print(np.concatenate([lgOneHot,[12]]))
    X = []
    Y = []
    with open("/Users/hongyanma/okooo/okoodata.csv",'r') as inputfile:
        line = inputfile.readline()
        while line:
            x = []
            y = []
            # print(line.replace('\n','').split(','))
            lineArr = line.replace('\n','').split(',')
            itemIndex = np.argwhere(nameArr == lineArr[0])
            nameIndex = itemIndex[0][0]
            nameOneHot = nameOneHotArr[nameIndex]
            #print(nameOneHot)
            x = np.concatenate([x,nameOneHot])
            #print(x)
            itemIndex = np.argwhere(nameArr == lineArr[1])
            nameIndex = itemIndex[0][0]
            nameOneHot = nameOneHotArr[nameIndex]
            x = np.concatenate([x, nameOneHot])
            x = np.concatenate([x, [float(lineArr[2])]])
            x = np.concatenate([x, [float(lineArr[3])]])
            x = np.concatenate([x, [float(lineArr[4])]])

            itemIndex = np.argwhere(lgArr == lineArr[5])
            lgIndex = itemIndex[0][0]
            lgOneHot = lgOneHotArr[lgIndex]
            #print(lgOneHot)
            x = np.concatenate([x, lgOneHot])
            #print(x)
            X.append(x)
            y = np.concatenate([y, [float(lineArr[6])]])
            y = np.concatenate([y, [float(lineArr[7])]])
            y = np.concatenate([y, [float(lineArr[8])]])
            Y.append(y)
            #print(y)
            line = inputfile.readline()
    X = np.array(X, dtype=np.float32)
    Y = np.array(Y, dtype=np.float32)
    # print(X)
    # print(Y)
    # print(len(Y))
    train_data = X[:10000]
    test_data = X[10000:]
    hs_train_label = Y[:10000][:, [0]]
    hs_test_label = Y[10000:][:, [0]]
    print(hs_test_label)
    # print(hs_train_label)
    #7414

    model = build_model()
    model.summary()
    history = model.fit(train_data, hs_train_label, epochs=EPOCHS,
                        shuffle=True,validation_split=0, verbose=1,
                        callbacks=[PrintDot()])
    loss, acc = model.evaluate(test_data, hs_test_label, batch_size=8,verbose=1)
    print(loss)
    print(acc)
    # plot_history(history)
