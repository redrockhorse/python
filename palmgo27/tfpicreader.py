__author__ = 'mahone'
import tensorflow as tf
reader = tf.WholeFileReader()
key,value = reader.read(tf.train.string_input_producer(['cat.jpg']))
image0 = tf.image.decode_jpeg(value)
image = tf.expand_dims(image0,0)
image_summary = tf.summary.image('origin image',image)
histogram_summary = tf.summary.histogram('image hist',image)
e = tf.reduce_mean(image)
scalar_summary = tf.summary.scalar('image mean',e)

resized_image = tf.image.resize_images(image,[256,256],method=tf.image.ResizeMethod.AREA)
img_resize_summary = tf.summary.image('image resized',resized_image)
cropped_image = tf.image.crop_to_bounding_box(image0,20,20,256,256)
cropped_image_summary = tf.summary.image('image cropped',tf.expand_dims(cropped_image,0))
flipped_image = tf.image.flip_left_right(image0)
flipped_image_summary = tf.summary.image('image flipped',tf.expand_dims(flipped_image,0))
rotated_image = tf.image.rot0(image0,k=1)
rotated_image_summary = tf.summary.image('image rotated',tf.expand_dims(rotated_image,0))
grayed_image = tf.image.rgb_to_grayscale(image0)
grayed_image_summary = tf.summary.image('image grayed',tf.expand_dims(grayed_image,0))
merged = tf.summary.merge_all()
init_op = tf.initialize_all_variables()
with tf.Session() as sess:
    print(sess.run(init_op))
    cord =  tf.train.Coordinator()
    threads = tf.train.start_queue_runners(coord=cord)
    img = image.eval()
    print(img.shape)
    cord.request_stop()
    cord.join(threads)
    summary_writer = tf.summary.FileWriter('/tmp/tensorboard',sess.graph)
    summary_all = sess.run(merged)
    summary_writer.add_summary(summary_all,0)
    summary_writer.close()



