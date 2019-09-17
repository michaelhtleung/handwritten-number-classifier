# Raspberry Pi Handwritten Digit Classifier
## What it does
A machine learning number classifier that recognizes handwritten digits powered by the Raspberry Pi.

The Raspberry Pi photographs images of handwritten digits and sends them to a web server that trains a neural network to classify each image. The neural network's prediction is then displayed on the 7 segment display.

## Video
1. [Raspberry Pi number classifier demonstration](https://www.youtube.com/watch?v=Z3Cs39XH9RQ&list=PLmkl7ubDbpoRxQLwzbyAhze0Nra6oTlvD&index=2&t=0s)

2. [Larson scanner demonstration](https://www.youtube.com/watch?v=gzLvlS6BXd0&list=PLmkl7ubDbpoRxQLwzbyAhze0Nra6oTlvD&index=2)

## Pictures
1. Handwritten digit classifier input image

![](https://github.com/michaelhtleung/rpi-number-classifier/blob/master/media/rpi-input.png)

2. Handwritten digit classifier loading shown with Larson scanner

![](https://github.com/michaelhtleung/rpi-number-classifier/blob/master/media/rpi-loading.png)

3. Handwritten digit classifier output answer

![](https://github.com/michaelhtleung/rpi-number-classifier/blob/master/media/rpi-output.png)

4. Hardware close up

![](https://github.com/michaelhtleung/rpi-number-classifier/blob/master/media/rpi-close-up.JPG)

## Python3 Libraries, Frameworks, and Modules
### Server-side
- OpenCV
- TensorFlow
- Flask
- numpy
- os

### Client-side
- PiCamera
- threading
- requests
- RPi.GPIO 
- os


## Parts List
- Raspberry Pi 3 B+
- Raspberry Pi Camera V2.1
- 7 segment display
- 74HC595 shift register
- potentiometer

## Concepts Applied
- neural networks
- computer vision
- image processing
- multi-threaded programming (to run Larson Scanner)
- webserver communication
- bit shifting 
