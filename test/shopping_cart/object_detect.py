import cv2
import numpy as np

# numpy 배열로 hsv 형식의 색 범위를 정해줍니다.
# 노란색으로 범위를 정해주었습니다.
lower = np.array([0, 150, 140])
upper = np.array([50, 255, 255])

# 카메라를 연결합니다.
webcam_video = cv2.VideoCapture(0)


while True:
 	# 카메라의 프레임을 읽고 가져옵니다.
    success, video = webcam_video.read()
   
   	# RGB 형식의 카메라 프레임을 HSV 형식으로 변환합니다.
    img = cv2.cvtColor(video, cv2.COLOR_BGR2HSV) 
    img_h, img_w, img_c = img.shape  
      
    # 정한 범위 내의 색을 표시해줍니다.
    mask = cv2.inRange(img, lower, upper) 
    
    # 표시된 것에서 윤곽선을 찾습니다.
    mask_contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
    
    # 모든 윤곽선의 위치를 찾습니다.
    if len(mask_contours) != 0:
        for mask_contour in mask_contours:
            if cv2.contourArea(mask_contour) > 1000:
                x, y, w, h = cv2.boundingRect(mask_contour)
                # 사각형을 그려줍니다.
                # cv2.rectangle(video, (x, y), (x + w, y + h), (0, 0, 255), 3) 
                if(x + w/2 > img_w * 0.4 and x + w/2 < img_w * 0.6):
                    print("center")
                elif (x + w/2 < img_w * 0.4):
                    print("left")
                elif (x + w/2 > img_w * 0.6):
                    print("right")
                
    
    cv2.imshow("mask image", mask)
    cv2.imshow("window", video)
    
    # ESC 키를 누르면 프로그램이 종료됩니다.
    if cv2.waitKey(1) & 0xFF == 27:
        break

webcam_video.release()
cv2.destroyAllWindows()