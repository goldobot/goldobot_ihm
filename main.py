import sys
import signal
import math
import struct

from optparse import OptionParser

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QLineEdit, QGridLayout, QFrame, QPushButton, QSpinBox, QSizePolicy
from PyQt5.QtCore import QObject, pyqtSignal, QSize, QRectF, QPointF, Qt, QTimer
from PyQt5.QtWidgets import QTabWidget, QAction, QDialog, QVBoxLayout, QCheckBox
from PyQt5.QtWidgets import  QHBoxLayout

from widgets.table_view import TableViewWidget

from zmq_client import ZmqClient

from widgets.robot_status import RobotStatusWidget
from widgets.properties_editor import PropertiesEditorWidget
from dialogs.odometry_config import OdometryConfigDialog
from dialogs.propulsion_controller_config import PropulsionControllerConfigDialog
from dialogs.test_propulsion import PropulsionTestDialog
from dialogs.test_arms import TestArmsDialog

ax12_registers = [
    ('model_number',0x00, 2, 'r'),
    ('firmware_version',0x02, 1, 'r'),
    ('id',0x03, 1, 'rwp'),
    ('baud_rate',0x04, 1, 'rwp'),
    ('return_delay_time', 0x05, 1, 'rwp'),
    ('cw_angle_limit', 0x06, 2, 'rw'),
    ('ccw_angle_limit', 0x08, 2, 'rw'),
    ('temperature_max_limit', 0x0B, 1, 'rw'),
    ('voltage_min_limit', 0x0C, 1, 'rw'),
    ('voltage_max_limit', 0x0D, 1, 'rw'),
    ('max_torque', 0x0E, 2, 'rw'),
    ('status_return_level', 0x10, 1, 'rw'),
    ('alarm_led', 0x11, 1, 'rw'),
    ('alarm_shutdown', 0x12, 1, 'rw'),
    ('down_calibration', 0x14, 2, 'r'),
    ('up_calibration', 0x16, 2, 'r'),
    ]
dynamixel_registers = [
    ('model_number',0x00, 2, 'r'),
    ('firmware_version',0x02, 1, 'r'),
    ('id',0x03, 1, 'rwp'),
    ('baud_rate',0x04, 1, 'rwp'),
    ('return_delay_time', 0x05, 1, 'rwp')
    ]

class TestDynamixelAx12Dialog(QDialog):
    def __init__(self, parent = None):
        super(TestDynamixelAx12Dialog, self).__init__(None)
        self._registers = ax12_registers

        layout = QGridLayout()
        self._spinbox_id = QSpinBox()
        self._spinbox_id.setRange(0,253)
        layout.addWidget(self._spinbox_id, 0,1)

        self._widgets = {}
        i = 1
        for k,a,s,r in self._registers:            
            wid = QLineEdit()
            layout.addWidget(QLabel(k), i, 0)
            layout.addWidget(wid, i, 1)
            self._widgets[k] = wid
            i += 1

        self._button_read_registers = QPushButton('Read')
        layout.addWidget(self._button_read_registers, i, 0)

        self._button_write_registers = QPushButton('Write')
        layout.addWidget(self._button_write_registers, i, 1)

        self.setLayout(layout)

        self._button_read_registers.clicked.connect(self.read_registers)
        self._button_write_registers.clicked.connect(self.write_registers)       

    def set_client(self, client):
        self._client = client
        self._client.dynamixel_registers.connect(self._on_dynamixel_registers)

    def read_registers(self):
        id_ = self._spinbox_id.value()
        for k, a, s, r in self._registers:
            self._client.send_message(77,struct.pack('<BBB',id_, a, s))

    def write_registers(self):
        id_ = self._spinbox_id.value()
        for k, a, s, r in self._registers:
            if 'w' in r and 'p' not in r:
                if s == 1:
                    self._client.send_message(78,struct.pack('<BBB',id_, a, int(self._widgets[k].text())))


    def _on_dynamixel_registers(self, id_, address, data):
        if id_ == self._spinbox_id.value():
            for k, a, s, r in self._registers:
                if address == a and len(data) == s:
                    if s == 1:
                        val = struct.unpack('<B', data)[0]
                    else:
                        val = struct.unpack('<H', data)[0]
                    self._widgets[k].setText(str(val))
       





class ServoWidget(QWidget):
    def __init__(self, parent = None):
        super(ServoWidgetWidget, self).__init__(None)
        self._client = None
        wid = QLineEdit()

        self._get_button = QPushButton('Get')

    def set_client(self, client):
        self._client = client



class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(None)
        # Create actions
        self._action_open_odometry_config = QAction("Configure Odometry")
        self._action_open_propulsion_controller_config = QAction("Configure Propulsion controller")
        self._action_propulsion_test = QAction("Test propulsion")
        self._action_arms_test = QAction("Test arms")
        self._action_dynamixel_ax12_test = QAction("Test dynamixel AX12")
        # Add menu
        tools_menu = self.menuBar().addMenu("Tools")
        tools_menu.addAction(self._action_open_odometry_config)
        tools_menu.addAction(self._action_open_propulsion_controller_config)
        tools_menu.addAction(self._action_propulsion_test)
        tools_menu.addAction(self._action_arms_test)
        tools_menu.addAction(self._action_dynamixel_ax12_test)

        self._main_widget = QWidget()
        self._table_view = TableViewWidget()
        self._widget_robot_status = RobotStatusWidget()

        layout1 = QHBoxLayout()
        layout2 = QVBoxLayout()
        self.setCentralWidget(self._main_widget)
        layout1.addWidget(self._widget_robot_status)
        layout1.addLayout(layout2)
        layout2.addWidget(self._table_view)
        layout2.addStretch(1)

        self._main_widget.setLayout(layout1)

        # Connect signals
        self._action_open_odometry_config.triggered.connect(self._open_odometry_config)
        self._action_open_propulsion_controller_config.triggered.connect(self._open_propulsion_controller_config)
        self._action_propulsion_test.triggered.connect(self._open_propulsion_test)
        self._action_arms_test.triggered.connect(self._open_arms_test)
        self._action_dynamixel_ax12_test.triggered.connect(self._open_dynamixel_ax12_test)

        self._dialog_odometry_config = OdometryConfigDialog(self)
        self._dialog_propulsion_controller_config = PropulsionControllerConfigDialog(self)
        self._dialog_propulsion_test = PropulsionTestDialog()
        self._dialog_arms_test = TestArmsDialog()
        self._dialog_dynamixel_ax12_test = TestDynamixelAx12Dialog()

        #Dirty
        parser = OptionParser()
        parser.add_option('--robot-ip', default='192.168.1.222')
        (options, args) = parser.parse_args(sys.argv)
        self._client = ZmqClient(ip=options.robot_ip)
        self._dialog_odometry_config.set_client(self._client)
        self._dialog_propulsion_controller_config.set_client(self._client)
        self._dialog_propulsion_test.set_client(self._client)
        self._dialog_arms_test.set_client(self._client)
        self._dialog_dynamixel_ax12_test.set_client(self._client)
        self._widget_robot_status.set_client(self._client)
        self._table_view.set_client(self._client)

    def _open_odometry_config(self):
        self._dialog_odometry_config.show()

    def _open_propulsion_controller_config(self):
        self._dialog_propulsion_controller_config.show()

    def _open_propulsion_test(self):
        self._dialog_propulsion_test.show()  

    def _open_arms_test(self):
        self._dialog_arms_test.show()

    def _open_dynamixel_ax12_test(self):
        self._dialog_dynamixel_ax12_test.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)

    main_window = MainWindow()
    main_window.show()


    #wid5 = TestPropulsionWidget()
    #wid5.set_client(c)
    #wid5.show()

    

    
    # Ensure that the application quits using CTRL-C
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    sys.exit(app.exec_())