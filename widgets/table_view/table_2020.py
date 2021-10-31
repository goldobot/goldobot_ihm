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
        
        
class Table:
    def __init__(self, scene):
        self._scene = scene
        
        f=open("widgets/table_2020_600x400.png","rb")
        my_buff=f.read()
        test_img_pixmap2 = QPixmap()
        test_img_pixmap2.loadFromData(my_buff)
        #self.setPixmap(test_img_pixmap2)
        self._bg_img = QGraphicsPixmapItem(test_img_pixmap2)
        self._bg_img.setTransform(QTransform(1.0, 0.0, 0.0,  0.0, -1.0, 0.0,   0.0, 0.0, 0.2))
        self._bg_img.setRotation(-90)
        self._bg_img.setPos(0, -1500)

        redium = QColor.fromCmykF(0,1,1,0.1)
        greenium = QColor.fromCmykF(0.7,0,0.9,0)
        blueium = QColor.fromCmykF(0.9,0.4,0,0)
        goldenium = QColor('white')
        yellow = QColor.fromCmykF(0,0.25,1,0)
        purple = QColor.fromCmykF(0.5,0.9,0,0.05)
        background = QColor(40,40,40)
        darker = QColor(20,20,20)        

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