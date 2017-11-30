# -*- coding: utf-8 -*-
#encoding=utf-8
__author__ = 'mahy'
import  tensorflow as tf
import  numpy as np
import math
from six.moves import xrange
import time
import os

'''
#1、增加6个参数
2、用测试集统计准确率，并提前退出
#3、增加正则化
4、增加online学习能力
#5、RNN
#6、dropout
'''

data_size = 1739*2+140+18
hidden1_units = 36
hidden2_units = 18
labels_size = 8
batch_size = 200
keep_prob = tf.placeholder(tf.float32)
log_dir="/root/tensorcode/logs"
save_dir = '/root/tensorcode/data/'
export_dir = '/root/tensorcode/data/'
namefile = "/root/tensorcode/data/allname.txt"
lgfile = "/root/tensorcode/data/lg20170725.txt"
learning_rate=0.01
max_steps = 1500000
time_step = 50

def inference(data):
    with tf.name_scope("hidden1"):
        cell = tf.nn.rnn_cell.BasicLSTMCell(hidden1_units)
        cell = tf.nn.rnn_cell.DropoutWrapper(cell=cell,input_keep_prob=1.0,output_keep_prob=keep_prob)
        init_state = cell.zero_state(batch_size,dtype=tf.float32)
        input_rnn = tf.reshape(data,[-1,time_step,data_size])
        output_rnn,final_states = tf.nn.dynamic_rnn(cell,input_rnn,initial_state=init_state,dtype=tf.float32)
        output = tf.reshape(output_rnn,[-1,hidden1_units])

        weights = tf.Variable(tf.truncated_normal([data_size,hidden1_units],stddev=1.0/math.sqrt(float(data_size))),name="weights")
        tf.add_to_collection("losses",tf.nn.l2_loss(weights))
        biases = tf.Variable(tf.zeros([hidden1_units]),name="biases")
        hidden1 = tf.nn.relu(tf.matmul(output,weights)+biases)

    with tf.name_scope("hidden2"):
        cell = tf.nn.rnn_cell.BasicLSTMCell(hidden2_units)
        cell = tf.nn.rnn_cell.DropoutWrapper(cell=cell,input_keep_prob=1.0,output_keep_prob=keep_prob)
        init_state = cell.zero_state(batch_size,dtype=tf.float32)
        input_rnn = tf.reshape(hidden1,[-1,time_step,hidden1_units])
        output_rnn,final_states = tf.nn.dynamic_rnn(cell,input_rnn,initial_state=init_state,dtype=tf.float32)
        output = tf.reshape(output_rnn,[-1,hidden2_units])

        weights = tf.Variable(tf.truncated_normal([hidden1_units,hidden2_units],stddev=1.0/math.sqrt(float(hidden1_units))),name="weights")
        tf.add_to_collection("losses",tf.nn.l2_loss(weights))
        biases = tf.Variable(tf.zeros([hidden2_units]),name="biases")
        hidden2 = tf.nn.relu(tf.matmul(output,weights)+biases)

    with tf.name_scope("softmax_linear"):
        cell = tf.nn.rnn_cell.BasicLSTMCell(labels_size)
        cell = tf.nn.rnn_cell.DropoutWrapper(cell=cell,input_keep_prob=1.0,output_keep_prob=keep_prob)
        init_state = cell.zero_state(batch_size,dtype=tf.float32)
        input_rnn = tf.reshape(hidden2,[-1,time_step,hidden2_units])
        output_rnn,final_states = tf.nn.dynamic_rnn(cell,input_rnn,initial_state=init_state,dtype=tf.float32)
        output = tf.reshape(output_rnn,[-1,labels_size])

        weights = tf.Variable(tf.truncated_normal([hidden2_units,labels_size],stddev=1.0/math.sqrt(float(hidden2_units))),name="weights")
        tf.add_to_collection("losses",tf.nn.l2_loss(weights))
        biases = tf.Variable(tf.zeros([labels_size]),name="biases")
        logits = tf.nn.relu(tf.matmul(output,weights)+biases)
    return logits

def loss_function(labels,logits):
    labels = tf.to_int64(labels)
    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=labels,logits=logits)
    unr_loss = tf.reduce_mean(cross_entropy,name="unr_loss")
    tf.add_to_collection("losses",unr_loss)
    loss = tf.add_n(tf.get_collection("losses"),name="loss")
    return loss;


def training(loss,learning_rate):
    tf.summary.scalar("loss",loss)
    train_op = tf.train.AdamOptimizer(learning_rate).minimize(loss)
    return train_op

def read_and_decode(file_queue):
    reader = tf.TFRecordReader()
    _,seralized_example = reader.read(file_queue)
    features = tf.parse_single_example(seralized_example,
                                        features={
                                            'data':tf.FixedLenFeature([data_size],tf.float32),
                                            'label':tf.FixedLenFeature([],tf.int64)
                                        }
                                      )
    data_out = features['data']
    label_out = features['label']
    return data_out,label_out

def inputs(filedir, batch_size, num_epochs):
    with tf.name_scope("inputs"):
        filename_queue = tf.train.string_input_producer([filedir],shuffle=False,num_epochs=num_epochs)
        data,label = read_and_decode(filename_queue)
        datas, sparse_labels = tf.train.batch([data, label], batch_size=batch_size, num_threads=2,capacity=1000 + 3 * batch_size)
        return datas, sparse_labels


def evaluation(logits, labels):
    with tf.name_scope('evaluation'):
        correct = tf.nn.in_top_k(logits, labels, 1)
        evaluation = tf.reduce_sum(tf.cast(correct, tf.int32),name='eval')
    return evaluation

def run_training():
    with tf.Graph().as_default() as graph:
        sess = tf.Session()
        data,labels = inputs(save_dir+'train_v1.tfrecord', batch_size=batch_size,num_epochs=None)
        data_test,labels_test = inputs(save_dir+'test_v1.tfrecord', batch_size=batch_size,num_epochs=None)
        logits = inference(data)
        tf.identity(logits, name='logits')
        loss = loss_function(logits, labels)
        train_op = training(loss, learning_rate)
        true_count = 0
        eval_correct = evaluation(logits, labels)
        tf.identity(eval_correct, name='eval_correct')

        logits_test = inference(data_test)
        test_correct = evaluation(logits_test, labels_test)

        summary = tf.summary.merge_all()
        init = tf.group(tf.global_variables_initializer(),
                       tf.local_variables_initializer())
        saver = tf.train.Saver()
        summary_writer = tf.summary.FileWriter(log_dir, sess.graph)

        sess.run(init)

        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(sess=sess, coord=coord)

        for step in xrange(max_steps):
            start_time = time.time()
            _, loss_value = sess.run([train_op, loss])
            duration = time.time() - start_time
            if step % 1000 == 0 or (step + 1) == max_steps:
                print('Step %d: loss = %.2f (%.3f sec)' % (step, loss_value, duration))
                true_count += sess.run(eval_correct)
                summary_str = sess.run(summary)
                summary_writer.add_graph(graph,step)
                summary_writer.add_summary(summary_str, step)
                summary_writer.flush()
                checkpoint_file = os.path.join(log_dir, 'model_v1.ckpt')
                saver.save(sess, checkpoint_file, global_step=step)

                test_count = sess.run(test_correct)
                test_correct_rate = test_count/batch_size*1.00
                print("test_correct_rate:",test_correct_rate)
                if test_correct_rate>0.50:
                    break

        coord.request_stop()
        coord.join(threads)

        #训练完成后将权重和偏置保存下来嵌入图中
        weights1 = graph.get_tensor_by_name('hidden1/weights:0')
        biases1 = graph.get_tensor_by_name('hidden1/biases:0')
        weights2 = graph.get_tensor_by_name('hidden2/weights:0')
        biases2 = graph.get_tensor_by_name('hidden2/biases:0')
        weights_sl = graph.get_tensor_by_name('softmax_linear/weights:0')
        biases_sl = graph.get_tensor_by_name('softmax_linear/biases:0')

    _weights1 = weights1.eval(session=sess)
    _biases1 = biases1.eval(session=sess)
    _weights2 = weights2.eval(session=sess)
    _biases2 = biases2.eval(session=sess)
    _weights_sl = weights_sl.eval(session=sess)
    _biases_sl = biases_sl.eval(session=sess)
    sess.close()

    g_2 = tf.Graph()
    with g_2.as_default():
        gambling_data = tf.placeholder(tf.float32,[1,data_size],name="gambling_data")
        w1 = tf.constant(_weights1, name="p_weights1")
        b1 = tf.constant(_biases1, name="p_biases1")
        w2 = tf.constant(_weights2, name="p_weights2")
        b2 = tf.constant(_biases2, name="p_biases2")
        wsl = tf.constant(_weights_sl, name="p_weights_sl")
        bsl = tf.constant(_biases_sl, name="p_biases_sl")

        cell = tf.nn.rnn_cell.BasicLSTMCell(hidden1_units)
        cell = tf.nn.rnn_cell.DropoutWrapper(cell=cell,input_keep_prob=1.0,output_keep_prob=keep_prob)
        init_state = cell.zero_state(batch_size,dtype=tf.float32)
        input_rnn = tf.reshape(gambling_data,[-1,time_step,data_size])
        output_rnn,final_states = tf.nn.dynamic_rnn(cell,input_rnn,initial_state=init_state,dtype=tf.float32)
        output = tf.reshape(output_rnn,[-1,hidden1_units])
        hidden1 = tf.nn.relu(tf.matmul(output,w1)+b1)

        cell = tf.nn.rnn_cell.BasicLSTMCell(hidden2_units)
        cell = tf.nn.rnn_cell.DropoutWrapper(cell=cell,input_keep_prob=1.0,output_keep_prob=keep_prob)
        init_state = cell.zero_state(batch_size,dtype=tf.float32)
        input_rnn = tf.reshape(hidden1,[-1,time_step,hidden1_units])
        output_rnn,final_states = tf.nn.dynamic_rnn(cell,input_rnn,initial_state=init_state,dtype=tf.float32)
        output = tf.reshape(output_rnn,[-1,hidden2_units])
        hidden2 = tf.nn.relu(tf.matmul(output,w2)+b2)

        cell = tf.nn.rnn_cell.BasicLSTMCell(labels_size)
        cell = tf.nn.rnn_cell.DropoutWrapper(cell=cell,input_keep_prob=1.0,output_keep_prob=keep_prob)
        init_state = cell.zero_state(batch_size,dtype=tf.float32)
        input_rnn = tf.reshape(hidden2,[-1,time_step,hidden2_units])
        output_rnn,final_states = tf.nn.dynamic_rnn(cell,input_rnn,initial_state=init_state,dtype=tf.float32)
        output = tf.reshape(output_rnn,[-1,labels_size])
        predict_logits = tf.nn.relu(tf.matmul(output,wsl)+bsl)
        tf.identity(predict_logits, name='predict_logits')

        predict_result = tf.argmax(predict_logits,axis=0,name="predict_result")
        sess_2 = tf.Session()
        init_2 = tf.global_variables_initializer();
        sess_2.run(init_2)
        graph_def = g_2.as_graph_def()
        tf.train.write_graph(graph_def, export_dir, 'gbs-graph-v1.pb', as_text=False)
    sess_2.close()


if __name__ == '__main__':
    run_training()
