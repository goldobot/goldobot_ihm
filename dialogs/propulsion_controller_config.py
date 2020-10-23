from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QTabWidget, QWidget
from widgets.properties_editor import PropertiesEditorWidget

from goldobot.messages import PropulsionControllerConfig
from goldobot.messages import PIDConfig
from goldobot.messages import PropulsionControllerLowLevelConfig
from goldobot import message_types

import google.protobuf as _pb
_sym_db = _pb.symbol_database.Default()

PIDConfig =  _sym_db.GetSymbol('goldo.nucleo.propulsion.PIDConfig')()

class PropulsionLowLevelPIDConfigWidget(QTabWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        
        pid_props = [            
            ('kp', float,),
            ('kd', float,),
            ('ki', float,),            
            ('lim_i', float,),
            ('lim_d', float,),
            ('d_filter_frequency', float,),
            ('out_min', float,),
            ('out_max', float,)
            ]        

        self._speed_props = PropertiesEditorWidget(PIDConfig, pid_props)
        self.addTab(self._speed_props, "speed")
        
        self._longi_props = PropertiesEditorWidget(PIDConfig, pid_props)
        self.addTab(self._longi_props, "longi")

        self._yaw_rate_props = PropertiesEditorWidget(PIDConfig, pid_props)
        self.addTab(self._yaw_rate_props, "yaw_rate")

        self._yaw_props = PropertiesEditorWidget(PIDConfig, pid_props)
        self.addTab(self._yaw_props, "yaw")
        
    def setValue(self, val):
        self._speed_props.set_value(val.speed)
        self._yaw_rate_props.set_value(val.yaw_rate)
        self._longi_props.set_value(val.longi)
        self._yaw_props.set_value(val.yaw)
    

class PropulsionControllerConfigDialog(QDialog):
    def __init__(self, parent = None):
        super(PropulsionControllerConfigDialog, self).__init__(None)
        self._client = None

        self._get_button = QPushButton('Get')
        self._set_button = QPushButton('Set')

        layout = QGridLayout()
        
        tab_widget = PropulsionLowLevelPIDConfigWidget()       
      

        layout.addWidget(tab_widget,0,0,1,2)
        
        self._pid_config_widget = tab_widget

        self._props = PropertiesEditorWidget(PropulsionControllerConfig, [
            ('lookahead_distance', float,),
            ('lookahead_time', float,),
            ('static_pwm_limit', float,),
            ('moving_pwm_limit', float,),
            ('repositioning_pwm_limit', float,)
            ])
        layout.addWidget(self._props,1,0,1,2) 

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
            self._client.publishTopic('nucleo/in/propulsion/config/get', _sym_db.GetSymbol('google.protobuf.Empty')())

    def on_set_button_clicked(self):
        config = self._props.get_value()
        
        config.config_static = PropulsionControllerLowLevelConfig()
        config.config_static.speed_pid_config = self._speed_pid_props.get_value()
        config.config_static.yaw_rate_pid_config = self._yaw_rate_pid_props.get_value()
        config.config_static.translation_pid_config = self._translation_pid_props.get_value()
        config.config_static.yaw_pid_config = self._yaw_pid_props.get_value()
        
        config.config_cruise = PropulsionControllerLowLevelConfig()
        config.config_cruise.speed_pid_config = self._speed_pid_cruise_props.get_value()
        config.config_cruise.yaw_rate_pid_config = self._yaw_rate_pid_cruise_props.get_value()
        config.config_cruise.translation_pid_config = self._translation_pid_cruise_props.get_value()
        config.config_cruise.yaw_pid_config = self._yaw_pid_cruise_props.get_value()
        
        config.config_rotate = config.config_static
        
        if self._client is not None:
            self._client.send_message(message_types.DbgSetPropulsionConfig,config.serialize())

    def update_propulsion_controller_config(self, config):
        print(config)
        self._pid_config_widget.setValue(config.pid_configs[0])
        return
        self._speed_pid_props.set_value(config.config_static.speed_pid_config)
        self._yaw_rate_pid_props.set_value(config.config_static.yaw_rate_pid_config)
        self._translation_pid_props.set_value(config.config_static.translation_pid_config)
        self._yaw_pid_props.set_value(config.config_static.yaw_pid_config)
        
        self._speed_pid_cruise_props.set_value(config.config_cruise.speed_pid_config)
        self._yaw_rate_pid_cruise_props.set_value(config.config_cruise.yaw_rate_pid_config)
        self._translation_pid_cruise_props.set_value(config.config_cruise.translation_pid_config)
        self._yaw_pid_cruise_props.set_value(config.config_cruise.yaw_pid_config)
        
        
        
        
        self._props.set_value(config)
