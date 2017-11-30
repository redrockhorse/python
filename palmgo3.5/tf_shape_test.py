# -*- coding: utf-8 -*-
#encoding=utf-8
import  tensorflow as tf
X=tf.constant([1,2,3])#Tensor("Const:0", shape=(3,), dtype=int32)
print(X)
Y=tf.constant([[1],[2],[3]])#Tensor("Const_1:0", shape=(3, 1), dtype=int32)
print(Y)
Z=tf.constant([[1,2],[2,4],[3,5]])#Tensor("Const_2:0", shape=(3, 2), dtype=int32)
print(Z)
A=tf.constant([[[1,2,3],[2,4,3],[3,5,3]]])#Tensor("Const_3:0", shape=(1, 3, 3), dtype=int32)
print(A)
B=tf.constant([[[1,2,3],[2,4,3],[3,5,3]],[[1,2,3],[2,4,3],[3,5,3]]])#Tensor("Const_4:0", shape=(2, 3, 3), dtype=int32)
print(B)
C=tf.constant(3)#Tensor("Const_5:0", shape=(), dtype=int32)
print(C)