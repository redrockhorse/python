#!/usr/bin/python
# -*- coding:utf-8 -*-


'''
def create_vocabulary(vocabulary_path, data_path, max_vocabulary_size,
                      tokenizer=None, normalize_digits=True):
'''

import data_utils
import tensorflow as tf
import jieba

'''
def main(_):
    data_path = 'E:\\ctfo\\tensorflow\palm\\traffic_event\\data\\content.txt'
    jieba_path = 'E:\\ctfo\\tensorflow\palm\\traffic_event\\data\\jieba.txt'
    vocabulary_path= 'E:\\ctfo\\tensorflow\palm\\traffic_event\\data\\vocab'
    jieba_dic = 'E:\\ctfo\\tensorflow\palm\\traffic_event\\data\\dict.txt'
    max_vocabulary_size = 1000000
    jieba.load_userdict(jieba_dic)
    jieba_file = open(jieba_path,'w+')
    with open(data_path,'r',encoding='utf8') as f:
        for line in f:
            line = line.replace('&nbsp','')
            seg_list = jieba.cut(line,cut_all=True)
            jieba_line=" ".join(seg_list)
            jieba_file.write(jieba_line)
    jieba_file.close()
    data_utils.create_vocabulary(vocabulary_path,jieba_path,max_vocabulary_size)
'''
def main(_):
    jieba_dic = 'E:\\ctfo\\tensorflow\palm\\traffic_event\\data\\dict.txt'
    input= 'E:\\ctfo\\tensorflow\\palm\\traffic_event\\data\\train\\title-train.txt'
    output = 'E:\\ctfo\\tensorflow\\palm\\traffic_event\\data\\train\\title-train-1.txt'
    jieba.load_userdict(jieba_dic)
    of = open(output,'w+')
    with open(input,'r') as f:
        for line in f:
            line = line.replace('&nbsp','')
            seg_list = jieba.cut(line,cut_all=False)
            jieba_line=" ".join(seg_list)
            of.write(jieba_line)
    of.close()




if __name__=="__main__":
    tf.app.run()