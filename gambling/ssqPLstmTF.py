import numpy as np
import tensorflow as tf
import tensorflow.contrib.rnn as rnn
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt


TIME_STEPS=3
#BATCH_SIZE=128
BATCH_SIZE=128
HIDDEN_UNITS1=30
HIDDEN_UNITS=1
LEARNING_RATE=0.001
EPOCH=50

TRAIN_EXAMPLES=1500
TEST_EXAMPLES=150

#------------------------------------Generate Data-----------------------------------------------#
#generate data
def generate(seq):
    X=[]
    y=[]
    for i in range(len(seq)-TIME_STEPS):
        X.append([seq[i:i+TIME_STEPS]])
        y.append([seq[i+TIME_STEPS]])
    return np.array(X,dtype=np.float32),np.array(y,dtype=np.float32)

#s=[i for i in range(30)]
#X,y=generate(s)
#print(X)
#print(y)


import pymysql
from collections import Counter
conn=pymysql.connect(host='127.0.0.1',user='root',passwd='Qd@#$mo658',db='jc',port=3306,charset='utf8', cursorclass = pymysql.cursors.DictCursor)
cursor = conn.cursor()
sql="select * from td_ptl_lt_data order by pdate asc"
cursor.execute(sql)
v1_result = cursor.fetchall()
dic ={}
v1=[]
v2=[]
v3=[]
v4=[]
v5=[]
v6=[]
v7=[]
for row in v1_result:
    #print(row)
    v1.append(row['v1'])
    v2.append(row['v2'])
    v3.append(row['v3'])
    v4.append(row['v4'])
    v5.append(row['v5'])
    v6.append(row['v6'])
    v7.append(row['v7'])

l=len(v1)
print(l)
import collections
v1d=collections.OrderedDict()
v2d=collections.OrderedDict()
v3d=collections.OrderedDict()
v4d=collections.OrderedDict()
v5d=collections.OrderedDict()
v6d=collections.OrderedDict()
v7d=collections.OrderedDict()

n=200
i=1
#print(Counter(v1).most_common())
for v in Counter(v1).most_common():
    v1d[v[0]]=v[1]/l*1.00
for v in Counter(v2).most_common():
    v2d[v[0]]=v[1]/l*1.00
for v in Counter(v3).most_common():
    v3d[v[0]]=v[1]/l*1.00
for v in Counter(v4).most_common():
    v4d[v[0]]=v[1]/l*1.00
for v in Counter(v5).most_common():
    v5d[v[0]]=v[1]/l*1.00
for v in Counter(v6).most_common():
    v6d[v[0]]=v[1]/l*1.00
for v in Counter(v7).most_common():
    v7d[v[0]]=v[1]/l*1.00
#print(v1d['01'])


v1p=[]
v2p=[]
v3p=[]
v4p=[]
v5p=[]
v6p=[]
v7p=[]
i=0
while i<l:
    v1p.append(v1.count(v1[i]) / l * 1.00)
    v2p.append(v2.count(v2[i]) / l * 1.00)
    v3p.append(v3.count(v3[i]) / l * 1.00)
    v4p.append(v4.count(v4[i]) / l * 1.00)
    v5p.append(v5.count(v5[i]) / l * 1.00)
    v6p.append(v6.count(v6[i]) / l * 1.00)
    v7p.append(v7.count(v7[i]) / l * 1.00)
    i += 1
#print(len(v1p))
#print(v4d)
#print(v5d)
#print(v6d)
#print(v7d)
a=v1p
#seq_train=np.sin(np.linspace(start=0,stop=100,num=TRAIN_EXAMPLES,dtype=np.float32))
#seq_test=np.sin(np.linspace(start=100,stop=110,num=TEST_EXAMPLES,dtype=np.float32))
#print(seq_train)
#a = np.array(v1p)
seq_train=a[0:TRAIN_EXAMPLES]
seq_test=a[TRAIN_EXAMPLES:TRAIN_EXAMPLES+TEST_EXAMPLES]
seq_pre=a[l-BATCH_SIZE-3:l]
#plt.bar(range(TRAIN_EXAMPLES),seq_train)
test_x=[]
for xt in range(TEST_EXAMPLES):
    test_x.append(xt+TRAIN_EXAMPLES)
#plt.bar(test_x,seq_test)
#plt.plot(np.linspace(start=0,stop=TRAIN_EXAMPLES,num=TRAIN_EXAMPLES,dtype=np.float32),seq_train)

#plt.plot(np.linspace(start=100,stop=TEST_EXAMPLES,num=TEST_EXAMPLES,dtype=np.float32),seq_test)
#plt.show()





X_train,y_train=generate(seq_train)
#print(X_train.shape,y_train.shape)
X_test,y_test=generate(seq_test)
X_pre,y_pre=generate(seq_pre)
#print(X_train)
#print(y_train)

#reshape to (batch,time_steps,input_size)
X_train=np.reshape(X_train,newshape=(-1,TIME_STEPS,1))
X_test=np.reshape(X_test,newshape=(-1,TIME_STEPS,1))
X_pre=np.reshape(X_pre,newshape=(-1,TIME_STEPS,1))
#draw y_test
#plt.plot(range(BATCH_SIZE),y_test[:BATCH_SIZE,0],"r")
#print(X_train.shape)
#print(X_test.shape)


#-----------------------------------------------------------------------------------------------------#


#--------------------------------------Define Graph---------------------------------------------------#
graph=tf.Graph()
with graph.as_default():

    #------------------------------------construct LSTM------------------------------------------#
    #place hoder
    X_p=tf.placeholder(dtype=tf.float32,shape=(None,TIME_STEPS,1),name="input_placeholder")
    y_p=tf.placeholder(dtype=tf.float32,shape=(None,1),name="pred_placeholder")

    #lstm instance
    lstm_cell1=rnn.BasicLSTMCell(num_units=HIDDEN_UNITS1)
    lstm_cell=rnn.BasicLSTMCell(num_units=HIDDEN_UNITS)

    multi_lstm=rnn.MultiRNNCell(cells=[lstm_cell1,lstm_cell])

    #initialize to zero
    init_state=multi_lstm.zero_state(batch_size=BATCH_SIZE,dtype=tf.float32)

    #dynamic rnn
    outputs,states=tf.nn.dynamic_rnn(cell=multi_lstm,inputs=X_p,initial_state=init_state,dtype=tf.float32)
    #print(outputs.shape)
    h=outputs[:,-1,:]
    #print(h.shape)
    #--------------------------------------------------------------------------------------------#

    #---------------------------------define loss and optimizer----------------------------------#
    mse=tf.losses.mean_squared_error(labels=y_p,predictions=h)
    #print(loss.shape)
    optimizer=tf.train.AdamOptimizer(LEARNING_RATE).minimize(loss=mse)


    init=tf.global_variables_initializer()


#-------------------------------------------Define Session---------------------------------------#
with tf.Session(graph=graph) as sess:
    sess.run(init)
    for epoch in range(1,EPOCH+1):
        results = np.zeros(shape=(TEST_EXAMPLES, 1))
        t_results = np.zeros(shape=(TEST_EXAMPLES, 1))
        train_losses=[]
        test_losses=[]
        print("epoch:",epoch)
        for j in range(TRAIN_EXAMPLES//BATCH_SIZE):
            _,train_loss=sess.run(
                    fetches=(optimizer,mse),
                    feed_dict={
                            X_p:X_train[j*BATCH_SIZE:(j+1)*BATCH_SIZE],
                            y_p:y_train[j*BATCH_SIZE:(j+1)*BATCH_SIZE]
                        }
            )
            train_losses.append(train_loss)
        print("average training loss:", sum(train_losses) / len(train_losses))
        #t_results[j * BATCH_SIZE:(j + 1) * BATCH_SIZE] = t_result
        #plt.plot(range(BATCH_SIZE), t_results[:BATCH_SIZE, 0])

        for j in range(TEST_EXAMPLES//BATCH_SIZE):
            result,test_loss=sess.run(
                    fetches=(h,mse),
                    feed_dict={
                            X_p:X_test[j*BATCH_SIZE:(j+1)*BATCH_SIZE],
                            y_p:y_test[j*BATCH_SIZE:(j+1)*BATCH_SIZE]
                        }
            )
            results[j*BATCH_SIZE:(j+1)*BATCH_SIZE]=result
            test_losses.append(test_loss)
        #print(result)
        print("average test loss:", sum(test_losses) / len(test_losses))
        plt.plot(range(BATCH_SIZE),results[:BATCH_SIZE,0])
    #plt.show()
    result_pre, pre_loss = sess.run(
        fetches=(h, mse),
        feed_dict={
            X_p: X_pre,
            y_p: y_pre
        }
    )
    print(result_pre)



