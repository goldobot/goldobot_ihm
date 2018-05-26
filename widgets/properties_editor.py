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
            layout.addWidget(QLabel(k),i,0)
            layout.addWidget(wid,i,1)
            self._widgets.append(wid)
            i+=1

        self.setLayout(layout)

    def set_value(self, obj):
        for i in range(len(self._properties)):
            k, t = self._properties[i]
            self._widgets[i].setText(str(getattr(obj,k)))

    def get_value(self):
        val = self._class()
        for i in range(len(self._properties)):
            k, t = self._properties[i]
            fv = t(self._widgets[i].text())
            setattr(val,k,fv)
        return val