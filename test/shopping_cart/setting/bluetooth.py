import multiprocessing as mp

import asyncio
from bleak import BleakScanner
import numpy as np
TARGET_DEVICE_ADDRESS = "90:E2:02:9F:D5:E5"
mid = 0
distance = 0
distance_list = []
calibration = 0
rssi_list=[] 

async def calibrate_run():
    # 1m에 해당하는 데시벨 값 얻기
    
    scanner = BleakScanner()
    def detection_callback(device, advertisement_data):
        if device.address == TARGET_DEVICE_ADDRESS:
            global rssi_list
            global calibration
            global mid
            
            rssi = device.rssi
            if(len(rssi_list)<10):
                rssi_list.append(rssi)
                mid = np.mean(rssi_list)
            
            elif(len(rssi_list)<19):                            
                if(abs(mid-rssi)<=5):
                    rssi_list.append(rssi) # 튀는 rssi값들 제거 - 이주승
                    mid = sum(rssi_list)/len(rssi_list)

            else:
                rssi_list.append(rssi)
                mid = sum(rssi_list)/len(rssi_list)     
                # 20240128에 추가함 - 이주승
                if ((len(rssi_list)==20) and (calibration==0)):
                    rssi_list.pop()
                    calibration = mid
                    print(f"\rcalibrated {calibration}")
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


async def calculate_dist():
    # 새롭게 받아온 rssi값을 이용해서 최종 distance 계산
    
    scanner = BleakScanner()

    # 장치가 검색되면 호출되는 콜백 함수
    def detection_callback(device, advertisement_data):
        global distance
        global distance_list
        global calibration
        if device.address == TARGET_DEVICE_ADDRESS:
            
            rssi = device.rssi
            if (calibration!=0):
                if (len(distance_list)<3):
                    distance_list.append(10**((calibration-rssi)/(10*2)))

                elif(len(distance_list)==3):
                    distance_list.pop()
                    distance_list.insert(0,10**((calibration-rssi)/(10*2)))
                    final_distance = np.mean(distance_list)
                    print("final distance: ",final_distance)
                    distance = final_distance

                    # 여기까지 추가함 - 이주승
            loop = asyncio.get_event_loop()
            loop.create_task(scanner.stop())
            
            

    # 콜백 함수 등록
    scanner.register_detection_callback(detection_callback)

    # 검색 시작
    await scanner.start()
    # 원하는 기기를 찾을 때까지 대기 (예: 5초)
    await asyncio.sleep(0.2)
    
    await scanner.stop()



def initializing():
    while(calibration==0):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(calibrate_run())
    while(distance==0):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(calculate_dist())
    # Return True if detecting user works.
    # Return User degree
    # return_dict['initial_distance'] = distance
    print("Bluetooth initializing done")
    return True


def calculate_distance(dist_queue: mp.Queue):
    while(True):
        # print("calculate_distance")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(calculate_dist())
        # print("current_distance", distance)
        
        dist_queue.put(distance)
        print(f"[Bluetooth-calculate_distance] >>> {distance:.2f}")

