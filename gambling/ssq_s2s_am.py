# -*- coding: utf-8 -*-
#encoding=utf-8
__author__ = 'mahy'
'''
seq2seq base on attention model
'''
import  tensorflow as tf
import os
import seq2seq_model
import sys
import data_utils
from six.moves import xrange
import time
import math
import  numpy as np

file_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(file_path, "data")
train_dir = os.path.join(file_path, "sqlogs")
src_train = os.path.join(data_path, "sq.txt")
buckets = [(7, 7)]


class SmallConfig(object):
    learning_rate = 0.1
    init_scale = 0.04
    learning_rate_decay_factor = 0.99
    max_gradient_norm = 5.0
    num_samples = 512 # Sampled Softmax
    batch_size = 16
    size = 32 # Number of Node of each layer
    num_layers = 2
    vocab_size = 50

config = SmallConfig()
tf.app.flags.DEFINE_float("learning_rate", config.learning_rate, "Learning rate.")
tf.app.flags.DEFINE_float("learning_rate_decay_factor", config.learning_rate_decay_factor, "Learning rate decays by this much.")
tf.app.flags.DEFINE_float("max_gradient_norm", config.max_gradient_norm, "Clip gradients to this norm.")
tf.app.flags.DEFINE_integer("num_samples", config.num_samples, "Number of Samples for Sampled softmax")
tf.app.flags.DEFINE_integer("batch_size", config.batch_size, "Batch size to use during training.")
tf.app.flags.DEFINE_integer("size", config.size, "Size of each model layer.")
tf.app.flags.DEFINE_integer("num_layers", config.num_layers, "Number of layers in the model.")
tf.app.flags.DEFINE_integer("vocab_size", config.vocab_size, "vocabulary size.")

tf.app.flags.DEFINE_string("data_dir", data_path, "Data directory")
tf.app.flags.DEFINE_string("train_dir", train_dir, "Training directory.")
tf.app.flags.DEFINE_integer("max_train_data_size", 0, "Limit on the size of training data (0: no limit).")
tf.app.flags.DEFINE_integer("steps_per_checkpoint", 1000, "How many training steps to do per checkpoint.")
tf.app.flags.DEFINE_boolean("decode", False, "Set to True for interactive decoding.") # true for prediction
tf.app.flags.DEFINE_boolean("use_fp16", False, "Train using fp16 instead of fp32.")

# define namespace for this model only
tf.app.flags.DEFINE_string("headline_scope_name", "ssq_scope", "Variable scope of Headline textsum model")

FLAGS = tf.app.flags.FLAGS


def read_data(source_path):
  print(source_path)
  data_set = [[] for _ in buckets]
  tmp_arr = []
  with open(source_path, 'r',encoding='utf-8') as source_file:
      for line in source_file:
        #print(line)
        ids = [int(x) for x in line.split(',')]
        tmp_arr.append(ids)
  for i in range(len(tmp_arr)-1):
      data_set[0].append([tmp_arr[i], tmp_arr[i+1]])
  return data_set


def create_model(session, forward_only):
  """Create headline model and initialize or load parameters in session."""
  # dtype = tf.float16 if FLAGS.use_fp16 else tf.float32
  # dtype = tf.float32
  initializer = tf.random_uniform_initializer(-config.init_scale, config.init_scale)
  # Adding unique variable scope to model
  with tf.variable_scope(FLAGS.headline_scope_name, reuse=None, initializer=initializer):
    model = seq2seq_model.Seq2SeqModel(
        FLAGS.vocab_size,
        FLAGS.vocab_size,
        buckets,
        FLAGS.size,
        FLAGS.num_layers,
        FLAGS.max_gradient_norm,
        FLAGS.batch_size,
        FLAGS.learning_rate,
        FLAGS.learning_rate_decay_factor,
        use_lstm = True, # LSTM instend of GRU
        num_samples = FLAGS.num_samples,
        forward_only=forward_only)

  ckpt = tf.train.get_checkpoint_state(FLAGS.train_dir)
  if ckpt:
    model_checkpoint_path = ckpt.model_checkpoint_path
    print("Reading model parameters from %s" % model_checkpoint_path)
    saver = tf.train.Saver()
    saver.restore(session, tf.train.latest_checkpoint(FLAGS.train_dir))
  else:
    print("Created model with fresh parameters.")
    session.run(tf.global_variables_initializer())

  return model



def train():
    print('start')
    # device config for CPU usage
    config = tf.ConfigProto(device_count={"CPU": 4}, # limit to 4 CPU usage
                   inter_op_parallelism_threads=1,
                   intra_op_parallelism_threads=2) # n threads parallel for ops
    train_set = read_data(src_train)
    with tf.Session(config = config) as sess:
        print("Creating %d layers of %d units." % (FLAGS.num_layers, FLAGS.size))
        model = create_model(sess, False)
        step_time, loss = 0.0, 0.0
        current_step = 0
        previous_losses = []
        bucket_id = 0
        while True:
            start_time = time.time()
            encoder_inputs, decoder_inputs, target_weights = model.get_batch(
                  train_set, bucket_id)

            _, step_loss, _ = model.step(sess, encoder_inputs, decoder_inputs,
                                           target_weights, bucket_id, False)
            step_time += (time.time() - start_time) / FLAGS.steps_per_checkpoint
            loss += step_loss / FLAGS.steps_per_checkpoint
            current_step += 1

            # Once in a while, we save checkpoint, print statistics, and run evals.
            if current_step % FLAGS.steps_per_checkpoint == 0:
                # Print statistics for the previous epoch.
                perplexity = math.exp(float(loss)) if loss < 300 else float("inf")
                print ("global step %d learning rate %.4f step-time %.2f perplexity "
                       "%.2f" % (model.global_step.eval(), model.learning_rate.eval(),
                                 step_time, perplexity))
                # Decrease learning rate if no improvement was seen over last 3 times.
                if len(previous_losses) > 2 and loss > max(previous_losses[-3:]):
                  sess.run(model.learning_rate_decay_op)
                previous_losses.append(loss)
                # Save checkpoint and zero timer and loss.
                checkpoint_path = os.path.join(FLAGS.train_dir, "headline_large.ckpt")
                model.saver.save(sess, checkpoint_path, global_step=model.global_step)
                sys.stdout.flush()


def decode():
    bucket_id = 0
    with tf.Session() as sess:
        # Create model and load parameters.
        model = create_model(sess, True)
        sys.stdout.write("> ")
        sys.stdout.flush()
        sentence = sys.stdin.readline()
        while sentence:
            if (len(sentence.strip('\n')) == 0):
                sys.stdout.flush()
                sentence = sys.stdin.readline()
            token_ids = [int(x) for x in sentence.split(',')]
            encoder_inputs, decoder_inputs, target_weights = model.get_batch({bucket_id: [(token_ids, [])]}, bucket_id)
            _, _, output_logits_batch = model.step(sess, encoder_inputs, decoder_inputs, target_weights, bucket_id, True)
            output_logits = []
            for item in output_logits_batch:
                output_logits.append(item[0])
            outputs = [int(np.argmax(logit)) for logit in output_logits]
            # If there is an EOS symbol in outputs, cut them at that point.
            if data_utils.EOS_ID in outputs:
                outputs = outputs[:outputs.index(data_utils.EOS_ID)]
            print(" ".join([str(output) for output in outputs]))
            print("> ", end="")
            sys.stdout.flush()
            sentence = sys.stdin.readline()

def main(_):
  #train()
  decode()

if __name__ == "__main__":
  tf.app.run()
