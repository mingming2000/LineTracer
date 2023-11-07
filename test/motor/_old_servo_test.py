import RPi.GPIO as GPIO # 라즈베리파이 GPIO 핀을 쓰기위해 임포트
import time # 시간 간격으로 제어하기 위해 임포트

def servoMotor(pin, degree, t):
    GPIO.setmode(GPIO.BCM) # 핀의 번호를 보드 기준으로 설정, BCM은 GPIO 번호로 호출함
    GPIO.setup(pin, GPIO.OUT) # GPIO 통신할 핀 설정
    pwm=GPIO.PWM(pin, 50) # 서보모터는 PWM을 이용해야됨. 12번핀을 50Hz 주기로 설정

    pwm.start(0) # 초기 시작값, 반드시 입력해야됨
    time.sleep(t) # 초기 시작값으로 이동하고 싶지 않으면 이 라인을 삭제하면 된다.
    # for cnt in range(0,3):
    #     pwm.ChangeDutyCycle(5.0) # 0도
    #     time.sleep(5.0)
    #     pwm.ChangeDutyCycle(7.5) # 90도
    #     time.sleep(5.0)
    #     pwm.ChangeDutyCycle(12.5) # 180도
    #     time.sleep(5.0)
    for t in range(7, 12):
        pwm.ChangeDutyCycle(t)
        print(f"DutyCycle: {t}")
        time.sleep(5.0)
    # time.sleep(5.0)

    # 아래 두줄로 깨끗하게 정리해줘야 다음번 실행할때 런타임 에러가 안남
    pwm.stop()
    GPIO.cleanup(pin)

servoMotor(12, 90, 1) # 신호선을 16번 핀에 연결, 8의 각도로 1초동안 실행