def initializing(return_dict):
    import RPi.GPIO as GPIO
    import pigpio
    
    servoPin = 17
    servo = pigpio.pi()
    servo.set_mode(servoPin, pigpio.OUTPUT)
    servo.set_PWM_frequency(servoPin, 50)
    

def keep_degree(return_dict):
    import pigpio
    servoPin =17
    servo = pigpio.pi()
    degree = return_dict["current_degree"]
    degree_servo = degree * 6 + 1300
    
    if(degree_servo)

    servo.set_servo_pulsewidth(servoPin, 1300)

    pass
    

def quit():
    servo.set_PWM_dutycycle(servoPin, 0)
    servo.set_PWM_frequency(servoPin, 0)
    GPIO.cleanup()