# -*- coding: utf-8 -*-
#encoding=utf-8
__author__ = 'mahy'
import  tensorflow as tf
import  numpy as np
import math
import xlrd
from six.moves import xrange
import time
import os


'''
#1、增加6个参数
#2、用测试集统计准确率，并提前退出
#3、增加正则化
增加继续学习能力#4、增加online学习能力
不适用，去掉#5、RNN
与rnn一同去掉#6、dropout
'''

data_size = 1739*2+140+18
hidden1_units = 36
hidden2_units = 18
labels_size = 8
batch_size = 200
keep_prob = tf.placeholder(tf.float32)
log_dir="./logs"
save_dir = './data/'
export_dir = './data/'
namefile = "./data/allname.txt"
lgfile = "./data/lg20170725.txt"
learning_rate=0.01
max_steps = 1000
time_step = 1

def inference(data,w1,b1,w2,b2,wsl,bsl):
    with tf.name_scope("hidden1"):
        tf.add_to_collection("losses",tf.nn.l2_loss(w1)*0.1)
        hidden1 = tf.nn.relu(tf.matmul(data,w1)+b1)

    with tf.name_scope("hidden2"):
        tf.add_to_collection("losses",tf.nn.l2_loss(w2)*0.1)
        hidden2 = tf.nn.relu(tf.matmul(hidden1,w2)+b2)

    with tf.name_scope("softmax_linear"):
        tf.add_to_collection("losses",tf.nn.l2_loss(wsl)*0.1)
        logits = tf.nn.relu(tf.matmul(hidden2,wsl)+bsl)
    return logits

def loss_function(logits,labels):
    labels = tf.to_int64(labels)
    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=labels,logits=logits)
    unr_loss = tf.reduce_mean(cross_entropy,name="unr_loss")
    tf.add_to_collection("losses",unr_loss)
    loss = tf.add_n(tf.get_collection("losses"),name="loss")
    #loss = tf.reduce_mean(cross_entropy,name="unr_loss")
    return loss;


def training(loss,learning_rate):
    tf.summary.scalar("loss",loss)
    #train_op = tf.train.AdamOptimizer(learning_rate).minimize(loss)
    optimizer = tf.train.GradientDescentOptimizer(learning_rate)
    global_step = tf.Variable(0, name='global_step', trainable=False)
    train_op = optimizer.minimize(loss, global_step=global_step)
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
        #datas, sparse_labels = tf.train.batch([data, label], batch_size=batch_size, num_threads=2)
        return datas, sparse_labels


def evaluation(logits, labels):
    with tf.name_scope('evaluation'):
        correct = tf.nn.in_top_k(logits, labels, 1)
        evaluation = tf.reduce_sum(tf.cast(correct, tf.int32),name='eval')
    return evaluation

def run_training():
    with tf.Graph().as_default() as graph:
        reload_flag = False;
        w1 = tf.Variable(tf.truncated_normal([data_size,hidden1_units],stddev=1.0/math.sqrt(float(data_size))),name="w1")
        b1 = tf.Variable(tf.zeros([hidden1_units]),name="b1")
        w2 = tf.Variable(tf.truncated_normal([hidden1_units,hidden2_units],stddev=1.0/math.sqrt(float(hidden1_units))),name="w2")
        b2 = tf.Variable(tf.zeros([hidden2_units]),name="b2")
        wsl = tf.Variable(tf.truncated_normal([hidden2_units,labels_size],stddev=1.0/math.sqrt(float(hidden2_units))),name="wsl")
        bsl = tf.Variable(tf.zeros([labels_size]),name="bsl")

        data,labels = inputs(save_dir+'train_v1.tfrecord', batch_size=batch_size,num_epochs=None)
        data_test,labels_test = inputs(save_dir+'test_v1.tfrecord', batch_size=999,num_epochs=None)
        logits = inference(data,w1,b1,w2,b2,wsl,bsl)
        tf.identity(logits, name='logits')
        loss = loss_function(logits,labels)
        train_op = training(loss, learning_rate)
        true_count = 0
        eval_correct = evaluation(logits, labels)
        tf.identity(eval_correct, name='eval_correct')
        module_file = tf.train.latest_checkpoint(log_dir)
        saver = tf.train.Saver()
        sess = tf.Session()
        if module_file == None:
            reload_flag = True
        else:
            saver.restore(sess, module_file)

        summary = tf.summary.merge_all()
        summary_writer = tf.summary.FileWriter(log_dir, sess.graph)

        logits_test = inference(data_test,w1,b1,w2,b2,wsl,bsl)
        test_correct = evaluation(logits_test, labels_test)
        init = tf.group(tf.global_variables_initializer(),
                       tf.local_variables_initializer())
        if reload_flag:
            sess.run(init)

        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(sess=sess, coord=coord)

        for step in xrange(max_steps):
            start_time = time.time()
            _, loss_value = sess.run([train_op, loss])
            duration = time.time() - start_time
            if step % 100 == 0 or (step + 1) == max_steps:
                print('Step %d: loss = %.2f (%.3f sec)' % (step, loss_value, duration))
                true_count += sess.run(eval_correct)
                summary_str = sess.run(summary)
                summary_writer.add_graph(graph,step)
                summary_writer.add_summary(summary_str, step)
                summary_writer.flush()
                checkpoint_file = os.path.join(log_dir, 'model_v1.ckpt')
                saver.save(sess, checkpoint_file, global_step=step)


                #print('logits_test:',sess.run(logits_test[1]))
                #print('labels_test:',sess.run(labels_test[1]))

                test_count = sess.run(test_correct)
                print('test_count:',test_count)
                test_correct_rate = test_count*1.00/(batch_size*5)
                print("test_correct_rate:",test_correct_rate)
                if test_correct_rate>0.50:
                    break

        coord.request_stop()
        coord.join(threads)

    _weights1 = w1.eval(session=sess)
    _biases1 = b1.eval(session=sess)
    _weights2 = w2.eval(session=sess)
    _biases2 = b2.eval(session=sess)
    _weights_sl = wsl.eval(session=sess)
    _biases_sl = bsl.eval(session=sess)
    sess.close()

    g_2 = tf.Graph()
    with g_2.as_default():
    #predict class
        gambling_data = tf.placeholder(tf.float32,[1,data_size],name="gambling_data")
        w1_c = tf.constant(_weights1, name="p_weights1")
        b1_c = tf.constant(_biases1, name="p_biases1")
        w2_c = tf.constant(_weights2, name="p_weights2")
        b2_c = tf.constant(_biases2, name="p_biases2")
        wsl_c = tf.constant(_weights_sl, name="p_weights_sl")
        bsl_c = tf.constant(_biases_sl, name="p_biases_sl")
        hidden_layer1 = tf.nn.relu(tf.matmul(gambling_data, w1_c) + b1_c)
        hidden_layer2 = tf.nn.relu(tf.matmul(hidden_layer1, w2_c) + b2_c)
        predict_logits = tf.nn.relu(tf.matmul(hidden_layer2, wsl_c) + bsl_c)
        #predict_logits = inference(gambling_data, hidden1, hidden2)
        tf.identity(predict_logits, name='predict_logits')
        predict_result = tf.argmax(predict_logits,axis=0,name="predict_result")
        sess_2 = tf.Session()
        #init_2 = tf.initialize_all_variables();
        init_2 = tf.global_variables_initializer();
        sess_2.run(init_2)
        graph_def = g_2.as_graph_def()
        tf.train.write_graph(graph_def, export_dir, 'gbs-graph-v1.pb', as_text=False)
    sess_2.close()

def check_model():
    with tf.Graph().as_default():
        output_graph_def = tf.GraphDef()
        output_graph_path = export_dir+'gbs-805.pb'
        data_test,labels_test = inputs(save_dir+'ctest_v1.tfrecord', batch_size=1,num_epochs=None)
        with open(output_graph_path, "rb") as f:
            output_graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(output_graph_def, name="")
            with tf.Session() as sess:
                tf.global_variables_initializer().run()
                #p_weights_sl = sess.graph.get_tensor_by_name("p_weights_sl:0")
                #print(sess.run(p_weights_sl))
                predict_result = sess.graph.get_tensor_by_name('predict_logits:0')
                coord = tf.train.Coordinator()
                threads = tf.train.start_queue_runners(sess=sess, coord=coord)
                #rs = sess.run(predict_result,feed_dict={'gambling_data:0':np.reshape(data_test,[1,data_size])})
                t =0
                for i in range(218):
                    if i%100==0:
                        print('step:',i)
                    gambling_data,lt = sess.run([data_test,labels_test])
                    rs = sess.run(predict_result,feed_dict={'gambling_data:0':gambling_data})
                    #print(gambling_data)
                    #print(rs)
                    #print(lt)
                    tc= evaluation(rs, lt)
                    t=t+ sess.run(tc)
                coord.request_stop()
                coord.join(threads)
                print(t)


'''
def check_model():
    with tf.Graph().as_default():
        output_graph_def = tf.GraphDef()
        output_graph_path = export_dir+'gbs-505.pb'
        data_test,labels_test = inputs(save_dir+'test_v1.tfrecord', batch_size=999,num_epochs=None)
        with open(output_graph_path, "rb") as f:
            output_graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(output_graph_def, name="")
            with tf.Session() as sess:
                tf.global_variables_initializer().run()
                w1_c = sess.graph.get_tensor_by_name("p_weights1:0")
                b1_c = sess.graph.get_tensor_by_name("p_biases1:0")
                w2_c = sess.graph.get_tensor_by_name("p_weights2:0")
                b2_c = sess.graph.get_tensor_by_name("p_biases2:0")
                wsl_c = sess.graph.get_tensor_by_name("p_weights_sl:0")
                bsl_c = sess.graph.get_tensor_by_name("p_biases_sl:0")
                w1 = w1_c.eval(session=sess)
                b1 = b1_c.eval(session=sess)
                w2 = w2_c.eval(session=sess)
                b2 = b2_c.eval(session=sess)
                wsl = wsl_c.eval(session=sess)
                bsl = bsl_c.eval(session=sess)

                #p_weights_sl = sess.graph.get_tensor_by_name("p_weights_sl:0")
                #print(sess.run(p_weights_sl))
                #predict_result = sess.graph.get_tensor_by_name('predict_logits:0')



                coord = tf.train.Coordinator()
                threads = tf.train.start_queue_runners(sess=sess, coord=coord)
                #rs = sess.run(predict_result,feed_dict={'gambling_data:0':np.reshape(data_test,[1,data_size])})
               # predict_result = inference(data_test,w1_c,b1_c,w2_c,b2_c,wsl_c,bsl_c)
                gambling_data,lt = sess.run([data_test,labels_test])
                rs = inference(gambling_data,w1,b1,w2,b2,wsl,bsl)
                tc= evaluation(rs, lt)
                t = sess.run(tc)
                coord.request_stop()
                coord.join(threads)
                print(t)
'''


def rcheck_model():
    with tf.Session() as sess:
        w1 = tf.Variable(tf.truncated_normal([data_size,hidden1_units],stddev=1.0/math.sqrt(float(data_size))),name="w1")
        b1 = tf.Variable(tf.zeros([hidden1_units]),name="b1")
        w2 = tf.Variable(tf.truncated_normal([hidden1_units,hidden2_units],stddev=1.0/math.sqrt(float(hidden1_units))),name="w2")
        b2 = tf.Variable(tf.zeros([hidden2_units]),name="b2")
        wsl = tf.Variable(tf.truncated_normal([hidden2_units,labels_size],stddev=1.0/math.sqrt(float(hidden2_units))),name="wsl")
        bsl = tf.Variable(tf.zeros([labels_size]),name="bsl")
        data_test,labels_test = inputs(save_dir+'test_v1.tfrecord', batch_size=999,num_epochs=None)
        module_file = tf.train.latest_checkpoint(log_dir)
        saver = tf.train.Saver()
        saver.restore(sess, module_file)
        #logits_test = inference(data_test,w1,b1,w2,b2,wsl,bsl)


        hidden_layer1 = tf.nn.relu(tf.matmul(data_test, w1) + b1)
        hidden_layer2 = tf.nn.relu(tf.matmul(hidden_layer1, w2) + b2)
        logits_test = tf.matmul(hidden_layer2, wsl) + bsl

        test_correct = evaluation(logits_test, labels_test)

        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(sess=sess, coord=coord)
        test_count = sess.run(test_correct)
        print('test_count:',test_count)
        test_correct_rate = test_count*1.00/(batch_size*5)
        print("test_correct_rate:",test_correct_rate)
        coord.request_stop()
        coord.join(threads)


'''
以下是预测部分
'''
def changeNumToLabel(num):
    rs = None
    if num == 0:
        rs = "00"
    if num == 1:
        rs = "01"
    if num == 2:
        rs = "03"
    if num == 3:
        rs = "10"
    if num == 4:
       rs = "13"
    if num == 5:
       rs = "30"
    if num == 6:
       rs = "31"
    if num == 7:
       rs = "33"
    return rs

rsdic = ['00','01','03','10','13','30','31','33']
def pbmodelTest(testdata):
    with tf.Graph().as_default():
        output_graph_def = tf.GraphDef()
        output_graph_path = export_dir+'gbs-805.pb'
        with open(output_graph_path, "rb") as f:
            output_graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(output_graph_def, name="")
            with tf.Session() as sess:
                #tf.initialize_all_variables().run()
                tf.global_variables_initializer().run()
                predict_result = sess.graph.get_tensor_by_name('predict_logits:0')
                #testdata = makeTestData()
                #rs = sess.run(predict_result,feed_dict={'gambling_data:0':np.reshape(testdata,[1,3586])})
                rs = sess.run(predict_result,feed_dict={'gambling_data:0':np.reshape(testdata,[1,data_size])})
                predict_order = tf.argmax(rs,dimension=1)
                grs = sess.run(predict_order)[0]
                prs_label = changeNumToLabel(grs)
                #prs_label = rsdic[grs]
                return prs_label


def getOneHotCodeDic(infile):
    i=0
    dict ={}
    with open(infile,'r',encoding='UTF-8') as file:
        for l in file:
            l=l.strip('\n')
            l=l.strip('\ufeff')
            i+=1
            dict[l]=i
    return dict


def getOneHotCode(key,dict):
    #print(len(dict))
    namepos = dict[key]
    oneHotMatrix = np.zeros((1, len(dict)))
    oneHotMatrix[0,namepos-1] = 1
    #oneHotTensor = tf.convert_to_tensor(oneHotMatrix)
    res =[]
    list = oneHotMatrix.tolist()
    return  list[0]

def predict():
    prefile = "E:\\ctfo\\tensorflow\\gambling\\data\\tb_pr_20170831.xls"
    workbook = xlrd.open_workbook(prefile)
    sheet = workbook.sheet_by_index(0)
    namedict = getOneHotCodeDic(namefile)
    lgdict = getOneHotCodeDic(lgfile)
    t = 0
    for i in range(1,218):
        try:
            lg = sheet.cell(i,0).value
            homesxname = sheet.cell(i,1).value
            awaysxname = sheet.cell(i,2).value
            print("-------------------------------------------------------")
            #print(" lg,homesxname,awaysxname:",lg,homesxname,awaysxname)
            lgOneHotCode = getOneHotCode(lg,lgdict)
            homenameHotCode =  getOneHotCode(homesxname,namedict)
            awaynameHotCode =  getOneHotCode(awaysxname,namedict)
            win	= sheet.cell(i,3).value
            draw =sheet.cell(i,4).value
            lost =sheet.cell(i,5).value
            win_rq=sheet.cell(i,6).value
            draw_rq=sheet.cell(i,7).value
            lost_rq	=sheet.cell(i,8).value

            win_c	= sheet.cell(i,9).value
            draw_c =sheet.cell(i,10).value
            lost_c =sheet.cell(i,11).value
            win_rq_c=sheet.cell(i,12).value
            draw_rq_c=sheet.cell(i,13).value
            lost_rq_c	=sheet.cell(i,14).value

            chupan_l=sheet.cell(i,15).value
            ypbegin=sheet.cell(i,16).value
            chupan_r=sheet.cell(i,17).value
            jishi_l=sheet.cell(i,18).value
            ypend=sheet.cell(i,19).value
            jishi_r=sheet.cell(i,20).value
            label=sheet.cell(i,21).value*10+sheet.cell(i,22).value
            if label == 3:
                label = 2
            if label == 10:
                label = 3
            if label == 13:
                label = 4
            if label == 30:
                label = 5
            if label == 31:
                label = 6
            if label == 33:
                label = 7
            data_sets = np.concatenate((lgOneHotCode, homenameHotCode), axis=0)
            data_sets = np.concatenate((data_sets, awaynameHotCode), axis=0)
            data_sets = np.concatenate((data_sets, [win]), axis=0)
            data_sets = np.concatenate((data_sets, [draw]), axis=0)
            data_sets = np.concatenate((data_sets, [lost]), axis=0)
            data_sets = np.concatenate((data_sets, [win_rq]), axis=0)
            data_sets = np.concatenate((data_sets, [draw_rq]), axis=0)
            data_sets = np.concatenate((data_sets, [lost_rq]), axis=0)

            data_sets = np.concatenate((data_sets, [win_c]), axis=0)
            data_sets = np.concatenate((data_sets, [draw_c]), axis=0)
            data_sets = np.concatenate((data_sets, [lost_c]), axis=0)
            data_sets = np.concatenate((data_sets, [win_rq_c]), axis=0)
            data_sets = np.concatenate((data_sets, [draw_rq_c]), axis=0)
            data_sets = np.concatenate((data_sets, [lost_rq_c]), axis=0)

            data_sets = np.concatenate((data_sets, [chupan_l]), axis=0)
            data_sets = np.concatenate((data_sets, [ypbegin]), axis=0)
            data_sets = np.concatenate((data_sets, [chupan_r]), axis=0)
            data_sets = np.concatenate((data_sets, [jishi_l]), axis=0)
            data_sets = np.concatenate((data_sets, [ypend]), axis=0)
            data_sets = np.concatenate((data_sets, [jishi_r]), axis=0)

            prs_label = pbmodelTest(data_sets)
            print(" 预测结果：",prs_label)
            print(" 实际结果：",changeNumToLabel(label))
            if prs_label == changeNumToLabel(label):
                t = t+1
            print("******************************************************")
        except Exception as e:
            print(e)
    print(t)

if __name__ == '__main__':
    #run_training()
    #check_model()
    predict()
