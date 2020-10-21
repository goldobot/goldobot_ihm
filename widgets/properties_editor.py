import math
from operator import attrgetter
from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QGridLayout

class PropertiesEditorWidget(QWidget):
    def __init__(self, class_, properties, readonly = False, parent = None):
        super(PropertiesEditorWidget, self).__init__(parent)
        self._properties = properties
        self._class = class_
        self._widgets = []
        layout = QGridLayout()

        i = 0
        for k, t in self._properties:
            wid = QLineEdit(str(t()))
            wid.setReadOnly(readonly)       
            if (k=='x') or (k=='y'):
                layout.addWidget(QLabel(k+' (mm)'),i,0)
            elif k=='yaw':
                layout.addWidget(QLabel(k+' (°)'),i,0)
            else:
                layout.addWidget(QLabel(k),i,0)
            layout.addWidget(wid,i,1)
            self._widgets.append(wid)
            i+=1

        self.setLayout(layout)

    def set_value(self, obj):
        for i in range(len(self._properties)):
            k, t = self._properties[i]
            val=attrgetter(k)(obj)
            if (k=='pose.position.x') or (k=='pose.position.y'):
                val=val*1000.0
                self._widgets[i].setText("%.1f"%val)
            elif k=='pose.yaw':
                val=val*180.0/math.pi
                self._widgets[i].setText("%.1f"%val)
            else:
                self._widgets[i].setText(str(val))

    def get_value(self):
        val = self._class()
        for i in range(len(self._properties)):
            k, t = self._properties[i]
            fv = t(self._widgets[i].text())
            setattr(val,k,fv)
        return val
