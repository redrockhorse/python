# -*- coding: utf-8 -*-
#encoding=utf-8
__author__ = 'mahy'
import tensorflow as tf
import pandas as pd
import math
import numpy as np

f=open('./data/lt.csv','r', encoding='UTF-8')
df=pd.read_csv(f)
data=np.array(df[:])
#normalize_data=data[:,np.newaxis]#为什么要增加维度呢？因为原来的文件中只有一列，读出来是标量
normalize_data = data
#print(data[0])
#print(len(normalize_data[0]))
#print(normalize_data[0])

#生成训练集
#设置常量
time_step=5      #时间步
rnn_unit=5       #hidden layer units
batch_size=60     #每一批次训练多少个样例
input_size=7      #输入层维度
output_size=7     #输出层维度
lr=0.0005         #学习率
train_x,train_y=[],[]   #训练集
for i in range(len(normalize_data)-time_step-1):
    x=normalize_data[i:i+time_step]
    y=normalize_data[i+1:i+time_step+1]
    train_x.append(x.tolist())
    train_y.append(y.tolist())
#print(train_x[0])
#print(len(train_x[0][0]))


#——————————————————定义神经网络变量——————————————————
X=tf.placeholder(tf.float32, [None,time_step,input_size])    #每批次输入网络的tensor
Y=tf.placeholder(tf.float32, [None,time_step,output_size])   #每批次tensor对应的标签

#输入层、输出层权重、偏置
weights={
         'in':tf.Variable(tf.random_normal([input_size,rnn_unit])),
         'out':tf.Variable(tf.random_normal([rnn_unit,output_size]))
         }
biases={
        'in':tf.Variable(tf.constant(0.1,shape=[rnn_unit,])),
        'out':tf.Variable(tf.constant(0.1,shape=[output_size,]))
        }

#——————————————————定义神经网络变量——————————————————
def lstm(batch):      #参数：输入网络批次数目
    w_in=weights['in']
    b_in=biases['in']
    input=tf.reshape(X,[-1,input_size])  #需要将tensor转成2维进行计算，计算后的结果作为隐藏层的输入
    print('\n')
    print('X',X)
    print('input',input)
    input_rnn=tf.matmul(input,w_in)+b_in
    print('input_rnn',input_rnn)
    input_rnn=tf.reshape(input_rnn,[-1,time_step,rnn_unit])  #将tensor转成3维，作为lstm cell的输入
    print('input_rnn_1',input_rnn)
    cell=tf.nn.rnn_cell.BasicLSTMCell(rnn_unit)
    init_state=cell.zero_state(batch,dtype=tf.float32)
    output_rnn,final_states=tf.nn.dynamic_rnn(cell, input_rnn,initial_state=init_state, dtype=tf.float32)  #output_rnn是记录lstm每个输出节点的结果，final_states是最后一个cell的结果
    print('output_rnn',output_rnn)
    output=tf.reshape(output_rnn,[-1,rnn_unit]) #作为输出层的输入
    print('output',output)
    w_out=weights['out']
    b_out=biases['out']
    pred=tf.matmul(output,w_out)+b_out
    print('pred',pred)
    print('\n')
    return pred,final_states

#——————————————————训练模型——————————————————
def train_lstm():
    global batch_size
    pred,_=lstm(batch_size)
    #损失函数
    '''
    print('-----------------------------------------------------')
    print(pred)
    print(Y)
    print(tf.reshape(pred,[-1]))
    print(tf.reshape(Y, [-1]))
    print('-----------------------------------------------------')
    '''
    loss=tf.reduce_mean(tf.square(tf.reshape(pred,[-1])-tf.reshape(Y, [-1])))
    train_op=tf.train.AdamOptimizer(lr).minimize(loss)
    saver=tf.train.Saver(tf.global_variables())
    module_file = tf.train.latest_checkpoint('./sqlogs/')
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        #saver.restore(sess, module_file)
        #重复训练10000次
        for i in range(500):
            step=0
            start=0
            end=start+batch_size
            while(end<len(train_x)):
                _,loss_=sess.run([train_op,loss],feed_dict={X:train_x[start:end],Y:train_y[start:end]})
                start+=batch_size
                end=start+batch_size
                #每10步保存一次参数
                if i%10==0:
                    print(i,step,loss_)
                    print("保存模型：",saver.save(sess,'./sqlogs/sq.model',global_step=i))
                step+=1


#————————————————预测模型————————————————————
def prediction():
    print('*************************************prediction*****************************************')
    pred,_=lstm(1)      #预测时只输入[1,time_step,input_size]的测试数据
    saver=tf.train.Saver(tf.global_variables())
    with tf.Session() as sess:
        #参数恢复
        module_file = tf.train.latest_checkpoint('./sqlogs/')
        saver.restore(sess, module_file)

        #取训练集最后一行为测试样本。shape=[1,time_step,input_size]
        prev_seq=train_x[-1]
        prev_seq=[ [7, 11, 18, 26, 28, 4, 5], [3, 4, 13, 24, 33, 1, 11], [2, 15, 18, 21, 22, 3, 10],[9,11,13,18,33,2,3], [5,17,20,32,33,4,9]]
        print(prev_seq)
        predict=[]
        #得到之后100个预测结果
        for i in range(1):
            next_seq=sess.run(pred,feed_dict={X:[prev_seq]})
            predict.append(next_seq[-1])
            #每次得到最后一个时间步的预测结果，与之前的数据加在一起，形成新的测试样本
            prev_seq=np.vstack((prev_seq[1:],next_seq[-1]))
        #以折线图表示结果
            print(next_seq)
        '''
        plt.figure()
        plt.plot(list(range(len(normalize_data))), normalize_data, color='b')
        plt.plot(list(range(len(normalize_data), len(normalize_data) + len(predict))), predict, color='r')
        plt.show()
        '''
        print('*************************************prediction*****************************************')

if __name__ == "__main__":
    print('done')
    #train_lstm()
    prediction()