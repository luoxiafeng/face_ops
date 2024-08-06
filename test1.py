import cv2
import numpy as np

def apply_smooth_skin(image_path):
    image = cv2.imread(image_path)
    # 高斯模糊
    smoothed = cv2.GaussianBlur(image, (15, 15), 0)
    # 双边滤波
    bilateral = cv2.bilateralFilter(image, 15, 75, 75)
    # 将高斯模糊和双边滤波结果融合
    smooth_skin = cv2.addWeighted(smoothed, 0.5, bilateral, 0.5, 0)
    return smooth_skin

# 测试函数
path = "D:\\code\\python\\face\\1.jpg"
# display the image
image = cv2.imread(path)
cv2.imshow('image', image)
smooth_skin_image = apply_smooth_skin(path)
cv2.imwrite('D:\\code\\python\\face\\smooth_skin_image.jpg', smooth_skin_image)
cv2.imshow('smooth_skin_image', smooth_skin_image)
cv2.waitKey(0)
