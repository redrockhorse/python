import json
import numpy as np
import cv2
from functools import reduce
import base64
import os
import math
from utils import label_map_util
from utils import visualization_utils as vis_util
import tensorflow as tf
import tarfile
import six.moves.urllib as urllib
from queue import Queue
from threading import Thread
#目标检测服务

#global variable
class_dic = {}
size = [256,256]
image_hash_name_arr = []
box_center_arr_pre = []
image_hash_name_arr_pre = []

#解码器
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)

# 差值感知算法
def dHash(img):
    # 缩放8*8
    img = cv2.resize(img, (9, 8))
    # 转换灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hash_str = ''
    # 每行前一个像素大于后一个像素为1，相反为0，生成哈希
    for i in range(8):
        for j in range(8):
            if gray[i, j] > gray[i, j + 1]:
                hash_str = hash_str + '1'
            else:
                hash_str = hash_str + '0'
    return hash_str
#均值哈希算法
def aHash(img):
    #缩放为8*8
    img=cv2.resize(img,(8,8))
    #转换为灰度图
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #s为像素和初值为0，hash_str为hash值初值为''
    s=0
    hash_str=''
    #遍历累加求像素和
    for i in range(8):
        for j in range(8):
            s=s+gray[i,j]
    #求平均灰度
    avg=s/64
    #灰度大于平均值为1相反为0生成图片的hash值
    for i in range(8):
        for j in range(8):
            if  gray[i,j]>avg:
                hash_str=hash_str+'1'
            else:
                hash_str=hash_str+'0'
        if i<7:
            hash_str = hash_str + ' '
    return hash_str

#将8位2进制数解码为2位16进制
def decode(s):
    rs = ''
    for  b in s.split(' '):
        tstr = str(hex(int(b,2)))[2:]
        if len(tstr) < 2:
            tstr ='0'+tstr
        rs = rs + tstr
    return rs

#对比hash值差异
def cmpHash(hash1, hash2):
    n = 0
    # hash长度不同则返回-1代表传参出错
    if len(hash1)!=len(hash2):
        return -1
    # 遍历判断
    for i in range(len(hash1)):
        # 不相等则n计数+1，n最终为相似度
        a = int(hash1[i],16)
        b = int(hash2[i],16)
        c = list(bin(a ^ b)[2:])
        d = reduce(lambda x, y: int(x)+int(y), c)
        n = n + int(d)
    return n
qi =  Queue()
def extractData(image_np,boxes,classes,scores,category_index,images_container,max_boxes_to_draw=20,min_score_thresh=.6,enbale_class =[8,3,6]):
    global image_hash_name_arr
    global box_center_arr_pre
    global image_hash_name_arr_pre
    global class_dic
    global size
    if not max_boxes_to_draw:
        max_boxes_to_draw = boxes.shape[0]
    box_center_arr_now = []
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
    #               ahash_str = dHash(cropImg)
    #               ahash_code = decode(ahash_str)
    #               png_image = cv2.imencode('.png', cropImg)[1]
    #               png_image_code = str(base64.b64encode(png_image))[2:-1]
    #               cropImgCenter = [int((xmax_p-xmin_p)/2+xmin_p),int((ymax_p-ymin_p)/2+ymin_p)]
    #               box_center_arr_now.append(cropImgCenter)
    #               image_hash_name_arr.append(ahash_code)
    #               min_len = min(int(xmax_p-xmin_p),int(ymax_p-ymin_p))
    #               if len(box_center_arr_pre) == 0:
    #                   images_container[ahash_code] = {'class': class_name, 'image': png_image_code,
    #                                                   'score': scores[i]}
    #                   # cv2.imwrite('/Users/hongyanma/gitspace/python/python/data/img/' + ahash_code + '.png',
    #                   #             cropImg)
    #                   #
    #                   # cv2.imshow('Image', cropImg)
    #               for bc in range(len(box_center_arr_pre)):
    #                   bc_point = box_center_arr_pre[bc]
    #                   distance_center = math.sqrt((cropImgCenter[0]-bc_point[0])**2+(cropImgCenter[1]-bc_point[1])**2)
    #                   if distance_center < min_len:#矩形中心距离小 短边，是同一辆车
    #                       if images_container[image_hash_name_arr_pre[bc]]['score'] < scores[i]:
    #                           images_container[image_hash_name_arr_pre[bc]] = {'class': class_name, 'image': png_image_code,
    #                                                   'score': scores[i]}
    #                           # os.remove('/Users/hongyanma/gitspace/python/python/data/img/' + image_hash_name_arr_pre[bc] + '.png')
    #                           # cv2.imwrite('/Users/hongyanma/gitspace/python/python/data/img/' + image_hash_name_arr_pre[bc] + '.png',
    #                           #             cropImg)
    #                           # cv2.imshow('Image', cropImg)
    #                   else:
    #                       images_container[ahash_code] = {'class': class_name, 'image': png_image_code,
    #                                                       'score': scores[i]}
    #                       # cv2.imwrite('/Users/hongyanma/gitspace/python/python/data/img/' + ahash_code + '.png',
    #                       #             cropImg)
    #                       # cv2.imshow('Image', cropImg)
    # box_center_arr_pre = box_center_arr_now
    # image_hash_name_arr_pre = image_hash_name_arr


q = Queue()

video_end_flag = False
def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper
@async
def dealVideo():
    global size
    q.empty()
    '''
        检测视频中的目标
    '''
    cap = cv2.VideoCapture('/Users/hongyanma/gitspace/python/python/data/1.avi')  # 打开摄像头
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    #fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    #fps = cap.get(cv2.CAP_PROP_FPS)
    #videoWriter = cv2.VideoWriter('/Users/hongyanma/gitspace/python/python/data/output.mp4', fourcc, fps, size)

    ##################### Download Model
    # What model to download.
    '''
    MODEL_NAME = 'ssd_inception_v2_coco_11_06_2017'
    MODEL_NAME = 'rfcn_resnet101_coco_11_06_2017'
    MODEL_NAME = 'faster_rcnn_resnet101_coco_11_06_2017'
    MODEL_NAME = 'faster_rcnn_inception_resnet_v2_atrous_coco_11_06_2017'
    '''
    # MODEL_NAME = 'ssd_mobilenet_v1_coco_2017_11_17'
    # MODEL_NAME = 'ssd_resnet'
    MODEL_NAME = 'ssd_mobilenet_v1_coco_2018_01_28'
    MODEL_FILE = MODEL_NAME + '.tar.gz'
    DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'

    # Path to frozen detection graph. This is the actual model that is used for the object detection.
    PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

    # List of the strings that is used to add correct label for each box.
    PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')

    NUM_CLASSES = 90

    # Download model if not already downloaded
    if not os.path.exists(PATH_TO_CKPT):
        print('Downloading model... (This may take over 5 minutes)')
        opener = urllib.request.URLopener()
        opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, MODEL_FILE)
        print('Extracting...')
        tar_file = tarfile.open(MODEL_FILE)
        for file in tar_file.getmembers():
            file_name = os.path.basename(file.name)
            if 'frozen_inference_graph.pb' in file_name:
                tar_file.extract(file, os.getcwd())
    else:
        print('Model already downloaded.')

    ##################### Load a (frozen) Tensorflow model into memory.
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
    #test
    # path = '/Users/hongyanma/gitspace/python/python/data/test.mp4'
    # with open(path, 'rb') as fmp3:
    #     data = fmp3.read(1024)
    #     while data:
    #         data = fmp3.read(1024)
    #         q.put(data)
    #test
    image_container = {}
    #cv2.namedWindow('Image')
    with detection_graph.as_default():
        with tf.Session(graph=detection_graph) as sess:
            while True:
                ret, image_np = cap.read()  # 从摄像头中获取每一帧图像
                #print('aaa')
                #def generate():
                #data = bytes(image_np)
                #yield data
                #q.put(data)
                #print('sss')
                image_np_expanded = np.expand_dims(image_np, axis=0)
                image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
                boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
                scores = detection_graph.get_tensor_by_name('detection_scores:0')
                classes = detection_graph.get_tensor_by_name('detection_classes:0')
                num_detections = detection_graph.get_tensor_by_name('num_detections:0')
                # Actual detection.
                if not ret:
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

                extractData(image_np, np.squeeze(boxes), np.squeeze(classes).astype(np.int32), np.squeeze(scores),
                             category_index, image_container)
                vis_util.visualize_boxes_and_labels_on_image_array(
                    image_np,
                    np.squeeze(boxes),
                    np.squeeze(classes).astype(np.int32),
                    np.squeeze(scores),
                    category_index,
                    use_normalized_coordinates=True,
                    line_thickness=8)
                q.put(image_np)
                # data = bytes(image_np)
                # yield data
                #videoWriter.write(image_np)
    global video_end_flag
    video_end_flag = True
    cap.release()
    #videoWriter.release()
                # cv2.imshow('object detection', cv2.resize(image_np, (size[0], size[1])))
                # if cv2.waitKey(25) & 0xFF == ord('q'):
                #     cv2.destroyAllWindows()
                #     break
            # with open('/Users/hongyanma/gitspace/python/python/data/image_container.json', 'w') as outfile:
            #     json.dump(image_container, outfile, cls=MyEncoder)



import time
# http server  part
from flask import Flask, request,stream_with_context,render_template
app = Flask(__name__)
from flask import Response
@app.route('/test')  # 主页
def testHtml():
    #print('start deal video')
    # jinja2模板，具体格式保存在index.html文件中
    return render_template('test.html')
@app.route('/')  # 主页
def index():
    print('start deal video')
    # jinja2模板，具体格式保存在index.html文件中
    return render_template('index.html')
@app.route('/testVideo')
def stream():
    return Response(dealVideo(), mimetype="video/mpeg4")

def gen():
    #print(q.qsize())
    #global video_end_flag
    while not q.empty():
        image = q.get()
        time.sleep(0.05)
        ret, jpeg = cv2.imencode('.jpg', image)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
def gen_i():
    #print(q.qsize())
    #global video_end_flag
    while not qi.empty():
        image = qi.get()
        time.sleep(1)
        ret, jpeg = cv2.imencode('.jpg', image)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
@app.route('/video_feed')  # 这个地址返回视频流响应
def video_feed():
    if q.empty():
        dealVideo()
        time.sleep(10)
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/pic_feed')  # 这个地址返回视频流响应
def pic_feed():
    #time.sleep(2)
    return Response(gen_i(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/tv')
def tv():
    dealVideo()
    #cap = cv2.VideoCapture('/Users/hongyanma/gitspace/python/python/data/1.avi')
    # def generate():
    #     path = '/Users/hongyanma/gitspace/python/python/data/test.mp4'
    #     with open(path, 'rb') as fmp3:
    #         data = fmp3.read(1024)
    #         while data:
    #             yield data
    #             data = fmp3.read(1024)
    #             print('sss')
    #time.sleep(10)
    def generate():
        #if not q.empty():
        print(q.qsize())
        data = q.get()
        print(type(data))
        while True:
            #print('sss')
            yield data
            data = q.get()
            #print(q.qsize())
    return Response(generate(), mimetype='video/mp4')
    #return Response(stream_with_context(generate()), mimetype='video/mp4')

if __name__ == '__main__':
    #dealVideo()
    app.run(host='0.0.0.0', port=5000)
