import sys
import signal
import math
import struct

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QLineEdit, QGridLayout, QFrame, QPushButton, QSpinBox, QSizePolicy
from PyQt5.QtCore import QObject, pyqtSignal, QSize, QRectF, QPointF, Qt, QTimer
from PyQt5.QtWidgets import QTabWidget, QAction, QDialog, QVBoxLayout, QCheckBox
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QHBoxLayout
from PyQt5.QtGui import QPolygonF, QPen, QBrush, QColor

from widgets.table_view import TableViewWidget

from zmq_client import ZmqClient

from widgets.robot_status import RobotStatusWidget
from widgets.properties_editor import PropertiesEditorWidget
from dialogs.odometry_config import OdometryConfigDialog
from dialogs.propulsion_controller_config import PropulsionControllerConfigDialog

ax12_registers = {
    ('model_number',0x00, 2),
    ('firmware_version',0x02, 1),
    ('id',0x03, 1),
    ('baud_rate',0x04, 1),
    ('torque_enable',0x18, 1),
    ('goal_position',0x1E, 2),
    ('torque_limit',0x22, 2),
}



class ServoWidget(QWidget):
    def __init__(self, parent = None):
        super(ServoWidgetWidget, self).__init__(None)
        self._client = None
        wid = QLineEdit()

        self._get_button = QPushButton('Get')

    def set_client(self, client):
        self._client = client


class ArmValuesWidget(QWidget):
    def __init__(self, servos):
        super(ArmValuesWidget, self).__init__()
        self.ids = [s[1] for s in servos]        
        self._widgets = {}
        layout = QGridLayout()

        i = 0
        for k, id_ in servos:
            wid_goal_pos = QSpinBox()
            wid_goal_pos.setRange(0,4096)
            cb = (lambda b: lambda : self._on_value_changed(b))(id_)
            wid_goal_pos.valueChanged.connect(cb)

            wid_torque_enable = QCheckBox()

            wid_current_pos = QLineEdit()
            wid_current_pos.setReadOnly(True)

            wid_current_speed = QLineEdit()
            wid_current_speed.setReadOnly(True)

            wid_current_load = QLineEdit()
            wid_current_load.setReadOnly(True)

            wid_current_voltage = QLineEdit()
            wid_current_voltage.setReadOnly(True)

            wid_current_temp = QLineEdit()
            wid_current_temp.setReadOnly(True)


            layout.addWidget(QLabel(k),i,0)
            layout.addWidget(wid_goal_pos,i,1)
            layout.addWidget(wid_torque_enable,i,2)
            layout.addWidget(wid_current_pos,i,4)
            layout.addWidget(wid_current_speed,i,5)
            layout.addWidget(wid_current_load,i,6)
            layout.addWidget(wid_current_voltage,i,7)
            layout.addWidget(wid_current_temp,i,8)
            self._widgets[id_] = (wid_goal_pos, wid_torque_enable, None, wid_current_pos, wid_current_speed,
             wid_current_load, wid_current_voltage, wid_current_temp)
            i+=1
        self._button_read_state = QPushButton('Read')
        self._button_copy_pos = QPushButton('Copy')
        layout.addWidget(self._button_read_state,i, 0)
        layout.addWidget(self._button_copy_pos,i, 1)
        self.setLayout(layout)

        self._button_read_state.clicked.connect(self.read_dynamixels_state)
        self._button_copy_pos.clicked.connect(self._copy_pos)

    def update_dynamixel_state(self, id_, values):
        if id_ in self._widgets:
            wids = self._widgets[id_]
            wids[3].setText(str(values[0]))
            wids[4].setText(str(values[1]))
            wids[5].setText(str(values[2]))
            wids[6].setText(str(values[3]))
            wids[7].setText(str(values[4]))

    def set_client(self, client):
        self._client = client
        self._client.dynamixel_registers.connect(self._on_dynamixel_registers)

    def read_dynamixels_state(self):
        for id_ in self.ids:
            self._client.send_message(75,struct.pack('<BBB',id_, 0x24, 8))

    def _on_dynamixel_registers(self, id_, address, data):
        if address == 36 and len(data) == 8:
            vals = struct.unpack('<HHHBB', data)
            self.update_dynamixel_state(id_,vals)
    def _copy_pos(self):
        for wids in self._widgets.values():
            wids[0].setValue(int(wids[3].text()))

    def _on_value_changed(self, id_):
        wids = self._widgets[id_]
        if wids[1].isChecked():
            self._client.send_message(74,struct.pack('<BH',id_, wids[0].value()))

    def update_values(self, values):
        for k, v in values.items():
            self._widgets[k].setValue(v)

    

class ArmsWidget(QWidget):
    def __init__(self, parent = None):
        super(ArmsWidget, self).__init__(None)
        self._client = None
        self._button = QPushButton('set pwm')
        self._left_pwm_spinbox = QSpinBox()
        self._left_pwm_spinbox.setRange(0,1024)
        self._left_arm_values = ArmValuesWidget([
            ('slider',4),
            ('rotation', 83),
            ('shoulder', 84),
            ('elbow', 5),
            ('wrist', 6)])
        self._right_arm_values = ArmValuesWidget([
            ('slider',1),
            ('rotation', 81),
            ('shoulder', 82),
            ('elbow', 2),
            ('wrist', 3)])

        self._other_values = ArmValuesWidget([
            ('rack',62),
           ])


        layout = QGridLayout()
        tab_widget = QTabWidget()
        tab_widget.addTab(self._left_arm_values, "Left arm")
        tab_widget.addTab(self._right_arm_values, "Right arm")
        tab_widget.addTab(self._other_values, "Others")
        layout.addWidget(tab_widget)
        self.setLayout(layout)
        

    def set_client(self, client):
        self._client = client
        self._left_arm_values.set_client(client)
        self._right_arm_values.set_client(client)
        self._other_values.set_client(client)

    def _set_dynamixels_positions(self):
        for id_ in self._left_arm_values.ids:
            self._client.send_message(75,struct.pack('<BBB',id_, 0x24, 8))

    def _on_dynamixel_registers(self, id_, address, data):
        if address == 36 and len(data) == 8:
            vals = struct.unpack('<HHHBB', data)
            self._left_arm_values.update_dynamixel_state(id_,vals)

class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(None)
        # Create actions
        self._action_open_odometry_config = QAction("Configure Odometry")
        self._action_open_propulsion_controller_config = QAction("Configure Propulsion controller")
        self._action_arms_test = QAction("Test arms")
        # Add menu
        tools_menu = self.menuBar().addMenu("Tools")
        tools_menu.addAction(self._action_open_odometry_config)
        tools_menu.addAction(self._action_open_propulsion_controller_config)
        tools_menu.addAction(self._action_arms_test)

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
        self._action_arms_test.triggered.connect(self._open_arms_test)

        self._dialog_odometry_config = OdometryConfigDialog(self)
        self._dialog_propulsion_controller_config = PropulsionControllerConfigDialog(self)
        self._dialog_arms_test = ArmsWidget()

        self._client = ZmqClient()
        self._dialog_odometry_config.set_client(self._client)
        self._dialog_propulsion_controller_config.set_client(self._client)
        self._dialog_arms_test.set_client(self._client)
        self._widget_robot_status.set_client(self._client)
        self._table_view.set_client(self._client)

    def _open_odometry_config(self):
        self._dialog_odometry_config.show()

    def _open_propulsion_controller_config(self):
        self._dialog_propulsion_controller_config.show()

    def _open_arms_test(self):
        self._dialog_arms_test.show()



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