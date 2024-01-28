# import datetime
# import time
# import pytz

# kst = pytz.timezone('Asia/Seoul')

# def clock():
#     second = str(time.time())
#     second = int(second.split('.')[1])
#     return second

# flag = 0
# while(True):
#     key = input()
#     if(key == 'w' and flag == 0):
#         clk = 0
#         flag = 1
#     if(key == 'q'):
#         print(f"time slice: {clk}")
#         clk = 0
#     clk += 1



import RPi.GPIO as GPIO
import pigpio
import time

servoPin = 17
RPWM = 26    # forward    Physical 37
LPWM = 21    # reverse    Physical 40
R_EN = 19    #                    35
L_EN = 20    #                     38

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

last_timestamp = 0
path = list()
def record_input(key, timestamp):
    global last_timestamp
    global path

    timestamp = int(str(timestamp).split('.')[0])
    if(last_timestamp == 0):
        last_timestamp = timestamp
    path.append((key, timestamp - last_timestamp))
    last_timestamp = timestamp
    return path


servo, pwm_r, pwm_l = pin_init()
GPIO.output(R_EN, HIGH)
GPIO.output(L_EN, HIGH)

print("test starts")

path = list()
key = 'w'
record_mode = False
while True:
    last = key
    key = input()

    if key == 'q':
        servo.set_servo_pulsewidth(servoPin, 1600)
        print("q pressed")
        print(path)
        break

    if key in ['w', 's', 'a', 'd']:
        record_input(key, time.time())

    if key == 'w':
        print("w pressed")
        pwm_r.ChangeDutyCycle(15)
        pwm_l.ChangeDutyCycle(0)
    elif key == 's':
        print("s pressed")
        pwm_r.ChangeDutyCycle(0)
        pwm_l.ChangeDutyCycle(15)
    else:
        # pass
        pwm_r.ChangeDutyCycle(0)
        pwm_l.ChangeDutyCycle(0)

    if key == 'a':
        print("a pressed")
        servo.set_servo_pulsewidth(servoPin, 1300)
        if last == 'w':
            # pass
            pwm_r.ChangeDutyCycle(20)
            pwm_l.ChangeDutyCycle(0)
        elif last == 's':
            # pass
            pwm_l.ChangeDutyCycle(20)
            pwm_r.ChangeDutyCycle(0)
    elif key == 'd':
        print("d pressed")
        servo.set_servo_pulsewidth(servoPin, 1900)
        if last == 'w':
            # pass
            pwm_r.ChangeDutyCycle(20)
            pwm_l.ChangeDutyCycle(0)
        elif last == 's':
            # pass
            pwm_r.ChangeDutyCycle(0)
            pwm_l.ChangeDutyCycle(20)
    else:
        # pass
        servo.set_servo_pulsewidth(servoPin, 1600)
    time.sleep(0.03)

print("test over")

print("Return to original location")

last = key
num = len(path)
for i in range(num-1, -1, -1):
    print("Remaining Step:", i)
    command = path[i]
    key = command[0]

    if key == 'q':
        servo.set_servo_pulsewidth(servoPin, 1600)
        print("q pressed")
        print(path)
        break

    if key == 'w':
        print("w pressed")
        pwm_r.ChangeDutyCycle(15)
        pwm_l.ChangeDutyCycle(0)
    elif key == 's':
        print("s pressed")
        pwm_r.ChangeDutyCycle(0)
        pwm_l.ChangeDutyCycle(15)
    else:
        pass
        pwm_r.ChangeDutyCycle(0)
        pwm_l.ChangeDutyCycle(0)

    if key == 'a':
        print("a pressed")
        servo.set_servo_pulsewidth(servoPin, 1300)
        if last == 'w':
            pass
            pwm_r.ChangeDutyCycle(20)
            pwm_l.ChangeDutyCycle(0)
        elif last == 's':
            pass
            pwm_l.ChangeDutyCycle(20)
            pwm_r.ChangeDutyCycle(0)
    elif key == 'd':
        print("d pressed")
        servo.set_servo_pulsewidth(servoPin, 1900)
        if last == 'w':
            pass
            pwm_r.ChangeDutyCycle(20)
            pwm_l.ChangeDutyCycle(0)
        elif last == 's':
            # pass
            pwm_r.ChangeDutyCycle(0)
            pwm_l.ChangeDutyCycle(20)
    else:
        # pass
        servo.set_servo_pulsewidth(servoPin, 1600)
    time.sleep(command[1])


servo.set_PWM_dutycycle(servoPin, 0)
servo.set_PWM_frequency(servoPin, 0)
pwm_r.stop()
pwm_l.stop()
GPIO.cleanup()

