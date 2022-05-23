import weakref

from PyQt5.QtCore import QObject, pyqtSignal, QSize, QRectF, QPointF, Qt

from PyQt5.QtWidgets import QGraphicsPixmapItem

from PyQt5.QtGui import QPen, QColor
from PyQt5.QtGui import QPainterPath, QTransform
from PyQt5.QtGui import QImage, QImageReader, QPixmap



class AstarView:
    def __init__(self, parent):
        self._parent = weakref.ref(parent)
        self._scene = parent._scene
        self._item_group = self._scene.createItemGroup([])
        self._path_item = None
        self._bg_img = None
        
        
        
    
        
    def set_client(self, client):
        self._client = client
        self._client.registerCallback('strategy/debug/astar_arr', self.on_msg_astar)
       
    def on_msg_astar(self, msg):
        image = QImage(msg.value, 300, 200, QImage.Format_Grayscale8)
        image.setColorTable([Qt.black, Qt.white])

        goldo_pixmap = QPixmap()
        goldo_pixmap.convertFromImage(image)
        
        if self._bg_img is not None:
            self._scene.removeItem(self._bg_img)

        self._bg_img = QGraphicsPixmapItem(goldo_pixmap)
        self._bg_img.setTransform(QTransform(1.0, 0.0, 0.0,  0.0, -1.0, 0.0,   0.0, 0.0, 0.1))
        self._bg_img.setRotation(-90)
        self._bg_img.setPos(0, -1500)
        self._bg_img.setZValue(-9)
        self._bg_img.setOpacity(0.2)
        
        self._scene.addItem(self._bg_img)