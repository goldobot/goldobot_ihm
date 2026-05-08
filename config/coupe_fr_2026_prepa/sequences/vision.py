import asyncio
import numpy as np

import time

aruco_x_configuration = "0000"
aruco_y_configuration = "0000"

#reference x values:
# 303 -> ref_x1 = 0.303
# 358 -> ref_x2 = 0.358
# 409 -> ref_x3 = 0.409
# 466 -> ref_x4 = 0.466
def aruco_x_detection():
    global aruco_x_configuration

    aruco_x_configuration = "0000"

    ref_x = [0.303, 0.358, 0.409, 0.466]
    segm_ref_x = [0.330, 0.383, 0.438]

    if (robot.start_zone==1):   # BLUE   (Y+,id=36)
        print("my_color = BLUE (id=36)")
        my_color = 36
    elif (robot.start_zone==2): # YELLOW (Y-,id=47)
        print("my_color = YELLOW (id=47)")
        my_color = 47
    else:
        print("No start zone!")
        aruco_x_configuration = "0000"
        return aruco_x_configuration

    detections_file = "/tmp/detections.txt"
    #detections_file = "/tmp/last_good_detections.txt"

    detections = []
    try:
        with open(detections_file) as f:
            for line in f:
                print ("DETECTIONS FILE: {}".format(line)) 
                line = line.strip()
                parts = line.split()
                if len(parts) != 4:
                    continue
                ts_str, my_id_str, x_str, y_str = parts
                ts = float(ts_str)
                my_id = int(my_id_str)
                x_real = float(x_str)/1000.0
                y_real = float(y_str)/1000.0
                if (x_real>(ref_x[0]-0.050)) and (x_real<(ref_x[3]+0.050)) and (y_real>-0.030) and (y_real<0.030):
                    detections.append((ts,my_id,x_real,y_real))
    except:
        print ("Cannot read (and parse) {}".format(detections_file))
        aruco_x_configuration = "0000"
        return aruco_x_configuration

    detections.sort(key=lambda d: d[2])

    pres_idx = []

    for i in range(len(detections)):
        ts, my_id, x_real, y_real = detections[i]
        print ("ts={:.2f} id={:d} x={:6.3f} y={:6.3f}".format(ts, my_id, x_real, y_real))
        if (x_real<segm_ref_x[0]):
            pres_idx.append(0)
        elif (x_real<segm_ref_x[1]):
            pres_idx.append(1)
        elif (x_real<segm_ref_x[2]):
            pres_idx.append(2)
        else:
            pres_idx.append(3)
    print("Present: {}".format(pres_idx))

    if (len(detections)<3 or len(detections)>4):
        print("len(detections)={}".format(len(detections)))
        print("Cannot detect aruco_x_configuration!")
        aruco_x_configuration = "0000"
        return aruco_x_configuration

    if (len(detections)==3):
        miss_idx = None
        miss_color_code = None
        my_color_cnt = 0
        adv_color_cnt = 0
        for i in range(0,4):
            if (i not in pres_idx):
                miss_idx = i
        for i in range(0,3):
            if (detections[i][1]==my_color):
                my_color_cnt = my_color_cnt + 1
            else:
                adv_color_cnt = adv_color_cnt + 1
        print ("miss_idx={}".format(miss_idx))
        print ("my_color_cnt={}".format(my_color_cnt))
        print ("adv_color_cnt={}".format(adv_color_cnt))
        if (my_color_cnt>adv_color_cnt):
            miss_color_code = '0'
        else:
            miss_color_code = '1'
        print ("miss_color_code={}".format(miss_color_code))
        for i in range(0,3):
            if (detections[i][1]==my_color):
                aruco_x_configuration = aruco_x_configuration[:pres_idx[i]] + '1' + aruco_x_configuration[pres_idx[i]+1:]
            print("  STEP {} : {}".format(i,aruco_x_configuration))
        aruco_x_configuration = aruco_x_configuration[:miss_idx] + miss_color_code + aruco_x_configuration[miss_idx+1:]

    elif (len(detections)==4):
        for i in range(0,4):
            if (detections[i][1]==my_color):
                aruco_x_configuration = aruco_x_configuration[:i] + '1' + aruco_x_configuration[i+1:]

    print("aruco_x_configuration = {}".format(aruco_x_configuration))

    return aruco_x_configuration


#reference x values: REF_X = 0.328
# -80 -> ref_y1 = -0.079
# -30 -> ref_y2 = -0.030
#  30 -> ref_y3 =  0.030
#  80 -> ref_y4 =  0.079
def aruco_y_detection():
    global aruco_y_configuration
    REF_X = 0.328
    x_shift = 0.0
    y_shift = 0.0

    aruco_y_configuration = "0000"

    ref_y = [-0.080, -0.030, 0.030, 0.080]
    segm_ref_y = [-0.055, 0.000, 0.055]

    if (robot.start_zone==1):   # BLUE   (Y+,id=36)
        print("my_color = BLUE (id=36)")
        my_color = 36
    elif (robot.start_zone==2): # YELLOW (Y-,id=47)
        print("my_color = YELLOW (id=47)")
        my_color = 47
    else:
        print("No start zone!")
        aruco_y_configuration = "0000"
        return aruco_y_configuration, 0.0, 0.0

    detections_file = "/tmp/detections.txt"
    #detections_file = "/tmp/last_good_detections.txt"

    detections = []
    try:
        with open(detections_file) as f:
            for line in f:
                print ("DETECTIONS FILE: {}".format(line)) 
                line = line.strip()
                parts = line.split()
                if len(parts) != 4:
                    continue
                ts_str, my_id_str, x_str, y_str = parts
                ts = float(ts_str)
                my_id = int(my_id_str)
                x_real = float(x_str)/1000.0
                y_real = float(y_str)/1000.0
                if (x_real>(0.330-0.030)) and (x_real<(0.330+0.030)) and (y_real>(ref_y[0]-0.050)) and (y_real<(ref_y[3]+0.050)):
                    detections.append((ts,my_id,x_real,y_real))
    except:
        print ("Cannot read (and parse) {}".format(detections_file))
        aruco_y_configuration = "0000"
        return aruco_y_configuration, 0.0, 0.0

    detections.sort(key=lambda d: d[3])

    pres_idx = []

    for i in range(len(detections)):
        ts, my_id, x_real, y_real = detections[i]
        print ("ts={:.2f} id={:d} x={:6.3f} y={:6.3f}".format(ts, my_id, x_real, y_real))
        if (y_real<segm_ref_y[0]):
            pres_idx.append(0)
        elif (y_real<segm_ref_y[1]):
            pres_idx.append(1)
        elif (y_real<segm_ref_y[2]):
            pres_idx.append(2)
        else:
            pres_idx.append(3)
    print("Present: {}".format(pres_idx))

    if (len(detections)<3 or len(detections)>4):
        print("len(detections)={}".format(len(detections)))
        print("Cannot detect aruco_y_configuration!")
        aruco_y_configuration = "0000"
        return aruco_y_configuration, 0.0, 0.0

    if (len(detections)==3):
        miss_idx = None
        miss_color_code = None
        my_color_cnt = 0
        adv_color_cnt = 0
        for i in range(0,4):
            if (i not in pres_idx):
                miss_idx = i
        for i in range(0,3):
            if (detections[i][1]==my_color):
                my_color_cnt = my_color_cnt + 1
            else:
                adv_color_cnt = adv_color_cnt + 1
        print ("miss_idx={}".format(miss_idx))
        print ("my_color_cnt={}".format(my_color_cnt))
        print ("adv_color_cnt={}".format(adv_color_cnt))
        if (my_color_cnt>adv_color_cnt):
            miss_color_code = '0'
        else:
            miss_color_code = '1'
        print ("miss_color_code={}".format(miss_color_code))
        x_sum = 0.0
        y_sum = 0.0
        for i in range(0,3):
            ts, my_id, x_real, y_real = detections[i]
            x_sum += x_real
            if (my_id==my_color):
                aruco_y_configuration = aruco_y_configuration[:pres_idx[i]] + '1' + aruco_y_configuration[pres_idx[i]+1:]
            print("  STEP {} : {}".format(i,aruco_y_configuration))
        aruco_y_configuration = aruco_y_configuration[:miss_idx] + miss_color_code + aruco_y_configuration[miss_idx+1:]
        x_shift = x_sum/3 - REF_X
        if (miss_idx==1) or (miss_idx==2):
            y_shift = (detections[0][3] + detections[2][3])/2
        elif (miss_idx==0):
            y_shift = (detections[0][3] + detections[1][3])/2
        elif (miss_idx==3):
            y_shift = (detections[1][3] + detections[2][3])/2

    elif (len(detections)==4):
        x_sum = 0.0
        y_sum = 0.0
        for i in range(0,4):
            ts, my_id, x_real, y_real = detections[i]
            x_sum += x_real
            y_sum += y_real
            if (my_id==my_color):
                aruco_y_configuration = aruco_y_configuration[:i] + '1' + aruco_y_configuration[i+1:]
        x_shift = x_sum/4 - REF_X
        y_shift = y_sum/4

    print("aruco_y_configuration = {}".format(aruco_y_configuration))
    print("x_shift = {}".format(x_shift))
    print("y_shift = {}".format(y_shift))

    return aruco_y_configuration, x_shift, y_shift

