import time
import numpy as np
import cv2
 
 
def mopi(src):
    high_pass = src.copy()
    opacity = 50
    high_pass = cv2.bilateralFilter(high_pass, 0, 100, 15)
    high_pass = high_pass - src + 128
    high_pass = cv2.GaussianBlur(high_pass, (3, 3), 0)
    dest = (src + 2*high_pass-256)*opacity/100 + src*(100-opacity)/100
    return dest
 
 
start_time = time.time()
img = cv2.imread("D:\\code\\python\\face\\1.jpg").astype(np.float32)
cv2.imshow('img', img.astype(np.uint8))
out = mopi(img)
# show
cv2.imshow('mopi', out.astype(np.uint8))
print('time: ', time.time() - start_time)
cv2.waitKey(0)