import numpy as np
#from . import robot_config as rc

def symetrie(pose):
    if isinstance(pose, np.ndarray):
        if pose.shape[0] == 2:
            return np.array([pose[0], -pose[1]])
    return (pose[0], -pose[1], -pose[2])


class Side:
    Unknown = 0
    Green = 1
    Blue = 2


# FIXME : TODO
Resource = {
    "R0-" : ( 0.800, -1.300,  -90.0),
    "R1-" : ( 1.600, -1.300,  -90.0),
    "R2-" : ( 1.800, -0.400,    0.0),
    "R3-" : ( 1.200, -0.350, -180.0),
    "R3+" : ( 1.200,  0.350, -180.0),
    "R2+" : ( 1.800,  0.400,    0.0),
    "R1+" : ( 1.600,  1.300,   90.0),
    "R0+" : ( 0.800,  1.300,   90.0),
    }

# FIXME : TODO
DropPoint = {
    "D0-" : ( 1.200, -1.400,  -90.0),
    "D1-" : ( 1.900, -0.800,    0.0),
    "D2-" : ( 1.200, -0.700,    0.0),
    "D3-" : ( 0.550, -0.250, -180.0),
    "D4"  : ( 1.200,  0.000, -180.0),
    "D5"  : ( 1.900,  0.000,    0.0),
    "D3+" : ( 0.550,  0.250, -180.0),
    "D2+" : ( 1.200,  0.700,    0.0),
    "D1+" : ( 1.900,  0.800,    0.0),
    "D0+" : ( 1.200,  1.400,   90.0),
    }

# FIXME : TODO
DjWayPoint_preprise = {
    -10 : ( 1.600, -1.085,  -90.0), # R1-
    -20 : ( 1.585, -0.400,    0.0), # R2-
    -30 : ( 0.985, -0.350,    0.0), # R3-
    -31 : ( 1.415, -0.350, -180.0), # R3-
     31 : ( 1.415,  0.350, -180.0), # R3+
     30 : ( 0.985,  0.350,    0.0), # R3+
     20 : ( 1.585,  0.400,    0.0), # R2+
     10 : ( 1.600,  1.085,   90.0), # R1+
    }

# FIXME : TODO
DjWayPoint_predepose = {
      1 : ( 0.850,  0.000, -180.0),
      2 : ( 0.935,  0.000,    0.0), # D4
      3 : ( 1.465,  0.000, -180.0), # D4
      4 : ( 1.635,  0.000,    0.0), # D5
   -100 : ( 1.200, -1.135,  -90.0), # D0-
   -110 : ( 1.635, -0.800,    0.0), # D1-
   -120 : ( 1.465, -0.700, -180.0), # D2-
   -121 : ( 0.935, -0.700,    0.0), # D2-
    121 : ( 0.935,  0.700,    0.0), # D2+
    120 : ( 1.465,  0.700, -180.0), # D2+
    110 : ( 1.635,  0.800,    0.0), # D1+
    100 : ( 1.200,  1.135,   90.0), # D0+
    }

# FIXME : TODO
DjWayPoint_start = {
   -200 : ( 0.320, -1.320,    0.0),
    200 : ( 0.320,  1.320,    0.0),
    }

# FIXME : TODO
DjWayPoint_extra = {
   -300 : ( 0.500, -1.075,    0.0),
   -310 : ( 0.800, -1.075,    0.0),
   -320 : ( 1.720, -1.075,    0.0),
   -330 : ( 0.960, -1.000,    0.0),
   -340 : ( 0.700, -1.300,    0.0),
    340 : ( 0.700,  1.300,    0.0),
    330 : ( 0.960,  1.000,    0.0),
    320 : ( 1.720,  1.075,    0.0),
    310 : ( 0.800,  1.075,    0.0),
    300 : ( 0.500,  1.075,    0.0),
    }

DjWayPoint = {}
DjWayPoint.update (DjWayPoint_preprise)
DjWayPoint.update (DjWayPoint_predepose)
DjWayPoint.update (DjWayPoint_start)
DjWayPoint.update (DjWayPoint_extra)

# FIXME : TODO
DjWayPointNet = [
    (    1, -121),
    (    1, -300),
    (    1, -310),
    (    2, -121),
    (    2,  -30),
    (    3,  -20),
    (    4,  -20),
    (    3,  -31),
    (    4,  -31),
    (  -30,  -31),
    (  -20,  -31),
    (  -30, -121),
    ( -330, -121),
    ( -120,  -31),
    ( -110,  -20),
    ( -120,  -20),
    ( -110,  -31),
    ( -110, -120),
    (  -10, -110),
    ( -100, -120),
    (  -10, -100),
    (  -10, -120),
    ( -100, -110),
    ( -300, -310),
    ( -310, -330),
    ( -330, -100),
    ( -330, -110),
    ( -340, -100),
    ( -340, -310),
    ( -340, -300),
    ( -200, -300),
    ( -200, -340),
    ( -310, -100),
    ( -330, -340),

    (   30,  -30),
    (    1,    2),
    (   31,  -31),

    (  330,  340),
    (  310,  100),
    (  200,  340),
    (  200,  300),
    (  340,  300),
    (  340,  310),
    (  340,  100),
    (  330,  110),
    (  330,  100),
    (  310,  330),
    (  300,  310),
    (  100,  110),
    (   10,  120),
    (   10,  100),
    (  100,  120),
    (   10,  110),
    (  110,  120),
    (  110,   31),
    (  120,   20),
    (  110,   20),
    (  120,   31),
    (  330,  121),
    (   30,  121),
    (   20,   31),
    (   30,   31),
    (    4,   31),
    (    3,   31),
    (    4,   20),
    (    3,   20),
    (    2,   30),
    (    2,  121),
    (    1,  310),
    (    1,  300),
    (    1,  121),
    ]

# robot offset : 82 mm

# BLUE : ZONE 1
class BluePoses:
    # Poses de depart
    Start_pose       = (  0.320,  1.320,   0)

    # REAL
    First_grab_wp1   = (  0.510,  1.320,   0)
    First_grab_wp2   = (  0.560,  1.320,   0)
    First_grab_wp3   = (  0.610,  1.320,   0)
    First_grab_wp4   = (  0.660,  1.320,   0)

    First_push       = (  0.980,  1.320,   0)
    First_push_out   = (  1.100,  1.320,   0)

    #First_return_wp  = (  0.200,  1.200,   0)
    #First_return_wp  = (  0.700,  1.300,   0)
    First_return_wp  = (  0.600,  1.300,   0)

    Inter_wp0        = (  0.500,  1.075,   0)
    Inter_wp1        = (  0.800,  1.075,   0)
    Inter_wp2        = (  1.720,  1.075,   0)
    Inter_test_wp    = (  1.100,  0.800,   0)

    Corner_wp        = (  1.850,  1.200, -60)

    #Border_wp1       = (  1.850,  0.630, -90)
    Border_wp1       = (  1.850,  0.650, -90)
    Border_wp1_N     = (  1.850,  1.500, -90)

    #Action1_grab_wp1 = (  1.600,  1.084,  90)
    Action1_grab_wp1 = (  1.605,  1.084,  90)
    Action1_drop_wp1 = (  1.634,  0.800,   0)

    Action2_grab_wp0 = (  1.550,  0.400,   0)
    #Action2_grab_wp1 = (  1.584,  0.400,   0)
    Action2_grab_wp1 = (  1.594,  0.400,   0)
    Action2_drop_wp1 = (  1.441,  0.000,-180)

    Action42_grab_wp0 = (  1.480, -0.350,-180)
    Action42_grab_wp1 = (  1.451, -0.350,-180)
    Action42_drop_wp0 = (  1.100, -0.350,-180)
    Action42_drop_wp1 = (  0.850,  0.000,-180)

    #Action3_grab_wp0 = (  1.480,  0.350,-180)
    ##Action3_grab_wp1 = (  1.441,  0.350,-180)
    #Action3_grab_wp1 = (  1.460,  0.350,-180)
    #Action3_drop_wp1 = (  1.440,  0.700,-180)

    Action3_grab_wp0 = (  0.940,  0.350,   0)
    Action3_grab_wp1 = (  0.960,  0.350,   0)
    Action3_drop_wp1 = (  0.960,  0.700,   0)

    Action3_loot_wp0 = (  0.940, -0.700,   0)
    Action3_loot_wp1 = (  0.960, -0.700,   0)

    #Final_escape_wp0 = (  1.440,  1.000,-180)
    Final_escape_wp0 = (  0.960,  1.000,-180)
    Final_escape_wp1 = (  0.700,  1.300,-180)
    Final_pose_wp    = (  0.300,  1.300,-180)


# YELLOW : ZONE 2
class YellowPoses:
    # Poses de depart
    Start_pose       = symetrie(BluePoses.Start_pose)

    # REAL
    First_grab_wp1   = symetrie(BluePoses.First_grab_wp1)
    First_grab_wp2   = symetrie(BluePoses.First_grab_wp2)
    First_grab_wp3   = symetrie(BluePoses.First_grab_wp3)
    First_grab_wp4   = symetrie(BluePoses.First_grab_wp4)

    First_push       = symetrie(BluePoses.First_push)
    First_push_out   = symetrie(BluePoses.First_push_out)

    First_return_wp  = symetrie(BluePoses.First_return_wp)

    Inter_wp0        = symetrie(BluePoses.Inter_wp0)
    Inter_wp1        = symetrie(BluePoses.Inter_wp1)
    Inter_wp2        = symetrie(BluePoses.Inter_wp2)
    Inter_test_wp    = symetrie(BluePoses.Inter_test_wp)

    Corner_wp        = symetrie(BluePoses.Corner_wp)

    #Border_wp1       = symetrie(BluePoses.Border_wp1)
    Border_wp1       = (  1.850, -0.640, -90)
    Border_wp1_N     = symetrie(BluePoses.Border_wp1_N)

    Action1_grab_wp1 = symetrie(BluePoses.Action1_grab_wp1)
    Action1_drop_wp1 = symetrie(BluePoses.Action1_drop_wp1)

    Action2_grab_wp0 = symetrie(BluePoses.Action2_grab_wp0)
    Action2_grab_wp1 = symetrie(BluePoses.Action2_grab_wp1)
    Action2_drop_wp1 = symetrie(BluePoses.Action2_drop_wp1)

    Action42_grab_wp0 = symetrie(BluePoses.Action42_grab_wp0)
    Action42_grab_wp1 = symetrie(BluePoses.Action42_grab_wp1)
    Action42_drop_wp0 = symetrie(BluePoses.Action42_drop_wp0)
    Action42_drop_wp1 = symetrie(BluePoses.Action42_drop_wp1)

    Action3_grab_wp0 = symetrie(BluePoses.Action3_grab_wp0)
    Action3_grab_wp1 = symetrie(BluePoses.Action3_grab_wp1)
    Action3_drop_wp1 = symetrie(BluePoses.Action3_drop_wp1)

    Action3_loot_wp0 = symetrie(BluePoses.Action3_loot_wp0)
    Action3_loot_wp1 = symetrie(BluePoses.Action3_loot_wp1)

    Final_escape_wp0 = symetrie(BluePoses.Final_escape_wp0)
    Final_escape_wp1 = symetrie(BluePoses.Final_escape_wp1)
    Final_pose_wp    = symetrie(BluePoses.Final_pose_wp)


@robot.sequence
async def print_start_zone():
    print("Start zone : " + str(robot.start_zone))

@robot.sequence
async def led_off():
    await robot.gpioSet('keyboard_led', False)

@robot.sequence
async def led_on():
    await robot.gpioSet('keyboard_led', True)
