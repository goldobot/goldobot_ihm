from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QGridLayout, QLabel, QGridLayout, QFrame
from widgets.properties_editor import PropertiesEditorWidget
import math

_controller_state = {
    0: 'Inactive',
    1: 'Stopped',
    2: 'FollowTrajectory',
    3: 'Rotate',
    4: 'Reposition',
    5: 'ManualControl',
    6: 'EmergencyStop',
    7: 'Error'
    }
    
_controller_error = {
    0: 'None',
    1: 'EmergencyStop',
    2: 'RobotBlocked',
    3: 'TrackingError'
    }

class RobotStatusWidget(QWidget):
    def __init__(self, parent = None, ihm_type='pc'):
        super(RobotStatusWidget, self).__init__(None)
        self._client = None
        self._time_wid = QLineEdit()
        self._x_wid = QLineEdit()
        self._y_wid = QLineEdit()
        self._button = QPushButton('Emergency Stop')
        self._robot_state_wid = QLineEdit('')
        self._robot_side_wid = QLineEdit('')
        self._sensors_wid = QLabel()
        self._gpio_wid = QLabel()
        self._debug_goldo_wid = QLabel()

        self._time_wid.setReadOnly(True)

        layout = QGridLayout()
        layout.addWidget(QLabel('time:'),0,0)
        layout.addWidget(self._time_wid,0,1,1,1)
        layout.addWidget(QLabel('DbgGoldo:'),0,2,1,1)
        layout.addWidget(self._debug_goldo_wid,0,3,1,1)
        layout.addWidget(self._robot_state_wid,1,0,1,1)
        layout.addWidget(self._robot_side_wid,1,1,1,1)
        layout.addWidget(self._sensors_wid,1,2,1,1)
        layout.addWidget(self._gpio_wid,1,3,1,1)

        frame = QFrame()
        frame.setFrameShape(QFrame.HLine)
        layout.addWidget(frame,2,0,1,2)

        if ihm_type=='pc':
            self._telemetry_props = PropertiesEditorWidget(None,
                [
                ('pose.position.x', float, lambda x: '{:0>6.1f}'.format(x *1000.0)),
                ('pose.position.y', float, lambda x: '{:0>6.1f}'.format(x *1000.0)),
                ('pose.yaw', float, lambda x: '{:0>5.1f}'.format(x * 180.0/math.pi)),
                ('pose.speed', float, '{:0>3.2f}'),
                ('pose.yaw_rate', float, '{:0>3.2f}'),
                ('pose.acceleration', float),
                ('pose.angular_acceleration', float),
                ('left_encoder', float, '{:0>4}'),
                ('right_encoder', float, '{:0>4}'),
                ('left_pwm', float,),
                ('right_pwm', float,),
                ('state', int, lambda x: _controller_state[x]),
                ('error',int,  lambda x: _controller_error[x])
                ],True)
        else:
            self._telemetry_props = PropertiesEditorWidget(None,
                [
                ('x', float,),
                ('y', float,),
                ('yaw', float,)
                ],True)

        if ihm_type=='pc':
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
        else:
            self._telemetry_ex_props = PropertiesEditorWidget(None,
                [
                ],True)

        layout.addWidget(self._telemetry_props,3,0,1,2)
        layout.addWidget(self._telemetry_ex_props,4,0,1,2)
        layout.addWidget(self._button,5,0,1,2)
        self.setLayout(layout)
        self._button.clicked.connect(self._on_emergency_stop_button_clicked)
        self._sensors_wid.setText('sensors')

        self.goldo_dbg_info = 0

    def set_client(self, client):
        self._client = client
        self._client.propulsion_telemetry_ex.connect(self.update_telemetry_ex)
        self._client.heartbeat.connect(self.update_heartbeat)
        self._client.propulsion_telemetry.connect(self.update_telemetry)
        self._client.sensors.connect(self.update_sensors)
        self._client.gpio.connect(self.update_gpio)
        self._client.debug_goldo.connect(self.update_debug_goldo)
        self._client.match_state_change.connect(self.match_state_change)

    def update_heartbeat(self, timestamp):
        self._time_wid.setText("%.1f"%(timestamp*1e-3))

    def update_telemetry(self, telemetry):
        self._telemetry_props.set_value(telemetry)
    def update_telemetry_ex(self, telemetry_ex):
        self._telemetry_ex_props.set_value(telemetry_ex)
        
    def update_sensors(self, sensors):
        self._sensors_wid.setText('{0:b}'.format(sensors).zfill(6))
        
    def update_gpio(self, sensors):
        self._gpio_wid.setText('{0:b}'.format(sensors).zfill(6))
        
    def update_debug_goldo(self, dbg_info):
        if self.goldo_dbg_info != dbg_info:
            self.goldo_dbg_info = dbg_info
            print ("  debug_goldo : %8x"%dbg_info)
        self._debug_goldo_wid.setText("%8x"%(dbg_info))
        
    def match_state_change(self, state, side):
        states = {
            0: 'Unconfigured',
            1: 'Idle',
            2: 'PreMatch',
            3: 'WaitMatch',
            4: 'Match',
            5: 'PostMatch',
            6: 'Debug'
            }
        sides =  {
        0:'Unknown',
        1: 'Yellow',
        2:'Purple'
        }
        self._robot_state_wid.setText(states[state])
        self._robot_side_wid.setText(sides[side])


    def _on_emergency_stop_button_clicked(self):
        self._client.send_message(16,b'')
