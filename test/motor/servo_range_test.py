import RPi.GPIO as GPIO
import pigpio
import time
import keyboard
import numpy as np

servoPin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPin, GPIO.OUT)
servo = pigpio.pi('pi123')
servo.set_mode(servoPin, pigpio.OUTPUT)
servo.set_PWM_frequency(servoPin, 50)

#servo.start    (0)

value = 0
try: 
    for value in np.arange(1300, 1900, 100):
        print(f'value: {value}')
        servo.set_servo_pulsewidth(servoPin, value) # 1600 center
        time.sleep(1)
	#1300~1900 1600




except:
	servo.set_PWM_dutycycle(servo, 0)
	servo.set_PWM_frequency( servo, 0 )

servo.set_PWM_dutycycle( servoPin, 0)
servo.set_PWM_frequency( servoPin, 0)