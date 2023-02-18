import struct
import math
import os
from numpy import arange


def normalize_angle(theta_rad):
    while theta_rad>math.pi:
        theta_rad -= 2.0*math.pi
    while theta_rad<=-math.pi:
        theta_rad += 2.0*math.pi
    return theta_rad

def recompute_plot_xy(plot_l,dx,dy,dtheta):
    for pl in plot_l:
        pl.x = pl.raw_R * math.cos (pl.raw_theta + pl.odo_theta + dtheta) + pl.odo_x + dx;
        pl.y = pl.raw_R * math.sin (pl.raw_theta + pl.odo_theta + dtheta) + pl.odo_y + dy;

def get_corner(plot_l,min_x,min_y,max_x,max_y,ref_x,ref_y):
    min_corner_score = 1.0
    corner_x = -1000
    corner_y = -1000
    corner_theta = 0
    corner_i = 0

    i = 0
    for pl in plot_l:
        my_x = pl.x
        my_y = pl.y
        my_theta = pl.raw_theta

        if (my_x>min_x) and (my_x<max_x) and (my_y>min_y) and (my_y<max_y):
            dx = my_x - ref_x
            dy = my_y - ref_y
            corner_score = abs(dx)+abs(dy)
            if corner_score<min_corner_score:
                min_corner_score = corner_score
                corner_i = i
                corner_x = my_x
                corner_y = my_y
                corner_theta = my_theta

        i = i + 1

    return (min_corner_score,corner_i,corner_x,corner_y,corner_theta)

def process_plots(plot_l):
    (min_corner1_score,corner1_i,corner1_x,corner1_y,corner1_theta) = get_corner(plot_l,1.9,-1.6,2.2,-1.3,1.9,-1.3)
    (min_corner2_score,corner2_i,corner2_x,corner2_y,corner2_theta) = get_corner(plot_l,-0.2,-0.15,0.1,0.15,0.1,-0.15)
    (min_corner3_score,corner3_i,corner3_x,corner3_y,corner3_theta) = get_corner(plot_l,-0.2,-0.15,0.1,0.15,0.1,0.15)
    (min_corner4_score,corner4_i,corner4_x,corner4_y,corner4_theta) = get_corner(plot_l,1.9,1.3,2.2,1.6,1.9,1.3)

    N1 = 0
    N2 = 0
    N3 = 0
    N4 = 0
    N5 = 0
    N6 = 0
    N7 = 0
    for pl in plot_l:
        my_x = pl.x
        my_y = pl.y

        pl.dbg_i = 0

        if (my_x>1.9) and (my_x<2.2) and (my_y>-1.6) and (my_y<-1.3):
            if normalize_angle(pl.raw_theta-corner1_theta)<0:
                pl.dbg_i = 1
                N1 = N1 + 1
            else:
                pl.dbg_i = 4
                N2 = N2 + 1

        if (my_x>-0.2) and (my_x<0.1) and (my_y>-0.15) and (my_y<0.15):
            if normalize_angle(pl.raw_theta-corner2_theta)<0:
                if normalize_angle(pl.raw_theta-corner3_theta)<0:
                    pl.dbg_i = 7
                    N5 = N5 + 1
                else:
                    pl.dbg_i = 2
                    N6 = N6 + 1
            else:
                pl.dbg_i = 5
                N7 = N7 + 1

        if (my_x>1.9) and (my_x<2.2) and (my_y>1.3) and (my_y<1.6):
            if normalize_angle(pl.raw_theta-corner4_theta)<0:
                pl.dbg_i = 3
                N3 = N3 + 1
            else:
                pl.dbg_i = 6
                N4 = N4 + 1

    if (min_corner1_score<0.999):
        plot_l[corner1_i].dbg_i = 10
    if (min_corner2_score<0.999):
        plot_l[corner2_i].dbg_i = 20
    if (min_corner3_score<0.999):
        plot_l[corner3_i].dbg_i = 30
    if (min_corner4_score<0.999):
        plot_l[corner4_i].dbg_i = 40

    #if (N1!=0) or (N2!=0) or (N3!=0) or (N4!=0) or (N5!=0) or (N6!=0) or (N7!=0):
    #    print(N1, N2, N3, N4, N5, N6, N7)
    #    new_l = plot_l.copy()
    #    s0 = get_global_score(new_l)
    #    print ("s0 = {}".format(s0))

    return (N1, N2, N3, N4, N5, N6, N7)

def get_plot_score(pl):
    s = 0
    if (pl.dbg_i == 1) or (pl.dbg_i == 10):
        s = abs (pl.x - (2.023))
    elif (pl.dbg_i == 2):
        s = abs (pl.x - (-0.023))
    elif (pl.dbg_i == 3):
        s = abs (pl.y - (1.400))
    elif (pl.dbg_i == 4):
        s = abs (pl.y - (-1.400))
    elif (pl.dbg_i == 5) or (pl.dbg_i == 20):
        s = abs (pl.y - (-0.050))
    elif (pl.dbg_i == 6) or (pl.dbg_i == 40):
        s = abs (pl.x - (2.023))
    elif (pl.dbg_i == 7) or (pl.dbg_i == 30):
        s = abs (pl.y - (0.050))
    return s

def get_global_score(plot_l):
    s = 0
    for pl in plot_l:
        s = s + get_plot_score(pl)
    return s

def get_min_score(plot_l,err_x0,err_y0,err_theta0,q):
    min_s = 1000000.0
    min_x = 0.0
    for err_x in arange(err_x0-10.0*q,err_x0+10.0*q,q):
        recompute_plot_xy(plot_l,err_x,err_y0,err_theta0)
        s = get_global_score(plot_l)
        if min_s>s:
            min_s=s
            min_x=err_x

    min_s = 1000000.0
    min_y = 0.0
    for err_y in arange(err_y0-10.0*q,err_y0+10.0*q,q):
        recompute_plot_xy(plot_l,err_x0,err_y,err_theta0)
        s = get_global_score(plot_l)
        if min_s>s:
            min_s=s
            min_y=err_y

    min_s = 1000000.0
    min_theta = 0.0
    for err_theta in arange(err_theta0-10.0*q,err_theta0+10.0*q,q):
        recompute_plot_xy(plot_l,err_x0,err_y0,err_theta)
        s = get_global_score(plot_l)
        if min_s>s:
            min_s=s
            min_theta=err_theta

    return (min_x,min_y,min_theta)

def do_gps(plot_l):
    new_l = plot_l.copy()
    (min_x0,min_y0,min_theta0) = get_min_score(new_l,0.0,0.0,0.0,0.01)
    (min_x1,min_y1,min_theta1) = get_min_score(new_l,min_x0,min_y0,min_theta0,0.01)
    (min_x2,min_y2,min_theta2) = get_min_score(new_l,min_x1,min_y1,min_theta1,0.01)
    (min_x3,min_y3,min_theta3) = get_min_score(new_l,min_x2,min_y2,min_theta2,0.001)
    (min_x4,min_y4,min_theta4) = get_min_score(new_l,min_x3,min_y3,min_theta3,0.001)
    return (min_x4,min_y4,min_theta4)
