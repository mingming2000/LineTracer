import multiprocessing as mp

from setting import degree # 서보모터
from setting import distance
from setting import bluetooth
from setting import camera


# instantiating
state = 'off'
# mp_lock = mp.Lock()
# manager = mp.Manager()
# return_dict = manager.dict()
# return_dict = {
#     "current_distance": None,
# }

dist_queue = mp.Queue()

procs = [
    mp.Process(
        target=bluetooth.calculate_distance, 
        name="receive distance info.",
        args=(dist_queue,),
        daemon=True
    ),
    mp.Process(
        target=distance.keep_distance, 
        name="Manipulate motor",
        args=(dist_queue,),
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
    # bluetooth_ready = True
 
    # object_distance = initial_distance

    print("bluetooth_ready: ", bluetooth_ready)

    """
        'Working' State
    """
    if(bluetooth_ready == True):
        state = 'working'
        print("Multi-process: ", state)
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

            

