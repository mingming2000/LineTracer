import asyncio
from bleak import BleakScanner
import numpy as np
import csv
# from ultrasoundsenser import distancebyEcho

#TARGET_DEVICE_ADDRESS = "F0:C7:7F:36:E6:F3" #90:E2:02:9F:D5:E5
TARGET_DEVICE_ADDRESS = "90:E2:02:9F:D5:E5"
mid = 0
distance = 0
distance_list = []
calibration = 0
rssi_list=[] 

# distance, calibration 추가함 - 이주승



async def run():
    # 검색 클래스 생성
    
    scanner = BleakScanner()

    # 장치가 검색되면 호출되는 콜백 함수
    def detection_callback(device, advertisement_data):

        
        if device.address == TARGET_DEVICE_ADDRESS:
            global rssi_list
            global distance
            global distance_list
            global calibration
            global mid
            
            rssi = device.rssi
            if(len(rssi_list)<10):
                rssi_list.append(rssi)
                mid = np.mean(rssi_list)
            
            elif(len(rssi_list)<29):                            
                if(abs(mid-rssi)<=5):
                    rssi_list.append(rssi) # 튀는 rssi값들 제거 - 이주승
                    mid = sum(rssi_list)/len(rssi_list)

            else:
                rssi_list.append(rssi)
                mid = sum(rssi_list)/len(rssi_list)
                print("what's the length..",len(rssi_list))       
                # 20240128에 추가함 - 이주승
                if ((len(rssi_list)==30) and (calibration==0)):
                    rssi_list.pop()
                    calibration= mid
                if (calibration!=0):
                    print("start calibration")
                    distance_list.append(10**((calibration-rssi)/(10*2)))
                if(len(distance_list)==10):
                    final_distance = np.mean(distance_list)
                    print("final distance: ",final_distance)
                # 여기까지 추가함 - 이주승
            print(f"\rRSSI: {rssi}, mid: {mid}, list {rssi_list}",end="")
            loop = asyncio.get_event_loop()
            loop.create_task(scanner.stop())

            
            

    # 콜백 함수 등록
    scanner.register_detection_callback(detection_callback)

    # 검색 시작
    await scanner.start()
    # 원하는 기기를 찾을 때까지 대기 (예: 5초)
    await asyncio.sleep(0.2)
    
    await scanner.stop()

while(1):
    loop = asyncio.get_event_loop()
# 비동기 형태로 run(검색)함수 실행
# 완료될때까지 대기
    loop.run_until_complete(run())

