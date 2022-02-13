from operator import attrgetter
from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QGridLayout

class PropertiesEditorWidget(QWidget):
    def __init__(self, class_, properties, readonly = False, parent = None):
        super(PropertiesEditorWidget, self).__init__(parent)
        self._properties = []
        self._class = class_
        self._widgets = []
        if self._class:
            self._obj = self._class()
        layout = QGridLayout()

        i = 0
        for prop in properties:
            k, t = prop[0:2]
            if len(prop) >=3 and prop[2] is not None:
                fmt_str = prop[2]
                if isinstance(fmt_str, str):
                    fmt = (lambda b: lambda x: b.format(x))(fmt_str)
                else:
                    fmt = fmt_str
            else:
                fmt = lambda x: '{}'.format(x)
                
            self._properties.append((k, t, fmt))                
            wid = QLineEdit(fmt(t()))
            wid.setReadOnly(readonly)
            wid.setFixedWidth(70)
            if (k=='x') or (k=='y'):
                layout.addWidget(QLabel(k+' (mm)'),i,0)
            elif k=='yaw':
                layout.addWidget(QLabel(k+' (°)'),i,0)
            else:
                layout.addWidget(QLabel(k),i,0)
            layout.addWidget(wid,i,1)
            self._widgets.append(wid)
            if not readonly:
                wid.editingFinished.connect(lambda x=i: self._on_editing_finished(x))
            i+=1

        self.setLayout(layout)
        if self._class:
            self._obj = self._class()
        
    def setValue(self, value):
        self.set_value(value)
        
    def set_value(self, obj):
        self._obj = obj
        for i in range(len(self._properties)):
            k, t, fmt = self._properties[i]
            val=attrgetter(k)(obj)
            self._widgets[i].setText(fmt(val))

    def getValue(self):
        return self.get_value()
        
    def get_value(self):
        val = self._obj
        for i in range(len(self._properties)):
            k, t, fmt = self._properties[i]
            fv = t(self._widgets[i].text())
            setattr(val,k,fv)
        return val
        
    def _on_editing_finished(self, i):
        k, t, fmt = self._properties[i]
        fv = t(self._widgets[i].text())
        setattr(self._obj,k,fv)
        val=attrgetter(k)(self._obj)
        self._widgets[i].setText(fmt(val))
