import cv2
import numpy as np

def initializing():
    lower = np.array([0, 150, 140])
    upper = np.array([50, 255, 255])

    webcam_video = cv2.VideoCapture(0)
    while True:
        success, video = webcam_video.read()
        img = cv2.cvtColor(video, cv2.COLOR_BGR2HSV) 
        img_h, img_w, img_c = img.shape  

        mask = cv2.inRange(img, lower, upper) 
        mask_contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
        
        if len(mask_contours) != 0:
            for mask_contour in mask_contours:
                if cv2.contourArea(mask_contour) > 1000:
                    x, y, w, h = cv2.boundingRect(mask_contour)
                    if (x + w/2 > img_w * 0.4 and x + w/2 < img_w * 0.6):
                        print("camera Ready done")
                        return True

def calculate_degree(degree_queue):

    lower = np.array([0, 150, 140])
    upper = np.array([50, 255, 255])

    webcam_video = cv2.VideoCapture(0)
    while True:
        success, video = webcam_video.read()
        img = cv2.cvtColor(video, cv2.COLOR_BGR2HSV) 
        img_h, img_w, img_c = img.shape  

        mask = cv2.inRange(img, lower, upper) 
        mask_contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
        
        if len(mask_contours) != 0:
            for mask_contour in mask_contours:
                if cv2.contourArea(mask_contour) > 1000:
                    x, y, w, h = cv2.boundingRect(mask_contour)
                    degree = (x + w/2) * 100 / img_w
                    # print(degree)                    

        degree_queue.put(degree)