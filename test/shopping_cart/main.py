import multiprocessing as mp
from setting import degree # 서보모터
from setting import distance
from setting import bluetooth
from setting import camera



# instantiating
state = 'off'
manager = mp.Manager()
return_dict = manager.dict()
dist_queue = mp.Queue()
degree_queue = mp.Queue()



procs = [
    # receive distance info.
    mp.Process(
        target=bluetooth.calculate_distance,
        name="receive distance info.",
        args=(dist_queue,),
        daemon=True
    ),

    #  Detect user by using camera
    mp.Process(
        target=camera.calculate_degree,
        name="Detect user by using camera",
        args=(degree_queue,),
        daemon=True
    ),

    # Manipulate motor
    mp.Process(
        target=distance.keep_distance, 
        name="Manipulate motor",
        args=(dist_queue,),
        daemon=True
    ),

    # Manipulate servo-motor
    mp.Process(
        target=degree.keep_degree,
        name="Manipulate servo-motor",
        args=(degree_queue,),
        daemon=True
    ),
]




# Waiting for user instruction
key_info = '==========================================\nKEY INFORMATION\n\ns : Get information for shopping\nq : Finish shopping\n==========================================\n'
user_instruction = input(key_info)

"""
    'ON' state
"""


if(user_instruction == 's'):
    state = 'on'

    # initial_distance= distance.initializing()
    bluetooth_ready= bluetooth.initializing()
    # user_ready = camera.initializing()
    degree.initializing()





    """
        'Working' State
    """
    if(bluetooth_ready == True):
        state = 'working'

        for p in procs:
            p.start()

        while(True):





            """
                'Quit' State
            """
            user_instruction = input()
            if(user_instruction == 'q'):
                state = 'quit'
                distance.quit()
                # complete the processes
                for p in procs:
                    p.join()

            

