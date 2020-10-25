from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QTabWidget, QWidget
from PyQt5.QtWidgets import QComboBox
from widgets.properties_editor import PropertiesEditorWidget

from goldobot.messages import PropulsionControllerConfig
from goldobot.messages import PropulsionControllerLowLevelConfig
from goldobot import message_types

import google.protobuf as _pb
_sym_db = _pb.symbol_database.Default()

PIDConfig =  _sym_db.GetSymbol('goldo.nucleo.propulsion.PIDConfig')

class PropulsionLowLevelPIDConfigWidget(QTabWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        
        pid_props = [            
            ('kp', float, '{:.2e}' ),
            ('kd', float, '{:.2e}'),
            ('ki', float, '{:.2e}'),            
            ('lim_i', float, '{:.2e}'),
            ('lim_d', float, '{:.2e}'),
            ('d_filter_frequency', float, '{:.2e}'),
            ('out_min', float, '{:.2e}'),
            ('out_max', float, '{:.2e}')
            ]        

        self._speed_props = PropertiesEditorWidget(PIDConfig, pid_props)
        self.addTab(self._speed_props, "speed")
        
        self._longi_props = PropertiesEditorWidget(PIDConfig, pid_props)
        self.addTab(self._longi_props, "longi")

        self._yaw_rate_props = PropertiesEditorWidget(PIDConfig, pid_props)
        self.addTab(self._yaw_rate_props, "yaw_rate")

        self._yaw_props = PropertiesEditorWidget(PIDConfig, pid_props)
        self.addTab(self._yaw_props, "yaw")
        
    def getValue(self):
        val = self._obj
        self._speed_props.get_value()
        self._yaw_rate_props.get_value()
        self._longi_props.get_value()
        self._yaw_props.get_value()
        return val
        
    def setValue(self, val):
        self._obj = val
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
        
        self._pid_config_combobox = QComboBox()
        self._pid_config_combobox.addItem('default')
        self._pid_config_combobox.addItem('reserved')
        self._pid_config_combobox.addItem('reserved')
        self._pid_config_combobox.addItem('reserved')
        
        tab_widget = PropulsionLowLevelPIDConfigWidget()       
      

        layout.addWidget(self._pid_config_combobox,0,0,1,2)
        layout.addWidget(tab_widget,1,0,1,2)
        
        self._pid_config_widget = tab_widget

        self._props = PropertiesEditorWidget(PropulsionControllerConfig, [
            ('lookahead_distance', float, '{:.2e}'),
            ('lookahead_time', float, '{:.2e}'),
            ('static_pwm_limit', float, '{:.2e}'),
            ('cruise_pwm_limit', float, '{:.2e}'),
            ('reposition_pwm_limit', float, '{:.2e}')
            ])
            
        layout.addWidget(self._props,2,0,1,2) 

        layout.addWidget(self._get_button,4,0)
        layout.addWidget(self._set_button,4,1)

        self._get_button.clicked.connect(self.on_get_button_clicked)
        self._set_button.clicked.connect(self.on_set_button_clicked)
        self._pid_config_combobox.currentIndexChanged.connect(self._on_pid_config_index_changed)
        self.setLayout(layout)

    def set_client(self, client):
        self._client = client
        client.propulsion_controller_config.connect(self.update_propulsion_controller_config)

    def _on_pid_config_index_changed(self, index):
        self._pid_config_widget.getValue()
        self._pid_config_widget.setValue(self._config.pid_configs[index])
        
    def on_get_button_clicked(self):
        if self._client is not None:
            self._client.publishTopic('nucleo/in/propulsion/config/get', _sym_db.GetSymbol('google.protobuf.Empty')())

    def on_set_button_clicked(self):
        self._pid_config_widget.getValue()
        self._props.getValue()
        if self._client is not None:
            self._client.publishTopic('nucleo/in/propulsion/config/set', self._config)

    def update_propulsion_controller_config(self, config):
        self._config = config
        self._pid_config_widget.setValue(config.pid_configs[self._pid_config_combobox.currentIndex()])
        self._props.setValue(config)
        return