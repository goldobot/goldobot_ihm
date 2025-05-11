# import base modules
import asyncio
import numpy as np

import time

# import modules from sequence directory
from . import positions as pos
from . import recalages
from . import actuators_pneuma
from . import actuators_dyna
from . import robot_config as rc

# objects included in the _sequences_globals of RobotMain class, defined in robot_main.py of goldo_main, are available as global variables
# those objects are used to interact with the robot (send commands, read data)

global_long_speed = 0.6
global_turn_speed = 3.0
global_turn_speed_slow = 1.5
global_debug_action_timeout = 0.5
global_debug_timeout = 2.0
global_T0 = 0.0
global_T = 0.0

global_dyn_prise_k = [-50]
global_dyn_depose_k = [130]

global_goldo_dijkstra = None

class WPNode:
    def __init__(self,_wp):
        self.x = _wp[0]
        self.y = _wp[1]
        self.ngb_dist = {}
        self.enabled = True
    def __str__(self):
        return "x={} y={} ngb_dist={}".format(self.x, self.y, self.ngb_dist)


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
                if not self.wp_graph[v].enabled: dist_uv = 1e7
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
        print ("DEBUG : wpn_k = {}".format(wpn_k))
        wpn = self.wp_graph[wpn_k]
        my_path = [(wpn_k,wpn.x,wpn.y)]
        for cout in range(len(self.keys)):
            wpn_k = self.prev[wpn_k]
            print ("DEBUG : wpn_k = {}".format(wpn_k))
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
        return global_dyn_prise_k.pop()

async def dyn_goto(my_pos):
    global global_goldo_dijkstra
    global global_turn_speed
    global global_long_speed
    x = propulsion.pose.position.x
    y = propulsion.pose.position.y
    dj_src = global_goldo_dijkstra.get_nearest_dijkstra(x, y)
    dj_dst = my_pos
    (dj_dist, dj_prev) = global_goldo_dijkstra.do_dijkstra(dj_src)
    (dj_dist, dj_prev) = global_goldo_dijkstra.do_dijkstra(dj_src)
    dj_path = global_goldo_dijkstra.get_path(dj_dst)
    print()
    print ("dijkstra_dist:")
    for k in global_goldo_dijkstra.keys:
        print (" k={} : dist[k]={} ; prev[k]={}".format(k,dj_dist[k],dj_prev[k]))
    print()
    print ("dijkstra_path({} -> {}):".format(dj_src, dj_dst))
    first = True
    for it in dj_path:
        print (" ({} : ({} , {}))".format(it[0], it[1], it[2]))
        if not first:
            await propulsion.pointTo((it[1], it[2]), global_turn_speed)
            await asyncio.sleep(0.5)
            await propulsion.moveToRetry((it[1], it[2]), global_long_speed)
            await asyncio.sleep(0.5)
        else:
            first = False

async def dyn_preprise(preprise_pos):
    global global_turn_speed
    global global_long_speed

    # recul
    await actuators_dyna.bras_standby()
    await asyncio.sleep(0.2)
    # FIXME : TODO : get direction from 'preprise_pos'
    await propulsion.faceDirection(90, global_turn_speed)
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

def dyn_choix_depose():
    global global_dyn_depose_k
    if len(global_dyn_depose_k) == 0:
        return None
    else:
        return global_dyn_depose_k.pop()

async def dyn_construction_goldo(predepose_pos):
    global global_turn_speed
    global global_debug_action_timeout
    global global_debug_timeout
    global global_T0
    global global_T

    short_timeout = 0.1
    long_timeout = 0.3

    # FIXME : TODO : get direction from 'predepose_pos'
    await propulsion.faceDirection(-90, global_turn_speed)
    await asyncio.sleep(0.2)

    print ("Prise planches")
    await actuators_dyna.ascenseur_soulage()
    await asyncio.sleep(short_timeout)
    await actuators_dyna.soulageur_up()
    await asyncio.sleep(short_timeout)
    await actuators_dyna.pump_on()
    await asyncio.sleep(short_timeout)
    await actuators_dyna.bras_prise_hard()
    await asyncio.sleep(long_timeout)
    #await actuators_dyna.bras_up()
    #await asyncio.sleep(short_timeout)
    await asyncio.sleep(long_timeout)
    
    print ("Approche initiale du site de construction")
    await propulsion.translation(-0.15, 0.15)

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

    while (global_T-global_T0)<85.0:
        preprise_pos = dyn_choix_prise()
        if (preprise_pos == None): break

        await dyn_goto(preprise_pos)
        global_T = time.time()
        if (global_T-global_T0)>85.0: break

        await dyn_preprise(preprise_pos)
        global_T = time.time()
        if (global_T-global_T0)>85.0: break

        predepose_pos = dyn_choix_depose()
        if (predepose_pos == None): break

        await dyn_goto(predepose_pos)
        global_T = time.time()
        if (global_T-global_T0)>85.0: break

        await dyn_construction_goldo(predepose_pos)
        await robot.setScore(robot.score + 4)
        await robot.setScore(robot.score + 8)

        await asyncio.sleep(0.1)
        global_T = time.time()


