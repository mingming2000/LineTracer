import multiprocessing as mp
from setting import degree
from setting import distance
from setting import bluetooth
from setting import camera



# instantiating
state = 'off'
manager = mp.Manager()
return_dict = manager.dict()

procs = [
    # receive distance info.
    mp.Process(
        target=bluetooth.calculate_distance, 
        args=(),
        daemon=True),

    #  Detect user by using camera
    mp.Process(
        target=camera.calculate_degree,
        args=(),
        daemon=True),

    # Manipulate motor
    mp.Process(
        target=distance.keep_distance, 
        args=(return_dict),
        daemon=True),

    # Manipulate servo-motor
    mp.Process(
        target=degree.keep_degree,
        args=(return_dict),
        daemon=True)
]




# Waiting for user instruction
key_info = '==========================================\nKEY INFORMATION\n\ns : Get information for shopping\nq : Finish shopping\n==========================================\n'
user_instruction = input(key_info)

"""
    'ON' state
"""


if(user_instruction == 's'):
    state = 'on'

    bluetooth_ready, initial_distance = distance.initializing()
    user_ready = bluetooth.initializing()

    object_distance = initial_distance





    """
        'Working' State
    """
    if(bluetooth_ready == 'True' and user_ready == 'True'):
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
                # complete the processes
                for p in procs:
                    p.join()

            

