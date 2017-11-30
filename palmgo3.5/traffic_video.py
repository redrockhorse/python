__author__ = 'mahy'
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": "E:\\ImageMagick-6.2.7-Q16\\convert.exe"})
import imageio
from moviepy.editor import *
import  tensorflow as tf
from PIL import Image
from matplotlib import pyplot as plt
import numpy as np
import os
from utils import label_map_util
from utils import visualization_utils as vis_util

IMAGE_SIZE = (12, 8)
NUM_CLASSES = 90
#video_dir ="E:\\ctfo\\tensorflow\\palm\\data\\t.mp4"
video_dir ="E:\\ctfo\\tensorflow\\palm\\data\\gaosu.mp4"
model_dir = "E:\\ctfo\\tensorflow\\palm\\data\\frozen_inference_graph.pb"
#out_video_dir="E:\\ctfo\\tensorflow\\palm\\data\\object.mp4"
out_video_dir="E:\\ctfo\\tensorflow\\palm\\data\\gs.mp4"
data_dir = "E:\\ctfo\\tensorflow\\palm\\data\\"

def invert_green_blue(image):
    return image[:,:,[0,2,1]]

def scroll(get_frame, t):
    """
    This function returns a 'region' of the current frame.
    The position of this region depends on the time.
    """
    frame = get_frame(t)
    frame_region = frame[int(t):int(t)+120,:]
    return frame_region
def videoClip(star,end):
    # Load myHolidays.mp4 and select the subclip 00:00:50 - 00:00:60
    #clip = VideoFileClip(video_dir).subclip(1,9)
    clip = VideoFileClip(video_dir).subclip(1,15)
    #modifiedClip = clip.fl_image( invert_green_blue )
    #modifiedClip = clip.fl( scroll )
    #my_frame = clip.get_frame(3)

    for i in range(15):
        imgname = data_dir +str(i)+".jpg"
        clip.save_frame(imgname,t=i*1)
        save_image_name = data_dir+"c" +str(i)+".jpg"
        filtr = lambda im: object_detection(imgname, save_image_name)
        clip.fl_image(filtr)


    # Reduce the audio volume (volume x 0.8)
    #clip = clip.volumex(0.8)


    # Generate a text clip. You can customize the font, color, etc.
    #txt_clip = TextClip("My Holidays 2013",fontsize=70,color='white',font="Amiri-Bold",)

    # Say that you want it to appear 10s at the center of the screen
    #txt_clip = txt_clip.set_pos('center').set_duration(10)

    # Overlay the text clip on the first video clip
    #video = CompositeVideoClip([modifiedClip])

    # Write the result to a file (many options available !)
    #video.write_videofile(out_video_dir)
    clip.write_videofile(out_video_dir)
def load_image_into_numpy_array(image):
  #print(image)
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)

PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

def object_detection(image_path,save_image_name):
    with tf.Graph().as_default() as detection_graph:
        output_graph_def = tf.GraphDef()
        output_graph_path = model_dir
        with open(output_graph_path, "rb") as f:
            output_graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(output_graph_def, name="")
            with tf.Session() as sess:
              image = Image.open(image_path)
              # the array based representation of the image will be used later in order to prepare the
              # result image with boxes and labels on it.
              image_np = load_image_into_numpy_array(image)
              # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
              image_np_expanded = np.expand_dims(image_np, axis=0)
              image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
              # Each box represents a part of the image where a particular object was detected.
              boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
              # Each score represent how level of confidence for each of the objects.
              # Score is shown on the result image, together with the class label.
              scores = detection_graph.get_tensor_by_name('detection_scores:0')
              classes = detection_graph.get_tensor_by_name('detection_classes:0')
              num_detections = detection_graph.get_tensor_by_name('num_detections:0')
              # Actual detection.
              (boxes, scores, classes, num_detections) = sess.run(
                  [boxes, scores, classes, num_detections],
                  feed_dict={image_tensor: image_np_expanded})
              # Visualization of the results of a detection.
              vis_util.visualize_boxes_and_labels_on_image_array(
                  image_np,
                  np.squeeze(boxes),
                  np.squeeze(classes).astype(np.int32),
                  np.squeeze(scores),
                  category_index,
                  use_normalized_coordinates=True,
                  line_thickness=8)
              plt.figure(figsize=IMAGE_SIZE)
              plt.imshow(image_np)
              plt.savefig(save_image_name)
              return image_np
              #plt.show()


'''
detection_graph = tf.Graph.as_default()
output_graph_def = tf.GraphDef()
output_graph_path = model_dir
f=open(output_graph_path, "rb")
output_graph_def.ParseFromString(f.read())
_ = tf.import_graph_def(output_graph_def, name="")
sess = tf.Session()
'''
with tf.Graph().as_default() as detection_graph:
    output_graph_def = tf.GraphDef()
    output_graph_path = model_dir
    with open(output_graph_path, "rb") as f:
        output_graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(output_graph_def, name="")
        with tf.Session() as sess:
            def detect_object(image):
                image_pil = Image.fromarray(np.uint8(image)).convert('RGB')
                image_np = load_image_into_numpy_array(image_pil)
                image_np_expanded = np.expand_dims(image_np, axis=0)
                image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
                # Each box represents a part of the image where a particular object was detected.
                boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
                # Each score represent how level of confidence for each of the objects.
                # Score is shown on the result image, together with the class label.
                scores = detection_graph.get_tensor_by_name('detection_scores:0')
                classes = detection_graph.get_tensor_by_name('detection_classes:0')
                num_detections = detection_graph.get_tensor_by_name('num_detections:0')
                # Actual detection.
                (boxes, scores, classes, num_detections) = sess.run(
                        [boxes, scores, classes, num_detections],
                        feed_dict={image_tensor: image_np_expanded})
                # Visualization of the results of a detection.
                vis_util.visualize_boxes_and_labels_on_image_array(
                              image_np,
                              np.squeeze(boxes),
                              np.squeeze(classes).astype(np.int32),
                              np.squeeze(scores),
                              category_index,
                              use_normalized_coordinates=True,
                              line_thickness=8)
                return image_np

def object_detect_from_vedio():
    clip = VideoFileClip(video_dir)
    clip_blurred = clip.fl_image( detect_object )
    clip_blurred.write_videofile(out_video_dir)
'''
def object_detection():
    print('sss')
'''
if __name__ == "__main__":
    #videoClip(10,20)
    object_detect_from_vedio()

f.close()
sess.close()
