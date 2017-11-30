# -*- coding: utf-8 -*-
#encoding=utf-8
__author__ = 'mahy'
import tensorflow as tf
import pandas as pd
import math

f=open('./data/sq.csv')
df=pd.read_csv(f)
data=df.iloc[:,0:7].values
_X = tf.placeholder(tf.float32, [1, 7])
y = tf.placeholder(tf.float32, [1, 7])
data_size  =7
hidden1_units = 8
hidden2_units = 8
labels_size =7
def inference(data):
    with tf.name_scope("hidden1"):
        weights = tf.Variable(tf.truncated_normal([data_size,hidden1_units],stddev=1.0/math.sqrt(float(data_size))),name="weights")
        tf.add_to_collection("losses",tf.nn.l2_loss(weights))
        biases = tf.Variable(tf.zeros([hidden1_units]),name="biases")
        hidden1 = tf.nn.relu(tf.matmul(data,weights)+biases)

    with tf.name_scope("hidden2"):
        weights = tf.Variable(tf.truncated_normal([hidden1_units,hidden2_units],stddev=1.0/math.sqrt(float(hidden1_units))),name="weights")
        tf.add_to_collection("losses",tf.nn.l2_loss(weights))
        biases = tf.Variable(tf.zeros([hidden2_units]),name="biases")
        hidden2 = tf.nn.relu(tf.matmul(hidden1,weights)+biases)

    with tf.name_scope("softmax_linear"):
        weights = tf.Variable(tf.truncated_normal([hidden2_units,7],stddev=1.0/math.sqrt(float(hidden2_units))),name="weights")
        tf.add_to_collection("losses",tf.nn.l2_loss(weights))
        biases = tf.Variable(tf.zeros([labels_size]),name="biases")
        logits = tf.matmul(hidden2,weights)+biases
    return logits

def loss_function(logits,labels):
    # labels = tf.to_int64(labels)
    # cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=labels,logits=logits)
    # unr_loss = tf.reduce_mean(cross_entropy,name="unr_loss")
    # tf.add_to_collection("losses",unr_loss)
    # loss = tf.add_n(tf.get_collection("losses"),name="loss")
    # #loss = tf.reduce_mean(cross_entropy,name="unr_loss")
    loss = tf.sqrt(tf.reduce_sum(tf.square(logits-labels), 2))
    return loss;

def training(loss,learning_rate):
    tf.summary.scalar("loss",loss)
    #train_op = tf.train.AdamOptimizer(learning_rate).minimize(loss)
    optimizer = tf.train.GradientDescentOptimizer(learning_rate)
    global_step = tf.Variable(0, name='global_step', trainable=False)
    train_op = optimizer.minimize(loss, global_step=global_step)
    return train_op
tf.nn.seq2seq.embedding_attention_seq2seq()
tf.nn.seq2seq.embedding_attention_seq2seq


