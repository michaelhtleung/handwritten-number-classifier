''' 
installation instructions:
sudo pip3 install opencv-python
'''

import cv2

# load/read an image from the file system into main memory
image = cv2.imread('rainbow.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
inverse = cv2.bitwise_not(image)
size = (28, 28)
smoll = cv2.resize(image, size)
smoll_gray = cv2.resize(gray, size)

# render the image
cv2.imshow('image', image)
cv2.waitKey(0)

cv2.imshow('gray', gray)
cv2.waitKey(0)

cv2.imshow('inverse', inverse)
cv2.waitKey(0)

cv2.imshow('smoll', smoll)
cv2.waitKey(0)

cv2.imshow('smoll gray', smoll_gray)
cv2.waitKey(0)
# close all windows opened
cv2.destroyAllWindows()

# write the loaded image to the file system
cv2.imwrite('gray.png', gray)
cv2.imwrite('inverse.png', inverse)
cv2.imwrite('smoll.png', smoll)
cv2.imwrite('smoll_gray.png', smoll_gray)
