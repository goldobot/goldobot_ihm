from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QDial
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import pyqtSignal, QObject

class OffsetDial(QDial):
    offsetChanged = pyqtSignal(float)

    def __init__(self):
        super().__init__()
        self.setMinimum(0)
        self.setMaximum(100)
        self.setWrapping(True)
        self.sliderMoved.connect(self._on_slider_moved)        
        
        self.offset = 0
        self.scale = 1
        self._dial_offset_old = 0

    def sizeHint(self):
        return self.minimumSizeHint()
        
    def _on_slider_moved(self, val: int):
        diff = (val - self._dial_offset_old) % 100
        if diff > 50:
            diff -= 100
        self._dial_offset_old = val
        self.offset = self.offset + diff * 0.01 * self.scale
        self.offsetChanged.emit(self.offset)
        