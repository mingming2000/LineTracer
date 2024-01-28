import RPi.GPIO as GPIO
import pigpio

# servo = pigpio.pi()
# servoPin = 17

# def initializing():
#     global servoPin

#     servoPin = 17
#     servo = pigpio.pi()
#     servo.set_mode(servoPin, pigpio.OUTPUT)
#     servo.set_PWM_frequency(servoPin, 50)
#     return True
    
servoPin = 17
servo = pigpio.pi()
servo.set_mode(servoPin, pigpio.OUTPUT)
servo.set_PWM_frequency(servoPin, 50)


def keep_degree(degree_queue, ):
    # def initializing():
    #     servoPin = 17
    #     servo = pigpio.pi()
    #     servo.set_mode(servoPin, pigpio.OUTPUT)
    #     servo.set_PWM_frequency(servoPin, 50)
    #     return servo, servoPin
    
    # def quit(servo, servoPin) -> None:
    #     print("test entering to quit status")
    #     servo.set_servo_pulsewidth(servoPin,1600)
    #     # servoPin =17
    #     # servo = pigpio.pi()
    #     servo.set_PWM_dutycycle(servoPin, 0)
    #     servo.set_PWM_frequency(servoPin, 0)
    #     servo.stop()
    
    # servoPin =17
    # servo = pigpio.pi()
    
    # servo, servoPin = initializing()
    print(">>>>, keep_degree")

    while(True):
        degree = degree_queue.get()
        print(">>>>", degree)
        degree_servo = 1300 + degree * 6 
            
        if(degree_servo < 1500) :
            servo.set_servo_pulsewidth(servoPin, degree_servo)

        elif (degree_servo > 1700 ):
                servo.set_servo_pulsewidth(servoPin, degree_servo)
        else :
                servo.set_servo_pulsewidth(servoPin, 1600)
    # quit(servo, servoPin)
        

def quit():
    global servo, servoPin
    print("test entering to quit status")
    servo.set_servo_pulsewidth(servoPin,1600)
    # servoPin =17
    # servo = pigpio.pi()
    servo.set_PWM_dutycycle(servoPin, 0)
    servo.set_PWM_frequency(servoPin, 0)
    servo.stop()