# enter ```ssh -R 80:localhost:3000 ssh.localhost.run``` to make local host publically exposed, but
# beware: this isn't a secure connection 
 
from flask import Flask, request
import os

import numpy as np
from PIL import Image
import tensorflow as tf

# dimensions to shrink RPI picture to
size = 28, 28

img_path = "./server-received-capture.jpg"
processed_img_path = './processed-picture.jpg'

# functions
def processImg(img):
	img.thumbnail(size)
	img.save(processed_img_path)
	img = np.invert(img).ravel()
	return img

app = Flask(__name__)


@app.route('/', methods = ['GET', 'POST'])
def index():
	if request.method == 'GET':
		return "Hello World!"
	if request.method == 'POST':
		prediction = ''
		print(request.data)
#		os.remove(img_path)
#		img_fd = os.open(img_path, os.O_WRONLY | os.O_CREAT)
#		os.write(img_fd, (request.data)) 
#		os.close(img_fd)
#
#		with tf.Session() as sess:
#			new_saver = tf.train.import_meta_graph('./tensorflow-demo/my_test_model-1000.meta')
#			new_saver.restore(sess, tf.train.latest_checkpoint('./tensorflow-demo/'))
#
#			graph = tf.get_default_graph()
#			X = graph.get_tensor_by_name("X:0")
#			Y = graph.get_tensor_by_name("Y:0")
#
#			# manipulate single image
#			img = Image.open(img_path).convert('L')
#			img = processImg(img)
#
#			op_to_restore = graph.get_tensor_by_name("output:0")
#
#			# generate prediction on single image
#			prediction = sess.run(tf.argmax(op_to_restore, 1), feed_dict={X: [img]})
#			# print("Prediction for test image:", np.squeeze(prediction))
#			prediction = str( np.squeeze(prediction) )
#			print(prediction)
#			return prediction
		return "8"

app.run(port=3000)
