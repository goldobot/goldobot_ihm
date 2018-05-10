import sys
import signal

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QGridLayout, QFrame, QPushButton, QSpinBox
from PyQt5.QtCore import QObject, pyqtSignal
from messages import OdometryConfig

from zmq_client import ZmqClient


class PropertiesEditorWidget(QWidget):
    def __init__(self, class_, properties, readonly = False, parent = None):
        super(PropertiesEditorWidget, self).__init__(parent)
        self._properties = properties
        self._class = class_
        self._widgets = []
        layout = QGridLayout()

        i = 0
        for k, t in self._properties:
            wid = QLineEdit()
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

class RobotStatusWidget(QWidget):
    def __init__(self, parent = None):
        super(RobotStatusWidget, self).__init__(None)
        self._client = None
        self._time_wid = QLineEdit()
        self._x_wid = QLineEdit()
        self._y_wid = QLineEdit()
        self._button = QPushButton()

        self._time_wid.setReadOnly(True)

        layout = QGridLayout()
        layout.addWidget(QLabel('time:'),0,0)
        layout.addWidget(self._time_wid,0,1,1,1)

        frame = QFrame()
        frame.setFrameShape(QFrame.HLine)
        layout.addWidget(frame,1,0,1,2)

        self._telemetry_props = PropertiesEditorWidget(None,
            [
            ('x', float,),
            ('y', float,),
            ('yaw', float,),
            ('speed', float,),
            ('yaw_rate', float,),
            ('left_encoder', float,),
            ('right_encoder', float,),
            ('left_pwm', float,),
            ('right_pwm', float,)
            ],True)
        layout.addWidget(self._telemetry_props,2,0,1,2)
        self.setLayout(layout)

    def set_client(self, client):
        self._client = client

    def update_heartbeat(self, timestamp):
        self._time_wid.setText(str(timestamp*1e-3))

    def update_telemetry(self, telemetry):
        self._telemetry_props.set_value(telemetry)

class OdometryConfigWidget(QWidget):
    def __init__(self, parent = None):
        super(OdometryConfigWidget, self).__init__(None)
        self._client = None

        self._get_button = QPushButton('Get')
        self._set_button = QPushButton()

        layout = QGridLayout()

        props = PropertiesEditorWidget(OdometryConfig,
            [
            ('dist_per_count_left', float,),
            ('dist_per_count_right', float,),
            ('wheel_spacing', float,),
            ('update_period', float,),
            ('speed_filter_period', float,),
            ('encoder_period', float,)
            ])
        layout.addWidget(props,0,0,1,2)
        self._properties = props       

        layout.addWidget(self._get_button,1,0)
        layout.addWidget(self._set_button,1,1)

        self._get_button.clicked.connect(self.on_get_button_clicked)
        self._set_button.clicked.connect(self.on_set_button_clicked)
        self.setLayout(layout)

    def set_client(self, client):
        self._client = client
        client.odometry_config.connect(self.update_odometry_config)

    def on_get_button_clicked(self):
        if self._client is not None:
            self._client.send_message(65,b'')

    def on_set_button_clicked(self):
        print(self._properties.get_value().__dict__)
        if self._client is not None:
            self._client.send_message(65,b'')

    def update_odometry_config(self, config):
        self._properties.set_value(config)        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    #w = Example()
    c = ZmqClient()

    wid = RobotStatusWidget()
    wid.show()
    wid.set_client(c)

    wid2 = OdometryConfigWidget()
    wid2.set_client(c)
    wid2.show()

    c.heartbeat.connect(lambda ts:wid.update_heartbeat(ts))
    c.propulsion_telemetry.connect(lambda telemetry:wid.update_telemetry(telemetry))
    # Ensure that the application quits using CTRL-C
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    sys.exit(app.exec_())