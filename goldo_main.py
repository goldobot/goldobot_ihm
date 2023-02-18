import sys
import signal
import math
import struct
import config
import subprocess
import yaml

from optparse import OptionParser

import PyQt5.QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QLineEdit, QGridLayout, QFrame, QPushButton, QSpinBox, QSizePolicy
from PyQt5.QtCore import QObject, pyqtSignal, QSize, QRectF, QPointF, Qt, QTimer
from PyQt5.QtWidgets import QTabWidget, QAction, QDialog, QVBoxLayout, QCheckBox
from PyQt5.QtWidgets import QHBoxLayout, QComboBox, QMessageBox, QShortcut
from PyQt5.QtGui import QKeySequence, QFont

from widgets.table_view import TableViewWidget
from widgets.plot_dialog import PlotDialog, ControlPlots

from zmq_client import ZmqClient

from widgets.robot_status import RobotStatusWidget
from widgets.properties_editor import PropertiesEditorWidget
from dialogs.odometry_config import OdometryConfigDialog
from dialogs.propulsion_controller_config import PropulsionControllerConfigDialog
from dialogs.test_propulsion import PropulsionTestDialog
from dialogs.test_arms import TestArmsDialog
from dialogs.test_actuators import TestActuatorsDialog
from dialogs.test_dynamixels import TestDynamixelAx12Dialog
from dialogs.debug_fpga import DebugFpgaDialog
from dialogs.sequences import SequencesDialog
from widgets.plot_astar import PlotAstarWidget

from parse_sequence import SequenceParser

import message_types

import config

dialogs = [
    ("Configure Odometry", OdometryConfigDialog),
    ("Configure Propulsion controller", PropulsionControllerConfigDialog),
    ("Test propulsion", PropulsionTestDialog),
    ("Test arms", TestArmsDialog),
    ("Test dynamixels", TestDynamixelAx12Dialog),
    ("Test actionneurs", TestActuatorsDialog),
    ("Debug FPGA", DebugFpgaDialog),
    ("Test sequences", SequencesDialog),
 ]

        
class MainWindow(QMainWindow):
    nucleo_ver_prefix_s = "Nucleo firmware version : "

    def __init__(self, parent = None):
        #PArse arguments
        parser = OptionParser()
        parser.add_option('--robot-ip', default='192.168.1.222')
        parser.add_option('--config-path', default='petit_robot')
        parser.add_option('--ihm-type', default='pc')
        (options, args) = parser.parse_args(sys.argv)
        self._ihm_type = options.ihm_type
        
        #QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        if self._ihm_type == "raspi":
            super(MainWindow, self).__init__(None, Qt.WindowStaysOnTopHint)
        else:
            super(MainWindow, self).__init__(None)
        
        self._client = ZmqClient(ip=options.robot_ip)
        no_yaml_loader = (self._ihm_type == "raspi")
        config.load_config(options.config_path,no_yaml_loader)

        # Create actions
        self._action_reset = QAction("Reset",self)
        self._action_enter_debug = QAction("Debug enter",self)
        self._action_exit_debug = QAction("Debug exit",self)
        self._action_upload_config = QAction("Upload config",self)
        self._action_rplidar_start = QAction("Rplidar start",self)
        self._action_rplidar_stop = QAction("Rplidar stop",self)
        self._action_dbg_strat_go = QAction("Debug strat GO",self)
        self._action_dbg_strat_clear_err = QAction("Debug strat clear err",self)
        self._action_dbg_strat_pause = QAction("Debug strat pause",self)
        self._action_dbg_strat_resume = QAction("Debug strat resume",self)
        
        # Add menu
        tools_menu = self.menuBar().addMenu("Tools")
        
        self._actions = []
        self._dialogs = []
        
        for d in dialogs:
            action = QAction(d[0],self)
            widget = d[1]()
            tools_menu.addAction(action)
            self._actions.append(action)
            self._dialogs.append(widget)
            action.triggered.connect(widget.show)
            
        tools_menu.addAction(self._action_enter_debug)
        tools_menu.addAction(self._action_exit_debug)
        tools_menu.addAction(self._action_reset)
        tools_menu.addAction(self._action_upload_config)

        self._main_widget = QWidget()
        self._score = QLabel()
        self._table_view = TableViewWidget(ihm_type=self._ihm_type,parent=self)
        self._widget_robot_status = RobotStatusWidget(ihm_type=self._ihm_type)
        self._conf_button = QPushButton('Load Conf')
        self._rplidar_start_button = QPushButton('Start Rplidar')
        self._rplidar_stop_button = QPushButton('Stop Rplidar')
        self._dbg_strat_go_button = QPushButton('Debug Strat GO!')
        self._dbg_strat_clear_err_button = QPushButton('Clear error (Strat)')
        self._dbg_strat_pause_button = QPushButton('Debug Strat pause')
        self._dbg_strat_resume_button = QPushButton('Debug Strat resume')
        self._dbg_strat_display_button = QPushButton('Display Strat')
        self._dbg_strat_clear_button = QPushButton('Clear Strat')
        self._dbg_strat_fname_edit = QLineEdit('')
        self._nucleo_firmware_version = QLabel(self.nucleo_ver_prefix_s + "Unknown")
        self._astar_view = PlotAstarWidget()

        self.zoomL = QLabel()
        self.zoomL.setText("Zoom")
        self.zoomL.setDisabled(False)

        self.zoomPlusB = QPushButton()
        self.zoomPlusB.setText("+")
        self.zoomPlusB.setDisabled(False)
        self.zoomPlusB.clicked.connect(self._table_view.zoomPlus)

        self.zoomDefB = QPushButton()
        self.zoomDefB.setText("o")
        self.zoomDefB.setDisabled(False)
        self.zoomDefB.clicked.connect(self._table_view.zoomDef)

        self.zoomMinusB = QPushButton()
        self.zoomMinusB.setText("-")
        self.zoomMinusB.setDisabled(False)
        self.zoomMinusB.clicked.connect(self._table_view.zoomMinus)

        self.testPlotB = QPushButton()
        self.testPlotB.setText("Test Plot")
        self.testPlotB.setDisabled(False)
        self.testPlotB.clicked.connect(self._table_view.testPlot)

        self.posL = QLabel()
        self.posL.setText("Pos & dist:")
        self.posL.setDisabled(False)

        self.posXL = QLabel()
        self.posXL.setText(" x:")
        self.posXL.setDisabled(False)

        self.posYL = QLabel()
        self.posYL.setText(" y:")
        self.posYL.setDisabled(False)

        self.posXRL = QLabel()
        self.posXRL.setText(" xr:")
        self.posXRL.setDisabled(False)

        self.posYRL = QLabel()
        self.posYRL.setText(" yr:")
        self.posYRL.setDisabled(False)

        self.posDRL = QLabel()
        self.posDRL.setText(" dr:")
        self.posDRL.setDisabled(False)

        self.posDbg1L = QLabel()
        self.posDbg1L.setText(" DEBUG: ")
        self.posDbg1L.setDisabled(False)

        self.posDbg2L = QLabel()
        self.posDbg2L.setText(" DEBUG: ")
        self.posDbg2L.setDisabled(False)


        main_layout = QHBoxLayout()
        table_layout = QVBoxLayout()
        under_table_layout = QHBoxLayout()
        raspi_layout = QGridLayout()
        right_layout = QVBoxLayout()

        self.setCentralWidget(self._main_widget)

        raspi_layout.addWidget(self._rplidar_start_button,        1, 1)
        raspi_layout.addWidget(self._rplidar_stop_button,         1, 2)
        raspi_layout.addWidget(self._dbg_strat_go_button,         2, 1)
        raspi_layout.addWidget(self._dbg_strat_clear_err_button,  2, 2)
        raspi_layout.addWidget(self._dbg_strat_pause_button,      3, 1)
        raspi_layout.addWidget(self._dbg_strat_resume_button,     3, 2)
        if self._ihm_type != "raspi":
            raspi_layout.addWidget(self._dbg_strat_display_button,    4, 1)
            raspi_layout.addWidget(self._dbg_strat_fname_edit,        4, 2)
            raspi_layout.addWidget(self._dbg_strat_clear_button,      5, 1)

        under_table_layout.addLayout(raspi_layout)
        if self._ihm_type != "raspi":
            under_table_layout.addWidget(self._astar_view)

        table_layout.addWidget(self._nucleo_firmware_version)
        table_layout.addWidget(self._table_view)
        table_layout.addWidget(self._conf_button)
        table_layout.addLayout(under_table_layout)
        table_layout.addStretch(1)

        right_layout.addWidget(self.zoomL)
        right_layout.addWidget(self.zoomPlusB)
        right_layout.addWidget(self.zoomDefB)
        right_layout.addWidget(self.zoomMinusB)
        right_layout.addWidget(self.testPlotB)
        right_layout.addWidget(self.posL)
        right_layout.addWidget(self.posXL)
        right_layout.addWidget(self.posYL)
        right_layout.addWidget(self.posXRL)
        right_layout.addWidget(self.posYRL)
        right_layout.addWidget(self.posDRL)
        right_layout.addWidget(self.posDbg1L)
        right_layout.addWidget(self.posDbg2L)
        right_layout.addStretch(16)

        main_layout.addWidget(self._widget_robot_status)
        self._score_val = 0
        if self._ihm_type == "raspi":
            my_font = QFont ( "Arial", 40, QFont.Bold)
            self._score.setFont(my_font)
            self._score.setAlignment(Qt.AlignCenter)
            self._score.setText("Score:\n{:d}".format(self._score_val))
            main_layout.addWidget(self._score)
        main_layout.addLayout(table_layout)
        if self._ihm_type != "raspi":
            main_layout.addLayout(right_layout)

        self._main_widget.setLayout(main_layout)

        self._action_reset.triggered.connect(self._send_reset) 
        self._action_enter_debug.triggered.connect(self._send_enter_debug) 
        self._action_exit_debug.triggered.connect(self._send_exit_debug)
        self._action_upload_config.triggered.connect(self._upload_config) 
        self._action_rplidar_start.triggered.connect(self._rplidar_start_control) 
        self._action_rplidar_stop.triggered.connect(self._rplidar_stop_control) 
        self._action_dbg_strat_go.triggered.connect(self._dbg_strat_go_control) 
        self._action_dbg_strat_clear_err.triggered.connect(self._dbg_strat_clear_err_control) 
        self._action_dbg_strat_pause.triggered.connect(self._dbg_strat_pause_control) 
        self._action_dbg_strat_resume.triggered.connect(self._dbg_strat_resume_control) 

        self._F1_shortcut = QShortcut(QKeySequence(Qt.Key_F1), self)
        self._F1_shortcut.activated.connect(self._get_nucleo_firmware_version)

        # FIXME : DEBUG : pour l'ergonomie des tests d'asserv..
        self._F2_shortcut = QShortcut(QKeySequence(Qt.Key_F2), self)
        self._goldo_test_propulsion = PropulsionTestDialog()
        self._goldo_test_propulsion.set_client(self._client)
        self._F2_shortcut.activated.connect(self._goldo_test_propulsion.show)

        self._F5_shortcut = QShortcut(QKeySequence(Qt.Key_F5), self)
        self._F5_shortcut.activated.connect(self._upload_config)

        self._conf_button.clicked.connect(self._upload_config)
        self._rplidar_start_button.clicked.connect(self._rplidar_start_control)
        self._rplidar_stop_button.clicked.connect(self._rplidar_stop_control)
        self._dbg_strat_go_button.clicked.connect(self._dbg_strat_go_control)
        self._dbg_strat_clear_err_button.clicked.connect(self._dbg_strat_clear_err_control)
        self._dbg_strat_pause_button.clicked.connect(self._dbg_strat_pause_control)
        self._dbg_strat_resume_button.clicked.connect(self._dbg_strat_resume_control)
        self._dbg_strat_display_button.clicked.connect(self._dbg_strat_display)
        self._dbg_strat_clear_button.clicked.connect(self._dbg_strat_clear)

        self._client.robot_end_load_config_status.connect(self._upload_status)
        self._client.nucleo_firmware_version.connect(self._display_nucleo_firmware_version)
       
        
        for d in self._dialogs:
            d.set_client(self._client)
                
        # Add status bar
        self._status_link_state = QLabel('')
        self.statusBar().addWidget(self._status_link_state)
        self._status_match_state = QLabel('')
        self.statusBar().addWidget(self._status_match_state)
        
        self._client.comm_stats.connect(self._on_comm_stats)
        self._client.match_state_change.connect(self._on_match_state_change)
        self._widget_robot_status.set_client(self._client)
        self._table_view.set_client(self._client)
        self._astar_view.set_client(self._client)
        
        #plt = ControlPlots()
        #plt.show()
        #self.plt = plt
        ##plt.plot_curve([0,2,1])

    def _send_reset(self):
        self._client.send_message(message_types.DbgReset, b'')
        
    def _send_enter_debug(self):
        self._client.send_message(message_types.SetMatchState, struct.pack('<B', 6))
        
    def _send_exit_debug(self):
        self._client.send_message(message_types.SetMatchState, struct.pack('<B', 1))
        
    def _on_comm_stats(self, stats):
        self._status_link_state.setText('download {} {}'.format(*stats))
        
    def _on_match_state_change(self, state,side):
        self._status_match_state.setText('{} {}'.format(state, side))
        
    def _upload_sequence(self):
        config.load_dynamixels_config()
        config.load_sequence()

    def _upload_config(self):
        cfg = config.robot_config
        #cfg.update_config()
        cfg.compile()
        #Get nucleo firmware version
        #self._client.send_message(message_types.GetNucleoFirmwareVersion, b'')
        #Start programming
        self._client.send_message(message_types.RobotBeginLoadConfig, b'')
        #Upload codes by packets
        buff = cfg.binary
        while len(buff) >32:
            self._client.send_message(message_types.RobotLoadConfig, buff[0:32])
            buff = buff[32:]
        self._client.send_message(message_types.RobotLoadConfig, buff)
        #Finish programming
        self._client.send_message(message_types.RobotEndLoadConfig, struct.pack('<H', cfg.crc))
        
    def _upload_status(self, status):
        if status == True:
            QMessageBox.information(self, "Upload config status", "Success")
        else:
            QMessageBox.critical(self, "Upload config status", "Failure")

    def _start_sequence(self):
        self._client.send_message(43, struct.pack('<H',1))

    def _rplidar_start_control(self):
        self._client.send_message_rplidar(message_types.RplidarStart, b'')

    def _rplidar_stop_control(self):
        self._client.send_message_rplidar(message_types.RplidarStop, b'')

    def _dbg_strat_go_control(self):
        self._client.send_message_rplidar(message_types.RobotStratDbgStartMatch, b'')

    def _dbg_strat_clear_err_control(self):
        #self._client.send_message(message_types.PropulsionClearError, b'')
        self._client.send_message_rplidar(message_types.PropulsionClearError, b'')

    def _dbg_strat_pause_control(self):
        self._client.send_message_rplidar(message_types.RobotStratDbgPauseMatch, b'')

    def _dbg_strat_resume_control(self):
        self._client.send_message_rplidar(message_types.RobotStratDbgResumeMatch, b'')

    def _dbg_strat_display(self):
        strat_fname_in = self._dbg_strat_fname_edit.text()
        if (strat_fname_in == ""):
            strat_fname = "dbg/B.yaml"
        else:
            strat_fname = "dbg/" + self._dbg_strat_fname_edit.text()
        print ("Debug strat file : {}".format(strat_fname))
        try:
            strat_fd = open(strat_fname)
        except:
            print ("No such file or directory: {}".format(strat_fname))
        if self._ihm_type == "raspi":
            strat_yaml = yaml.load(strat_fd)
        else:
            strat_yaml = yaml.load(strat_fd,Loader=yaml.FullLoader)
        print (strat_yaml)
        idx=0
        my_x = 0
        my_y = 0
        for act in strat_yaml["dbg_task"]["actions"]:
            act_type = act["type"]
            print ("act {} : {}".format(idx,act_type))
            if act_type == "TRAJ":
                first_wp = True
                for wp in act["param_traj"]["wp"]:
                    my_x = wp[0]
                    my_y = wp[1]
                    print ("  <{:>10.3f} {:>10.3f}>".format(my_x,my_y))
                    if first_wp:
                        TableViewWidget.g_table_view.debug_set_start(my_x,my_y)
                    else:
                        TableViewWidget.g_table_view.debug_line_to(my_x,my_y)
                    first_wp = False
            elif act_type == "GOTO_ASTAR":
                TableViewWidget.g_table_view.debug_set_start(my_x,my_y)
                wp = act["param_goto_astar"]["target"]
                my_x = wp[0]
                my_y = wp[1]
                print ("  <{:>10.3f} {:>10.3f}>".format(my_x,my_y))
                TableViewWidget.g_table_view.debug_line_to(my_x,my_y,0,0,255)
            idx += 1

    def _dbg_strat_clear(self):
        TableViewWidget.g_table_view.debug_clear_lines()

    def _get_nucleo_firmware_version(self):
        self._client.send_message(message_types.GetNucleoFirmwareVersion, b'')

    def _display_nucleo_firmware_version(self, firm_ver):
        self._nucleo_firmware_version.setText(self.nucleo_ver_prefix_s + firm_ver)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    #app.setAttribute(Qt.AA_EnableHighDpiScaling)

    main_window = MainWindow()
    main_window.show()
    
    # Ensure that the application quits using CTRL-C
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    sys.exit(app.exec_())
