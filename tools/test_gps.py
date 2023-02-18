import sys
import os
import inspect
import re
import math
import struct
from numpy import arange

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from messages import RplidarPlot, RplidarDebugPlot
from gps import process_plots, recompute_plot_xy, get_global_score, get_min_score


if __name__ == '__main__':
    plot_l = []

    data_fd = open(sys.argv[1],"rt")
    err_odo_x = float(sys.argv[2])
    err_odo_y = float(sys.argv[3])
    err_odo_theta = float(sys.argv[4])

    for li in data_fd.readlines():
        tok=li.split()
        pl = RplidarDebugPlot(b'\0'*32)
        pl.timestamp = int(tok[0])
        pl.raw_R     = float(tok[1])
        pl.raw_theta = float(tok[2])
        pl.odo_x     = float(tok[3]) + err_odo_x
        pl.odo_y     = float(tok[4]) + err_odo_y
        pl.odo_theta = float(tok[5]) + err_odo_theta
        pl.dbg_i     = int(tok[6])
        pl.dbg_f     = float(tok[7])
        pl.x         = pl.raw_R * math.cos (pl.raw_theta + pl.odo_theta) + pl.odo_x;
        pl.y         = pl.raw_R * math.sin (pl.raw_theta + pl.odo_theta) + pl.odo_y;
        plot_l.append(pl)

    process_plots(plot_l)

    new_l = plot_l.copy()

    (min_x0,min_y0,min_theta0) = get_min_score(plot_l,0.0,0.0,0.0,0.01)

    print("min_x0={:12.4f}".format(min_x0))
    print("min_y0={:12.4f}".format(min_y0))
    print("min_theta0={:12.4f}".format(min_theta0))
    print()

    (min_x1,min_y1,min_theta1) = get_min_score(plot_l,min_x0,min_y0,min_theta0,0.01)

    print("min_x1={:12.4f}".format(min_x1))
    print("min_y1={:12.4f}".format(min_y1))
    print("min_theta1={:12.4f}".format(min_theta1))
    print()

    (min_x2,min_y2,min_theta2) = get_min_score(plot_l,min_x1,min_y1,min_theta1,0.01)

    print("min_x2={:12.4f}".format(min_x2))
    print("min_y2={:12.4f}".format(min_y2))
    print("min_theta2={:12.4f}".format(min_theta2))
    print()

    (min_x3,min_y3,min_theta3) = get_min_score(plot_l,min_x2,min_y2,min_theta2,0.001)

    print("min_x3={:12.4f}".format(min_x3))
    print("min_y3={:12.4f}".format(min_y3))
    print("min_theta3={:12.4f}".format(min_theta3))
    print()

    (min_x4,min_y4,min_theta4) = get_min_score(plot_l,min_x3,min_y3,min_theta3,0.001)

    print("min_x4={:12.4f}".format(min_x4))
    print("min_y4={:12.4f}".format(min_y4))
    print("min_theta4={:12.4f}".format(min_theta4))
    print()

    data_fd.close()


