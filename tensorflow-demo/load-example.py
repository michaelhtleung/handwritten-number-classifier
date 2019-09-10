import numpy as np
from PIL import Image
import tensorflow as tf

# functions
def processImg(img):
	img = img.convert('L')
	img.thumbnail(size)
	img.save('processed-picture.png')
	img = np.invert(img).ravel()
	return img

with tf.Session() as sess:
	new_saver = tf.train.import_meta_graph('./tensorflow/demo/my_test_model-1000.meta')
	new_saver.restore(sess, tf.train.latest_checkpoint('./'))

	graph = tf.get_default_graph()
	X = graph.get_tensor_by_name("X:0")
	Y = graph.get_tensor_by_name("Y:0")

	# manipulate single image
	size = 28, 28
	#img = Image.open("square-pug.jpeg").convert('L')
	img_list = []

	img = Image.open("./custom_data/num/2-1.png")
	img = processImg(img)
	img_list.append(img)

	img = Image.open("./custom_data/num/3-1.png")
	img = processImg(img)
	img_list.append(img)

	img = Image.open("./custom_data/num/9-1.png")
	img = processImg(img)
	img_list.append(img)

	op_to_restore = graph.get_tensor_by_name("output:0")

	# generate prediction on single image
	for picture in img_list:
		prediction = sess.run(tf.argmax(op_to_restore, 1), feed_dict={X: [picture]})
		print("Prediction for test image:", np.squeeze(prediction))
