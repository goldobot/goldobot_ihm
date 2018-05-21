from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QDialog
from widgets.properties_editor import PropertiesEditorWidget

from messages import PropulsionControllerConfig

class PropulsionControllerConfigDialog(QDialog):
    def __init__(self, parent = None):
        super(PropulsionControllerConfigDialog, self).__init__(None)
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

        self._yaw_rate_pid_props = PropertiesEditorWidget(PIDConfig,pid_props)
        tab_widget.addTab(self._yaw_rate_pid_props, "yaw_rate")

        self._translation_pid_props = PropertiesEditorWidget(PIDConfig,pid_props)
        tab_widget.addTab(self._translation_pid_props, "translation")

        self._yaw_pid_props = PropertiesEditorWidget(PIDConfig,pid_props)
        tab_widget.addTab(self._yaw_pid_props, "yaw")

        layout.addWidget(tab_widget,0,0,1,2)

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