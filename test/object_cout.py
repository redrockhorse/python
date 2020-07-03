# -*- coding:utf-8 -*-
#@Time : 2020/2/17 下午7:03
#@Author: kkkkibj@163.com
#@File : object_cout.py
#图片物体数量

import cv2
import os

import numpy as np
import tensorflow as tf
from utils import label_map_util
from utils import visualization_utils as vis_util

def load_image_into_numpy_array(image):
	(im_width, im_height) = image.size
	return np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)



from PIL import Image


# image_np = cv2.imread("/Users/hongyanma/Desktop/wood.jpeg")
image_path = "/Users/hongyanma/Desktop/wood.jpeg"


MODEL_NAME = 'ssd_mobilenet_v1_coco_2018_01_28'
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'
# PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')
PATH_TO_LABELS = os.path.join('data', 'mscoco_complete_label_map.pbtxt')
NUM_CLASSES = 90
print('Loading model...')
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')
print('Loading label map...')
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                                use_display_name=True)
category_index = label_map_util.create_category_index(categories)
print('Detecting...')
with detection_graph.as_default():
    with tf.Session(graph=detection_graph) as sess:
        image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
        detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
        detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
        detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
        num_detections = detection_graph.get_tensor_by_name('num_detections:0')

        image = Image.open(image_path)
        image_np = load_image_into_numpy_array(image)
        image_np_expanded = np.expand_dims(image_np, axis=0)
        (boxes, scores, classes, num) = sess.run(
            [detection_boxes, detection_scores, detection_classes, num_detections],
            feed_dict={image_tensor: image_np_expanded})

        vis_util.visualize_boxes_and_labels_on_image_array(image_np, np.squeeze(boxes),
                                                           np.squeeze(classes).astype(np.int32), np.squeeze(scores),
                                                           category_index, use_normalized_coordinates=True,
                                                           line_thickness=8)
        print(classes)

        cv2.imshow('mahy', image_np)
        cv2.imwrite('/Users/hongyanma/Desktop/target.jpeg', image_np)
        cv2.waitKey(0)

