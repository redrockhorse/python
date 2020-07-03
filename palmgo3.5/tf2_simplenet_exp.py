# -*- coding:utf-8 -*-
#@Time : 2020/5/19 上午10:38
#@Author: kkkkibj@163.com
#@File : tf2_test.py
import tensorflow as tf
import numpy as np
import pydot
#print(pydot.call_graphviz())
inputs = tf.keras.Input(shape=(784,), name='img')
h1 = tf.keras.layers.Dense(32, activation='relu')(inputs)
h2 = tf.keras.layers.Dense(32, activation='relu')(h1)
outputs = tf.keras.layers.Dense(10, activation='softmax')(h2)
model = tf.keras.Model(inputs=inputs, outputs=outputs, name='mnist model')

model.summary()
tf.keras.utils.plot_model(model, 'mnist_model.png')
tf.keras.utils.plot_model(model, 'model_info.png', show_shapes=True)