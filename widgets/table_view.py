import struct
import math
import os

from PyQt5.QtCore import QObject, pyqtSignal, QSize, QRectF, QPointF, Qt

from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtWidgets import QGraphicsPixmapItem

from PyQt5.QtGui import QPolygonF, QPen, QBrush, QColor, QFont, QTransform
from PyQt5.QtGui import QImage, QImageReader, QPixmap

from PyQt5.QtCore import QTimer

from messages import RplidarPlot, RplidarDebugPlot
from gps import process_plot

def normalize_angle(theta_rad):
    while theta_rad>math.pi:
        theta_rad -= 2.0*math.pi
    while theta_rad<=-math.pi:
        theta_rad += 2.0*math.pi
    return theta_rad

class MyGraphicsScene(QGraphicsScene):
    def mouseMoveEvent(self, event):
        x_mm = event.scenePos().x()
        y_mm = event.scenePos().y()
        rel_x_mm = x_mm - self.parent()._little_robot_x
        rel_y_mm = y_mm - self.parent()._little_robot_y
        d_mm = math.sqrt(rel_x_mm*rel_x_mm + rel_y_mm*rel_y_mm)
        #print ("MyGraphicsScene:<{},{}>".format(x_mm,y_mm))
        disp_window = self.parent().parent().parent()
        disp_window.posXL.setText(" x: {:>6.1f}".format(x_mm))
        disp_window.posYL.setText(" y: {:>6.1f}".format(y_mm))
        disp_window.posXRL.setText(" xr: {:>6.1f}".format(rel_x_mm))
        disp_window.posYRL.setText(" yr: {:>6.1f}".format(rel_y_mm))
        disp_window.posDRL.setText(" dr: {:>6.1f}".format(d_mm))

    def mousePressEvent(self, event):
        x_mm = event.scenePos().x()
        y_mm = event.scenePos().y()
        if self.parent()._debug_edit_mode:
            self.parent()._debug_edit_point_l.append((x_mm,y_mm))
            self.parent().debug_line_to(x_mm,y_mm)

class TableViewWidget(QGraphicsView):
    g_table_view = None
    g_detect_size = 200
    g_detect_text = "position"
    #g_detect_text = "quality"
    #g_detect_text = "none"
    g_rplidar_remanence = False
    #g_rplidar_plot_life_ms = 1000 # FIXME : DEBUG : FSCK QT!
    g_rplidar_plot_life_ms = 300
    g_update_other_robots = False
    g_show_theme = False
    g_debug = True
    g_dbg_plt_sz = 1.2
    g_dbg_pen_sz = 0.8


    def __init__(self, parent = None, ihm_type='pc'):
        super(TableViewWidget, self).__init__(parent)
        if ihm_type=='pc':
            #self.setFixedSize(900,600)
            self.setFixedSize(1000,700)
        elif ihm_type=='pc-mini':
            #self.setFixedSize(600,400)
            self.setFixedSize(640,440)
        else:
            #self.setFixedSize(225,150)
            self.setFixedSize(240,165)
        #self.setSceneRect(QRectF(0,-1500,2000,3000))
        self.setSceneRect(QRectF(-200,-1700,2400,3400))
        #self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        little_robot_poly = QPolygonF([
            QPointF(  50,   0),
            QPointF( 100,  85),
            QPointF(  65, 115),
            QPointF( -65, 115),
            QPointF(-100,  85),
            QPointF(-100, -85),
            QPointF( -65,-115),
            QPointF(  65,-115),
            QPointF( 100, -85)
            ])

        old_beacon_poly = QPolygonF([
            QPointF( 50,  50),

            QPointF(-50,  50),

            QPointF(-50,  40),
            QPointF( 50,  40),
            QPointF(-50,  40),

            QPointF(-50,  30),
            QPointF( 50,  30),
            QPointF(-50,  30),

            QPointF(-50,  20),
            QPointF( 50,  20),
            QPointF(-50,  20),

            QPointF(-50,  10),
            QPointF( 50,  10),
            QPointF(-50,  10),

            QPointF(-50,   0),
            QPointF( 50,   0),
            QPointF(-50,   0),

            QPointF(-50, -10),
            QPointF( 50, -10),
            QPointF(-50, -10),

            QPointF(-50, -20),
            QPointF( 50, -20),
            QPointF(-50, -20),

            QPointF(-50, -30),
            QPointF( 50, -30),
            QPointF(-50, -30),

            QPointF(-50, -40),
            QPointF( 50, -40),
            QPointF(-50, -40),

            QPointF(-50, -50),

            QPointF( 50, -50)
            ])

        beacon_poly = QPolygonF([
            QPointF( 50, -50),

            QPointF( 50,  50),

            QPointF( 40,  50),
            QPointF( 40, -50),
            QPointF( 40,  50),

            QPointF( 30,  50),
            QPointF( 30, -50),
            QPointF( 30,  50),

            QPointF( 20,  50),
            QPointF( 20, -50),
            QPointF( 20,  50),

            QPointF( 10,  50),
            QPointF( 10, -50),
            QPointF( 10,  50),

            QPointF(  0,  50),
            QPointF(  0, -50),
            QPointF(  0,  50),

            QPointF(-10,  50),
            QPointF(-10, -50),
            QPointF(-10,  50),

            QPointF(-20,  50),
            QPointF(-20, -50),
            QPointF(-20,  50),

            QPointF(-30,  50),
            QPointF(-30, -50),
            QPointF(-30,  50),

            QPointF(-40,  50),
            QPointF(-40, -50),
            QPointF(-40,  50),

            QPointF(-50,  50),

            QPointF(-50, -50)
            ])


        #self._scene = QGraphicsScene(QRectF(0,-1500,2000,3000))
        self._scene = MyGraphicsScene(QRectF(-200,-1700,2400,3400),self)

        self._beacon_middle = self._scene.addPolygon(beacon_poly, QPen(QBrush(QColor('black')),0.2), QBrush(QColor('white')))
        self._beacon_middle.setZValue(1)
        self._beacon_middle.setPos(-73.0, 0.0)
        self._beacon_left = self._scene.addPolygon(beacon_poly, QPen(QBrush(QColor('black')),0.2), QBrush(QColor('white')))
        self._beacon_left.setZValue(1)
        self._beacon_left.setPos(2073.0, -1450.0)
        self._beacon_right = self._scene.addPolygon(beacon_poly, QPen(QBrush(QColor('black')),0.2), QBrush(QColor('white')))
        self._beacon_right.setZValue(1)
        self._beacon_right.setPos(2073.0, 1450.0)

#        self._big_robot = self._scene.addPolygon(big_robot_poly, QPen(), QBrush(QColor('red')))
#        self._big_robot.setZValue(1)
        self._little_robot = self._scene.addPolygon(little_robot_poly, QPen(), QBrush(QColor('red')))
        self._little_robot.setZValue(1)
        # FIXME : DEBUG
        if TableViewWidget.g_debug:
            dbg_plt_sz = TableViewWidget.g_dbg_plt_sz
            dbg_pen_sz = TableViewWidget.g_dbg_pen_sz
            self._little_robot_center = self._scene.addEllipse(1000.0 - dbg_plt_sz, -1397.0 - dbg_plt_sz, 2*dbg_plt_sz, 2*dbg_plt_sz, QPen(QBrush(QColor('black')),dbg_pen_sz), QBrush(QColor('yellow')))
            self._little_robot_center.setZValue(100)
            new_p = self._scene.addEllipse(1000.0 - dbg_plt_sz, -1397.0 - dbg_plt_sz, 2*dbg_plt_sz, 2*dbg_plt_sz, QPen(QBrush(QColor('black')),dbg_pen_sz), QBrush(QColor('yellow')))
            new_p.setZValue(100)
        #self._friend_robot = self._scene.addEllipse(-100, -100, 200, 200, QPen(QBrush(QColor('black')),4), QBrush(QColor('green')))
        self._friend_robot = self._scene.addEllipse(-100, -100, TableViewWidget.g_detect_size, TableViewWidget.g_detect_size, QPen(QBrush(QColor('black')),4), QBrush(QColor('white')))
        self._friend_robot.setZValue(1)
        self._friend_robot.setPos(-1 * 1000, -1 * 1000)
        if os.name == 'nt':
            self._friend_robot_text = self._scene.addText("0123456", QFont("Calibri",80));
        else:
            self._friend_robot_text = self._scene.addText("0123456", QFont("System",40));
        self._friend_robot_text.setPos(-1 * 1000 - 60, -1 * 1000 - 40)
        self._friend_robot_text.setRotation(-90)
        self._friend_robot_text.setTransform(QTransform(1.0, 0.0, 0.0,  0.0, -1.0, 0.0,   0.0, 0.0, 1.0))
        self._friend_robot_text.setZValue(1)
        #self._adv1_robot = self._scene.addEllipse(-100, -100, 200, 200, QPen(QBrush(QColor('black')),4), QBrush(QColor('white')))
        self._adv1_robot = self._scene.addEllipse(-100, -100, TableViewWidget.g_detect_size, TableViewWidget.g_detect_size, QPen(QBrush(QColor('black')),4), QBrush(QColor('white')))
        self._adv1_robot.setZValue(1)
        self._adv1_robot.setPos(-1 * 1000, -1 * 1000)
        if os.name == 'nt':
            self._adv1_robot_text = self._scene.addText("0", QFont("Calibri",80));
        else:
            self._adv1_robot_text = self._scene.addText("0", QFont("System",40));
        self._adv1_robot_text.setPos(-1 * 1000 - 60, -1 * 1000 - 40)
        self._adv1_robot_text.setRotation(-90)
        self._adv1_robot_text.setTransform(QTransform(1.0, 0.0, 0.0,  0.0, -1.0, 0.0,   0.0, 0.0, 1.0))
        self._adv1_robot_text.setZValue(1)
        #self._adv2_robot = self._scene.addEllipse(-100, -100, 200, 200, QPen(QBrush(QColor('black')),4), QBrush(QColor('blue')))
        self._adv2_robot = self._scene.addEllipse(-100, -100, TableViewWidget.g_detect_size, TableViewWidget.g_detect_size, QPen(QBrush(QColor('black')),4), QBrush(QColor('white')))
        self._adv2_robot.setZValue(1)
        self._adv2_robot.setPos(-1 * 1000, -1 * 1000)
        if os.name == 'nt':
            self._adv2_robot_text = self._scene.addText("0", QFont("Calibri",80));
        else:
            self._adv2_robot_text = self._scene.addText("0", QFont("System",40));
        self._adv2_robot_text.setPos(-1 * 1000 - 60, -1 * 1000 - 40)
        self._adv2_robot_text.setRotation(-90)
        self._adv2_robot_text.setTransform(QTransform(1.0, 0.0, 0.0,  0.0, -1.0, 0.0,   0.0, 0.0, 1.0))
        self._adv2_robot_text.setZValue(1)
        self.setScene(self._scene)

        self.rotate(90)
        self._my_scale = 0.3
        if ihm_type=='pc':
            self._my_scale = 0.3
        elif ihm_type=='pc-mini':
            self._my_scale = 0.2
        else:
            self._my_scale = 0.075
        self.scale(self._my_scale, -self._my_scale)

        #purple = QColor.fromCmykF(0.5,0.9,0,0.05)
        #background = QColor(40,40,40)
        #darker = QColor(20,20,20)
        #self._scene.addRect(QRectF(0,-1500,2000,3000),QPen(), QBrush(background))

        if TableViewWidget.g_show_theme:
            f=open("widgets/table_2020_600x400.png","rb")
            my_buff=f.read()
            test_img_pixmap2 = QPixmap()
            test_img_pixmap2.loadFromData(my_buff)
            #self.setPixmap(test_img_pixmap2)
            self._bg_img = QGraphicsPixmapItem(test_img_pixmap2)
            self._bg_img.setTransform(QTransform(1.0, 0.0, 0.0,  0.0, -1.0, 0.0,   0.0, 0.0, 0.2))
            self._bg_img.setRotation(-90)
            self._bg_img.setPos(0, -1500)
            self._scene.addItem(self._bg_img);
        else:
            self._scene.addRect(QRectF(0,-1500,2000,3000))

        self._traj_segm_l = []

        self._debug_edit_mode = False
        self._debug_edit_point_l = []

#        self._big_robot_x = 0
#        self._big_robot_y = 0
        self._little_robot_x = 0
        self._little_robot_y = 0
        self._little_robot_theta = 0
        self._dbg_x_mm = 0
        self._dbg_y_mm = 0
        self._dbg_target_x_mm = 0
        self._dbg_target_y_mm = 0
        self._dbg_traj_x_mm = 0
        self._dbg_traj_y_mm = 0
        self._dbg_shift_rot_mm = 0
        self._dbg_rot_cnt = 0

        # Debug lidar plots
        dbg_plt_sz = 1
        self.plot_obj0 = []
        self.plot_obj1 = []
        self.plot_obj2 = []
        self.plot_obj3 = []
        self.plot_obj4 = []
        self.plot_obj5 = []
        self.plot_obj6 = []
        self.plot_obj7 = []
        for i in range(0,2000):
            plt_sz = dbg_plt_sz
            my_plot_obj0 = self._scene.addRect(QRectF(-plt_sz, -plt_sz, 2*plt_sz, 2*plt_sz), QPen(QBrush(QColor('black')),0.2), QBrush(QColor('black')))
            my_plot_obj0.setZValue(100)
            my_plot_obj0.setPos(-2 * 1000, -2 * 1000)
            self.plot_obj0.append(my_plot_obj0)
        for i in range(0,500):
            plt_sz = dbg_plt_sz
            my_plot_obj1 = self._scene.addRect(QRectF(-plt_sz, -plt_sz, 2*plt_sz, 2*plt_sz), QPen(QBrush(QColor('black')),0.2), QBrush(QColor('red')))
            my_plot_obj1.setZValue(100)
            my_plot_obj1.setPos(-2 * 1000 + 100, -2 * 1000)
            self.plot_obj1.append(my_plot_obj1)
            plt_sz = dbg_plt_sz
            my_plot_obj2 = self._scene.addRect(QRectF(-plt_sz, -plt_sz, 2*plt_sz, 2*plt_sz), QPen(QBrush(QColor('black')),0.2), QBrush(QColor('blue')))
            my_plot_obj2.setZValue(100)
            my_plot_obj2.setPos(-2 * 1000 + 200, -2 * 1000)
            self.plot_obj2.append(my_plot_obj2)
            my_plot_obj3 = self._scene.addRect(QRectF(-plt_sz, -plt_sz, 2*plt_sz, 2*plt_sz), QPen(QBrush(QColor('black')),0.2), QBrush(QColor('green')))
            my_plot_obj3.setZValue(100)
            my_plot_obj3.setPos(-2 * 1000 + 300, -2 * 1000)
            self.plot_obj3.append(my_plot_obj3)
            my_plot_obj4 = self._scene.addEllipse(-plt_sz, -plt_sz, 2*plt_sz, 2*plt_sz, QPen(QBrush(QColor('black')),0.2), QBrush(QColor('red')))
            my_plot_obj4.setZValue(100)
            my_plot_obj4.setPos(-2 * 1000 + 400, -2 * 1000)
            self.plot_obj4.append(my_plot_obj4)
            my_plot_obj5 = self._scene.addEllipse(-plt_sz, -plt_sz, 2*plt_sz, 2*plt_sz, QPen(QBrush(QColor('black')),0.2), QBrush(QColor('blue')))
            my_plot_obj5.setZValue(100)
            my_plot_obj5.setPos(-2 * 1000 + 500, -2 * 1000)
            self.plot_obj5.append(my_plot_obj5)
            my_plot_obj6 = self._scene.addEllipse(-plt_sz, -plt_sz, 2*plt_sz, 2*plt_sz, QPen(QBrush(QColor('black')),0.2), QBrush(QColor('green')))
            my_plot_obj6.setZValue(100)
            my_plot_obj6.setPos(-2 * 1000 + 600, -2 * 1000)
            self.plot_obj6.append(my_plot_obj6)
            my_plot_obj7 = self._scene.addEllipse(-plt_sz, -plt_sz, 2*plt_sz, 2*plt_sz, QPen(QBrush(QColor('black')),0.2), QBrush(QColor('yellow')))
            my_plot_obj7.setZValue(100)
            my_plot_obj7.setPos(-2 * 1000 + 700, -2 * 1000)
            self.plot_obj7.append(my_plot_obj7)

        self.beacon_corner1 = self._scene.addRect(QRectF(-4*plt_sz, -4*plt_sz, 8*plt_sz, 8*plt_sz), QPen(QBrush(QColor('black')),0.2), QBrush(QColor('blue')))
        self.beacon_corner1.setZValue(100)
        self.beacon_corner1.setPos(-2 * 1000 + 500, -2 * 1000)
        self.beacon_corner2 = self._scene.addRect(QRectF(-4*plt_sz, -4*plt_sz, 8*plt_sz, 8*plt_sz), QPen(QBrush(QColor('black')),0.2), QBrush(QColor('green')))
        self.beacon_corner2.setZValue(100)
        self.beacon_corner2.setPos(-2 * 1000 + 510, -2 * 1000)
        self.beacon_corner3 = self._scene.addRect(QRectF(-4*plt_sz, -4*plt_sz, 8*plt_sz, 8*plt_sz), QPen(QBrush(QColor('black')),0.2), QBrush(QColor('red')))
        self.beacon_corner3.setZValue(100)
        self.beacon_corner3.setPos(-2 * 1000 + 520, -2 * 1000)
        self.beacon_corner4 = self._scene.addRect(QRectF(-4*plt_sz, -4*plt_sz, 8*plt_sz, 8*plt_sz), QPen(QBrush(QColor('black')),0.2), QBrush(QColor('yellow')))
        self.beacon_corner4.setZValue(100)
        self.beacon_corner4.setPos(-2 * 1000 + 530, -2 * 1000)

        self.last_plot_ts = 0
        self.curr_plot_ts = 0
        self.plot_l = []
        self.plot_dbg = 0
        self.plot_once = True
        self.max_edge_plt_score = 0.0

        self.plot_timer = QTimer(self)
        #self.plot_timer.timeout.connect(self.refresh_plot_display)
        self.plot_timer.timeout.connect(self.refresh_debug_plot_display)
        self.plot_timer.start(100)

        TableViewWidget.g_table_view = self


    def sizeHint(self):
        return QSize(600,400)

    def set_client(self, client):
        self._client = client
        self._client.propulsion_telemetry.connect(self.update_telemetry)
        self._client.propulsion_telemetry_ex.connect(self.update_telemetry_ex)
        self._client.goldo_debug_traj.connect(self.update_goldo_debug_traj)
        self._client.rplidar_plot.connect(self.update_plots)
        self._client.rplidar_debug_plot.connect(self.update_debug_plots)
        self._client.rplidar_robot_detection.connect(self.update_other_robots)
        

    def update_telemetry(self, telemetry):
#        self._big_robot.setPos(telemetry.x * 1000, telemetry.y * 1000)
#        self._big_robot.setRotation(telemetry.yaw * 180 / math.pi)
#        self._big_robot_x = telemetry.x * 1000
#        self._big_robot_y = telemetry.y * 1000
        self._little_robot.setPos(telemetry.x * 1000, telemetry.y * 1000)
        self._little_robot.setRotation(telemetry.yaw * 180 / math.pi)
        self._little_robot_x = telemetry.x * 1000
        self._little_robot_y = telemetry.y * 1000

        # FIXME : DEBUG
        if TableViewWidget.g_debug:
            new_theta = telemetry.yaw * 180 / math.pi
            self._little_robot_center.setPos(telemetry.x * 1000, telemetry.y * 1000)
            dbg_plt_sz = TableViewWidget.g_dbg_plt_sz
            dbg_pen_sz = TableViewWidget.g_dbg_pen_sz
            delta_x_mm = (telemetry.x * 1000 - self._dbg_x_mm)
            delta_y_mm = (telemetry.y * 1000 - self._dbg_y_mm)
            delta_d_mm = math.sqrt(delta_x_mm*delta_x_mm + delta_y_mm*delta_y_mm)
            if (delta_d_mm > 0.1):
                self._dbg_x_mm = telemetry.x * 1000
                self._dbg_y_mm = telemetry.y * 1000
                new_p = self._scene.addEllipse(self._dbg_x_mm-dbg_plt_sz, self._dbg_y_mm-dbg_plt_sz, 2*dbg_plt_sz, 2*dbg_plt_sz, QPen(QBrush(QColor('black')),dbg_pen_sz), QBrush(QColor('yellow')))
                new_p.setZValue(100)
            delta_center_x_mm = (telemetry.x * 1000 - 1000.0)
            delta_center_y_mm = (telemetry.y * 1000 + 1397.0)
            delta_center_R_mm = math.sqrt(delta_center_x_mm*delta_center_x_mm + delta_center_y_mm*delta_center_y_mm)
            if (self._dbg_shift_rot_mm<delta_center_R_mm) and (delta_center_R_mm<1000.0):
                self._dbg_shift_rot_mm = delta_center_R_mm
            disp_window = self.parent().parent()
            disp_window.posDbg1L.setText(" DEBUG : shift_rot={:>9.3f}".format(self._dbg_shift_rot_mm))
            old_theta = self._little_robot_theta
            theta_treshold = 90.01
            #theta_treshold = 89.99
            if ((old_theta>85.0) and (old_theta<theta_treshold)):
                if ((new_theta>=theta_treshold)):
                    #print ("old_theta={:f}".format(old_theta))
                    #print ("new_theta={:f}".format(new_theta))
                    self._dbg_rot_cnt += 1
            elif ((old_theta>=theta_treshold) and (old_theta<95.0)):
                if ((new_theta<theta_treshold)):
                    self._dbg_rot_cnt -= 1
            disp_window.posDbg2L.setText(" DEBUG : rot_cnt={:d}".format(self._dbg_rot_cnt))
            self._little_robot_theta = new_theta


    def update_telemetry_ex(self, telemetry_ex):
        #return # FIXME : DEBUG
        if TableViewWidget.g_debug:
            dbg_plt_sz = TableViewWidget.g_dbg_plt_sz
            dbg_pen_sz = TableViewWidget.g_dbg_pen_sz
            delta_x_mm = (telemetry_ex.target_x * 1000 - self._dbg_target_x_mm)
            delta_y_mm = (telemetry_ex.target_y * 1000 - self._dbg_target_y_mm)
            delta_d_mm = math.sqrt(delta_x_mm*delta_x_mm + delta_y_mm*delta_y_mm)
            if (delta_d_mm > 0.1):
                self._dbg_target_x_mm = telemetry_ex.target_x * 1000
                self._dbg_target_y_mm = telemetry_ex.target_y * 1000
                new_p = self._scene.addEllipse(self._dbg_target_x_mm-dbg_plt_sz, self._dbg_target_y_mm-dbg_plt_sz, 2*dbg_plt_sz, 2*dbg_plt_sz, QPen(QBrush(QColor('blue')),dbg_pen_sz), QBrush(QColor('red')))
                new_p.setZValue(100)


    def update_goldo_debug_traj(self, dbg_vec):
        return # FIXME : DEBUG
        if TableViewWidget.g_debug:
            dbg_plt_sz = TableViewWidget.g_dbg_plt_sz
            dbg_pen_sz = TableViewWidget.g_dbg_pen_sz
            delta_x_mm = (dbg_vec.x * 1000 - self._dbg_traj_x_mm)
            delta_y_mm = (dbg_vec.y * 1000 - self._dbg_traj_y_mm)
            delta_d_mm = math.sqrt(delta_x_mm*delta_x_mm + delta_y_mm*delta_y_mm)
            if (delta_d_mm > 0.1):
                self._dbg_traj_x_mm = dbg_vec.x * 1000
                self._dbg_traj_y_mm = dbg_vec.y * 1000
                new_p = self._scene.addEllipse(self._dbg_traj_x_mm-dbg_plt_sz, self._dbg_traj_y_mm-dbg_plt_sz, 2*dbg_plt_sz, 2*dbg_plt_sz, QPen(QBrush(QColor('blue')),dbg_pen_sz), QBrush(QColor('red')))
                new_p.setZValue(100)


    def update_other_robots(self, other_robot):
        if (not TableViewWidget.g_update_other_robots):
            return
        dbg_plt_sz = 3
        if (other_robot.id == 0):
            self._friend_robot.setPos(other_robot.x * 1000, other_robot.y * 1000)
            if (TableViewWidget.g_detect_text == "quality"):
                self._friend_robot_text.setPlainText("%d"%other_robot.samples)
            elif (TableViewWidget.g_detect_text == "position"):
                self._friend_robot_text.setPlainText("%d,%d"%(other_robot.x*1000,other_robot.y*1000))
            else:
                self._friend_robot_text.setPlainText("")
            self._friend_robot_text.setPos(other_robot.x * 1000 - 60, other_robot.y * 1000 - 40)
            if TableViewWidget.g_rplidar_remanence:
                self._scene.addEllipse(other_robot.x * 1000 - dbg_plt_sz, other_robot.y * 1000 - dbg_plt_sz, 2*dbg_plt_sz, 2*dbg_plt_sz, QPen(QBrush(QColor('white')),4), QBrush(QColor('white')))
        elif (other_robot.id == 1):
            self._adv1_robot.setPos(other_robot.x * 1000, other_robot.y * 1000)
            if (TableViewWidget.g_detect_text == "quality"):
                self._adv1_robot_text.setPlainText("%d"%other_robot.samples)
            elif (TableViewWidget.g_detect_text == "position"):
                self._adv1_robot_text.setPlainText("%d,%d"%(other_robot.x*1000,other_robot.y*1000))
            else:
                self._adv1_robot_text.setPlainText("")
            self._adv1_robot_text.setPos(other_robot.x * 1000 - 60, other_robot.y * 1000 - 40)
            if TableViewWidget.g_rplidar_remanence:
                self._scene.addEllipse(other_robot.x * 1000 - dbg_plt_sz, other_robot.y * 1000 - dbg_plt_sz, 2*dbg_plt_sz, 2*dbg_plt_sz, QPen(QBrush(QColor('white')),4), QBrush(QColor('white')))
        elif (other_robot.id == 2):
            self._adv2_robot.setPos(other_robot.x * 1000, other_robot.y * 1000)
            if (TableViewWidget.g_detect_text == "quality"):
                self._adv2_robot_text.setPlainText("%d"%other_robot.samples)
            elif (TableViewWidget.g_detect_text == "position"):
                self._adv2_robot_text.setPlainText("%d,%d"%(other_robot.x*1000,other_robot.y*1000))
            else:
                self._adv2_robot_text.setPlainText("")
            self._adv2_robot_text.setPos(other_robot.x * 1000 - 60, other_robot.y * 1000 - 40)
            if TableViewWidget.g_rplidar_remanence:
                self._scene.addEllipse(other_robot.x * 1000 - dbg_plt_sz, other_robot.y * 1000 - dbg_plt_sz, 2*dbg_plt_sz, 2*dbg_plt_sz, QPen(QBrush(QColor('white')),4), QBrush(QColor('white')))

    def debug_set_start(self, _new_x, _new_y):
        self.debug_start_x = _new_x
        self.debug_start_y = _new_y
        self.debug_cur_x = _new_x
        self.debug_cur_y = _new_y
        if self._debug_edit_mode:
            self._debug_edit_point_l.append((_new_x,_new_y))

    def debug_line_to(self, _new_x, _new_y, _r=0, _g=0, _b=0):
        if TableViewWidget.g_show_theme:
            my_segm = self._scene.addLine(self.debug_cur_x, self.debug_cur_y, _new_x, _new_y, QPen(QColor(255,255,255)));
        else:
            #my_segm = self._scene.addLine(self.debug_cur_x, self.debug_cur_y, _new_x, _new_y, QPen(QColor(128,128,128)));
            my_segm = self._scene.addLine(self.debug_cur_x, self.debug_cur_y, _new_x, _new_y, QPen(QColor(_r,_g,_b)));
        self._traj_segm_l.append(my_segm)
        self.debug_cur_x = _new_x
        self.debug_cur_y = _new_y

    def debug_clear_lines(self):
        for l in self._traj_segm_l:
            self._scene.removeItem(l)
        self._traj_segm_l = []

    def debug_start_edit(self, _new_x, _new_y):
        self.debug_clear_lines()
        self._debug_edit_mode = True
        self.debug_start_x = _new_x
        self.debug_start_y = _new_y
        self.debug_cur_x = _new_x
        self.debug_cur_y = _new_y
        self._debug_edit_point_l = [(_new_x,_new_y)]

    def debug_start_edit_rel(self):
        self.debug_clear_lines()
        self._debug_edit_mode = True
        self.debug_start_x = self._little_robot_x
        self.debug_start_y = self._little_robot_y
        self.debug_cur_x = self._little_robot_x
        self.debug_cur_y = self._little_robot_y
        self._debug_edit_point_l = [(self._little_robot_x,self._little_robot_y)]

    def debug_stop_edit(self):
        self._debug_edit_mode = False
        return self._debug_edit_point_l

    def zoomPlus(self):
        self._my_scale = 2.0
        self.scale(self._my_scale, self._my_scale)

    def zoomDef(self):
        self.resetTransform()
        self.rotate(90)
        self._my_scale = 0.3
        self.scale(self._my_scale, -self._my_scale)

    def zoomMinus(self):
        self._my_scale = 0.5
        self.scale(self._my_scale, self._my_scale)

    def update_plots(self, my_plot):
        self.last_plot_ts = my_plot.timestamp
        if self.curr_plot_ts == 0: self.curr_plot_ts = my_plot.timestamp
        self.plot_l.append(my_plot)

    def refresh_plot_display(self):
        for i in range(0,len(self.plot_obj0)):
            self.plot_obj0[i].setPos(-2 * 1000 + 100, -2 * 1000)
        i = 0
        for pl in self.plot_l:
            if (self.last_plot_ts-pl.timestamp>TableViewWidget.g_rplidar_plot_life_ms):
                self.plot_l.remove(pl)
        for pl in self.plot_l:
            if (i>=len(self.plot_obj0)):
                print ("WARNING : not enough plot obj")
                break
            self.plot_obj0[i].setPos(pl.x * 1000, pl.y * 1000)
            i = i + 1

    def update_debug_plots(self, my_debug_plot):
        self.last_plot_ts = my_debug_plot.timestamp
        if self.curr_plot_ts == 0: self.curr_plot_ts = my_debug_plot.timestamp
        self.plot_l.append(my_debug_plot)

    def refresh_debug_plot_display(self):
        for i in range(0,len(self.plot_obj0)):
            self.plot_obj0[i].setPos(-2 * 1000, -2 * 1000)
        for i in range(0,len(self.plot_obj1)):
            self.plot_obj1[i].setPos(-2 * 1000 + 100, -2 * 1000)
            self.plot_obj2[i].setPos(-2 * 1000 + 200, -2 * 1000)
            self.plot_obj3[i].setPos(-2 * 1000 + 300, -2 * 1000)
            self.plot_obj4[i].setPos(-2 * 1000 + 400, -2 * 1000)
            self.plot_obj5[i].setPos(-2 * 1000 + 500, -2 * 1000)
            self.plot_obj6[i].setPos(-2 * 1000 + 600, -2 * 1000)
            self.plot_obj7[i].setPos(-2 * 1000 + 700, -2 * 1000)
        self.beacon_corner1.setPos(-2 * 1000 + 500, -2 * 1000)
        self.beacon_corner2.setPos(-2 * 1000 + 510, -2 * 1000)
        self.beacon_corner3.setPos(-2 * 1000 + 520, -2 * 1000)
        self.beacon_corner4.setPos(-2 * 1000 + 530, -2 * 1000)

        if self.curr_plot_ts != 0: self.curr_plot_ts = self.curr_plot_ts + 100

        for pl in self.plot_l:
            if (self.curr_plot_ts-pl.timestamp>TableViewWidget.g_rplidar_plot_life_ms):
                self.plot_l.remove(pl)

        # FIXME : DEBUG
        process_plot(self.plot_l)

        i0 = 0
        i1 = 0
        i2 = 0
        i3 = 0
        i4 = 0
        i5 = 0
        i6 = 0
        i7 = 0
        calib_y=0.0
        calib_n=0
        for pl in self.plot_l:
            my_x = pl.x
            my_y = pl.y
            if (pl.dbg_i==0):
                if (i0>=len(self.plot_obj0)):
                    #print ("WARNING : not enough plot obj0")
                    pass
                else:
                    self.plot_obj0[i0].setPos(my_x * 1000, my_y * 1000)
                i0 = i0 + 1
                if (my_x>1.5) and (my_x<2.0) and (my_y>-1.5) and (my_y<1.3):
                    calib_y = calib_y + (my_y*1000)
                    calib_n = calib_n + 1
            elif (pl.dbg_i==1):
                if (i1>=len(self.plot_obj1)):
                    print ("WARNING : not enough plot obj1")
                    pass
                else:
                    self.plot_obj1[i1].setPos(my_x * 1000, my_y * 1000)
                i1 = i1 + 1
            elif (pl.dbg_i==2):
                if (i2>=len(self.plot_obj2)):
                    print ("WARNING : not enough plot obj2")
                    pass
                else:
                    self.plot_obj2[i2].setPos(my_x * 1000, my_y * 1000)
                i2 = i2 + 1
            elif (pl.dbg_i==3):
                if (i3>=len(self.plot_obj3)):
                    print ("WARNING : not enough plot obj3")
                    pass
                else:
                    self.plot_obj3[i3].setPos(my_x * 1000, my_y * 1000)
                i3 = i3 + 1
            elif (pl.dbg_i==4):
                if (i4>=len(self.plot_obj4)):
                    print ("WARNING : not enough plot obj4")
                    pass
                else:
                    self.plot_obj4[i4].setPos(my_x * 1000, my_y * 1000)
                i4 = i4 + 1
            elif (pl.dbg_i==5):
                if (i5>=len(self.plot_obj5)):
                    print ("WARNING : not enough plot obj5")
                    pass
                else:
                    self.plot_obj5[i5].setPos(my_x * 1000, my_y * 1000)
                i5 = i5 + 1
            elif (pl.dbg_i==6):
                if (i6>=len(self.plot_obj6)):
                    print ("WARNING : not enough plot obj6")
                    pass
                else:
                    self.plot_obj6[i6].setPos(my_x * 1000, my_y * 1000)
                i6 = i6 + 1
            elif (pl.dbg_i==7):
                if (i7>=len(self.plot_obj7)):
                    print ("WARNING : not enough plot obj7")
                    pass
                else:
                    self.plot_obj7[i7].setPos(my_x * 1000, my_y * 1000)
                i7 = i7 + 1
            elif (pl.dbg_i==10):
                self.beacon_corner1.setPos(my_x * 1000, my_y * 1000)
            elif (pl.dbg_i==20):
                self.beacon_corner2.setPos(my_x * 1000, my_y * 1000)
            elif (pl.dbg_i==30):
                self.beacon_corner3.setPos(my_x * 1000, my_y * 1000)
            elif (pl.dbg_i==40):
                self.beacon_corner4.setPos(my_x * 1000, my_y * 1000)

        self.plot_dbg = self.plot_dbg + 1
        if (self.plot_dbg==10):
            self.plot_dbg = 0
            if (calib_n!=0):
                #print ("{:8.1f}".format(1398.0 - (calib_y/calib_n)))
                pass


