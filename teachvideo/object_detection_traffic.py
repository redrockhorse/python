# -*- coding:utf-8 -*-
#@Time : 2020/2/21 下午5:04
#@Author: kkkkibj@163.com
#@File : object_detection_traffic.py
import os
import sys
import cv2
import numpy as np
import tensorflow as tf
sys.path.append('/Users/hongyanma/gitspace/python/python/models/research')
from utils import label_map_util
from utils import visualization_utils as vis_util

cap = cv2.VideoCapture('/Users/hongyanma/gitspace/python/python/data/视频源/源视频0.avi',cv2.CAP_FFMPEG)

MODEL_NAME = '/Users/hongyanma/gitspace/python/python/test/ssd_mobilenet_v1_coco_2018_01_28'
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

PATH_TO_LABELS = os.path.join('/Users/hongyanma/gitspace/python/python/test/data', 'mscoco_label_map.pbtxt')
NUM_CLASSES = 90

detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,use_display_name=True)
category_index = label_map_util.create_category_index(categories)

if cap.isOpened():
    with detection_graph.as_default():
        with tf.Session(graph=detection_graph) as sess:
            while True:
                ret, image_np = cap.read()
                image_np_expanded = np.expand_dims(image_np, axis=0)
                image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
                boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
                scores = detection_graph.get_tensor_by_name('detection_scores:0')
                classes = detection_graph.get_tensor_by_name('detection_classes:0')
                num_detections = detection_graph.get_tensor_by_name('num_detections:0')
                (boxes, scores, classes, num_detections) = sess.run([boxes, scores, classes, num_detections],feed_dict={image_tensor: image_np_expanded})
                vis_util.visualize_boxes_and_labels_on_image_array(image_np,np.squeeze(boxes),np.squeeze(classes).astype(np.int32),np.squeeze(scores),category_index,use_normalized_coordinates=True,line_thickness=8)

                cv2.imshow('mahy', image_np)  # 显示
                cv2.waitKey(int(1000 / int(40)))
            cap.release()
else:
    print('video open fail~~')