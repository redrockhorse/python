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

data_size = 1717*2+140+12
labels_size = 8
batch_size=1000
log_dir="E:\ctfo\tensorflow\tmp\tensorflow\mnist\logs"
learning_rate=0.01
max_steps = 20000
hidden1 = data_size
hidden2 = 1800
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
    oneHotTensor = tf.convert_to_tensor(oneHotMatrix)
    return  oneHotTensor


def placeholder_inputs(batch_size):
  data_size = 1717*2+140+12
  labels_size = 8
  data_placeholder = tf.placeholder(tf.float32, shape=(batch_size,
                                                         data_size))
  labels_placeholder = tf.placeholder(tf.int32, shape=(batch_size,labels_size))
  return data_placeholder, labels_placeholder


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


def loss(logits, labels):
  """Calculates the loss from the logits and the labels.

  Args:
    logits: Logits tensor, float - [batch_size, NUM_CLASSES].
    labels: Labels tensor, int32 - [batch_size].

  Returns:
    loss: Loss tensor of type float.
  """
  labels = tf.to_int64(labels)
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
  correct = tf.nn.in_top_k(logits, labels, 1)
  # Return the number of true entries.
  return tf.reduce_sum(tf.cast(correct, tf.int32))




def fill_feed_dict(data_sets,label_sets, data_pl, labels_pl):
  """Fills the feed_dict for training the given step.

  A feed_dict takes the form of:
  feed_dict = {
      <placeholder>: <tensor of values to be passed for placeholder>,
      ....
  }

  Args:
    data_set: The set of images and labels, from input_data.read_data_sets()
    images_pl: The images placeholder, from placeholder_inputs().
    labels_pl: The labels placeholder, from placeholder_inputs().

  Returns:
    feed_dict: The feed dictionary mapping from placeholders to values.
  """
  # Create the feed_dict for the placeholders filled with the next
  # `batch size` examples.
  #data_feed, labels_feed = next_batch(batch_size,data_sets,label_sets)
  feed_dict = {
      data_pl: data_sets,
      labels_pl: label_sets,
  }
  return feed_dict



def do_eval(sess,
            eval_correct,
            data_placeholder,
            labels_placeholder,
            data_set,label_set):
  """Runs one evaluation against the full epoch of data.

  Args:
    sess: The session in which the model has been trained.
    eval_correct: The Tensor that returns the number of correct predictions.
    images_placeholder: The images placeholder.
    labels_placeholder: The labels placeholder.
    data_set: The set of images and labels to evaluate, from
      input_data.read_data_sets().
  """
  # And run one epoch of eval.
  true_count = 0  # Counts the number of correct predictions.
  steps_per_epoch = data_set.num_examples // batch_size
  num_examples = steps_per_epoch * batch_size
  for step in xrange(steps_per_epoch):
    feed_dict = fill_feed_dict(data_set,label_set,
                               data_placeholder,
                               labels_placeholder)
    true_count += sess.run(eval_correct, feed_dict=feed_dict)
  precision = float(true_count) / num_examples
  print('  Num examples: %d  Num correct: %d  Precision @ 1: %0.04f' %
        (num_examples, true_count, precision))


def read_data_sets(dataFile,start,end):
    namefile = "E:\\ctfo\\tensorflow\\gambling\\data\\allname.txt"
    lgfile = "E:\\ctfo\\tensorflow\\gambling\\data\\lg20170725.txt"
    labelfile = "E:\\ctfo\\tensorflow\\gambling\\data\\label.txt"
    namedict = getOneHotCodeDic(namefile)
    lgdict = getOneHotCodeDic(lgfile)
    labeldict = getOneHotCodeDic(labelfile)

    workbook = xlrd.open_workbook(dataFile)
    sheet = workbook.sheet_by_index(0)
    data_sets = None
    label_sets = None
    for i in range(start,end):
        #lg=sheet.cell(i,0).value
        col = []
        lgOneHotCode = getOneHotCode(sheet.cell(i,0).value,lgdict)
        homenameHotCode =  getOneHotCode(sheet.cell(i,1).value,namedict)
        awaynameHotCode =  getOneHotCode(sheet.cell(i,2).value,namedict)
        tensor_row = lgOneHotCode
        tf.concat(0, [tensor_row, homenameHotCode])
        tf.concat(0, [tensor_row, awaynameHotCode])
        for j in range(3,15):
            col.append(sheet.cell(i,j).value)
        c = tf.constant(col,shape=[12])
        tf.concat(0, [tensor_row, c])
        #data_sets.append(tf.reshape(tensor_row,[-1]))
        tensor_row  = tf.reshape(tensor_row,[-1])
        if data_sets == None:
           data_sets = tensor_row
        else:
           data_sets = tf.concat(0, [data_sets, tensor_row])
        labelstr = sheet.cell(i,15).value+'_'+sheet.cell(i,16).value
        labelOneHotCode = getOneHotCode(labelstr,labeldict)
        if label_sets == None:
            label_sets = labelOneHotCode
        else:
            label_sets = tf.concat(0, [label_sets, labelOneHotCode])
    return data_sets,label_sets


def run_training():
  """Train MNIST for a number of steps."""
  # Get the sets of images and labels for training, validation, and
  # test on MNIST.
  dataFile = "E:\\ctfo\\tensorflow\\gambling\\data\\tb_pr_20170725.xls"
  data_sets_train,label_sets_train = read_data_sets(dataFile, 1,25000)
  data_sets_validation,label_sets_validation = read_data_sets(dataFile, 25000,29000)
  data_sets_test,label_sets_test = read_data_sets(dataFile, 29000,30000)

  # Tell TensorFlow that the model will be built into the default Graph.
  with tf.Graph().as_default():
    # Generate placeholders for the images and labels.
    data_placeholder, labels_placeholder = placeholder_inputs(batch_size)

    # Build a Graph that computes predictions from the inference model.
    logits = inference(data_placeholder,
                             hidden1,
                             hidden2)

    # Add to the Graph the Ops for loss calculation.
    loss = loss(logits, labels_placeholder)

    # Add to the Graph the Ops that calculate and apply gradients.
    train_op = training(loss, learning_rate)

    # Add the Op to compare the logits to the labels during evaluation.
    eval_correct = evaluation(logits, labels_placeholder)

    # Build the summary Tensor based on the TF collection of Summaries.
    summary = tf.summary.merge_all()

    # Add the variable initializer Op.
    init = tf.global_variables_initializer()

    # Create a saver for writing training checkpoints.
    saver = tf.train.Saver()

    # Create a session for running Ops on the Graph.
    sess = tf.Session()

    # Instantiate a SummaryWriter to output summaries and the Graph.
    summary_writer = tf.summary.FileWriter(log_dir, sess.graph)

    # And then after everything is built:

    # Run the Op to initialize the variables.
    sess.run(init)

    # Start the training loop.
    for step in xrange(max_steps):
      start_time = time.time()

      # Fill a feed dictionary with the actual set of images and labels
      # for this particular training step.
      feed_dict = fill_feed_dict(data_sets_train,label_sets_train,
                                 data_placeholder,
                                 labels_placeholder)

      # Run one step of the model.  The return values are the activations
      # from the `train_op` (which is discarded) and the `loss` Op.  To
      # inspect the values of your Ops or variables, you may include them
      # in the list passed to sess.run() and the value tensors will be
      # returned in the tuple from the call.
      _, loss_value = sess.run([train_op, loss],
                               feed_dict=feed_dict)

      duration = time.time() - start_time

      # Write the summaries and print an overview fairly often.
      if step % 100 == 0:
        # Print status to stdout.
        print('Step %d: loss = %.2f (%.3f sec)' % (step, loss_value, duration))
        # Update the events file.
        summary_str = sess.run(summary, feed_dict=feed_dict)
        summary_writer.add_summary(summary_str, step)
        summary_writer.flush()

      # Save a checkpoint and evaluate the model periodically.
      if (step + 1) % 1000 == 0 or (step + 1) == max_steps:
        checkpoint_file = os.path.join(log_dir, 'model.ckpt')
        saver.save(sess, checkpoint_file, global_step=step)
        # Evaluate against the training set.
        print('Training Data Eval:')
        do_eval(sess,
                eval_correct,
                data_placeholder,
                labels_placeholder,
                data_sets_train)
        # Evaluate against the validation set.
        print('Validation Data Eval:')
        do_eval(sess,
                eval_correct,
                data_placeholder,
                labels_placeholder,
                data_sets_validation)
        # Evaluate against the test set.
        print('Test Data Eval:')
        do_eval(sess,
                eval_correct,
                data_placeholder,
                labels_placeholder,
                data_sets.test)



if __name__ == '__main__':
    sess = tf.InteractiveSession()
    namefile = "E:\\ctfo\\tensorflow\\gambling\\data\\allname.txt"
    lgfile = "E:\\ctfo\\tensorflow\\gambling\\data\\lg20170725.txt"
    labelfile = "E:\\ctfo\\tensorflow\\gambling\\data\\label.txt"
    namedict = getOneHotCodeDic(namefile)
    lgdict = getOneHotCodeDic(lgfile)
    labeldict = getOneHotCodeDic(labelfile)
    dataFile = "E:\\ctfo\\tensorflow\\gambling\\data\\tb_pr_20170725.xls"
    #readData(dataFile,100,110)



