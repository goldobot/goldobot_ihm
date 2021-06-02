import sys
import re
import math
import struct
import subprocess
import yaml



def dbg_strat_mod(strat_fname):
    print ("Debug strat file : {}".format(strat_fname))
    try:
        strat_fd = open(strat_fname)
    except:
        print ("No such file or directory: {}".format(strat_fname))
    #strat_yaml = yaml.load(strat_fd)
    strat_yaml = yaml.load(strat_fd,Loader=yaml.FullLoader)
    print (strat_yaml)
    idx=0
    my_x = 0
    my_y = 0
    for act in strat_yaml["dbg_task"]["actions"]:
        act_type = act["type"]
        print ("act {} : {}".format(idx,act_type))
        if act_type == "TRAJ":
            first_wp = True
            for wp in act["param_traj"]["wp"]:
                my_x = wp[0]
                my_y = wp[1]
                print ("  <{:>10.3f} {:>10.3f}>".format(my_x,my_y))
                first_wp = False
        elif act_type == "GOTO_ASTAR":
            wp = act["param_goto_astar"]["target"]
            my_x = wp[0]
            my_y = wp[1]
            print ("  <{:>10.3f} {:>10.3f}>".format(my_x,my_y))
        idx += 1

if __name__ == '__main__':
    #dbg_strat_mod(sys.argv[1])

    strat_fd = open(sys.argv[1],"rt")

    for li in strat_fd:
        w = re.match(r"\s*-? \[(.+),(.+)\]", li)
        if w:
            #print ("BINGO : {} : <x={} ; y={}>".format(li.strip('\n'),w.group(1),w.group(2)))
            li_split = li.split(',')
            my_y = float(w.group(2))
            print ("{}, {:>6.1f}]".format(li_split[0],-my_y))
        else:
            print ("{}".format(li.strip('\n')))

