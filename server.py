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
	size = (28, 28)

	gray  = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
	#cv2.imshow('gray', gray)
	#cv2.waitKey(0)

	#thresh = 127
	thresh = 70
	bw = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)[1]

#	cv2.imshow('bw', bw)
#	cv2.waitKey(0)

	smoll_bw = cv2.resize(255-bw, size)
#	cv2.imshow('smoll bw', smoll_bw)
#	cv2.waitKey(0)

	cv2.destroyAllWindows()

	smoll_bw = smoll_bw.flatten() / 255.0
	return smoll_bw


app = Flask(__name__)


@app.route('/', methods = ['GET', 'POST'])
def index():
	if request.method == 'GET':
		return "Hello World!"
	if request.method == 'POST':
		print("processing...")
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
			prediction = str( np.squeeze(prediction) )
			print("Prediction for test image:", prediction)
			return prediction

app.run(port=3000)
