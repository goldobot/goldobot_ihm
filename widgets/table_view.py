import math

from PyQt5.QtCore import QObject, pyqtSignal, QSize, QRectF, QPointF, Qt

from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtWidgets import  QGraphicsRectItem

from PyQt5.QtGui import QPolygonF, QPen, QBrush, QColor


class TableViewWidget(QGraphicsView):
    def __init__(self, parent = None):
        super(TableViewWidget, self).__init__(parent)
        self.setFixedSize(1200,900)
        self.setSceneRect(QRectF(0,-1500,2000,3000))
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        redium = QColor.fromCmykF(0,1,1,0.1)
        greenium = QColor.fromCmykF(0.7,0,0.9,0)
        blueium = QColor.fromCmykF(0.9,0.4,0,0)
        goldenium = QColor('white')
        yellow = QColor.fromCmykF(0,0.25,1,0)
        purple = QColor.fromCmykF(0.5,0.9,0,0.05)
        background = QColor(40,40,40)
        darker = QColor(20,20,20)

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

        self._scene.addRect(QRectF(0,-1500,2000,3000),QPen(), QBrush(background))

        #Zones gauche
        self._scene.addRect(QRectF(300,-1500,300,450),QPen(), QBrush(redium))
        self._scene.addRect(QRectF(600,-1500,300,450),QPen(), QBrush(greenium))
        self._scene.addRect(QRectF(900,-1500,300,450),QPen(), QBrush(blueium))
        self._scene.addRect(QRectF(320,-1480,260,410),QPen(), QBrush(background))
        self._scene.addRect(QRectF(620,-1480,260,410),QPen(), QBrush(background))
        self._scene.addRect(QRectF(920,-1480,260,410),QPen(), QBrush(background))

        #Zones droite
        self._scene.addRect(QRectF(300,1050,300,450),QPen(), QBrush(redium))
        self._scene.addRect(QRectF(600,1050,300,450),QPen(), QBrush(greenium))
        self._scene.addRect(QRectF(900,1050,300,450),QPen(), QBrush(blueium))
        self._scene.addRect(QRectF(320,1070,260,410),QPen(), QBrush(background))
        self._scene.addRect(QRectF(620,1070,260,410),QPen(), QBrush(background))
        self._scene.addRect(QRectF(920,1070,260,410),QPen(), QBrush(background))
        #Zones de chaos
        self._scene.addEllipse(QRectF(785,-715,430,430),QPen(), QBrush(darker))
        self._scene.addEllipse(QRectF(785,285,430,430),QPen(), QBrush(darker))
        self._scene.addEllipse(QRectF(825,-675,350,350),QPen(), QBrush(background))
        self._scene.addEllipse(QRectF(825,325,350,350),QPen(), QBrush(background))

        #Balance
        self._scene.addRect(QRectF(1600,-272,400,252),QPen(), QBrush(yellow))
        self._scene.addRect(QRectF(1400,-20,600,40),QPen(), QBrush(background))
        self._scene.addRect(QRectF(1600,20,400,252),QPen(), QBrush(purple))

        #Pente
        self._scene.addRect(QRectF(1600, -1050, 400, 778), QPen(), QBrush(darker))
        self._scene.addRect(QRectF(1600, 272, 400, 778), QPen(), QBrush(darker))

        #Palets
        self._scene.addEllipse(QRectF(412,-1038,76,76),QPen(), QBrush(redium))
        self._scene.addEllipse(QRectF(712,-1038,76,76),QPen(), QBrush(redium))
        self._scene.addEllipse(QRectF(1012,-1038,76,76),QPen(), QBrush(greenium))
        self._scene.addEllipse(QRectF(412,962,76,76),QPen(), QBrush(redium))
        self._scene.addEllipse(QRectF(712,962,76,76),QPen(), QBrush(redium))
        self._scene.addEllipse(QRectF(1012,962,76,76),QPen(), QBrush(greenium))


        self._points = []
        #self.setSceneRect(QRectF(0,-150,200,300))

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
