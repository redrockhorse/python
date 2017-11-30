__author__ = 'mahy'
import tensorflow as tf
logits = [[ 4.04313469 ,-2.47008681, -2.57700396 , 4.38158655 ,-3.7977581 ,  0.16855487,
   4.13683128 , 3.73921204]]
labels = [7]
correct = tf.nn.in_top_k(logits, labels, 2)
sess = tf.Session()
init = tf.group(tf.global_variables_initializer(),
                       tf.local_variables_initializer())
sess.run(init)
print(sess.run(correct))
