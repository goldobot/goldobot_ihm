import math
import os

from PyQt5.QtCore import QObject, pyqtSignal, QSize, QRectF, QPointF, Qt

from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtWidgets import QGraphicsPixmapItem

from PyQt5.QtGui import QPolygonF, QPen, QBrush, QColor, QFont, QTransform
from PyQt5.QtGui import QImage, QImageReader, QPixmap


class MyGraphicsScene(QGraphicsScene):
    def mousePressEvent(self, event):
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
    g_rplidar_plot_life_ms = 1000
    g_update_other_robots = False
    g_show_theme = False
    g_debug = False


    def __init__(self, parent = None, ihm_type='pc'):
        super(TableViewWidget, self).__init__(parent)
        if ihm_type=='pc':
            #self.setFixedSize(900,600)
            self.setFixedSize(960,660)
        elif ihm_type=='pc-mini':
            #self.setFixedSize(600,400)
            self.setFixedSize(640,440)
        else:
            #self.setFixedSize(225,150)
            self.setFixedSize(240,165)
        #self.setSceneRect(QRectF(0,-1500,2000,3000))
        self.setSceneRect(QRectF(-100,-1600,2200,3200))
        #self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        redium = QColor.fromCmykF(0,1,1,0.1)
        greenium = QColor.fromCmykF(0.7,0,0.9,0)
        blueium = QColor.fromCmykF(0.9,0.4,0,0)
        goldenium = QColor('white')
        yellow = QColor.fromCmykF(0,0.25,1,0)
        purple = QColor.fromCmykF(0.5,0.9,0,0.05)
        background = QColor(40,40,40)
        darker = QColor(20,20,20)

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

        beacon_poly = QPolygonF([
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

        #self._scene = QGraphicsScene(QRectF(0,-1500,2000,3000))
        #self._scene = QGraphicsScene(QRectF(-100,-1600,2200,3200))
        self._scene = MyGraphicsScene(QRectF(-100,-1600,2200,3200),self)

        self._beacon_left_middle = self._scene.addPolygon(beacon_poly, QPen(), QBrush(QColor('white')))
        self._beacon_left_middle.setZValue(1)
        self._beacon_left_middle.setPos(1000.0, -1573.0)
        self._beacon_right_back = self._scene.addPolygon(beacon_poly, QPen(), QBrush(QColor('white')))
        self._beacon_right_back.setZValue(1)
        self._beacon_right_back.setPos(50.0, 1573.0)
        self._beacon_right_front = self._scene.addPolygon(beacon_poly, QPen(), QBrush(QColor('white')))
        self._beacon_right_front.setZValue(1)
        self._beacon_right_front.setPos(1950.0, 1573.0)

#        self._big_robot = self._scene.addPolygon(big_robot_poly, QPen(), QBrush(QColor('red')))
#        self._big_robot.setZValue(1)
        self._little_robot = self._scene.addPolygon(little_robot_poly, QPen(), QBrush(QColor('red')))
        self._little_robot.setZValue(1)
        # FIXME : DEBUG
        if TableViewWidget.g_debug:
            dbg_plt_sz = 0.2
            self._little_robot_center = self._scene.addEllipse(1000.0 - dbg_plt_sz, -1397.0 - dbg_plt_sz, 2*dbg_plt_sz, 2*dbg_plt_sz, QPen(QBrush(QColor('black')),0.1), QBrush(QColor('yellow')))
            self._little_robot_center.setZValue(100)
            new_p = self._scene.addEllipse(1000.0 - dbg_plt_sz, -1397.0 - dbg_plt_sz, 2*dbg_plt_sz, 2*dbg_plt_sz, QPen(QBrush(QColor('black')),0.1), QBrush(QColor('yellow')))
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

        # Scenario 2020

        #Port principal "bleu"
        self._scene.addRect(QRectF(500,-1120,570,20),QPen(), QBrush(blueium))
        self._scene.addRect(QRectF(500,-1500,30,400),QPen(), QBrush(greenium))
        self._scene.addRect(QRectF(1070,-1500,30,400),QPen(), QBrush(redium))

        #Port secondaire "bleu"
        self._scene.addRect(QRectF(1700,150,20,300),QPen(), QBrush(blueium))
        self._scene.addRect(QRectF(1700,150,300,100),QPen(), QBrush(greenium))
        self._scene.addRect(QRectF(1700,350,300,100),QPen(), QBrush(redium))

        #Bouees cote "bleu"
        self._scene.addEllipse(QRectF(1200-35,-1200-35,70,70),QPen(), QBrush(greenium))
        self._scene.addEllipse(QRectF(1080-35,-1050-35,70,70),QPen(), QBrush(redium))
        self._scene.addEllipse(QRectF(510-35,-1050-35,70,70),QPen(), QBrush(greenium))
        self._scene.addEllipse(QRectF(400-35,-1200-35,70,70),QPen(), QBrush(redium))

        self._scene.addEllipse(QRectF(100-35,-830-35,70,70),QPen(), QBrush(redium))
        self._scene.addEllipse(QRectF(400-35,-550-35,70,70),QPen(), QBrush(greenium))
        self._scene.addEllipse(QRectF(800-35,-400-35,70,70),QPen(), QBrush(redium))
        self._scene.addEllipse(QRectF(1200-35,-230-35,70,70),QPen(), QBrush(greenium))

        self._scene.addEllipse(QRectF(1650-35,-435-35,70,70),QPen(), QBrush(greenium))
        self._scene.addEllipse(QRectF(1650-35,-165-35,70,70),QPen(), QBrush(redium))
        self._scene.addEllipse(QRectF(1955-35,-495-35,70,70),QPen(), QBrush(redium))
        self._scene.addEllipse(QRectF(1955-35,-105-35,70,70),QPen(), QBrush(greenium))

        #Port principal "jaune"
        self._scene.addRect(QRectF(500,1100,570,20),QPen(), QBrush(yellow))
        self._scene.addRect(QRectF(500,1100,30,400),QPen(), QBrush(redium))
        self._scene.addRect(QRectF(1070,1100,30,400),QPen(), QBrush(greenium))

        #Port secondaire "jaune"
        self._scene.addRect(QRectF(1700,-450,20,300),QPen(), QBrush(yellow))
        self._scene.addRect(QRectF(1700,-450,300,100),QPen(), QBrush(greenium))
        self._scene.addRect(QRectF(1700,-250,300,100),QPen(), QBrush(redium))

        #Bouees cote "jaune"
        self._scene.addEllipse(QRectF(1200-35,1200-35,70,70),QPen(), QBrush(redium))
        self._scene.addEllipse(QRectF(1080-35,1050-35,70,70),QPen(), QBrush(greenium))
        self._scene.addEllipse(QRectF(510-35,1050-35,70,70),QPen(), QBrush(redium))
        self._scene.addEllipse(QRectF(400-35,1200-35,70,70),QPen(), QBrush(greenium))

        self._scene.addEllipse(QRectF(100-35,830-35,70,70),QPen(), QBrush(greenium))
        self._scene.addEllipse(QRectF(400-35,550-35,70,70),QPen(), QBrush(redium))
        self._scene.addEllipse(QRectF(800-35,400-35,70,70),QPen(), QBrush(greenium))
        self._scene.addEllipse(QRectF(1200-35,230-35,70,70),QPen(), QBrush(redium))

        self._scene.addEllipse(QRectF(1650-35,435-35,70,70),QPen(), QBrush(redium))
        self._scene.addEllipse(QRectF(1650-35,165-35,70,70),QPen(), QBrush(greenium))
        self._scene.addEllipse(QRectF(1955-35,495-35,70,70),QPen(), QBrush(greenium))
        self._scene.addEllipse(QRectF(1955-35,105-35,70,70),QPen(), QBrush(redium))

        #dbg_plt_sz = 3
        #self._scene.addEllipse(1000 - dbg_plt_sz, 0 - dbg_plt_sz, 2*dbg_plt_sz, 2*dbg_plt_sz, QPen(QBrush(QColor('white')),4), QBrush(QColor('white')))

        self._points = []
        #self.setSceneRect(QRectF(0,-150,200,300))

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
        self._dbg_shift_rot_mm = 0
        self._dbg_rot_cnt = 0

        self.last_plot_ts = 0
        self.plot_graph_l = []

        TableViewWidget.g_table_view = self

    def _add_cubes(self, x, y):
        self._scene.addRect(QRectF(x-29, y-29,58,58))
        self._scene.addRect(QRectF(x-87, y-29,58,58))
        self._scene.addRect(QRectF(x+29, y-29,58,58))
        self._scene.addRect(QRectF(x-29, y-87,58,58))
        self._scene.addRect(QRectF(x-29, y+29,58,58))

    def add_points_for_cubes(self, x, y, dist):
        points = [
        (x-87-dist,y),
        (x,y + 87 + dist),
        (x+87 + dist,y),
        (x,y - 87 - dist)]
        self.add_points(points)

    def add_points_for_cubes_2(self, x, y, dist):
        radius = math.ceil(math.sqrt(29**2+87**2)) + dist
        foo = math.ceil(dist/math.sqrt(2))
        points = [
        (x-radius,y),
        (x-foo,y+foo),
        (x,y+radius),
        ]
        self.add_points(points)


    def add_points(self, points):
        for p in points:
            pt = self._scene.addEllipse(p[0]-10, p[1]-10, 20, 20,  QPen(), QBrush(QColor('grey')))
            pt.setZValue(1)
            self._points.append((pt, p))

    def sizeHint(self):
        return QSize(600,400)

    def set_client(self, client):
        self._client = client
        self._client.propulsion_telemetry.connect(self.update_telemetry)
        self._client.rplidar_plot.connect(self.update_plots)
        self._client.rplidar_robot_detection.connect(self.update_other_robots)
        
    def draw_strategy(self,strategy):
        pass
        

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
            dbg_plt_sz = 0.2
            delta_x_mm = (telemetry.x * 1000 - self._dbg_x_mm)
            delta_y_mm = (telemetry.y * 1000 - self._dbg_y_mm)
            delta_d_mm = math.sqrt(delta_x_mm*delta_x_mm + delta_y_mm*delta_y_mm)
            if (delta_d_mm > 0.1):
                self._dbg_x_mm = telemetry.x * 1000
                self._dbg_y_mm = telemetry.y * 1000
                # new_p = self._scene.addEllipse(self._dbg_x_mm-dbg_plt_sz, self._dbg_y_mm-dbg_plt_sz, 2*dbg_plt_sz, 2*dbg_plt_sz, QPen(QBrush(QColor('black')),0.1), QBrush(QColor('yellow')))
                # new_p.setZValue(100)
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


    def update_plots(self, my_plot):
        dbg_plt_sz = 1
        self.last_plot_ts = my_plot.timestamp
        my_plot_ellipse = self._scene.addEllipse(my_plot.x * 1000 - dbg_plt_sz, my_plot.y * 1000 - dbg_plt_sz, 2*dbg_plt_sz, 2*dbg_plt_sz, QPen(QBrush(QColor('black')),2), QBrush(QColor('red')))
        my_plot_ellipse.setZValue(100)
        self.plot_graph_l.append((my_plot,my_plot_ellipse))
        for rec in self.plot_graph_l:
            if (self.last_plot_ts-rec[0].timestamp>TableViewWidget.g_rplidar_plot_life_ms):
                rec_ellipse = rec[1]
                self._scene.removeItem(rec_ellipse)
                self.plot_graph_l.remove(rec)

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

    def debug_line_to(self, _new_x, _new_y):
        if TableViewWidget.g_show_theme:
            my_segm = self._scene.addLine(self.debug_cur_x, self.debug_cur_y, _new_x, _new_y, QPen(QColor(255,255,255)));
        else:
            my_segm = self._scene.addLine(self.debug_cur_x, self.debug_cur_y, _new_x, _new_y, QPen(QColor(128,128,128)));
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


