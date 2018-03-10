# -*- coding: utf8 -*-
#encoding=utf-8
#By @mahy
#email:kkkkbj@163.com
import tensorflow as tf
h1 = tf.constant([[1.57,3.20,3.75,5,13]])
h1_w = tf.constant([[1.0],[1.0],[1.0],[1.0],[1.0]])
p = tf.constant([[0.6],[0.25],[0.15]])
product = tf.matmul(h1,h1_w)
pp = tf.matmul(p,product)
#print(product)
sess = tf.Session()
result = sess.run(pp)
print(result)

