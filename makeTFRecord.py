# -*- coding: utf-8 -*-
#encoding=utf-8
__author__ = 'mahy'
import  tensorflow as tf
import numpy as np
import os
import xlrd

test_dir = 'E:\\ctfo\\tensorflow\\gambling\\data\\'
save_dir = 'E:\\ctfo\\tensorflow\\gambling\\data\\'
namefile = "E:\\ctfo\\tensorflow\\gambling\\data\\allname.txt"
lgfile = "E:\\ctfo\\tensorflow\\gambling\\data\\lg20170725.txt"
BATCH_SIZE = 25

def int64_feature(value):
  """Wrapper for inserting int64 features into Example proto."""
  if not isinstance(value, list):
    value = [value]
  return tf.train.Feature(int64_list=tf.train.Int64List(value=value))

def float32_feature(value):
  return tf.train.Feature(float_list=tf.train.FloatList(value=value))


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

def getNameByOneHotCode(oneHot,dictArray):
    oneHotArray = np.array(oneHot)
    _positon =np.argmax(oneHotArray)
    name = dictArray[_positon]
    return name


def makeTFrecord(dataFile, start,end, save_dir, name):
    '''convert all images and labels to one tfrecord file.
    Args:
        images: list of image directories, string type
        labels: list of labels, int type
        save_dir: the directory to save tfrecord file, e.g.: '/home/folder1/'
        name: the name of tfrecord file, string type, e.g.: 'train'
    Return:
        no return
    Note:
        converting needs some time, be patient...
    '''
    namedict = getOneHotCodeDic(namefile)
    lgdict = getOneHotCodeDic(lgfile)
    writer = tf.python_io.TFRecordWriter(save_dir+name+'.tfrecord')
    workbook = xlrd.open_workbook(dataFile)
    sheet = workbook.sheet_by_index(0)
    for i in range(start,end):
        lg = sheet.cell(i,0).value
        #lg_raw = lg.tostring()
        homesxname = sheet.cell(i,1).value
        #homesxname_raw = homesxname.tostring()
        awaysxname = sheet.cell(i,2).value
        #awaysxname_raw = awaysxname.tostring()

        lgOneHotCode = getOneHotCode(lg,lgdict)
        homenameHotCode =  getOneHotCode(homesxname,namedict)
        awaynameHotCode =  getOneHotCode(awaysxname,namedict)
        #lgOneHotCode = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        #homenameHotCode =[0,1,0]
        #awaynameHotCode =[0,1,0,0]
        #lg1hot = lgOneHotCode.astype(np.uint8)
        #lg_raw = lg1hot.tostring()
        #homename1hot = homenameHotCode.astype(np.uint8)
        #homesxname_raw = homename1hot.tostring()
        #awayname1hot = awaynameHotCode.astype(np.uint8)
        #awaysxname_raw = awayname1hot.tostring()


        win	= sheet.cell(i,3).value
        draw =sheet.cell(i,4).value
        lost =sheet.cell(i,5).value
        win_rq=sheet.cell(i,6).value
        draw_rq=sheet.cell(i,7).value
        lost_rq	=sheet.cell(i,8).value
        chupan_l=sheet.cell(i,9).value
        ypbegin=sheet.cell(i,10).value
        chupan_r=sheet.cell(i,11).value
        jishi_l=sheet.cell(i,12).value
        ypend=sheet.cell(i,13).value
        jishi_r=sheet.cell(i,14).value
        label=sheet.cell(i,15).value*10+sheet.cell(i,16).value
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
        label = int(label)
        data_sets = np.concatenate((lgOneHotCode, homenameHotCode), axis=0)
        data_sets = np.concatenate((data_sets, awaynameHotCode), axis=0)
        data_sets = np.concatenate((data_sets, [win]), axis=0)
        data_sets = np.concatenate((data_sets, [draw]), axis=0)
        data_sets = np.concatenate((data_sets, [lost]), axis=0)
        data_sets = np.concatenate((data_sets, [win_rq]), axis=0)
        data_sets = np.concatenate((data_sets, [draw_rq]), axis=0)
        data_sets = np.concatenate((data_sets, [lost_rq]), axis=0)
        data_sets = np.concatenate((data_sets, [chupan_l]), axis=0)
        data_sets = np.concatenate((data_sets, [ypbegin]), axis=0)
        data_sets = np.concatenate((data_sets, [chupan_r]), axis=0)
        data_sets = np.concatenate((data_sets, [jishi_l]), axis=0)
        data_sets = np.concatenate((data_sets, [ypend]), axis=0)
        data_sets = np.concatenate((data_sets, [jishi_r]), axis=0)
        #print(' data_sets: ',data_sets)
        #label_raw = label.tostring()
        example = tf.train.Example(
            features = tf.train.Features(
                feature = {
                            #'lg':tf.train.Feature(bytes_list = tf.train.BytesList(value=[lg_raw])),
                            #'homesxname':tf.train.Feature(bytes_list = tf.train.BytesList(value = [homesxname_raw])),
                            #'awaysxname':tf.train.Feature(bytes_list = tf.train.BytesList(value = [awaysxname_raw])),
                            #'b':tf.train.Feature(int64_list = tf.train.Int64List(value = b)),
                            'data':tf.train.Feature(float_list = tf.train.FloatList(value=data_sets)),
                            'label':tf.train.Feature(int64_list = tf.train.Int64List(value = [label])),
                           }))
        serialized = example.SerializeToString()
        writer.write(serialized)
        if i%100==0:
            print('   writer',i,'DOWN!')
    writer.close()


def read_and_decode(filename_queue):
    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_queue)
    features = tf.parse_single_example(serialized_example,
            features={
                'data': tf.FixedLenFeature([1731*2+140+12], tf.float32),
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
        min_after_dequeue=1000)

    return datas, sparse_labels

def run_training(data,label):
    print(' data:',data)
    print(' label:',label)



if __name__ == '__main__':
    '''
    with tf.Graph().as_default():
        sess = tf.Session()
        data, labels = inputs(save_dir+'train.tfrecord', batch_size=200,
                            num_epochs=None)
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(sess=sess, coord=coord)
        init = tf.initialize_all_variables()
        sess.run(init)
        run_training(data,labels)
        try:
            for i in range(20000):
                if not coord.should_stop():
                    run_training(data,labels)
        except tf.errors.OutOfRangeError:
            print('error.....')
        finally:
            coord.request_stop()
        coord.join(threads)
        sess.close()
    '''
    dataFile = "E:\\ctfo\\tensorflow\\gambling\\data\\tb_pr_20170804.xls"
    makeTFrecord(dataFile, 1256,31255, save_dir, 'train')
    #makeTFrecord(dataFile, 1,10, save_dir, 'train')
    #makeTFrecord(dataFile, 1,25000, save_dir, 'train')
    #makeTFrecord(dataFile, 25000,30000, save_dir, 'validation')
    #makeTFrecord(dataFile, 30000,31000, save_dir, 'test')





