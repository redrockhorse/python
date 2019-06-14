import cv2
import argparse
import numpy as np
import os.path as path

#/Users/hongyanma/gitspace/python/python/data/test.mp4
video_path = '/Users/hongyanma/gitspace/python/python/data/test.mp4'
# 获得视频的格式
videoCapture = cv2.VideoCapture(video_path)

# 获得码率及尺寸
fps = videoCapture.get(cv2.CAP_PROP_FPS)
size = (int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
fNUMS = videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
print(size)

# 读帧
success, frame = videoCapture.read()
i =0
while success and i<100:
    cv2.imshow('mahy', frame)  # 显示
    cv2.waitKey(int(1000 / int(fps)))  # 延迟
    success, frame = videoCapture.read()  # 获取下一帧
    i+=1
videoCapture.release()
