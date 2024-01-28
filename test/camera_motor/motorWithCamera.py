from typing import *
import sys
sys.path.append("/usr/local/lib/python3.9/site-packages")
import cv2
import math
import numpy as np
import time
import RPi.GPIO as GPIO
import pigpio
import keyboard

servoPin = 17
RPWM = 26	# forward	Physical 37
LPWM = 21	# reverse	Physical 40
R_EN = 19	#                    35
L_EN = 20	#					 38

STOP = 0
FORWARD = 1
BACKWARD = 2
HIGH = 1
LOW = 0

def pin_init():
	# pin initialization
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    
    servo = pigpio.pi()
    servo.set_mode(servoPin, pigpio.OUTPUT)
    servo.set_PWM_frequency(servoPin, 50)

    GPIO.setup(R_EN, GPIO.OUT)
    GPIO.setup(L_EN, GPIO.OUT)
    GPIO.setup(RPWM, GPIO.OUT)
    GPIO.setup(LPWM, GPIO.OUT)

    pwm_r = GPIO.PWM(RPWM, 100)
    pwm_l = GPIO.PWM(LPWM, 100)

    pwm_r.start(0)
    pwm_l.start(0)
	
    return servo, pwm_r, pwm_l

def view_scope(frame: np.ndarray) -> np.ndarray:
    row, col = frame.shape[:2]
    zero_frame = np.zeros_like(frame.copy())
    pts = np.array( [[0,0], [col,0], [col,row], [0,row]] )
    boundary = cv2.fillConvexPoly( zero_frame.copy(), pts, (255,255,255) )
    return cv2.bitwise_and( frame, boundary )


def detect_lanes(frame: np.ndarray) -> np.ndarray:
    hsv_frame = cv2.cvtColor( frame.copy(), cv2.COLOR_BGR2HSV )
    hsv_blur_frame = cv2.GaussianBlur( hsv_frame, (9,9), 1 )

    def _detect_lane(frame: np.ndarray, lower_color: Tuple[int], upper_color: Tuple[int], threshold: int) -> np.ndarray:
        lower_bound = np.array( lower_color, np.uint8 )
        upper_bound = np.array( upper_color, np.uint8 )
        white_color = cv2.inRange( frame.copy(), lower_bound, upper_bound )
        lane_frame = cv2.bitwise_and( frame.copy(), frame.copy(), mask=white_color )

        lane_frame = cv2.cvtColor(lane_frame, cv2.COLOR_HSV2BGR)
        lane_frame = cv2.cvtColor(lane_frame, cv2.COLOR_BGR2GRAY)
        _, lane_frame = cv2.threshold(lane_frame, threshold, 255, cv2.THRESH_BINARY)
        kernel = np.ones((3,3), dtype= np.uint8)
        dilate = cv2.dilate(lane_frame, kernel, iterations=1)

        return dilate

    yellow_lane_frame = _detect_lane(hsv_blur_frame, (15, 55, 40), (66, 255, 160), 60)
    # white_lane_frame = _detect_lane(hsv_blur_frame, (0, 0, 80), (255, 50, 255), 100)
    black_line_frame = _detect_lane(hsv_blur_frame, (0, 0, 0), (255, 255, 50), 0)

    return cv2.bitwise_or( yellow_lane_frame, black_line_frame )


def _search_point(frame: np.ndarray, lane_frame: np.ndarray, std: int, pre_info: int):
    contours, _ = cv2.findContours(lane_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_angles = []
    for i, cnt in enumerate(contours):
        ys = []
        area = cv2.contourArea(cnt) #contours 영역 구하기
        if area > 40:
            for c in cnt:
                for pos in c:
                    y_pos = pos[1]
                    ys.append(y_pos)
            min_y = min(ys)
            max_y = max(ys)

            min_x = None
            max_x = None
            for c in cnt:
                for pos in c:
                    x_pos = pos[0] + std
                    y_pos = pos[1]
                    if y_pos == min_y:
                        min_x = x_pos
                    elif y_pos == max_y:
                        max_x = x_pos
            if max_x == None:
                max_x = min_x

            diff_x = max_x - min_x
            diff_y = max_y - min_y
            tan_angle = diff_y / diff_x
            angle = math.atan( tan_angle ) * (-180) / math.pi
            contours_angles.append( angle )
            cv2.line(frame, (min_x, min_y), (max_x, max_y), (0, 255, 255), 3 )
            cv2.putText(frame, f"{contours_angles[-1]:.2f}", (min_x+3, min_y), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)

    if len(contours_angles) == 1:
        return contours_angles[-1]
    elif len(contours_angles) == 0:
        return pre_info
    else:
        max_angle = 0
        for angle in contours_angles:
            if max_angle < angle:
                max_angle = angle
        return max_angle


def search_points(frame: np.ndarray, lane_frame: np.ndarray, pre_lanes: List[int]):
    row, col = lane_frame.shape[:2]
    left_lane_frame = lane_frame[:,:int(col/2)]
    right_lane_frame = lane_frame[:,int(col/2):]

    main_left_angle = _search_point(frame, left_lane_frame, 0, pre_lanes[0])
    main_right_angle = _search_point(frame, right_lane_frame, int(col/2), pre_lanes[1])

    # if main_left_angle - main_right_angle < 0:
    #     cv2.putText(frame, f"Right", (10, 40), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
    # elif main_left_angle - main_right_angle > 1:
    #     cv2.putText(frame, f"Left", (10, 40), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
    # else:
    #     cv2.putText(frame, f"Center", (10, 40), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)

    return [ main_left_angle, main_right_angle ]


##############################################################################################################
def controlDC(pwm_r, pwm_l, speed, dir):
    GPIO.output(R_EN, HIGH)
    GPIO.output(L_EN, HIGH)
    if dir == FORWARD:		# 16V 이상
        pwm_r.ChangeDutyCycle(speed)
        pwm_l.ChangeDutyCycle(0)

    elif dir == BACKWARD:
        pwm_r.ChangeDutyCycle(0)
        pwm_l.ChangeDutyCycle(speed)
		
    elif dir == STOP:
        pwm_r.ChangeDutyCycle(0)
        pwm_l.ChangeDutyCycle(0)

def controlServo(angle_L, angle_R, degree):
    if (angle_L == - angle_R):               #잘 가고 있음 
        servo.set_servo_pulsewidth(servoPin, 1600)
        degree = 1600
        return degree
    
    elif (angle_L < 0) :                    #급한 좌회전
        servo.set_servo_pulsewidth(servoPin, 1300)
        degree = 1300
        return degree
        
    elif (angle_R > 0) :                    #급한 우회전
        servo.set_servo_pulsewidth(servoPin, 1900)
        degree = 1900
        return degree
    
    else :
        k=10                                #각도 조절 점진적으로 각도를 조정하도록 함. K값에 따라서 달라지기에 조절해야함.
        angle = (angle_L + angle_R)/2 * k
        degree = degree + angle
        return degree
###################################################################################################        


if __name__ == '__main__':
    
    servo, pwm_r, pwm_l = pin_init()
    speed_max = 100
    speed = speed_max
    degree =1600
    GPIO.output(R_EN, HIGH)
    GPIO.output(L_EN, HIGH)
    #controlDC(pwm_r, pwm_l, speed, FORWARD)
    
    
    window_name = 'Lane detection'
    cv2.namedWindow(window_name)

    path = 'video/road.mp4'
    cap = cv2.VideoCapture(0)

    pre_lanes = [None, None]


    while True:
        ret, frame = cap.read()
        if cv2.waitKey(100) & 0xFF == 27:
            break
        elif not ret:
            cap = cv2.VideoCapture(path)
            ret, frame = cap.read()
        # Scale frame
        row, col = frame.shape[:2]
        cropsize = [int(row*1/2),int(row*3/4),int(col*1/6),int(col*4/5)]
        frame_crop = frame[cropsize[0]:cropsize[1],cropsize[2]:cropsize[3]]

        view_frame = view_scope(frame_crop)
        lanes_frame = detect_lanes(view_frame)
        pre_lanes = search_points(frame_crop, lanes_frame, pre_lanes)       
        
        
        degree = controlServo(pre_lanes[0], pre_lanes[1], degree)       # 방향 제어 
        speed = speed_max - abs(degree-1600)/6                          # 방향제어에 따른 속도 변환 (수치는 맞춰가야할 듯)
        #controlDC(pwm_r, pwm_l, speed, FORWARD) 
        

        lanes_frame = cv2.cvtColor(lanes_frame, cv2.COLOR_GRAY2BGR)
        cv2.putText(frame, f"degree : {degree}, speed:{speed}", (cropsize[2]+10, cropsize[1]-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
        frames = cv2.hconcat( [frame, lanes_frame] )
        
        cv2.imshow(window_name, frames)
        cv2.imshow('d',lanes_frame)






    cap.release()
    cv2.destroyAllWindows()
    print("Finish!")
    
    
    
    
    
    

