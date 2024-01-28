# Best Practice: Multiprocessing

1. `main.py`
```
from multi_tasks import MultiTasks
from setting.bluetooth import Bluetooth
from setting.camera import Camera

import RPi.GPIO as GPIO
import pigpio


servoPin = 17
servo = pigpio.pi()
servo.set_mode(servoPin, pigpio.OUTPUT)
servo.set_PWM_frequency(servoPin, 50)

RPWM = 26	# forward	Physical 37
LPWM = 21	# reverse	Physical 40
R_EN = 19	#                    35
L_EN = 20	#					 38

STOP = 0
FORWARD = 1
BACKWARD = 2
HIGH = 1
LOW = 0

lamda1 = 0.7
lamda2 = 1.3

pwm_r = GPIO.PWM(RPWM, 100)
pwm_l = GPIO.PWM(LPWM, 100)


if __name__ == "__main__":
    multi_tasks = MultiTasks()
    camera = Camera()
    bluetooth = Bluetooth()

    multi_tasks.register(camera.calculate_angle)
    multi_tasks.register(bluetooth.calculate_distance)
    multi_tasks.start()

    try:
        while True:
            # Measure angle and distance in parallel!
            measured_angle, measured_distance = multi_tasks()

            # Control DC Motor!
            if(measured_distance > lamda2): # Forward
                pwm_r.ChangeDutyCycle(20)
                pwm_l.ChangeDutyCycle(0)
            elif(measured_distance < lamda1): # Backward
                pwm_r.ChangeDutyCycle(0)
                pwm_l.ChangeDutyCycle(20)
            else:
                pwm_r.ChangeDutyCycle(0)
                pwm_l.ChangeDutyCycle(0)

            # Control Servo Motor!
            degree_servo = 1300 + measured_angle * 6 
            if(degree_servo < 1500) :
                servo.set_servo_pulsewidth(servoPin, degree_servo)
            elif (degree_servo > 1700 ):
                servo.set_servo_pulsewidth(servoPin, degree_servo)
            else:
                servo.set_servo_pulsewidth(servoPin, 1600)
    except KeyboardInterrupt as e: # Terminate GPIO and Servo Pins Safety!
        multi_tasks.join()
        pwm_r.stop()
        pwm_l.stop()
        GPIO.cleanup()
        servo.set_PWM_dutycycle(servoPin, 0)
        servo.set_PWM_frequency(servoPin, 0)
        servo.stop()
    finally:
        multi_tasks.join()
        pwm_r.stop()
        pwm_l.stop()
        GPIO.cleanup()
        servo.set_PWM_dutycycle(servoPin, 0)
        servo.set_PWM_frequency(servoPin, 0)
        servo.stop()
```

2. `camera.py`
```
import cv2
import numpy as np

class Camera:
    def __init__(
        self, 
        device_idx: int = 0,
        lower: np.ndarray = np.array([ 0, 150, 140]),
        upper: np.ndarray = np.array([50, 255, 255]),
    ):
        self.webcam = cv2.VideoCapture(device_idx)
        self.lower = lower
        self.upper = upper

    def calculate_angle(self) -> float | None:
        _, video = self.webcam_video.read()
        img = cv2.cvtColor(video, cv2.COLOR_BGR2HSV) 
        img_h, img_w, img_c = img.shape  

        mask = cv2.inRange(img, self.lower, self.upper) 
        mask_contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 

        if len(mask_contours) != 0:
            for mask_contour in mask_contours:
                if cv2.contourArea(mask_contour) > 1000:
                    x, y, w, h = cv2.boundingRect(mask_contour)
                    degree = (x + w/2) * 100 / img_w
            return degree
        else:
            return None
```

3. `bluetooth.py`
```
# Refer to `test/shopping_cart/setting/bluetooth.py`
from bleak import BleakScanner
import numpy as np
import asyncio

class Bluetooth:
    def __init__(
        self, 
        target_device = "90:E2:02:9F:D5:E5",
        calibration = 0,
    ):
        self.scanner = BleakScanner()
        self.calibration = calibration
        self.rssi_list = []
        self.distance_list = []
        self.mid = 0
        self.distance = 0
        self.target_device = target_device

    async def calibrate_run(self):
        def detection_callback(device, advertisement_data):
            if device.address == self.target_device:
                rssi = device.rssi
                if(len(self.rssi_list)<10):
                    self.rssi_list.append(rssi)
                    self.mid = np.mean(self.rssi_list)

                elif(len(self.rssi_list)<19):                            
                    if(abs(self.mid-rssi)<=5):
                        self.rssi_list.append(rssi)
                        self.mid = sum(self.rssi_list)/len(self.rssi_list)

                else:
                    self.rssi_list.append(rssi)
                    self.mid = sum(self.rssi_list)/len(self.rssi_list)     
                    if ((len(self.rssi_list)==20) and (self.calibration==0)):
                        self.rssi_list.pop()
                        self.calibration = self.mid
                        print(f"\rcalibrated {self.calibration}")
                print(f"\rRSSI: {rssi}, mid: {self.mid}, list {self.rssi_list}",end="")
                loop = asyncio.get_event_loop()
                loop.create_task(self.scanner.stop())

        self.scanner.register_detection_callback(detection_callback)
        await self.scanner.start()
        await asyncio.sleep(0.2)
        await self.scanner.stop()

    async def calculate_dist(self):
        def detection_callback(device):
            if device.address == self.target_device:
                rssi = device.rssi
                if (self.calibration!=0):
                    if (len(self.distance_list)<3):
                        self.distance_list.append(10**((self.calibration-rssi)/(10*2)))

                    elif(len(self.distance_list)==3):
                        self.distance_list.pop()
                        self.distance_list.insert(0,10**((self.calibration-rssi)/(10*2)))
                        final_distance = np.mean(self.distance_list)
                        print("final distance: ",final_distance)
                        self.distance = final_distance

                loop = asyncio.get_event_loop()
                loop.create_task(self.scanner.stop())

        self.scanner.register_detection_callback(detection_callback)
        await self.scanner.start()
        await asyncio.sleep(0.2)
        await self.scanner.stop()

    def initializing(self):
        while self.calibration == 0:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.calibrate_run())
        while self.distance == 0:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.calculate_dist())

    def calculate_distance(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.calculate_dist())
        return self.distance
```

