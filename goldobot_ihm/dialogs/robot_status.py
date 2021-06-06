from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QLineEdit
from widgets.properties_editor import PropertiesEditorWidget

from typing import Optional

import google.protobuf as _pb
_sym_db = _pb.symbol_database.Default()

class RobotStatusDialog(QDialog):
    _client : Optional['goldobot.zmq_client.ZmqClient']
    
    def __init__(self, parent = None):
        super(self).__init__(parent)
        self._client = None

        self._get_button = QPushButton('Get')
        self._set_button = QPushButton('Set')
        self._wid_left_encoder = QLineEdit('0')
        self._wid_right_encoder = QLineEdit('0')
        self._button_reset_counts = QPushButton('reset counts')

        layout = QGridLayout()

        props = PropertiesEditorWidget(_sym_db.GetSymbol('goldo.nucleo.propulsion.OdometryConfig'),
            [
            ('dist_per_count_left', float,),
            ('dist_per_count_right', float,),
            ('wheel_distance_left', float,),
            ('wheel_distance_right', float,),
            ('speed_filter_frequency', float,),
            ('accel_filter_frequency', float,)
            ])
        layout.addWidget(props,0,0,1,2)
        self._properties = props       

        layout.addWidget(self._get_button,1,0)
        layout.addWidget(self._set_button,1,1)
        layout.addWidget(self._wid_left_encoder, 3,0)
        layout.addWidget(self._wid_right_encoder, 3,1)
        layout.addWidget(self._button_reset_counts, 4,0,1,2)

        self.setLayout(layout)


    def set_client(self, client: ''):
        self._client = client
        #self._client.odometry_config.connect(self.update_odometry_config)
        #self._client.propulsion_telemetry.connect(self._on_telemetry)
        #self._client.propulsion_telemetry_ex.connect(self._on_telemetry_ex)

    def _on_telemetry(self, telemetry):        
        self._wid_left_encoder.setText(str(self._encoder_left_acc))
        self._wid_right_encoder.setText(str(self._encoder_right_acc))

     