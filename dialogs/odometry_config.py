from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QLineEdit
from widgets.properties_editor import PropertiesEditorWidget

from messages import OdometryConfig
import message_types

class OdometryConfigDialog(QDialog):
    def __init__(self, parent = None):
        super(OdometryConfigDialog, self).__init__(None)
        self._client = None

        self._get_button = QPushButton('Get')
        self._set_button = QPushButton('Set')
        self._wid_left_encoder = QLineEdit('0')
        self._wid_right_encoder = QLineEdit('0')
        self._button_reset_counts = QPushButton('reset counts')

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
        layout.addWidget(self._wid_left_encoder, 3,0)
        layout.addWidget(self._wid_right_encoder, 3,1)
        layout.addWidget(self._button_reset_counts, 4,0,1,2)

        self._get_button.clicked.connect(self.on_get_button_clicked)
        self._set_button.clicked.connect(self.on_set_button_clicked)
        self._button_reset_counts.clicked.connect(self._on_reset_counts_clicked)
        self.setLayout(layout)
        self._encoder_left_acc = 0
        self._encoder_right_acc = 0
        self._encoder_left_prev = 0
        self._encoder_right_prev = 0

    def set_client(self, client):
        self._client = client
        self._client.odometry_config.connect(self.update_odometry_config)
        self._client.propulsion_telemetry.connect(self._on_telemetry)

    def on_get_button_clicked(self):
        if self._client is not None:
            self._client.send_message(message_types.DbgGetOdometryConfig,b'')

    def on_set_button_clicked(self):
        print(self._properties.get_value().__dict__)
        if self._client is not None:
            self._client.send_message(message_types.DbgSetOdometryConfig,b'')

    def _on_telemetry(self, telemetry):
        diff_left = telemetry.left_encoder - self._encoder_left_prev
        diff_right = telemetry.right_encoder - self._encoder_right_prev

        self._encoder_left_prev = telemetry.left_encoder
        self._encoder_right_prev = telemetry.right_encoder

        if diff_left > 4096:
            diff_left -= 8192;
        if diff_left < -4096:
            diff_left += 8192;
        if diff_right > 4096:
            diff_right -= 8192;
        if diff_right < -4096:
            diff_right += 8192;
        self._encoder_left_acc += diff_left
        self._encoder_right_acc += diff_right
        self._wid_left_encoder.setText(str(self._encoder_left_acc))
        self._wid_right_encoder.setText(str(self._encoder_right_acc))

    def _on_reset_counts_clicked(self):
        self._encoder_left_acc = 0
        self._encoder_right_acc = 0
        self._wid_left_encoder.setText(str(self._encoder_left_acc))
        self._wid_right_encoder.setText(str(self._encoder_right_acc))

    def update_odometry_config(self, config):
        self._properties.set_value(config)        