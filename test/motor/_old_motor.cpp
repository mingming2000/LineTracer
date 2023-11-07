/**
 * 
 * 컴파일 하는 방법은 g++ -o exe파일로 만들이름 파일명.cpp -lwiringPi -lpthread이다.
실행은 ./(exe파일로 만든이름)을 적어주면 실행이 된다.
motor driver: L298N

*/


#include <wiringPi.h>//wiringPi를 사용하기 위해 헤더를 추가했다.
#include <softPwm.h>//PWM을 사용하기 위해 헤더를 추가했다.
#include <stdio.h>
#include <stdlib.h>
#include <iostream>

#define servo 6
// #define L_M1 0//Left_Motor1 wPi(GEN0번에 연결을 했다.) 왼쪽모터
// #define L_M2 2//Left_Motor2 wPi(GEN2번에 연결을 했다.) 왼쪽모터
// #define R_M1 3//Right_Motor1 wPi(GEN3번에 연결을 했다.)오른쪽 모터
// #define R_M2 1//Right_Motor2 wPi(GEN1번에 연결을 했다.)오른쪽 모터


int main()
{   

    int a = 100;
    a = wiringPiSetup();
    std::cout<< a <<std::endl;

    pinMode(servo,OUTPUT); 
    softPwmCreate(servo, 0 ,200);
    // softPwmCreate(5, 0 ,200);
    // softPwmCreate(4, 0 ,200);

    int time = 1000;

    delay(time); //딜레이를 적당 시간을 줘야 서보가 반응을 한다 더 짧게 줘도 된다.
    softPwmWrite(servo,15);//본인이 사용해본 결과 15가 중앙이고 그이상는 좌측 그이하는 우측을 향해 모터가 돌아갔다. 이건 나만 그런 것 일수 있으니 만약 이 글을 읽고 해보실 분은 수치를 직접 하나씩 넣어보시고 중앙을 찾아주어야 할 것이다.
    printf("1\n");
    delay(time); //딜레이를 적당 시간을 줘야 서보가 반응을 한다 더 짧게 줘도 된다.
    softPwmWrite(servo,20);//본인이 사용해본 결과 15가 중앙이고 그이상는 좌측 그이하는 우측을 향해 모터가 돌아갔다. 이건 나만 그런 것 일수 있으니 만약 이 글을 읽고 해보실 분은 수치를 직접 하나씩 넣어보시고 중앙을 찾아주어야 할 것이다.
    printf("2\n");
    delay(time); //딜레이를 적당 시간을 줘야 서보가 반응을 한다 더 짧게 줘도 된다.
    softPwmWrite(servo,50);//본인이 사용해본 결과 15가 중앙이고 그이상는 좌측 그이하는 우측을 향해 모터가 돌아갔다. 이건 나만 그런 것 일수 있으니 만약 이 글을 읽고 해보실 분은 수치를 직접 하나씩 넣어보시고 중앙을 찾아주어야 할 것이다.
    printf("3\n");
    delay(time); //딜레이를 적당 시간을 줘야 서보가 반응을 한다 더 짧게 줘도 된다.
    // digitalWrite(L_M1,1);
    // digitalWrite(L_M2,0);
    // softPwmWrite(4,180);//1,2,3줄은 좌측모터가 정회전이고 속도를 제어하는 코드이다
    // digitalWrite(R_M1,1);
    // digitalWrite(R_M2,0);
    // softPwmWrite(5,180);//4,5,6줄은 우측모터가 정회전이고 속도를 제어하는 코드이다.
    // delay(time);//time에 해당하는 시간 만큼 모터 두개가 정회전
}