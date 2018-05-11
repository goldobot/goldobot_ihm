import math

from PyQt5.QtCore import QObject, pyqtSignal, QSize, QRectF, QPointF, Qt

from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtWidgets import  QGraphicsRectItem

from PyQt5.QtGui import QPolygonF, QPen, QBrush, QColor


class TableViewWidget(QGraphicsView):
    def __init__(self, parent = None):
        super(TableViewWidget, self).__init__(parent)
        self.setFixedSize(1200,800)
        self.setSceneRect(QRectF(0,-1500,2000,3000))
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)



        big_robot_poly = QPolygonF([
            QPointF(-135,-151),
            QPointF(60,-151),
            QPointF(170,-91),
            QPointF(170,-45),
            QPointF(111,-40),
            QPointF(111,40),
            QPointF(170,45),
            QPointF(170,91),
            QPointF(60,151),
            QPointF(-135,151)
            ])
        self._scene = QGraphicsScene(QRectF(0,-1500,2000,3000))
        self._big_robot = self._scene.addPolygon(big_robot_poly, QPen(), QBrush(QColor('red')))
        self._big_robot.setZValue(1)
        self.setScene(self._scene)
        
        self.rotate(90)
        self.scale(0.4, -0.4)

        self._scene.addRect(QRectF(0,-1500,2000,3000))
        self._scene.addRect(QRectF(0,1100,650,400),QPen(), QBrush(QColor('orange')))
        self._scene.addRect(QRectF(0,-1500,650,400),QPen(), QBrush(QColor('green')))

        pen = QPen(QColor('orange'))
        pen.setWidth(8)
        self._scene.addRect(QRectF(0,540,180,560),pen, QBrush())

        pen = QPen(QColor('green'))
        pen.setWidth(8)
        self._scene.addRect(QRectF(0,-1100,180,560),pen, QBrush())

        self._add_cubes(540,-1500+850)
        self._add_cubes(540,1500-850)
        self._add_cubes(1190,-1500+300)
        self._add_cubes(1190,1500-300)
        self._add_cubes(1500,-1500+1100)
        self._add_cubes(1500,1500-1100)

        self._points = []

        points = [(240, -1320)]
        self.add_points( [(240, -1280), (240, 1280)])

        self.add_points_for_cubes(540,-1500+850,110)
        self.add_points_for_cubes_2(540,-1500+850,220)

        self.add_points_for_cubes(1190,-1500+300,110)
        self.add_points_for_cubes(1190,-1500+300,220)

        self.add_points_for_cubes(1500,-1500+1100,110)
        self.add_points_for_cubes(1500,-1500+1100,220)

        # add points

        

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

    def update_telemetry(self, telemetry):
        self._big_robot.setPos(telemetry.x * 1000, telemetry.y * 1000)
        self._big_robot.setRotation(telemetry.yaw * 180 / math.pi)