import sys
import signal
import math

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QGridLayout, QFrame, QPushButton, QSpinBox, QSizePolicy
from PyQt5.QtCore import QObject, pyqtSignal, QSize, QRectF, QPointF, Qt
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PyQt5.QtGui import QPolygonF, QPen, QBrush, QColor

from widgets.table_view import TableViewWidget
from messages import OdometryConfig
from messages import PIDConfig
from messages import PropulsionControllerConfig

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
        self._button = QPushButton('Emergency Stop')

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
            ('acceleration', float),
            ('angular_acceleration', float),
            ('left_encoder', float,),
            ('right_encoder', float,),
            ('left_pwm', float,),
            ('right_pwm', float,),
            ('state', int),
            ('error',int)
            ],True)

        self._telemetry_ex_props = PropertiesEditorWidget(None,
            [
            ('target_x', float,),
            ('target_y', float,),
            ('target_yaw', float,),
            ('target_speed', float,),
            ('target_yaw_rate', float,),
            ('longitudinal_error', float,),
            ('lateral_error', float,)  
            ],True)

        layout.addWidget(self._telemetry_props,2,0,1,2)
        layout.addWidget(self._telemetry_ex_props,3,0,1,2)
        layout.addWidget(self._button,4,0,1,2)
        self.setLayout(layout)
        self._button.clicked.connect(self._on_emergency_stop_button_clicked)

    def set_client(self, client):
        self._client = client
        self._client.propulsion_telemetry_ex.connect(self.update_telemetry_ex)

    def update_heartbeat(self, timestamp):
        self._time_wid.setText(str(timestamp*1e-3))

    def update_telemetry(self, telemetry):
        self._telemetry_props.set_value(telemetry)
    def update_telemetry_ex(self, telemetry_ex):
        self._telemetry_ex_props.set_value(telemetry_ex)

    def _on_emergency_stop_button_clicked(self):
        self._client.send_message(16,b'')

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
            self._client.send_message(64,b'')

    def on_set_button_clicked(self):
        print(self._properties.get_value().__dict__)
        if self._client is not None:
            self._client.send_message(65,b'')

    def update_odometry_config(self, config):
        self._properties.set_value(config)        


class PropulsionControllerConfigWidget(QWidget):
    def __init__(self, parent = None):
        super(PropulsionControllerConfigWidget, self).__init__(None)
        self._client = None

        self._get_button = QPushButton('Get')
        self._set_button = QPushButton('Set')

        layout = QGridLayout()

        pid_props = [
            ('period', float,),
            ('kp', float,),
            ('kd', float,),
            ('ki', float,),
            ('feed_forward', float,),
            ('lim_iterm', float,),
            ('lim_dterm', float,),
            ('min_output', float,),
            ('max_output', float,)
            ]

        tab_widget = QTabWidget()

        self._speed_pid_props = PropertiesEditorWidget(PIDConfig, pid_props)
        tab_widget.addTab(self._speed_pid_props, "speed")

        #layout.addWidget(self._speed_pid_props,0,0,1,2)

        self._yaw_rate_pid_props = PropertiesEditorWidget(PIDConfig,pid_props)
        tab_widget.addTab(self._yaw_rate_pid_props, "yaw_rate")
        #layout.addWidget(self._yaw_rate_pid_props,0,2,1,2)
        layout.addWidget(tab_widget,0,2,1,2)

        self._translation_pid_props = PropertiesEditorWidget(PIDConfig,pid_props)
        layout.addWidget(self._translation_pid_props,1,0,1,2)

        self._yaw_pid_props = PropertiesEditorWidget(PIDConfig,pid_props)
        layout.addWidget(self._yaw_pid_props,1,2,1,2)

        self._props = PropertiesEditorWidget(PropulsionControllerConfig, [
            ('lookahead_distance', float,),
            ('lookahead_time', float,),
            ('static_pwm_limit', float,),
            ('moving_pwm_limit', float,),
            ('repositioning_pwm_limit', float,)
            ])
        layout.addWidget(self._props,2,0,1,2)   

        layout.addWidget(self._get_button,4,0)
        layout.addWidget(self._set_button,4,1)

        self._get_button.clicked.connect(self.on_get_button_clicked)
        self._set_button.clicked.connect(self.on_set_button_clicked)
        self.setLayout(layout)

    def set_client(self, client):
        self._client = client
        client.propulsion_controller_config.connect(self.update_propulsion_controller_config)

    def on_get_button_clicked(self):
        if self._client is not None:
            self._client.send_message(66,b'')

    def on_set_button_clicked(self):
        config = self._props.get_value()
        config.speed_pid_config = self._speed_pid_props.get_value()
        config.yaw_rate_pid_config = self._yaw_rate_pid_props.get_value()
        config.translation_pid_config = self._translation_pid_props.get_value()
        config.yaw_pid_config = self._yaw_pid_props.get_value()
        if self._client is not None:
            self._client.send_message(67,config.serialize())

    def update_propulsion_controller_config(self, config):
        self._speed_pid_props.set_value(config.speed_pid_config)
        self._yaw_rate_pid_props.set_value(config.yaw_rate_pid_config)
        self._translation_pid_props.set_value(config.translation_pid_config)
        self._yaw_pid_props.set_value(config.yaw_pid_config)
        self._props.set_value(config)

class ServoWidget(QWidget):
    def __init__(self, parent = None):
        super(ServoWidgetWidget, self).__init__(None)
        self._client = None
        wid = QLineEdit()

        self._get_button = QPushButton('Get')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    #w = Example()
    c = ZmqClient()

    wid = RobotStatusWidget()
    wid.show()
    wid.set_client(c)

    wid2 = OdometryConfigWidget()
    wid2.set_client(c)
    wid2.show()

    wid3 = TableViewWidget()
    wid3.set_client(c)
    wid3.show()

    wid4 = PropulsionControllerConfigWidget()
    wid4.set_client(c)
    wid4.show()

    c.heartbeat.connect(lambda ts:wid.update_heartbeat(ts))
    c.propulsion_telemetry.connect(lambda telemetry:wid.update_telemetry(telemetry))
    # Ensure that the application quits using CTRL-C
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    sys.exit(app.exec_())