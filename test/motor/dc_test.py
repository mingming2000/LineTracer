import RPi.GPIO as GPIO
import time

RPWM = 18	# forward	Physical 12
LPWM = 17	# reverse	Physical 11
R_EN = 23	#                    16
L_EN = 22	#					 15

STOP = 0
FORWARD = 1
BACKWARD = 2

HIGH = 1
LOW = 0

def pin_init():
	# pin initialization
	GPIO.setup(R_EN, GPIO.OUT)
	GPIO.setup(L_EN, GPIO.OUT)
	GPIO.setup(RPWM, GPIO.OUT)
	GPIO.setup(LPWM, GPIO.OUT)


	pwm_r = GPIO.PWM(RPWM, 100)
	pwm_l = GPIO.PWM(LPWM, 100)

	pwm_r.start(0)
	pwm_l.start(0)
	
	return pwm_r, pwm_l

def setMotorControl(pwm_r, pwm_l, speed, stat):
	GPIO.output(R_EN, HIGH)
	GPIO.output(L_EN, HIGH)
	
	
	if stat == FORWARD:		# 16V 이상
		pwm_r.ChangeDutyCycle(speed)
		pwm_l.ChangeDutyCycle(0)
		
	elif stat == BACKWARD:
		pwm_r.ChangeDutyCycle(0)
		pwm_l.ChangeDutyCycle(speed)
		
	elif stat == STOP:
		pwm_r.ChangeDutyCycle(0)
		pwm_l.ChangeDutyCycle(0)
		
# ~ GPIO.cleanup()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

pwm_r, pwm_l = pin_init()

print("forward for 10 seconds")
setMotorControl(pwm_r, pwm_l, 20, FORWARD)
# setMotorControl(pwm_r, pwm_l, 10, FORWARD)		# For Testing
for i in range(10):
	print(i+1)
	time.sleep(1)

setMotorControl(pwm_r, pwm_l, 0, STOP)
time.sleep(0.5)

print("\nbackward for 10 seconds")
setMotorControl(pwm_r, pwm_l, 30, BACKWARD)
# setMotorControl(pwm_r, pwm_l, 10, BACKWARD)		# For Testing
for i in range(10):
	print(i+1)
	time.sleep(1)

print("\nstop for 10 seconds")
setMotorControl(pwm_r, pwm_l, 40, STOP)
for i in range(10):
	print(i+1)
	time.sleep(1)

print("test over")
GPIO.cleanup()
