from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTabWidget, QGridLayout, QLabel
from PyQt5.QtGui import QImage, QImageReader, QPixmap
from PyQt5.QtCore import QBuffer
import scapy
from scapy.all import hexdump


class PlotAstarWidget(QtWidgets.QWidget):
    def __init__(self,  parent=None):
        super(PlotAstarWidget, self).__init__(parent)
        #self.resize(1200,400)

        self.test_img_label = QLabel()
        self.test_img_label.resize(320,220)
        #test_img_reader = QImageReader ("/usr/share/cups/calibrate.ppm")
        ##test_img_reader = QImageReader ("test_bitmap.ppm")
        #test_img = test_img_reader.read()
        #test_img_pixmap = QPixmap.fromImage(test_img)
        #self.test_img_label.setPixmap(test_img_pixmap)
        f=open("test_bitmap.ppm","rb")
        my_buff=f.read()
        test_img_pixmap2 = QPixmap()
        test_img_pixmap2.loadFromData(my_buff)
        #result = self.test_img_label.grab(QtCore.QRect(QtCore.QPoint(0, 0), QtCore.QSize(300, 200))).loadFromData(my_buff)
        #print (result)
        self.test_img_label.setPixmap(test_img_pixmap2)
        #self.test_img_label.repaint()

        # set the layout
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.test_img_label)
        self.setLayout(layout)

    def set_client(self, client):
        self._client = client
        self._client.astar_dbg_map.connect(self.update_astar_dbg_map)
        
    def update_astar_dbg_map(self, astar_dbg_map_bytes):
        #print("update_astar_dbg_map()")
        #print(" len(astar_dbg_map_bytes)={}".format(len(astar_dbg_map_bytes)))
        #hexdump(astar_dbg_map_bytes)
        #print("")
        test_img_pixmap2 = QPixmap()
        test_img_pixmap2.loadFromData(astar_dbg_map_bytes)
        self.test_img_label.setPixmap(test_img_pixmap2)



