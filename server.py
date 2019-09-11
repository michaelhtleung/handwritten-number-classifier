# enter ```ssh -R 80:localhost:3000 ssh.localhost.run``` to make local host publically exposed, but
# beware: this isn't a secure connection 
 
from flask import Flask, request
import os

import numpy as np
import cv2
import tensorflow as tf

img_base_path = "./server-received-capture"

img_processed_base_path = './processed-picture'
img_processed_path = img_processed_base_path + ".jpg"

# functions
def processImg(img_path):
	# dimensions to shrink RPI picture to
	size = 28, 28

	image = cv2.imread(img_path)
	cv2.imshow('image', image)
	cv2.waitKey(0)

	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	cv2.imshow('gray', gray)
	cv2.waitKey(0)

	smoll_gray = cv2.resize(gray, size)
	cv2.imshow('smoll gray', smoll_gray)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	
	smoll_gray = np.array( smoll_gray ).flatten()

	return smoll_gray


app = Flask(__name__)


@app.route('/', methods = ['GET', 'POST'])
def index():
	if request.method == 'GET':
		return "Hello World!"
	if request.method == 'POST':
		prediction = ''
		#print(request.data)

		img_path = img_base_path + ".jpg"
		img_fd = os.open(img_path, os.O_WRONLY | os.O_CREAT)
		os.write(img_fd, (request.data)) 
		os.close(img_fd)

		with tf.Session() as sess:
			new_saver = tf.train.import_meta_graph('./tensorflow-demo/my_test_model-1000.meta')
			new_saver.restore(sess, tf.train.latest_checkpoint('./tensorflow-demo/'))

			graph = tf.get_default_graph()
			X = graph.get_tensor_by_name("X:0")
			Y = graph.get_tensor_by_name("Y:0")

			# manipulate single image
			img = processImg(img_path)

			op_to_restore = graph.get_tensor_by_name("output:0")

			# generate prediction on single image
			prediction = sess.run(tf.argmax(op_to_restore, 1), feed_dict={X: [img]})
			# print("Prediction for test image:", np.squeeze(prediction))
			prediction = str( np.squeeze(prediction) )
			print(prediction)
			return prediction

app.run(port=3000)
