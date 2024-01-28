import multiprocessing as mp
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


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    @staticmethod
    def print_blue(text: str):
        print(bcolors.OKBLUE + text + bcolors.ENDC)


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

    return True

def keep_distance(dist_queue: mp.Queue):
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
	
    # pwm_r, pwm_l = pin_init()
    GPIO.output(R_EN, HIGH)
    GPIO.output(L_EN, HIGH)
    
    object_distance = 1.0
    lamda1 = 0.7
    lamda2 = 1.3

    while(True):
        if not dist_queue.empty():
            _cur_distance = dist_queue.get()
            print(f"[Distance-keep_distance] >>> {_cur_distance:.2f}")

            if(_cur_distance is not None):
                # gap = abs(_cur_distance - object_distance)
                # print("gap", gap)
                if(_cur_distance > lamda2):
                    # print("Forward")
                    bcolors.print_blue("Move-Forward")
                    pwm_r.ChangeDutyCycle(20)
                    pwm_l.ChangeDutyCycle(0)
                
                elif(_cur_distance < lamda1):
                    # print("Backward")
                    bcolors.print_blue("Move-Backward")
                    pwm_r.ChangeDutyCycle(0)
                    pwm_l.ChangeDutyCycle(20)
                
                else:
                    pwm_r.ChangeDutyCycle(0)
                    pwm_l.ChangeDutyCycle(0)    
        else:  ###############################################################################
            continue
    pwm_r.stop()
    pwm_l.stop()
    GPIO.cleanup()
            
def quit():
    pwm_r.stop()
    pwm_l.stop()
    GPIO.cleanup()


if __name__ == "__main__":
    test_queue = mp.Queue()
    test_queue.put(1.5)
    try:
        print(test_queue.qsize())
        keep_distance(test_queue)
    except KeyboardInterrupt as e:
        quit()
