# -*- coding: utf-8 -*-
#encoding=utf-8
__author__ = 'mahy'
import  tensorflow as tf
import os
import sys
import codecs
import numpy as np
import xlwt
import xlrd
import math
import time
from six.moves import xrange  # pylint: disable=redefined-builtin
import objgraph
import gc

data_size = 1717*2+140+12
labels_size = 8
batch_size=200
log_dir="/root/tensorcode/logs"
save_dir = '/root/tensorcode/data/'
export_dir = '/root/tensorcode/data/'
namefile = "/root/tensorcode/data/allname.txt"
lgfile = "/root/tensorcode/data/lg20170725.txt"
learning_rate=0.01
max_steps = 2000000
hidden1 = 32
hidden2 = 16
"""
这个方法入参是文件路径，
返回一个文件内所有标称量组成的词典，键是标称量，值为标称量位置
"""
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
    namepos = dict[key]
    oneHotMatrix = np.zeros((1, len(dict)))
    oneHotMatrix[0,namepos-1] = 1
    #oneHotTensor = tf.convert_to_tensor(oneHotMatrix)
    res =[]
    list = oneHotMatrix.tolist()
    return  list[0]



def inference(data, hidden1_units, hidden2_units):
  """Build the MNIST model up to where it may be used for inference.

  Args:
    images: Images placeholder, from inputs().
    hidden1_units: Size of the first hidden layer.
    hidden2_units: Size of the second hidden layer.

  Returns:
    softmax_linear: Output tensor with the computed logits.
  """
  # Hidden 1
  with tf.name_scope('hidden1'):
    weights = tf.Variable(
        tf.truncated_normal([data_size, hidden1_units],
                            stddev=1.0 / math.sqrt(float(data_size))),
        name='weights')
    biases = tf.Variable(tf.zeros([hidden1_units]),
                         name='biases')
    hidden1 = tf.nn.relu(tf.matmul(data, weights) + biases)
  # Hidden 2
  with tf.name_scope('hidden2'):
    weights = tf.Variable(
        tf.truncated_normal([hidden1_units, hidden2_units],
                            stddev=1.0 / math.sqrt(float(hidden1_units))),
        name='weights')
    biases = tf.Variable(tf.zeros([hidden2_units]),
                         name='biases')
    hidden2 = tf.nn.relu(tf.matmul(hidden1, weights) + biases)
  # Linear
  with tf.name_scope('softmax_linear'):
    weights = tf.Variable(
        tf.truncated_normal([hidden2_units, labels_size],
                            stddev=1.0 / math.sqrt(float(hidden2_units))),
        name='weights')
    biases = tf.Variable(tf.zeros([labels_size]),
                         name='biases')
    logits = tf.matmul(hidden2, weights) + biases
  return logits


def loss_function(logits, labels):
  """Calculates the loss from the logits and the labels.

  Args:
    logits: Logits tensor, float - [batch_size, NUM_CLASSES].
    labels: Labels tensor, int32 - [batch_size].

  Returns:
    loss: Loss tensor of type float.
  """

  labels = tf.to_int64(labels)
  #print(' logits',logits)
  #print(' labels',labels)
  #print(tf.shape(logits))
  #print(tf.shape(labels))
  cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(
      labels=labels, logits=logits, name='xentropy')
  return tf.reduce_mean(cross_entropy, name='xentropy_mean')



def training(loss, learning_rate):
  """Sets up the training Ops.

  Creates a summarizer to track the loss over time in TensorBoard.

  Creates an optimizer and applies the gradients to all trainable variables.

  The Op returned by this function is what must be passed to the
  `sess.run()` call to cause the model to train.

  Args:
    loss: Loss tensor, from loss().
    learning_rate: The learning rate to use for gradient descent.

  Returns:
    train_op: The Op for training.
  """
  # Add a scalar summary for the snapshot loss.
  tf.summary.scalar('loss', loss)
  # Create the gradient descent optimizer with the given learning rate.
  optimizer = tf.train.GradientDescentOptimizer(learning_rate)
  # Create a variable to track the global step.
  global_step = tf.Variable(0, name='global_step', trainable=False)
  # Use the optimizer to apply the gradients that minimize the loss
  # (and also increment the global step counter) as a single training step.
  train_op = optimizer.minimize(loss, global_step=global_step)
  return train_op


def evaluation(logits, labels):
  """Evaluate the quality of the logits at predicting the label.

  Args:
    logits: Logits tensor, float - [batch_size, NUM_CLASSES].
    labels: Labels tensor, int32 - [batch_size], with values in the
      range [0, NUM_CLASSES).

  Returns:
    A scalar int32 tensor with the number of examples (out of batch_size)
    that were predicted correctly.
  """
  # For a classifier model, we can use the in_top_k Op.
  # It returns a bool tensor with shape [batch_size] that is true for
  # the examples where the label is in the top k (here k=1)
  # of all logits for that example.
  with tf.name_scope('evaluation'):
        correct = tf.nn.in_top_k(logits, labels, 1)
    # Return the number of true entries.
        evaluation = tf.reduce_sum(tf.cast(correct, tf.int32),name='eval')
  return evaluation



def read_and_decode(filename_queue):
    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_queue)
    features = tf.parse_single_example(serialized_example,
            features={
                'data': tf.FixedLenFeature([1717*2+140+12], tf.float32),
                'label': tf.FixedLenFeature([], tf.int64)
            }
        )
    data_out = features['data']
    label_out = features['label']
    return data_out,label_out


def inputs(filename, batch_size, num_epochs):
  """Reads input data num_epochs times.

  Args:
    train: Selects between the training (True) and validation (False) data.
    batch_size: Number of examples per returned batch.
    num_epochs: Number of times to read the input data, or 0/None to
       train forever.

  Returns:
    A tuple (images, labels), where:
    * images is a float tensor with shape [batch_size, mnist.IMAGE_PIXELS]
      in the range [-0.5, 0.5].
    * labels is an int32 tensor with shape [batch_size] with the true label,
      a number in the range [0, mnist.NUM_CLASSES).
    Note that an tf.train.QueueRunner is added to the graph, which
    must be run using e.g. tf.train.start_queue_runners().
  """
  with tf.name_scope('input'):
    filename_queue = tf.train.string_input_producer(
        [filename], num_epochs=num_epochs)

    # Even when reading in multiple threads, share the filename
    # queue.
    data, label = read_and_decode(filename_queue)

    # Shuffle the examples and collect them into batch_size batches.
    # (Internally uses a RandomShuffleQueue.)
    # We run this in two threads to avoid being a bottleneck.
    datas, sparse_labels = tf.train.shuffle_batch(
        [data, label], batch_size=batch_size, num_threads=2,
        capacity=1000 + 3 * batch_size,
        # Ensures a minimum amount of shuffling of examples.
        min_after_dequeue=batch_size)

    return datas, sparse_labels




def run_training():
  """Train MNIST for a number of steps."""
  # Get the sets of images and labels for training, validation, and
  # test on MNIST.
  #dataFile = "E:\\ctfo\\tensorflow\\gambling\\data\\tb_pr_20170725.xls"
  #data_sets_train,label_sets_train = read_data_sets(dataFile, 1,25000)
  #data_sets_validation,label_sets_validation = read_data_sets(dataFile, 25000,29000)
  #data_sets_test,label_sets_test = read_data_sets(dataFile, 29000,30000)

  # Tell TensorFlow that the model will be built into the default Graph.
  with tf.Graph().as_default() as graph:
    # Create a session for running Ops on the Graph.
    sess = tf.Session()
    # Generate placeholders for the images and labels.
    #data_placeholder, labels_placeholder = placeholder_inputs(batch_size)
    data, labels = inputs(save_dir+'train.tfrecord', batch_size=200,
                            num_epochs=None)

    # Build a Graph that computes predictions from the inference model.
    logits = inference(data, hidden1, hidden2)
    tf.identity(logits, name='logits')
    # Add to the Graph the Ops for loss calculation.
    loss = loss_function(logits, labels)

    # Add to the Graph the Ops that calculate and apply gradients.
    train_op = training(loss, learning_rate)

    # Add the Op to compare the logits to the labels during evaluation.
    true_count = 0
    eval_correct = evaluation(logits, labels)
    tf.identity(eval_correct, name='eval_correct')

    # Build the summary Tensor based on the TF collection of Summaries.
    summary = tf.summary.merge_all()

    # Add the variable initializer Op.
    init = tf.group(tf.global_variables_initializer(),
                       tf.local_variables_initializer())

    # Create a saver for writing training checkpoints.
    saver = tf.train.Saver()



    # Instantiate a SummaryWriter to output summaries and the Graph.
    summary_writer = tf.summary.FileWriter(log_dir, sess.graph)

    # And then after everything is built:

    # Run the Op to initialize the variables.
    sess.run(init)

    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(sess=sess, coord=coord)
    # Start the training loop.
    try:
        for step in xrange(max_steps):
            start_time = time.time()
            _, loss_value = sess.run([train_op, loss])

            duration = time.time() - start_time

            if step % 1000 == 0:
                # Print status to stdout.
                print('Step %d: loss = %.2f (%.3f sec)' % (step, loss_value, duration))
                # Update the events file.
                true_count += sess.run(eval_correct)
                print(' true_count:',true_count)
                summary_str = sess.run(summary)
                summary_writer.add_graph(graph,step)
                summary_writer.add_summary(summary_str, step)
                summary_writer.flush()
            if (step + 1) % 1000 == 0 or (step + 1) == max_steps:
                checkpoint_file = os.path.join(log_dir, 'model.ckpt')
                saver.save(sess, checkpoint_file, global_step=step)

    except tf.errors.OutOfRangeError:
        print('Done training for %d epochs, %d steps.' % (1, step))
    finally:
        # When done, ask the threads to stop.
        coord.request_stop()
    coord.join(threads)
    #训练完成后将权重和偏置保存下来嵌入图中
    weights1 = graph.get_tensor_by_name('hidden1/weights:0')
    biases1 = graph.get_tensor_by_name('hidden1/biases:0')
    weights2 = graph.get_tensor_by_name('hidden2/weights:0')
    biases2 = graph.get_tensor_by_name('hidden2/biases:0')
    weights_sl = graph.get_tensor_by_name('softmax_linear/weights:0')
    biases_sl = graph.get_tensor_by_name('softmax_linear/biases:0')

    #graph_def = graph.as_graph_def()
    #tf.train.write_graph(graph_def, export_dir, 'expert-graph.pb', as_text=False)

  _weights1 = weights1.eval(session=sess)
  _biases1 = biases1.eval(session=sess)
  _weights2 = weights2.eval(session=sess)
  _biases2 = biases2.eval(session=sess)
  _weights_sl = weights_sl.eval(session=sess)
  _biases_sl = biases_sl.eval(session=sess)
  sess.close()

  g_2 = tf.Graph()
  with g_2.as_default():
    #predict class
    gambling_data = tf.placeholder(tf.float32,[1,data_size],name="gambling_data")
    w1 = tf.constant(_weights1, name="p_weights1")
    b1 = tf.constant(_biases1, name="p_biases1")
    w2 = tf.constant(_weights2, name="p_weights2")
    b2 = tf.constant(_biases2, name="p_biases2")
    wsl = tf.constant(_weights_sl, name="p_weights_sl")
    bsl = tf.constant(_biases_sl, name="p_biases_sl")
    hidden_layer1 = tf.nn.relu(tf.matmul(gambling_data, w1) + b1)
    hidden_layer2 = tf.nn.relu(tf.matmul(hidden_layer1, w2) + b2)
    predict_logits = tf.matmul(hidden_layer2, wsl) + bsl
    #predict_logits = inference(gambling_data, hidden1, hidden2)
    tf.identity(predict_logits, name='predict_logits')
    predict_result = tf.argmax(predict_logits,axis=0,name="predict_result")
    sess_2 = tf.Session()
    init_2 = tf.initialize_all_variables();
    sess_2.run(init_2)
    graph_def = g_2.as_graph_def()
    tf.train.write_graph(graph_def, export_dir, 'gbpredict-graph.pb', as_text=False)
  sess_2.close()

def checkModel():
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        with tf.Session(graph=detection_graph) as sess:
            new_saver = tf.train.import_meta_graph('/root/tensorcode/logs/model.ckpt-1999999.meta')
            new_saver.restore(sess, tf.train.latest_checkpoint('/root/tensorcode/logs'))
            data, labels = inputs(save_dir+'test.tfrecord', batch_size=1,
                            num_epochs=None)
            coord = tf.train.Coordinator()
            threads = tf.train.start_queue_runners(sess=sess, coord=coord)
            #global_step = detection_graph.get_tensor_by_name('logits')
            #logits = detection_graph.get_operation_by_name('logits')
            size = tf.Variable(1, name="input/shuffle_batch/n")
            logits = detection_graph.get_tensor_by_name('softmax_linear/add:0')
            #input = detection_graph.get_tensor_by_name('input/input_producer/Const:0')
            input = detection_graph.get_tensor_by_name('input/shuffle_batch/n:0')


            #eval_correct =  detection_graph.get_operation_by_name('eval_correct')
            eval_correct =  detection_graph.get_tensor_by_name('evaluation/eval:0')
            #print(sess.run(global_step))
            truecount =0
            try:
                for step in xrange(1000):
                    start_time = time.time()
                    duration = time.time() - start_time
                    datasets ,labelsets = sess.run([data, labels])

                    results_logits  = sess.run(logits,feed_dict={'input/shuffle_batch/n:0':1,'input/input_producer/Const:0':[save_dir+'test.tfrecord']})
                    ev = evaluation(results_logits,labelsets)
                    #eval_correct = sess.run(eval_correct)
                    #ev = eval_correct.eval(feed_dict={'input/shuffle_batch/n:0':1,'input/input_producer/Const:0':[save_dir+'test.tfrecord']})
                    print(' logits:',results_logits)
                    print(' label:',labelsets)
                    ev_v = sess.run(ev)
                    print(' eval_correct:',ev_v)
                    truecount+=ev_v
                    if step % 1 == 0:
                        pass
                        # Print status to stdout.
                        #print('Step %d: loss = %.2f (%.3f sec)' % (step, eval_correct, duration))
                        #print(' step:',step)
                        #print(' labels:',labels)
            except tf.errors.OutOfRangeError:
                print('Done training for %d epochs, %d steps.' % (1, step))
            finally:
                # When done, ask the threads to stop.
                coord.request_stop()
            print(truecount)
            coord.join(threads)
            sess.close()

def pbmodelTest():
    with tf.Graph().as_default():
        output_graph_def = tf.GraphDef()
        output_graph_path = export_dir+'expert-graph.pb'
        with open(output_graph_path, "rb") as f:
            output_graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(output_graph_def, name="")
            with tf.Session() as sess:
                tf.initialize_all_variables().run()
                predict_result = sess.graph.get_tensor_by_name('predict_logits:0')
                testdata = makeTestData()
                rs = sess.run(predict_result,feed_dict={'gambling_data:0':np.reshape(testdata,[1,3586])})
                print(rs)

def makeTestData():
    namedict = getOneHotCodeDic(namefile)
    lgdict = getOneHotCodeDic(lgfile)
    '''
    lgOneHotCode = getOneHotCode('西甲',lgdict)
    homenameHotCode =  getOneHotCode('塞尔塔',namedict)
    awaynameHotCode =  getOneHotCode('皇马',namedict)
    data_sets = np.concatenate((lgOneHotCode, homenameHotCode), axis=0)
    data_sets = np.concatenate((data_sets, awaynameHotCode), axis=0)
    data_sets = np.concatenate((data_sets, [13]), axis=0)
    data_sets = np.concatenate((data_sets, [7.9]), axis=0)
    data_sets = np.concatenate((data_sets, [1.08]), axis=0)
    data_sets = np.concatenate((data_sets, [2.56]), axis=0)
    data_sets = np.concatenate((data_sets, [4.2]), axis=0)
    data_sets = np.concatenate((data_sets, [2]), axis=0)
    data_sets = np.concatenate((data_sets, [0.94]), axis=0)
    data_sets = np.concatenate((data_sets, [1]), axis=0)
    data_sets = np.concatenate((data_sets, [0.92]), axis=0)
    data_sets = np.concatenate((data_sets, [1.04]), axis=0)
    data_sets = np.concatenate((data_sets, [2]), axis=0)
    data_sets = np.concatenate((data_sets, [0.82]), axis=0)
    '''
    lgOneHotCode = getOneHotCode('西甲',lgdict)
    homenameHotCode =  getOneHotCode('皇马',namedict)
    awaynameHotCode =  getOneHotCode('塞维利',namedict)
    data_sets = np.concatenate((lgOneHotCode, homenameHotCode), axis=0)
    data_sets = np.concatenate((data_sets, awaynameHotCode), axis=0)
    data_sets = np.concatenate((data_sets, [1.14]), axis=0)
    data_sets = np.concatenate((data_sets, [5.75]), axis=0)
    data_sets = np.concatenate((data_sets, [9.6]), axis=0)
    data_sets = np.concatenate((data_sets, [2.17]), axis=0)
    data_sets = np.concatenate((data_sets, [4.3]), axis=0)
    data_sets = np.concatenate((data_sets, [2.3]), axis=0)
    data_sets = np.concatenate((data_sets, [0.88]), axis=0)
    data_sets = np.concatenate((data_sets, [-2.25]), axis=0)
    data_sets = np.concatenate((data_sets, [0.98]), axis=0)
    data_sets = np.concatenate((data_sets, [1.14]), axis=0)
    data_sets = np.concatenate((data_sets, [-2.25]), axis=0)
    data_sets = np.concatenate((data_sets, [0.72]), axis=0)

    return data_sets


if __name__ == '__main__':
    """
    sess = tf.InteractiveSession()
    namefile = "E:\\ctfo\\tensorflow\\gambling\\data\\allname.txt"
    lgfile = "E:\\ctfo\\tensorflow\\gambling\\data\\lg20170725.txt"
    labelfile = "E:\\ctfo\\tensorflow\\gambling\\data\\label.txt"
    namedict = getOneHotCodeDic(namefile)
    lgdict = getOneHotCodeDic(lgfile)
    labeldict = getOneHotCodeDic(labelfile)
    dataFile = "E:\\ctfo\\tensorflow\\gambling\\data\\tb_pr_20170725.xls"
    #readData(dataFile,100,110)
    """
    run_training()
    #checkModel()