import time

global_T0 = 0.0

def init_match_time():
    global global_T0
    global_T0 = time.time()

def match_time():
    global global_T0
    global_T = time.time()
    return (global_T - global_T0)


