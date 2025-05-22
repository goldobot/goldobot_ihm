# import base modules
import asyncio
import numpy as np
import copy
import time

# import modules from sequence directory
from . import positions as pos
from . import recalages
from . import actuators_pneuma
from . import actuators_dyna
from . import robot_config as rc

# objects included in the _sequences_globals of RobotMain class, defined in robot_main.py of goldo_main, are available as global variables
# those objects are used to interact with the robot (send commands, read data)

global_long_speed = 0.65
global_turn_speed = 3.2
global_turn_speed_slow = 1.5
global_debug_action_timeout = 0.2
global_debug_timeout = 2.0
global_T0 = 0.0
global_T = 0.0

global_dyn_prise_k = [-50,30]
global_dyn_depose_k = [130,110,-100]

global_goldo_dijkstra = None

global_danger_threshold = 0.5
global_danger_factor    = 10.0


def compute_dist(p0, p1):
    delta_x = p1[1] - p0[1]
    delta_y = p1[2] - p0[2]
    return np.sqrt(delta_x*delta_x + delta_y*delta_y)

def compute_angle(p0, p1, p2):
    delta_x0 = p1[1] - p0[1]
    delta_y0 = p1[2] - p0[2]
    delta_x1 = p1[1] - p2[1]
    delta_y1 = p1[2] - p2[2]

    dot_prod = delta_x0*delta_x1 + delta_y0*delta_y1
    mod_v0   = np.sqrt(delta_x0*delta_x0 + delta_y0*delta_y0)
    mod_v1   = np.sqrt(delta_x1*delta_x1 + delta_y1*delta_y1)

    return 180.0*(np.arccos(dot_prod/(mod_v0*mod_v1))/np.pi)

class WPNode:
    def __init__(self,_wp):
        self.x = _wp[0]
        self.y = _wp[1]
        self.ngb_dist = {}
        self.enabled = True
        self.extra_cost = 0
        self.preprise = False
        self.prise_faite = False
        self.predepose = False
        self.depose_faite = False
        self.preempt_depose_k = None
    def __str__(self):
        return "x={} y={} preprise={} predepose={} preempt_depose_k={} ngb_dist={}".format(self.x, self.y, self.preprise, self.predepose, self.preempt_depose_k, self.ngb_dist)


class GoldoDijkstra:
    def __init__(self, node_dico, edge_list):
        self.wp_graph = {k:WPNode(node_dico[k]) for k in node_dico.keys()}
        for edge in edge_list:
            wp0 = node_dico[edge[0]]
            wp1 = node_dico[edge[1]]
            delta_x = wp1[0] - wp0[0]
            delta_y = wp1[1] - wp0[1]
            dist = np.sqrt(delta_x*delta_x + delta_y*delta_y)
            self.wp_graph[edge[0]].ngb_dist[edge[1]] = dist
            self.wp_graph[edge[1]].ngb_dist[edge[0]] = dist
        self.keys = self.wp_graph.keys()

        self.reset()

    def reset(self):
        self.dist = {}
        self.prev = {}
        self.sptSet = {}
        for k in self.keys:
            self.dist[k] = 1e9
            self.prev[k] = None
            self.sptSet[k] = False
        self.src = None

    def compute_min_key(self):
        my_min = 2e9
        min_key = None
        for k in self.keys:
            if self.dist[k] < my_min and self.sptSet[k] == False:
                my_min = self.dist[k]
                min_key = k
        return min_key

    def do_dijkstra(self, src):
        self.reset()
        self.dist[src] = 0
        self.src = src

        for cout in range(len(self.keys)):
            u = self.compute_min_key()
            self.sptSet[u] = True
            for v in self.wp_graph[u].ngb_dist.keys():
                dist_uv = self.wp_graph[u].ngb_dist[v]
                # FIXME : DEBUG : EXPERIMENTAL
                #if not self.wp_graph[v].enabled: dist_uv = 1e7
                dist_uv = dist_uv + self.wp_graph[v].extra_cost
                if (self.sptSet[v]==False) and (self.dist[v] > self.dist[u] + dist_uv):
                    self.dist[v] = self.dist[u] + dist_uv
                    self.prev[v] = u
    
        return self.dist, self.prev
    
    def get_path(self, dst):
        if self.src==None:
            print ("DEBUG : (self.src==None)")
            return []
        if dst not in self.keys:
            print ("DEBUG : (dst not in self.keys)")
            return []
        wpn_k = dst
        #print ("DEBUG : wpn_k = {}".format(wpn_k))
        wpn = self.wp_graph[wpn_k]
        my_path = [(wpn_k,wpn.x,wpn.y)]
        for cout in range(len(self.keys)):
            wpn_k = self.prev[wpn_k]
            #print ("DEBUG : wpn_k = {}".format(wpn_k))
            if (wpn_k==None):
                # "src" was found in the previous iteration..
                # FIXME : TODO : check that the "src" node is indeed present in the path!..
                my_path.reverse()
                return my_path
            wpn = self.wp_graph[wpn_k]
            my_path.append((wpn_k,wpn.x,wpn.y))
        # something went wrong!..
        print ("DEBUG : something went wrong!..")
        return []

    def get_nearest_dijkstra(self, x, y):
        min_dist = 1e9
        min_k = None
        for k in self.keys:
            delta_x = self.wp_graph[k].x - x
            delta_y = self.wp_graph[k].y - y
            dist = np.sqrt(delta_x*delta_x + delta_y*delta_y)
            if dist < min_dist:
                min_dist = dist
                min_k = k
        return min_k


def dyn_choix_prise():
    global global_dyn_prise_k
    if len(global_dyn_prise_k) == 0:
        return None
    else:
        return global_dyn_prise_k.pop(0)


async def dyn_goto(my_pos):
    print ("******************************************************")
    print ("* dyn_goto({})".format(my_pos))
    print ("******************************************************")
    global global_goldo_dijkstra
    global global_turn_speed
    global global_long_speed
    global global_danger_threshold
    global global_danger_factor

    x = propulsion.pose.position.x
    y = propulsion.pose.position.y
    dj_src = global_goldo_dijkstra.get_nearest_dijkstra(x, y)
    dj_dst = my_pos

    # FIXME : DEBUG : EXPERIMENTAL
    detections = lidar.getDetections()
    if (len(detections)>0):
        first_det = detections[0]
        print ("Lidar detections : ")
        print (first_det)
        for k in global_goldo_dijkstra.keys:
            p0 = (-1, first_det.x, first_det.y)
            p1 = (k, global_goldo_dijkstra.wp_graph[k].x, global_goldo_dijkstra.wp_graph[k].y)
            dist = compute_dist(p0, p1)
            if (dist<global_danger_threshold):
                extra_cost = global_danger_factor*(global_danger_threshold-dist)
            else:
                extra_cost = 0.0
            print (" k={} dist={} extra_cost={}".format(k,dist,extra_cost))
            global_goldo_dijkstra.wp_graph[k].extra_cost = extra_cost
    else:
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print ("! No detections!")
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
 
    # FIXME : DEBUG : EXPERIMENTAL
    global_goldo_dijkstra.wp_graph[-220].extra_cost = 20.0
    global_goldo_dijkstra.wp_graph[-210].extra_cost = 20.0
    global_goldo_dijkstra.wp_graph[-200].extra_cost = 20.0
    global_goldo_dijkstra.wp_graph[ 220].extra_cost = 20.0
    global_goldo_dijkstra.wp_graph[ 210].extra_cost = 20.0
    global_goldo_dijkstra.wp_graph[ 200].extra_cost = 20.0
    global_goldo_dijkstra.wp_graph[-21].extra_cost = 10.0
    global_goldo_dijkstra.wp_graph[-20].extra_cost = 10.0
    global_goldo_dijkstra.wp_graph[ 20].extra_cost = 10.0
    global_goldo_dijkstra.wp_graph[-21].extra_cost = 10.0
    global_goldo_dijkstra.wp_graph[1].extra_cost = 0.5
    global_goldo_dijkstra.wp_graph[2].extra_cost = 0.5
    global_goldo_dijkstra.wp_graph[3].extra_cost = 0.5

    (dj_dist, dj_prev) = global_goldo_dijkstra.do_dijkstra(dj_src)
    dj_path = global_goldo_dijkstra.get_path(dj_dst)
    print()
    print ("dijkstra_dist:")
    for k in global_goldo_dijkstra.keys:
        print (" k={} : dist[k]={} ; prev[k]={}".format(k,dj_dist[k],dj_prev[k]))
    print()
    print ("dijkstra_path({} -> {}):".format(dj_src, dj_dst))

    robot_pose = (0, propulsion.pose.position.x, propulsion.pose.position.y)
    robot_dist = compute_dist(robot_pose, dj_path[0])
    print ("robot_dist = {}".format(robot_dist))
    if (robot_dist<0.1):
        dj_path[0] = robot_pose
    else:
        dj_path.insert(0,robot_pose)

    print ("First iteration:")
    # Get rid of unnecessary way points
    dj_path_1 = []
    path_len = len (dj_path)
    for i in range(0,path_len):
        it = dj_path[i]
        print (" ({} : ({} , {}))".format(it[0], it[1], it[2]))
        if (i!=0) and (i!=(path_len-1)):
            prev_it = dj_path[i-1]
            next_it = dj_path[i+1]
            angle = compute_angle(prev_it, it, next_it)
            print ("  angle = {}".format(angle))
            if (angle<179.0):
                dj_path_1.append(it)
        else:
            dj_path_1.append(it)

    print ("Second iteration:")
    # Split the global path into 'dynamically feasible sub-paths'
    dj_supra_path = []
    path_len_1 = len (dj_path_1)
    dj_sub_path = []
    for i in range(0,path_len_1):
        it = dj_path_1[i]
        print (" ({} : ({} , {}))".format(it[0], it[1], it[2]))
        if (i!=0) and (i!=(path_len_1-1)):
            prev_it = dj_path_1[i-1]
            next_it = dj_path_1[i+1]
            angle = compute_angle(prev_it, it, next_it)
            print ("  angle = {}".format(angle))
            if (angle>110.0):
                dj_sub_path.append(it)
            else:
                dj_sub_path.append(it)
                new_subpath = copy.deepcopy(dj_sub_path)
                dj_supra_path.append(new_subpath)
                dj_sub_path = [it]
        else:
            dj_sub_path.append(it)
    new_subpath = copy.deepcopy(dj_sub_path)
    dj_supra_path.append(new_subpath)
    dj_sub_path = []

    if (len(dj_supra_path)>1) and (len(dj_supra_path[0])==1) and (compute_dist(robot_pose, dj_supra_path[0][0])<0.1):
        del(dj_supra_path[0])

    print ("dj_supra_path = {}".format(dj_supra_path))

    # FIXME : DEBUG
    #await asyncio.sleep(10.0)

    for path in dj_supra_path:
        if (len(path)==0):
            print ("WTF!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        elif (len(path)==1):
            # Only one segment in path : point to the destination & execute a straight line..
            it = path[0]
            await propulsion.pointTo((it[1], it[2]), global_turn_speed)
            await asyncio.sleep(global_debug_action_timeout)
            await propulsion.moveToRetry((it[1], it[2]), global_long_speed)
            await asyncio.sleep(global_debug_action_timeout)
        else:
            # Multiple segments : try to execute a "spline"..
            # First thing to do : ensure that the trajectory starts with the current robot pose!
            it = path[0]
            robot_pose = (0, propulsion.pose.position.x, propulsion.pose.position.y)
            robot_dist = compute_dist(robot_pose, it)
            if (robot_dist>0.1):
                path.insert(0,robot_pose)
            else:
                path[0] = robot_pose

            action_traj = []
            for it in path:
                action_traj.append((it[1], it[2], 0))

            # Add intermediate way points to "force" the spline closer to the original "Dijkstra segments"
            action_traj_1 = [action_traj[0]]
            traj_len = len (action_traj)
            for i in range(1,traj_len):
                x0 = action_traj[i-1][0]
                y0 = action_traj[i-1][1]
                x1 = action_traj[i][0]
                y1 = action_traj[i][1]
                delta_x = x1 - x0
                delta_y = y1 - y0
                dist = np.sqrt(delta_x*delta_x + delta_y*delta_y)
                if (dist>0.2):
                    ix0 = x0 + (x1-x0)*0.1/dist
                    iy0 = y0 + (y1-y0)*0.1/dist
                    action_traj_1.append((ix0,iy0,0))
                    ix1 = x0 + (x1-x0)*(dist-0.1)/dist
                    iy1 = y0 + (y1-y0)*(dist-0.1)/dist
                    action_traj_1.append((ix1,iy1,0))
                action_traj_1.append((x1, y1, 0))

            # Do the moving..
            await propulsion.pointTo((action_traj_1[1][0], action_traj_1[1][1]), global_turn_speed)
            await asyncio.sleep(global_debug_action_timeout)
            try:
                await propulsion.trajectorySpline(action_traj_1, speed=global_long_speed)
            except Exception as e:
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print("    propulsion.trajectorySpline() EXCEPTION !")
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print("  DISABLE DETECTION")
                await asyncio.sleep(0.2)
                propulsion.adversary_detection_enable = False
                #print("  WAIT 10s..")
                #await asyncio.sleep(10.0)
                print("  RESTART..")
                print("  PROPULSION DISABLE/ENABLE (to clear error)")
                await propulsion.setEnable(False)
                await asyncio.sleep(0.2)
                await propulsion.setEnable(True)
                await asyncio.sleep(0.2)
                await propulsion.setMotorsEnable(True)
                await asyncio.sleep(0.2)
                print("  re-clear error")
                await propulsion.clearError()
                await asyncio.sleep(0.2)
                #await asyncio.sleep(10.0)
                print("  TEST TRANSLATION..")
                await propulsion.translation(-0.05, 0.15)
                await asyncio.sleep(1.0)
                #await asyncio.sleep(3600.0)
                print(" DYN_GOTO FAIL !")
                return False
            #await asyncio.sleep(global_debug_action_timeout)
            await asyncio.sleep(1.0)

            # FIXME : DEBUG
            # "fragmentary" execution ..
            #for it in action_traj_1[1:]:
            #    await propulsion.pointTo((it[0], it[1]), global_turn_speed)
            #    await asyncio.sleep(global_debug_action_timeout)
            #    try:
            #        await propulsion.moveTo((it[0], it[1]), global_long_speed)
            #    except Exception as e:
            #        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            #        print("    propulsion.moveTo() EXCEPTION !")
            #        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            #        print("  DISABLE DETECTION")
            #        await asyncio.sleep(0.2)
            #        #robot._adversary_detection_enable = False
            #        propulsion.adversary_detection_enable = False
            #        #await propulsion.setMotorsEnable(False)
            #        #await asyncio.sleep(0.2)
            #        print("  WAIT 10s..")
            #        await asyncio.sleep(10.0)
            #        print("  RESTART..")
            #        print("  PROPULSION DISABLE/ENABLE (to clear error)")
            #        await propulsion.setEnable(False)
            #        await asyncio.sleep(0.2)
            #        await propulsion.setEnable(True)
            #        await asyncio.sleep(0.2)
            #        await propulsion.setMotorsEnable(True)
            #        await asyncio.sleep(0.2)
            #        await asyncio.sleep(1.0)
            #        print("  re-clear error")
            #        #await odrive.clearErrors()
            #        await propulsion.clearError()
            #        await asyncio.sleep(10.0)
            #        print("  TEST TRANSLATION..")
            #        await propulsion.translation(-0.05, 0.15)
            #        await asyncio.sleep(1.0)
            #        #await asyncio.sleep(3600.0)
            #        return False
            #    await asyncio.sleep(global_debug_action_timeout)
            #await asyncio.sleep(global_debug_action_timeout)
            #await asyncio.sleep(1.0)

    print(" DYN_GOTO OK !")
    return True


async def dyn_preprise(preprise_pos):
    global global_turn_speed
    global global_long_speed

    # recul
    await actuators_dyna.bras_standby()
    await asyncio.sleep(0.2)
    # FIXME : TODO : get direction from 'preprise_pos' object..
    if preprise_pos in [-50,-40]:
        await propulsion.faceDirection(90, global_turn_speed)
    elif preprise_pos in [40,50]:
        await propulsion.faceDirection(-90, global_turn_speed)
    elif preprise_pos in [-30,-21,21,30]:
        await propulsion.faceDirection(0, global_turn_speed)
    elif preprise_pos in [-20,-10,10,20]:
        await propulsion.faceDirection(180, global_turn_speed)
    await asyncio.sleep(0.2)
    await actuators_pneuma.ventouses_ext_attrape()
    await asyncio.sleep(0.2)
    await actuators_pneuma.ventouses_int_attrape()
    await asyncio.sleep(0.2)
    await propulsion.translation(-0.10, 0.2)
    await asyncio.sleep(0.2)
    await actuators_dyna.ascenseur_soulage()
    await asyncio.sleep(0.2)
    await asyncio.sleep(1.0)

    # wooble..
    # FIXME : TODO : get behaviour from 'preprise_pos' object..
    if preprise_pos in [-50,-40,40,50]:
        if robot.side == pos.Side.Yellow:
            await propulsion.faceDirection(95, 1.0)
            await asyncio.sleep(0.2)
            await propulsion.faceDirection(85, 1.0)
            await asyncio.sleep(0.2)
            await propulsion.faceDirection(90, 1.0)
            await asyncio.sleep(0.2)
        elif robot.side == pos.Side.Blue:
            await propulsion.faceDirection(-95, 1.0)
            await asyncio.sleep(0.2)
            await propulsion.faceDirection(-85, 1.0)
            await asyncio.sleep(0.2)
            await propulsion.faceDirection(-90, 1.0)
            await asyncio.sleep(0.2)

    # verrouillage planches
    await actuators_dyna.soulageur_up()
    await actuators_dyna.bras_prise_hard()
    await asyncio.sleep(0.2)
    await actuators_dyna.pump_on()
    await asyncio.sleep(0.2)
    await actuators_dyna.bras_transport()
    await asyncio.sleep(0.2)
    await actuators_dyna.soulageur_transport()
    await asyncio.sleep(0.2)
    await propulsion.translation(0.10, 0.2)
    await asyncio.sleep(1.0)

    return True


def dyn_choix_depose():
    global global_dyn_depose_k
    if len(global_dyn_depose_k) == 0:
        return None
    else:
        return global_dyn_depose_k.pop(0)


async def dyn_construction_goldo(predepose_pos):
    global global_turn_speed
    global global_debug_action_timeout
    global global_debug_timeout
    global global_T0
    global global_T

    short_timeout = 0.1
    long_timeout = 0.3

    # FIXME : TODO : get direction from 'predepose_pos'
    if predepose_pos in [-140,-130]:
        await propulsion.faceDirection( 90, global_turn_speed)
    elif predepose_pos in [140,130]:
        await propulsion.faceDirection(-90, global_turn_speed)
    elif preprise_pos in [-100,-110,-120,-150,150,120,110,100]:
        await propulsion.faceDirection(180, global_turn_speed)
    await asyncio.sleep(0.2)

    print ("Prise planches")
    await actuators_dyna.ascenseur_soulage()
    await asyncio.sleep(short_timeout)
    #await actuators_dyna.soulageur_up()
    #await asyncio.sleep(short_timeout)
    await actuators_dyna.pump_off()
    await asyncio.sleep(short_timeout)
    await actuators_dyna.bras_up()
    await asyncio.sleep(short_timeout)
    await actuators_dyna.soulageur_transport()
    await asyncio.sleep(short_timeout)
    await actuators_dyna.soulageur_up()
    await asyncio.sleep(short_timeout)
    await actuators_dyna.soulageur_transport()
    await asyncio.sleep(short_timeout)
    await actuators_dyna.pump_on()
    await actuators_dyna.pump_on()
    await asyncio.sleep(short_timeout)
    await actuators_dyna.bras_prise_hard()
    await asyncio.sleep(short_timeout)
    await actuators_dyna.soulageur_up()
    await asyncio.sleep(short_timeout)
    #await actuators_dyna.bras_up()
    #await asyncio.sleep(short_timeout)
    await asyncio.sleep(long_timeout)
    
    print ("Approche initiale du site de construction")
    await propulsion.translation(-0.15, 0.15)
    await asyncio.sleep(long_timeout)

    print ("Construction niveau 1")
    await actuators_pneuma.ecarteur_on()
    await asyncio.sleep(short_timeout)
    await actuators_dyna.bras_standby()
    await asyncio.sleep(short_timeout)
    await actuators_pneuma.ventouses_int_lache()
    await asyncio.sleep(short_timeout)
    await actuators_pneuma.ventouses_int_attrape()
    await asyncio.sleep(short_timeout)
    await actuators_pneuma.ventouses_int_lache()
    await asyncio.sleep(short_timeout)
    await actuators_pneuma.ventouses_int_attrape()
    await asyncio.sleep(short_timeout)
    await actuators_pneuma.ventouses_int_lache()
    await asyncio.sleep(short_timeout)
    await actuators_pneuma.ventouses_int_lache()
    await asyncio.sleep(short_timeout)
    await actuators_dyna.ascenseur_down()
    await asyncio.sleep(short_timeout)
    await actuators_dyna.soulageur_down()
    await asyncio.sleep(short_timeout)
    await asyncio.sleep(long_timeout)

    print ("Translation")
    await propulsion.translation(0.08, 0.15)
    await asyncio.sleep(short_timeout)
    await actuators_pneuma.ecarteur_off()
    await asyncio.sleep(short_timeout)
    await asyncio.sleep(long_timeout)

    print ("Construction niveau 2")
    await actuators_dyna.ascenseur_stage2_high()
    await asyncio.sleep(long_timeout)
    await propulsion.translation(-0.10, 0.15)
    await asyncio.sleep(short_timeout)
    await actuators_dyna.bras_prise()
    await asyncio.sleep(short_timeout)
    await actuators_dyna.ascenseur_stage2_depose()
    await asyncio.sleep(short_timeout)
    await actuators_dyna.pump_off()
    await asyncio.sleep(short_timeout)
    await actuators_pneuma.ventouses_ext_lache()
    await asyncio.sleep(short_timeout)
    await asyncio.sleep(long_timeout)

    print ("Fin")
    await propulsion.translation(0.17, 0.15)
    await asyncio.sleep(short_timeout)
    await actuators_dyna.bras_standby()
    await asyncio.sleep(short_timeout)
    await actuators_dyna.ascenseur_standby()
    await asyncio.sleep(short_timeout)

    return True


@robot.sequence
async def dyn_action4():
    global global_goldo_dijkstra
    global global_turn_speed
    global global_debug_action_timeout
    global global_debug_timeout
    global global_T0
    global global_T

    await actuators_dyna.ascenseur_down()
    await asyncio.sleep(global_debug_action_timeout)
    await actuators_dyna.ascenseur_disable()

    # deplacement vers la zone d'attente finale
    if robot.side == pos.Side.Yellow:
        await dyn_goto(-50)
    elif robot.side == pos.Side.Blue:
        await dyn_goto(50)

    await actuators_dyna.pump_off()
    await actuators_pneuma.reset_valves()
    await actuators_pneuma.purge()

    await propulsion.faceDirection(180, global_turn_speed)
    await asyncio.sleep(0.2)

    print ("******************************************************")
    print ("* Attente finale")
    print ("******************************************************")
    # attente finale
    global_T = time.time()
    while (global_T-global_T0)<92.0:
        await asyncio.sleep(1.0)
        global_T = time.time()

    # deplacement final
    if robot.side == pos.Side.Yellow:
        poses = pos.YellowPoses
    elif robot.side == pos.Side.Blue:
        poses = pos.BluePoses

    await propulsion.moveToRetry(poses.Act4_final, global_long_speed)
    await robot.setScore(robot.score + 10)
    await asyncio.sleep(0.2)


@robot.sequence
async def dyn_strat():
    global global_goldo_dijkstra
    global global_turn_speed
    global global_debug_action_timeout
    global global_debug_timeout
    global global_T0
    global global_T

    global_T0 = time.time()
    global_T = global_T0

    global_goldo_dijkstra = GoldoDijkstra(pos.DjWayPoint, pos.DjWayPointNet)
    print()
    print ("GoldoDijkstra:")
    for k in global_goldo_dijkstra.keys:
        print (" k={}".format(k))

    action_ok = True
    while (global_T-global_T0)<85.0:
        preprise_pos = dyn_choix_prise()
        if (preprise_pos == None): break

        action_ok = await dyn_goto(preprise_pos)
        if not action_ok:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("    dyn_goto(preprise_pos) FAIL !")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            continue
        global_T = time.time()
        if (global_T-global_T0)>85.0: break

        await dyn_preprise(preprise_pos)
        global_T = time.time()
        if (global_T-global_T0)>85.0: break

        predepose_pos = dyn_choix_depose()
        if (predepose_pos == None): break

        action_ok = await dyn_goto(predepose_pos)
        if not action_ok:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("    dyn_goto(predepose_pos) FAIL !")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            continue
        global_T = time.time()
        if (global_T-global_T0)>85.0: break

        await dyn_construction_goldo(predepose_pos)
        await robot.setScore(robot.score + 4)
        await robot.setScore(robot.score + 8)

        await asyncio.sleep(0.1)
        global_T = time.time()


