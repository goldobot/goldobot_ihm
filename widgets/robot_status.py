from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QGridLayout, QLabel, QGridLayout, QFrame
from widgets.properties_editor import PropertiesEditorWidget

class RobotStatusWidget(QWidget):
    def __init__(self, parent = None):
        super(RobotStatusWidget, self).__init__(None)
        self._client = None
        self._time_wid = QLineEdit()
        self._x_wid = QLineEdit()
        self._y_wid = QLineEdit()
        self._button = QPushButton('Emergency Stop')
        self._sensors_wid = QLabel()
        self._gpio_wid = QLabel()

        self._time_wid.setReadOnly(True)

        layout = QGridLayout()
        layout.addWidget(QLabel('time:'),0,0)
        layout.addWidget(self._time_wid,0,1,1,1)
        layout.addWidget(self._sensors_wid,1,1,1,1)
        layout.addWidget(self._gpio_wid,1,2,1,1)

        frame = QFrame()
        frame.setFrameShape(QFrame.HLine)
        layout.addWidget(frame,2,0,1,2)

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

        layout.addWidget(self._telemetry_props,3,0,1,2)
        layout.addWidget(self._telemetry_ex_props,4,0,1,2)
        layout.addWidget(self._button,5,0,1,2)
        self.setLayout(layout)
        self._button.clicked.connect(self._on_emergency_stop_button_clicked)
        self._sensors_wid.setText('sensors')

    def set_client(self, client):
        self._client = client
        self._client.propulsion_telemetry_ex.connect(self.update_telemetry_ex)
        self._client.heartbeat.connect(self.update_heartbeat)
        self._client.propulsion_telemetry.connect(self.update_telemetry)
        self._client.sensors.connect(self.update_sensors)
        self._client.gpio.connect(self.update_gpio)

    def update_heartbeat(self, timestamp):
        self._time_wid.setText(str(timestamp*1e-3))

    def update_telemetry(self, telemetry):
        self._telemetry_props.set_value(telemetry)
    def update_telemetry_ex(self, telemetry_ex):
        self._telemetry_ex_props.set_value(telemetry_ex)
        
    def update_sensors(self, sensors):
        self._sensors_wid.setText('{0:b}'.format(sensors).zfill(6))
        
    def update_gpio(self, sensors):
        self._gpio_wid.setText('{0:b}'.format(sensors).zfill(6))

    def _on_emergency_stop_button_clicked(self):
        self._client.send_message(16,b'')