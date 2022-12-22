import numpy as np
import imageio.v2 as imageio
import skimage
import cv2
import matplotlib.pyplot as plt
import seaborn as sns
from skimage import color  # another package for HSV-RGB

imfile = '/Users/nanditakothari/Desktop/Sogang 22-2/Visual Media/Color rotation/porcu.jpeg'

im = imageio.imread(imfile)  # read in an image file
hsv_src = skimage.img_as_ubyte(color.rgb2hsv(im))  # rgb -> hsv -> hsv256
shifted = hsv_src.copy()                           # destination
step = 1 # hue step
recorder = cv2.VideoWriter("porcu.mp4", 
                                cv2.VideoWriter_fourcc(*'MP4V'),10,
                                (640, 640))

for i in range(510):  # repeat many times
    # shifted[:,200:,0] = (hsv_src[:,200:,0] + i*step) % 256  # change Hue channel
    shifted[:,:,0] = (hsv_src[:,:,0] + i*step) % 256  # change Hue channel, cyclic
    shifted_rgb = color.hsv2rgb(shifted)              # hsv -> rgb, don't forget
    shifted_rgb = shifted_rgb[:,:,::-1]               # RGB -> BGR for cv2 interface
    shifted_rgb = skimage.img_as_ubyte(shifted_rgb)   # BGR 256 uint8 type
    cv2.putText(shifted_rgb,                          # draw a text, PIL also provides this function.
                f'{i*step:3}', 
                org=(20,im.shape[0]), 
                fontFace=cv2.FONT_HERSHEY_PLAIN, 
                fontScale=5, 
                color=(220,220,0), 
                thickness=4)
    cv2.imshow("window",shifted_rgb)      # display image in the window
    recorder.write(shifted_rgb)
    if cv2.waitKey(10) == 27: break      # if ESC pressed? then stop

recorder.release()
cv2.destroyAllWindows()                  # kill the display window
