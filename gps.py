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


def process_plot(plot_l):
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

    if (N1!=0) or (N2!=0) or (N3!=0) or (N4!=0) or (N5!=0) or (N6!=0) or (N7!=0):
        print(N1, N2, N3, N4, N5, N6, N7)


