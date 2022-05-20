import math
import os

from PyQt5.QtCore import QObject, pyqtSignal, QSize, QRectF, QPointF, Qt

from PyQt5.QtWidgets import QLabel

from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtWidgets import QGraphicsItemGroup 
from PyQt5.QtWidgets import QGraphicsEllipseItem
from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtWidgets import QGraphicsPathItem 

from PyQt5.QtGui import QPolygonF, QPen, QBrush, QColor, QFont, QTransform
from PyQt5.QtGui import QImage, QImageReader, QPixmap, QPainterPath

from .table_2022 import Table
from .robot import Robot

import numpy as np
import scipy.interpolate

from .trajectory_view import TrajectoryView
import struct
_lidar_point_struct = struct.Struct('<ff')

        
class AdversaryDetection(QGraphicsItemGroup):
    def __init__(self,id_text):
        super().__init__()
        circle = QGraphicsEllipseItem(-100, -100, 200, 200, parent=self)
        circle.setPen(QPen(QBrush(QColor('blue')),8))
        #self.addEllipse(-100, -100, 200, 200, QPen(QBrush(QColor('black')),4), QBrush(QColor('white')))
        #self.addPolygon(little_robot_poly, QPen(), QBrush(QColor('red')))
        
class DebugTrajectory:
    def __init__(self, scene):
        self._scene = scene
        self._traj_segm_l = []
        self._spline_segm_l = []
        self._edit_point_l = []
        self.cur_x = 0
        self.cur_y = 0
        self._edit_mode = False
        
        
        
    def onMousePress(self, x, y):
        """"x, y in mm"""        
        print ("pix:<{},{}>".format(event.x(),event.y()))
        #realY = 3000.0*(event.x()-450.0)/900.0
        #realX = 2000.0*(event.y())/600.0
        realY = 3200.0*(event.x()-480.0)/960.0
        realX = 2200.0*(event.y()-30.0)/660.0
        print ("real:<{},{}>".format(realX,realY))
        if self._debug_trajectory._edit_mode:
            self._debug_trajectory.line_to(realX, realY)
            
    def onMouseMove(self, x, y):
        """"x, y in mm"""
        return
        
    def onMouseRelease(self, x, y):
        """"x, y in mm"""
        return
        
    def set_start(self, _new_x, _new_y):
        self.cur_x = _new_x
        self.cur_y = _new_y
        if self._debug_edit_mode:
            self._edit_point_l.append((_new_x,_new_y))

    def line_to(self, _new_x, _new_y):
        my_segm = self._scene.addLine(self._cur_x, self._cur_y, _new_x, _new_y, QPen(QColor(128,128,128)));
        self._traj_segm_l.append(my_segm)
        self._edit_point_l.append((_new_x,_new_y))
        self._cur_x = _new_x
        self._cur_y = _new_y
        self.update_spline()

    def clear(self):
        for l in self._traj_segm_l:
            self._scene.removeItem(l)
        self._traj_segm_l = []

    def start_edit(self, _new_x, _new_y):
        self.clear()
        self._edit_mode = True
        self._cur_x = _new_x
        self._cur_y = _new_y
        self._edit_point_l = [(_new_x,_new_y)]

    def stop_edit(self):
        self._edit_mode = False
        return self._sampled_points
        return self._edit_point_l
        
    def update_spline(self):
        # Clear existing segments
        for l in self._spline_segm_l:
            self._scene.removeItem(l)
        self._spline_segm_l = []
            
        #sample spline            
        points = self._edit_point_l
        ctr = np.array([points[0]] + points + [points[-1]])

        #control points, double first and last
        x=ctr[:,0]
        y=ctr[:,1]

        #knots
        l=len(x)
        t=np.linspace(0,1,l-2,endpoint=True)
        t=np.append([0,0,0],t)
        t=np.append(t,[1,1,1])

        tck=[t,[x,y],3]

        num_samples = 16

        u3=np.linspace(0,1,num_samples,endpoint=True)
        out = scipy.interpolate.splev(u3,tck)
        sampled_points = [(out[0][i], out[1][i]) for i in range(num_samples)]
        self._sampled_points = sampled_points
        for i in range(num_samples - 1):
            p1 = sampled_points[i]
            p2 = sampled_points[i+1]
            self._spline_segm_l.append(self._scene.addLine(p1[0], p1[1], p2[0], p2[1], QPen(QColor(128,128,128))));

        
class DebugGraphicsScene(QGraphicsScene):
    dbg_mouse_info = pyqtSignal(float,float,float,float,float)
    def mouseMoveEvent(self, event):
        x_mm = event.scenePos().x()
        y_mm = event.scenePos().y()
        rel_x_mm = x_mm - self.parent()._little_robot_x
        rel_y_mm = y_mm - self.parent()._little_robot_y
        d_mm = math.sqrt(rel_x_mm*rel_x_mm + rel_y_mm*rel_y_mm)
        self.dbg_mouse_info.emit(x_mm, y_mm, rel_x_mm, rel_y_mm, d_mm)

    def mousePressEvent(self, event):
        realX = event.scenePos().x()
        realY = event.scenePos().y()
        #print ("pix:<{},{}>".format(event.x(),event.y()))
        #print ("real:<{},{}>".format(realX,realY))
        if self.parent()._debug_trajectory._edit_mode:
            self.parent()._debug_trajectory.line_to(realX, realY)


class TableViewWidget(QGraphicsView):
    g_table_view = None
    g_detect_size = 200
    g_detect_text = "position"
    #g_detect_text = "quality"
    #g_detect_text = "none"
    g_rplidar_remanence = False
    g_rplidar_plot_life_ms = 1000
    g_show_theme = True
    g_debug = True
    g_dbg_plt_sz = 1.2
    g_dbg_pen_sz = 0.8
    g_debug_astar = True


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
        self.setSceneRect(QRectF(-100,-1600,2200,3200))
        #self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        
        
        self._robots = {}
        self._adversary_detections = {}
        self._waypoints = []
        self._sequences_poses = []
        self._colors = {
            'green': QColor.fromCmykF(0.7,0,0.9,0),
            'blue': QColor.fromCmykF(0.9,0.4,0,0)
            }

        redium = QColor.fromCmykF(0,1,1,0.1)
        greenium = QColor.fromCmykF(0.7,0,0.9,0)
        blueium = QColor.fromCmykF(0.9,0.4,0,0)
        goldenium = QColor('white')
        yellow = QColor.fromCmykF(0,0.25,1,0)
        purple = QColor.fromCmykF(0.5,0.9,0,0.05)
        background = QColor(40,40,40)
        darker = QColor(20,20,20)

        #self._scene = QGraphicsScene(QRectF(-100,-1600,2200,3200))
        self._scene = DebugGraphicsScene(QRectF(-100,-1600,2200,3200),self)
        
        self._layers = {
            'trajectory': TrajectoryView(self)
            }
        
        self._table = Table(self._scene)
        self._bg_img = self._table._bg_img
        self.refreshTheme()

        self._little_robot = Robot()
        self._little_robot.setZValue(1)
        
        self._scene.addItem(self._little_robot)
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
        
        self._lookahead_point = self._scene.addEllipse(0,0, 10, 10, QPen(QBrush(QColor('black')),4), QBrush(QColor('blue')))
        self._lookahead_point.setZValue(2)
        
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
        
        self._debug_trajectory = DebugTrajectory(self._scene)

        self.rotate(90)
        if ihm_type=='pc':
            self.scale(0.3, -0.3)
        elif ihm_type=='pc-mini':
            self.scale(0.2, -0.2)
        else:
            self.scale(0.075, -0.075)

        self._scene.addRect(QRectF(0,-1500,2000,3000))
        

        self._points = []

        self._traj_segm_l = []

        self._little_robot_x = 0
        self._little_robot_y = 0

        self.last_plot_ts = 0
        self.plot_graph_l = []
        
        self._plot_items = []

        self._dbg_x_mm = 0
        self._dbg_y_mm = 0
        self._dbg_l = []
        self._dbg_target_x_mm = 0
        self._dbg_target_y_mm = 0
        self._dbg_target_l = []

        TableViewWidget.g_table_view = self
        
    def refreshTheme(self):
        if TableViewWidget.g_show_theme:
            self._scene.addItem(self._bg_img)
        else:
            self._scene.removeItem(self._bg_img)

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
            
    def addPose(self, x, y, yaw, color = 'green'):
        path = QPainterPath()
        cos_ = math.cos(yaw * math.pi / 180)
        sin_ = math.sin(yaw * math.pi / 180)
        l = 40
        w = 20
        path.moveTo(x + l * cos_, y + l * sin_)
        path.lineTo(x -l * cos_ + w * sin_, y - l * sin_ - w * cos_)
        path.lineTo(x -l * cos_ - w * sin_, y - l * sin_ + w * cos_)
        path.closeSubpath()
        itm = self._scene.addPath(path, QPen(), QBrush(self._colors[color]))
        itm.setZValue(2)
        return itm
        
    def addPoint(self, x, y, color = 'green'):
        itm = self._scene.addEllipse(x-10, y-10, 20, 20,  QPen(), QBrush(self._colors[color]))
        itm.setZValue(2)
        return itm
        
    def addTrajectory(self, points):
        path = QPainterPath()
        p = points[0]
        path.moveTo(p[0] * 1000, p[1] * 1000)
        for p in points[1:]: 
            path.lineTo(p[0] * 1000, p[1] * 1000)
        greenium = QColor.fromCmykF(0.7,0,0.9,0)        
        itm = self._scene.addPath(path)
        pen = QPen()
        pen.setWidth(3)
        itm.setPen(pen)
        itm.setZValue(3)
        return itm
        
    def sizeHint(self):
        return QSize(600,400)

    def set_client(self, client):
        self._client = client
        for layer in self._layers.values():
            layer.set_client(client)
        self._client.propulsion_telemetry.connect(self.update_telemetry)
        self._client.propulsion_telemetry_ex.connect(self.update_telemetry_ex)
        self._client.rplidar_plot.connect(self.update_plots)
        self._client.rplidar_robot_detection.connect(self.update_other_robots)        
        self._client.registerCallback('gui/in/robot_state', self.on_msg_robot_state)
        
        self._client.registerCallback('strategy/debug/astar_arr', self.on_msg_astar)
        
    def set_config(self, config):     
        poses = config.BluePoses.__dict__
        for itm in self._sequences_poses:
            self._scene.removeItem(itm)
        self._sequences_poses = []
        for k, v in poses.items():
            if not k.startswith('_') and isinstance(v, tuple):
                itm = self.addPose(v[0] * 1000, v[1] * 1000, v[2])
                self._sequences_poses.append(itm)
            if not k.startswith('_') and isinstance(v, np.ndarray):
                itm = self.addPoint(v[0] * 1000, v[1] * 1000, 'blue')
                self._sequences_poses.append(itm)
            if not k.startswith('_') and isinstance(v, list):
                itm = self.addTrajectory(v)
                self._sequences_poses.append(itm)
            
        
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
                
            
        
    def on_msg_astar(self, msg):
        if not TableViewWidget.g_debug_astar:
            return
        image = QImage(msg.value, 300, 200, QImage.Format_Grayscale8)
        image.setColorTable([Qt.black, Qt.white])
        #self._astar_label = QLabel()
        #self._astar_label.setPixmap(QPixmap(image))
        #self._astar_label.show()
        #print(image)
        goldo_pixmap = QPixmap()
        goldo_pixmap.convertFromImage(image)
        self._scene.removeItem(self._bg_img)
        self._bg_img = QGraphicsPixmapItem(goldo_pixmap)
        self._bg_img.setTransform(QTransform(1.0, 0.0, 0.0,  0.0, -1.0, 0.0,   0.0, 0.0, 0.1))
        self._bg_img.setRotation(-90)
        self._bg_img.setPos(0, -1500)
        self._bg_img.setZValue(-1)
        if TableViewWidget.g_show_theme:
            self._scene.addItem(self._bg_img)
        
    def update_telemetry(self, telemetry):
        self._little_robot.onTelemetry(telemetry)        
        
        self._little_robot_x = telemetry.pose.position.x * 1000
        self._little_robot_y = telemetry.pose.position.y * 1000
        
        if TableViewWidget.g_debug:
            dbg_plt_sz = TableViewWidget.g_dbg_plt_sz
            dbg_pen_sz = TableViewWidget.g_dbg_pen_sz
            self._little_robot_center.setPos(telemetry.pose.position.x * 1000, telemetry.pose.position.y * 1000)
            delta_x_mm = (telemetry.pose.position.x * 1000 - self._dbg_x_mm)
            delta_y_mm = (telemetry.pose.position.y * 1000 - self._dbg_y_mm)
            delta_d_mm = math.sqrt(delta_x_mm*delta_x_mm + delta_y_mm*delta_y_mm)
            if (delta_d_mm > 0.1):
                self._dbg_x_mm = telemetry.pose.position.x * 1000
                self._dbg_y_mm = telemetry.pose.position.y * 1000
                new_p = self._scene.addEllipse(self._dbg_x_mm-dbg_plt_sz, self._dbg_y_mm-dbg_plt_sz, 2*dbg_plt_sz, 2*dbg_plt_sz, QPen(QBrush(QColor('black')),dbg_pen_sz), QBrush(QColor('yellow')))
                new_p.setZValue(100)
                self._dbg_l.append(new_p)

    def update_telemetry_ex(self, telemetry_ex):
        if TableViewWidget.g_debug:
            dbg_plt_sz = TableViewWidget.g_dbg_plt_sz
            dbg_pen_sz = TableViewWidget.g_dbg_pen_sz
            delta_x_mm = (telemetry_ex.target_pose.position.x * 1000 - self._dbg_target_x_mm)
            delta_y_mm = (telemetry_ex.target_pose.position.y * 1000 - self._dbg_target_y_mm)
            delta_d_mm = math.sqrt(delta_x_mm*delta_x_mm + delta_y_mm*delta_y_mm)

            try:
                self._lookahead_point.setPos(telemetry_ex.lookahead_position.x * 1000, telemetry_ex.lookahead_position.y * 1000)
            except:
                pass
            
            if (delta_d_mm > 0.1):
                self._dbg_target_x_mm = telemetry_ex.target_pose.position.x * 1000
                self._dbg_target_y_mm = telemetry_ex.target_pose.position.y * 1000
                new_p = self._scene.addEllipse(self._dbg_target_x_mm-dbg_plt_sz, self._dbg_target_y_mm-dbg_plt_sz, 2*dbg_plt_sz, 2*dbg_plt_sz, QPen(QBrush(QColor('blue')),dbg_pen_sz), QBrush(QColor('red')))
                new_p.setZValue(100)
                self._dbg_target_l.append(new_p)

    def clear_telemetry(self):
        for itm in self._dbg_l:
            self._scene.removeItem(itm)
        self._dbg_l = []
        for itm in self._dbg_target_l:
            self._scene.removeItem(itm)
        self._dbg_target_l = []

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
        self._debug_trajectory.set_start(_new_x, _new_y)        

    def debug_line_to(self, _new_x, _new_y):
        my_segm = self._scene.addLine(self.debug_cur_x, self.debug_cur_y, _new_x, _new_y, QPen(QColor(128,128,128)));
        self._traj_segm_l.append(my_segm)
        self.debug_cur_x = _new_x
        self.debug_cur_y = _new_y

    def debug_clear_lines(self):
        self._debug_trajectory.clear()

    def debug_start_edit(self, _new_x, _new_y):
        self._debug_trajectory.start_edit(_new_x, _new_y)

    def debug_start_edit_rel(self):
        self._debug_trajectory.start_edit(self._little_robot_x, self._little_robot_y)

    def debug_stop_edit(self):
        return self._debug_trajectory.stop_edit()

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


