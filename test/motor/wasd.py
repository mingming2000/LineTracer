import RPi.GPIO as GPIO
import pigpio
import time
# import keyboard

servoPin = 12
RPWM = 18	# forward
LPWM = 17	# reverse
R_EN = 23
L_EN = 22

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


servo, pwm_r, pwm_l = pin_init()
GPIO.output(R_EN, HIGH)
GPIO.output(L_EN, HIGH)

print("test starts")

while True:
    #print("while")
    key = input()

    if key == 'q':
    # if keyboard.is_pressed('q'):
        print("q pressed")
        break

    #forward-backward controll
    if key == 'w':
    # if keyboard.is_pressed('w'):
        print("w pressed")
        pwm_r.ChangeDutyCycle(30)
        pwm_l.ChangeDutyCycle(0)
        #dcControl(pwm_r, pwm_l, FORWARD, speed)
    elif key == 's':
    # elif keyboard.is_pressed('s'):
        print("s pressed")
        pwm_r.ChangeDutyCycle(0)
        pwm_l.ChangeDutyCycle(30)
        #dcControl(pwm_r, pwm_l, BACKWARD, speed)
    else:
        pwm_r.ChangeDutyCycle(0)
        pwm_l.ChangeDutyCycle(0)
        #dcControl(pwm_r, pwm_l, STOP, speed)
    
    #left-right controll
    if key == 'a':
    # if keyboard.is_pressed('a'):
        print("a pressed")
        servo.set_servo_pulsewidth(servoPin, 1300)
    elif key == 'd':
        print("d pressed")
        servo.set_servo_pulsewidth(servoPin, 1900)
    else:
        servo.set_servo_pulsewidth(servoPin, 1600)
    time.sleep(0.03)

print("test over")
servo.set_PWM_dutycycle(servoPin, 0)
servo.set_PWM_frequency(servoPin, 0)
pwm_r.stop()
pwm_l.stop()
GPIO.cleanup()