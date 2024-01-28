import RPi.GPIO as GPIO
import pigpio

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

    GPIO.setup(R_EN, GPIO.OUT)
    GPIO.setup(L_EN, GPIO.OUT)
    GPIO.setup(RPWM, GPIO.OUT)
    GPIO.setup(LPWM, GPIO.OUT)

    pwm_r = GPIO.PWM(RPWM, 100)
    pwm_l = GPIO.PWM(LPWM, 100)

    pwm_r.start(0)
    pwm_l.start(0)
	
    return pwm_r, pwm_l


def initializing():
    global object_distance, lamda1, lamda2
    global pwm_r, pwm_l

    pwm_r, pwm_l = pin_init()
    GPIO.output(R_EN, HIGH)
    GPIO.output(L_EN, HIGH)

    object_distance = 1.0
    lamda1 = 0.7
    lamda2 = 1.3
    
    # Return Ture/False according to whether user is in correct location

def keep_distance(return_dict):
    global object_distance, lamda1, lamda2

    gap = abs(return_dict['current_distance'] - object_distance)
    if(gap > lamda1):
        pwm_r.ChangeDutyCycle(40)
        pwm_l.ChangeDutyCycle(0)
    
    elif(gap < lamda2):
        pwm_r.ChangeDutyCycle(0)
        pwm_l.ChangeDutyCycle(40)
    
    else:
        pwm_r.ChangeDutyCycle(0)
        pwm_l.ChangeDutyCycle(0)       
    
def quit():
    pwm_r.stop()
    pwm_l.stop()
    GPIO.cleanup()


