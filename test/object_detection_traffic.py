# -*- coding:utf-8 -*-
#@Time : 2020/2/6 上午8:44
#@Author: kkkkibj@163.com
#@File : object_detection_traffic.py
import cv2
import os
import numpy as np
import tensorflow as tf
from utils import label_map_util
from utils import visualization_utils as vis_util
from queue import Queue
import requests
import time

qi = Queue()
class_dic = {}
size = [256,256]
image_hash_name_arr = []
box_center_arr_pre = []
image_hash_name_arr_pre = []


headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
,'Accept-Encoding': 'gzip, deflate, br'
,'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
,'Cache-Control': 'no-cache'
,'Connection': 'keep-alive'
,'Cookie': 'acw_tc=2f624a5d15795264267093767e0ec1eebcc28ef0a7105ba80ddc9a54412e6f'
,'Host': 'spglxtapi.jchc.cn'
# ,'Host': '36.112.134.107:9107'
,'Pragma': 'no-cache'
,'Sec-Fetch-Mode': 'navigate'
,'Sec-Fetch-Site': 'none'
,'Sec-Fetch-User': '?1'
,'Upgrade-Insecure-Requests': 1
,'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}

def getFlvUrl(cameraNum,cameraName):
    url = "https://spglxtapi.jchc.cn/service/video.GetCameraPlayURL";
    # url = "http://36.112.134.107:9107/service/video.GetCameraPlayURL"
    # https: // spglxtapi.jchc.cn / service / video.GetCameraPlayURL?user = PT1100202001110001 & videotype = 0 & cameraNum = sxjgl_shhungs_310000011011001001416 & cameraName = % E6 % B1 % BD % E8 % BD % A6 % E5 % 9F % 8E % E7 % AB % 8B % E4 % BA % A4 & _ = 1579521074466
    params = {
        'user': 'PT1100202001110001',
        # 'user': 'PT1100202001190002',
        'videotype': 1, # 0:低码流;1: 高码流
        'cameraNum':cameraNum,
        'cameraName':cameraName,
    # department: "20000320000"
    }
    #print(params)
    r = requests.get(url,params=params,headers=headers)
    #print(r)
    #print(r.url)
    result = r.json()
    print(result)
    return result['videoRequestUrl']['flv_url']
    #print(result)

def extractData(image_np,boxes,classes,scores,category_index,images_container,max_boxes_to_draw=20,min_score_thresh=.6,enbale_class =[8,3,6]):
    global image_hash_name_arr
    global box_center_arr_pre
    global image_hash_name_arr_pre
    global class_dic
    global size
    if not max_boxes_to_draw:
        max_boxes_to_draw = boxes.shape[0]
    for i in range(min(max_boxes_to_draw, boxes.shape[0])):
        if scores is None or scores[i] > min_score_thresh:
            box = tuple(boxes[i].tolist())
            if classes[i] in category_index.keys():
              class_name = category_index[classes[i]]['name']
              if class_name not in class_dic:
                  class_dic[class_name] = classes[i]
              if classes[i] in enbale_class:
                  ymin, xmin, ymax, xmax = box
                  xmax_p = int(xmax*size[0])
                  xmin_p = int(xmin * size[0])
                  ymax_p = int(ymax * size[1])
                  ymin_p = int(ymin * size[1])
                  cropImg = image_np[ymin_p:ymax_p, xmin_p:xmax_p]
                  qi.put(cropImg)
              print(class_name)

def dowloadVideo(cameraNum,cameraName,dir):
    flvurl = getFlvUrl(cameraNum, cameraName)
    print(flvurl)
    with open(dir+'/'+cameraNum+'.flv', 'wb+') as f:
        r = requests.get(flvurl,stream=True)
        i = 0
        for chunk in r.iter_content(chunk_size=512):
            if chunk and i < 1000:#1000*512大约2分05秒长度
                f.write(chunk)
                i = i+1
                if i % 100 == 0:
                    print(i)
            else:
                print('download complate!')
                break

q = Queue()
def dealVideo():
    global size
    # dir = '/Users/hongyanma/Downloads/trafficvideo'
    # flvurl = getFlvUrl('sxjgl_sdsdgs_370000011011001001267', 'G2_K459%2B246_右东')
    # dowloadVideo('fcd1f8027f524a059c59401ef6542b81', 'G1(京哈高速)天津段天昂公司K85%2B135遥控', dir)
    # flvurl = getFlvUrl('fcd1f8027f524a059c59401ef6542b81', 'G1(京哈高速)天津段天昂公司K85%2B135遥控')
    # flvurl = getFlvUrl('17c821b5-0dcd-40c8-aa86-bb92f0243392', '清河北出京出口广场(遥控)')

    # print(flvurl)
    # cap = cv2.VideoCapture('/Users/hongyanma/Downloads/trafficvideo/sxjgl_nhugs_320500011011001001063.flv')  # 打开摄像头
    # response = requests.get(flvurl, stream=True)
    # for chunk in response.iter_content(chunk_size=1024):
    #     cap = cv2.VideoCapture(chunk)
    # print(cv2.CAP_XINE)
    # cap = cv2.VideoCapture('https://youku.com-qq.net/20190526/494_d6346149/1000k/hls/index.m3u8')
    # cap = cv2.VideoCapture('https://60-9-3-149.xiu123.cn/httpflv/v69716930-171412695.flv') #https://www.6.cn/
    # cap = cv2.VideoCapture('https://ali-adaptive.pull.yximgs.com/gifshow/sgGRBqHEIW0.flv?auth_key=1581771209-0-0-77ee89696de9e928a5a0de8f47ec2db1&highTraffic=1&oidc=alihb')  # 快手的地址

    # print(cv2.VideoCaptureAPIs)
    # cap = cv2.VideoCapture(flvurl,cv2.CAP_FFMPEG)
    # cap = cv2.VideoCapture('rtmp://127.0.0.1:1935/live')
    #time.sleep(1)
    cap = cv2.VideoCapture('/Users/hongyanma/gitspace/python/python/data/视频源/源视频0.avi',cv2.CAP_FFMPEG)
    # cap.set(cv2.CAP_PROP_FPS,15)
    # print(cv2.CAP_PROP_FPS)
    print(cap.isOpened())
    # aaa = cap.grab()
    # print(aaa)
    # testframe = cap.retrieve()
    # print(testframe)
    # cv2.imshow('mahy', testframe[1])
    # for i in range(19):
    #     print(i, cap.get(i))
    #
    # if aaa is not True:
    #     print('error')
    #     exit(-1)
    # while True:
    #     ret, image_np = cap.read()
    #     # if ret is not True:
    #     #     continue
    #     print(ret)
    #     print(image_np)
    #     print('----------------------split')
    #     cv2.imshow('mahy', image_np)  # 显示
    #     cv2.waitKey(int(1000 / int(22)))
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print(size)
    # Path to frozen detection graph. This is the actual model that is used for the object detection.
    MODEL_NAME = 'ssd_mobilenet_v1_coco_2018_01_28'
    PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'
    # List of the strings that is used to add correct label for each box.
    PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')
    NUM_CLASSES = 90
    print('Loading model...')
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

    ##################### Loading label map
    print('Loading label map...')
    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                                use_display_name=True)
    category_index = label_map_util.create_category_index(categories)
    print('Detecting...')
    image_container = {}
    with detection_graph.as_default():
        with tf.Session(graph=detection_graph) as sess:
            while True:
                ret, image_np = cap.read()  # 从摄像头中获取每一帧图像
                # print(image_np)
                image_np_expanded = np.expand_dims(image_np, axis=0)
                image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
                boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
                scores = detection_graph.get_tensor_by_name('detection_scores:0')
                classes = detection_graph.get_tensor_by_name('detection_classes:0')
                num_detections = detection_graph.get_tensor_by_name('num_detections:0')
                # Actual detection.
                # print('~~~~~~~~~~~~~~')
                # print(cap.isOpened())
                if not cap.isOpened():
                    print('end of video !! ret flag')
                    break
                if not image_np_expanded.size:
                    print('end of video !!')
                    break
                try:
                    (boxes, scores, classes, num_detections) = sess.run(
                        [boxes, scores, classes, num_detections],
                        feed_dict={image_tensor: image_np_expanded})
                except:
                    print('error!!!')
                    break

                # extractData(image_np, np.squeeze(boxes), np.squeeze(classes).astype(np.int32), np.squeeze(scores),
                #              category_index, image_container)
                vis_util.visualize_boxes_and_labels_on_image_array(
                    image_np,
                    np.squeeze(boxes),
                    np.squeeze(classes).astype(np.int32),
                    np.squeeze(scores),
                    category_index,
                    use_normalized_coordinates=True,
                    line_thickness=8)
                q.put(image_np)
                cv2.imshow('mahy', image_np)  # 显示
                cv2.waitKey(int(1000 / int(22)))
    global video_end_flag
    video_end_flag = True
    cap.release()

if __name__ == '__main__':
    dealVideo()