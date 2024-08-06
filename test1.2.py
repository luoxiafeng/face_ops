# coding=utf-8
import numpy as np
from PIL import Image
import cv2  
import copy
import time




class Beauty():
    """face object"""
    def __init__(self, path, newpath=False):
        self.path = path  # img path
        self.newpath = newpath  # save path
        self.current_img =  cv2.imread(path)
        self.new_img = None
        self.skin_table = None
        current_img = self.current_img

    def generate_skin(self):
        """genrate skin table"""
        rows,cols,channels = self.current_img.shape
        current_img = copy.deepcopy(self.current_img)  # get img data
        current_img = cv2.edgePreservingFilter(current_img, flags=1, sigma_s=50, sigma_r=0.5)
        self.skin_table = np.ones(self.current_img.shape, np.uint8)  # get data is 0 matrix
        #self.skin_table = copy.deepcopy(self.current_img)
        # Skin is identified by pixels
        for r in range(rows):  
            for c in range(cols):  
                # get pixel value         
                B = current_img.item(r,c,0)  
                G = current_img.item(r,c,1)  
                R = current_img.item(r,c,2)  
                # non-skin area if skin equals 0, skin area equals 1.         
                if (abs(R - G) > 15) and (R > G) and (R > B):  
                    if (R > 95) and (G > 40) and (B > 20) and (max(R,G,B) - min(R,G,B) > 15):
                        pass
                    elif (R > 220) and (G > 210) and (B > 170):  
                        pass
                else:
                    self.skin_table.itemset((r,c,2),0)  
                    self.skin_table.itemset((r,c,1),0)
                    self.skin_table.itemset((r,c,0),0)

    def buffing(self, grade=3):
        # first judge skin is exist
        if self.skin_table == None:
            self.generate_skin()
        # buffing
        value = grade * 0.05
        current_img = cv2.edgePreservingFilter(self.current_img, flags=1, sigma_s=50, sigma_r=value)
        imgskin_c = np.uint8(-(self.skin_table - 1))
        skin = current_img * self.skin_table
        cv2.imwrite('skin.jpg', self.current_img * self.skin_table)
        skin = self.white_skin(skin, 8) # 磨皮中插入美白算法
        self.new_img = np.uint8(self.current_img * imgskin_c + skin)
        cv2.imwrite(self.newpath, self.new_img)
    
    def white_skin(self, skin, power=5):
        """
        power : 0 ~ 100
        """
        power = power / 100.0
        rows,cols,channels = skin.shape
        for r in range(rows):  
            for c in range(cols):  
                B = skin.item(r,c,0)  
                G = skin.item(r,c,1)  
                R = skin.item(r,c,2)  
                max_value = max([R, G, B])
                degree = 255 - max_value - int(max_value*power)
                if degree >= 0: degree = int(max_value*power)
                else: degree = 255 - max_value
                skin.itemset((r,c,0), B + degree) 
                skin.itemset((r,c,1), G + degree)
                skin.itemset((r,c,2), R + degree)
        return skin

    def show(self, img="Default"):
        if img == "Default":
            img = self.new_img
        print('正在加载')
        cv2.imshow('image', img)
        cv2.imshow('old', self.current_img)
        #cv2.imwrite('python3.png',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


b = Beauty(path="D:\\code\\python\\face\\1.jpg", newpath='new.jpg')
b.buffing(grade=5)
b.show()
