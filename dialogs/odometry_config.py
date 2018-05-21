from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QDialog
from widgets.properties_editor import PropertiesEditorWidget

from messages import OdometryConfig

class OdometryConfigDialog(QDialog):
    def __init__(self, parent = None):
        super(OdometryConfigDialog, self).__init__(None)
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