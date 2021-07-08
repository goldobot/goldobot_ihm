import math
import os

from PyQt5.QtCore import QObject, pyqtSignal, QSize, QRectF, QPointF, Qt

from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtWidgets import QGraphicsItemGroup 
from PyQt5.QtWidgets import QGraphicsEllipseItem
from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtWidgets import QGraphicsPathItem 

from PyQt5.QtGui import QPolygonF, QPen, QBrush, QColor, QFont, QTransform
from PyQt5.QtGui import QImage, QImageReader, QPixmap, QPainterPath

import struct
_lidar_point_struct = struct.Struct('<ff')


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
            
near_poly = QPolygonF([
            QPointF(  10, 10),
            QPointF(  10, -10),
            QPointF(  30, -30),
            QPointF(  30, 30),
            QPointF(  10, 10),            
            ])
            
far_poly = QPolygonF([
            QPointF(  30, 30),
            QPointF(  30, -30),
            QPointF(  50, -50),
            QPointF(  50, 50),
            QPointF(  30, 30),            
            ])
            
            
class Robot(QGraphicsItemGroup):
    def __init__(self):
        super().__init__()
        
        path = QPainterPath()
        path.addPolygon(little_robot_poly)
        #p = little_robot_poly[0}
        #path.moveTo(p.x * 1000, p.y * 1000)
        
        outline = QGraphicsPathItem(path, self)
        outline.setPen(QPen())
        outline.setBrush(QBrush(QColor('red')))
        
        path = QPainterPath()
        path.addPolygon(near_poly)
        self._near_front = QGraphicsPathItem(path, self)
        self._near_front.setPen(QPen())
        self._near_front.setBrush(QBrush(QColor('green')))
        
        path = QPainterPath()
        path.addPolygon(far_poly)
        self._far_front = QGraphicsPathItem(path, self)
        self._far_front.setPen(QPen())
        self._far_front.setBrush(QBrush(QColor('green')))
        
        path = QPainterPath()
        path.addPolygon(near_poly)
        self._near_back = QGraphicsPathItem(path, self)
        self._near_back.setPen(QPen())
        self._near_back.setBrush(QBrush(QColor('green')))
        self._near_back.setRotation(180)
        
        path = QPainterPath()
        path.addPolygon(far_poly)
        self._far_back = QGraphicsPathItem(path, self)
        self._far_back.setPen(QPen())
        self._far_back.setBrush(QBrush(QColor('green')))
        self._far_back.setRotation(180)
        
        
        #self.addPolygon(little_robot_poly, QPen(), QBrush(QColor('red')))
        
class AdversaryDetection(QGraphicsItemGroup):
    def __init__(self,id_text):
        super().__init__()
        circle = QGraphicsEllipseItem(-100, -100, 200, 200, parent=self)
        circle.setPen(QPen(QBrush(QColor('black')),4))
        #self.addEllipse(-100, -100, 200, 200, QPen(QBrush(QColor('black')),4), QBrush(QColor('white')))
        #self.addPolygon(little_robot_poly, QPen(), QBrush(QColor('red')))
        
        
class TableViewWidget(QGraphicsView):
    g_table_view = None
    g_detect_size = 200
    g_detect_text = "position"
    #g_detect_text = "quality"
    #g_detect_text = "none"
    g_rplidar_remanence = False
    g_rplidar_plot_life_ms = 1000


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
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self._robots = {}
        self._adversary_detections = {}
        self._waypoints = []

        redium = QColor.fromCmykF(0,1,1,0.1)
        greenium = QColor.fromCmykF(0.7,0,0.9,0)
        blueium = QColor.fromCmykF(0.9,0.4,0,0)
        goldenium = QColor('white')
        yellow = QColor.fromCmykF(0,0.25,1,0)
        purple = QColor.fromCmykF(0.5,0.9,0,0.05)
        background = QColor(40,40,40)
        darker = QColor(20,20,20)


        


        self._scene = QGraphicsScene(QRectF(-100,-1600,2200,3200))

#        self._big_robot = self._scene.addPolygon(big_robot_poly, QPen(), QBrush(QColor('red')))
#        self._big_robot.setZValue(1)
        #self._robots['little'] = Robot(self._scene)
        self._little_robot = Robot()
        self._little_robot.setZValue(1)
        self._scene.addItem(self._little_robot)
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
        if ihm_type=='pc':
            self.scale(0.3, -0.3)
        elif ihm_type=='pc-mini':
            self.scale(0.2, -0.2)
        else:
            self.scale(0.075, -0.075)

        #self._scene.addRect(QRectF(0,-1500,2000,3000),QPen(), QBrush(background))

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

        self.last_plot_ts = 0
        self.plot_graph_l = []
        
        self._plot_items = []

        TableViewWidget.g_table_view = self
        
    def set_strategy(self, strategy):
        greenium = QColor.fromCmykF(0.7,0,0.9,0)
        #greenium.setAlphaF(0.2)
        for id_, pos in strategy['strategy']['map']['waypoints'].items():
            wp = self._scene.addEllipse(QRectF(pos[0]-10,pos[1]-10,20,20),QPen(), QBrush(greenium))
            self._waypoints.append(wp)
        for id_, pose in strategy['strategy']['map']['poses'].items():
            p = strategy['strategy']['map']['waypoints'][pose[0]]
            path = QPainterPath()
            cos_ = math.cos(pose[1] * math.pi / 180)
            sin_ = math.sin(pose[1] * math.pi / 180)
            l = 40
            w = 20
            path.moveTo(p[0] + l * cos_, p[1] + l * sin_)
            path.lineTo(p[0] -l * cos_ + w * sin_, p[1] - l * sin_ - w * cos_)
            path.lineTo(p[0] -l * cos_ - w * sin_, p[1] - l * sin_ + w * cos_)
            path.closeSubpath()
            itm = self._scene.addPath(path, QPen(), QBrush(greenium))
            
        for id_, area in strategy['strategy']['map']['areas'].items():
            path = QPainterPath()
            v = area['vertices'][0]
            path.moveTo(v[0], v[1])
            for v in area['vertices'][1:]: 
                path.lineTo(v[0], v[1])
            path.closeSubpath()
            itm = self._scene.addPath(path, QPen(), QBrush(greenium))
            self._waypoints.append(wp)


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
        self._client.registerCallback('nucleo/in/propulsion/cmd/trajectory', self.on_msg_trajectory)
        self._client.registerCallback('gui/in/robot_state', self.on_msg_robot_state)
        
    def on_msg_robot_state(self, msg):
        for d in msg.rplidar.detections:
            if d.id not in self._adversary_detections:
                ad = AdversaryDetection(str(d.id))
                self._adversary_detections[d.id] = ad
                ad.setZValue(1)
                self._scene.addItem(ad)
            ad = self._adversary_detections[d.id]
            ad.setPos(d.x * 1000, d.y * 1000)
        zones = msg.rplidar.zones
        self._little_robot._near_front.setBrush(QBrush(QColor('red' if zones.front_near else 'green')))
        self._little_robot._far_front.setBrush(QBrush(QColor('red' if zones.front_far else 'green')))
        self._little_robot._near_back.setBrush(QBrush(QColor('red' if zones.back_near else 'green')))
        self._little_robot._far_back.setBrush(QBrush(QColor('red' if zones.back_far else 'green')))
                
            
        
        
        
    def on_msg_trajectory(self, msg):
        path = QPainterPath()
        p = msg.points[0]
        path.moveTo(p.x * 1000, p.y * 1000)
        for p in msg.points[1:]: 
            path.lineTo(p.x * 1000, p.y * 1000)
        greenium = QColor.fromCmykF(0.7,0,0.9,0)        
        itm = self._scene.addPath(path)
        pen = QPen()
        pen.setWidth(3)
        itm.setPen(pen)
        self._path_trajectory = itm
        
    def update_telemetry(self, telemetry):
#        self._big_robot.setPos(telemetry.x * 1000, telemetry.y * 1000)
#        self._big_robot.setRotation(telemetry.yaw * 180 / math.pi)
#        self._big_robot_x = telemetry.x * 1000
#        self._big_robot_y = telemetry.y * 1000
        self._little_robot.setPos(telemetry.pose.position.x * 1000, telemetry.pose.position.y * 1000)
        self._little_robot.setRotation(telemetry.pose.yaw * 180 / math.pi)
        self._little_robot_x = telemetry.pose.position.x * 1000
        self._little_robot_y = telemetry.pose.position.y * 1000

    def update_plots(self, my_plot):
        dbg_plt_sz = 1
        for i in self._plot_items:
            self._scene.removeItem(i)
        self._plot_items = []
        
        for i in range(my_plot.num_points):
            x, y = _lidar_point_struct.unpack(my_plot.data[i*8:(i+1)*8])
            itm = self._scene.addEllipse(x * 1000 - dbg_plt_sz, y * 1000 - dbg_plt_sz, 2*dbg_plt_sz, 2*dbg_plt_sz, QPen(QBrush(QColor('red')),4), QBrush(QColor('red')))
            self._plot_items.append(itm)
            
        #self.last_plot_ts = my_plot.timestamp
        return


    def update_other_robots(self, other_robot):
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
        my_segm = self._scene.addLine(self.debug_cur_x, self.debug_cur_y, _new_x, _new_y, QPen(QColor(255,255,255)));
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

    def mousePressEvent(self, event):
        print ("pix:<{},{}>".format(event.x(),event.y()))
        #realY = 3000.0*(event.x()-450.0)/900.0
        #realX = 2000.0*(event.y())/600.0
        realY = 3200.0*(event.x()-480.0)/960.0
        realX = 2200.0*(event.y()-30.0)/660.0
        print ("real:<{},{}>".format(realX,realY))
        if self._debug_edit_mode:
            self._debug_edit_point_l.append((realX,realY))
            self.debug_line_to(realX, realY)


