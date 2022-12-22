import cv2
import numpy as np

height = 500
width = 500
img = np.zeros((height,width,3), np.uint8)

#plotting initial three dots
x = np.random.randint(0, 500)
y = np.random.randint(0, 500)

#color = np.random.randint(0,256, size=1)
img[x, y, 0] = 0
img[x, y, 1] = 0
img[x, y, 2] = 255

img[x, y, 0] = 0
img[x, y, 1] = 255
img[x, y, 2] = 255

img[x, y, 0] = 255
img[x, y, 1] = 0
img[x, y, 2] = 255

while True:

    cv2.imshow('Chaos Game',img)

    ch = cv2.waitKey(10)
    if ch == 27:
        break 
