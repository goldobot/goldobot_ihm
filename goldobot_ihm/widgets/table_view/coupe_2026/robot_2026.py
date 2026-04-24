from PyQt5.QtWidgets import QLabel
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

import math

little_robot_poly = QPolygonF([
            QPointF(  65, 115),
            QPointF( -65, 115),
            QPointF(-100,  85),
            QPointF(-100, -85),
            QPointF( -65,-115),
            QPointF(  65,-115),
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

little_square = QPolygonF([
            QPointF(  10,  10),
            QPointF( -10,  10),
            QPointF( -10, -10),
            QPointF(  10, -10),
            ])


def cart2pol(x, y):
    rho = math.sqrt(x**2 + y**2)
    phi = math.atan2(y, x)
    return(rho, phi)

def pol2cart(rho, phi):
    x = rho * math.cos(phi)
    y = rho * math.sin(phi)
    return(x, y)


class Robot(QGraphicsItemGroup):
    g_show_detection_radius = True
    g_detection_radius_mm = 400.0
    def __init__(self):
        super().__init__()
        
        self.move_grab = False
        self.turn_grab = False
        
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
        
        path = QPainterPath()
        path.addPolygon(little_square)
        self._little_square = QGraphicsPathItem(path, self)
        self._little_square.setPen(QPen())
        self._little_square.setBrush(QBrush(QColor('yellow')))

        if (Robot.g_show_detection_radius):
            r = Robot.g_detection_radius_mm
            self._detection_circle = QGraphicsEllipseItem(-r, -r, 2*r, 2*r)
            self._detection_circle.setPen(QPen(QBrush(QColor('gray')),0.5))
            self.addToGroup(self._detection_circle)

        self.yaw_deg = 0

    def onMouseMoveTo(self, m_x_mm, m_y_mm):
        self.setPos(m_x_mm, m_y_mm)

    def onMousePointTo(self, m_x_mm, m_y_mm):
        delta_x_mm = m_x_mm - self.x()
        delta_y_mm = m_y_mm - self.y()
        (r, yaw) = cart2pol(delta_x_mm, delta_y_mm)
        self.yaw_deg = yaw * 180 / math.pi
        self.setRotation(yaw * 180 / math.pi)

    def onTelemetry(self, msg):
        self.setPos(msg.pose.position.x * 1000, msg.pose.position.y * 1000)
        self.setRotation(msg.pose.yaw * 180 / math.pi)

    def setRobotPose(self, x_mm, y_mm, yaw_deg):
        self.setPos(x_mm, y_mm)
        self.setRotation(yaw_deg)
        self.yaw_deg = yaw_deg
