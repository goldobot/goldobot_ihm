import weakref

from PyQt5.QtWidgets import QGraphicsItemGroup 

from PyQt5.QtGui import QPen, QColor
from PyQt5.QtGui import QPainterPath



class TrajectoryView:
    def __init__(self, parent):
        self._parent = weakref.ref(parent)
        self._scene = parent._scene
        self._item_group = self._scene.createItemGroup([])
        self._path_item = None
        
    def set_client(self, client):
        self._client = client
        self._client.registerCallback('nucleo/in/propulsion/cmd/trajectory', self.on_msg_trajectory)       
       
    def update_trajectory(self, points):
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
        if self._path_item is None:
            self._scene.removeItem(self._path_item)
        self._item_group.addToGroup(itm)
        self._path_item = itm
        
    def on_msg_move(self, msg):
        path = QPainterPath()
        
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