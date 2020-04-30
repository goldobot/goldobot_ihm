from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QLineEdit, QGridLayout, QFrame, QPushButton, QSpinBox, QSizePolicy
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTabWidget, QGridLayout, QLabel
from PyQt5.QtGui import QImage, QImageReader, QPixmap
from PyQt5.QtCore import QBuffer
import sys
app = QApplication(sys.argv)
test_img_reader = QImageReader ("test_bitmap.ppm")
test_img = test_img_reader.read()
test_img_pixmap = QPixmap.fromImage(test_img)
test_img_label = QLabel()
test_img_label.setPixmap(test_img_pixmap)
layout = QtWidgets.QGridLayout()
layout.addWidget(test_img_label)
_main_widget = QWidget()
_main_widget.setLayout(layout)
main_window = QMainWindow()
main_window.setCentralWidget(_main_widget)
main_window.show()

