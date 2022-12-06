import PyQt5.QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QLineEdit, QGridLayout, QFrame, QPushButton, QSpinBox, QSizePolicy
from PyQt5.QtCore import QObject, pyqtSignal, QSize, QRectF, QPointF, Qt, QTimer
from PyQt5.QtWidgets import QTabWidget, QAction, QDialog, QVBoxLayout, QCheckBox
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QComboBox, QMessageBox, QShortcut
from PyQt5.QtGui import QKeySequence

from goldobot_ihm.widgets.table_view import TableViewWidget

import google.protobuf as _pb
_sym_db = _pb.symbol_database.Default()

Rcalib_l = (84.27, 63.81, 45.84, 33.82, 25.04, 18.67, 12.78)
Tcalib_l = (26.00, 32.00, 41.00, 51.00, 61.00, 70.00, 80.00)
def conv_temp(adc_val):
    #Vmess = (3.3/4096)*adc_val
    Vmess = adc_val
    R = 22.0*Vmess/(3.3-Vmess)
    n = len(Rcalib_l)
    R0 = Rcalib_l[0]
    T0 = Tcalib_l[0]
    R1 = Rcalib_l[1]
    T1 = Tcalib_l[1]
    i = 1
    while (R<R1) and (i<(n-1)):
        R0 = Rcalib_l[i]
        T0 = Tcalib_l[i]
        R1 = Rcalib_l[i+1]
        T1 = Tcalib_l[i+1]
        i = i+1
    alpha = (T1-T0)/(R1-R0)
    T = T0 + alpha*(R-R0)
    return T

class Goldo1(QWidget):
    def __init__(self, client, table_view, **kwarg):
        super().__init__(**kwarg)

        self._client = client
        self._table_view = table_view

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

        self.showThemeC = QCheckBox()
        self.showThemeC.setText("Show Theme")
        self.showThemeC.setDisabled(False)
        self.showThemeC.setChecked(True)
        self.showThemeC.clicked.connect(self._enable_theme_display)

        self.clearTelemetryB = QPushButton()
        self.clearTelemetryB.setText("Clear Telemetry")
        self.clearTelemetryB.setDisabled(False)
        self.clearTelemetryB.clicked.connect(self._table_view.clear_telemetry)

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

        self.executePrematchB = QPushButton()
        self.executePrematchB.setText("Execute prematch")
        self.executePrematchB.setDisabled(False)
        self.executePrematchB.clicked.connect(self._prematch)

        self.simulStartB = QPushButton()
        self.simulStartB.setText("Start simulation")
        self.simulStartB.setDisabled(False)
        self.simulStartB.clicked.connect(self._start_simulation)

        self.simulPauseB = QPushButton()
        self.simulPauseB.setText("Pause simulation")
        self.simulPauseB.setDisabled(False)
        self.simulPauseB.clicked.connect(self._pause_simulation)

        self.simulResumeB = QPushButton()
        self.simulResumeB.setText("Resume simulation")
        self.simulResumeB.setDisabled(False)
        self.simulResumeB.clicked.connect(self._resume_simulation)

        self.testAstarB = QPushButton()
        self.testAstarB.setText("Test A*")
        self.testAstarB.setDisabled(False)
        self.testAstarB.clicked.connect(self._test_astar)

        self.testVerB = QPushButton()
        self.testVerB.setText("Test Ver.")
        self.testVerB.setDisabled(False)
        self.testVerB.clicked.connect(self._test_firmware_ver)

        self.liftTempL = QLabel()
        self.liftTempL.setText("Lift motor temp:")
        self.liftTempL.setDisabled(False)

        self.tempLeftL = QLabel()
        self.tempLeftL.setText(" L : ")
        self.tempLeftL.setDisabled(False)

        self.tempRightL = QLabel()
        self.tempRightL.setText(" R : ")
        self.tempRightL.setDisabled(False)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.zoomL)
        right_layout.addWidget(self.zoomPlusB)
        right_layout.addWidget(self.zoomDefB)
        right_layout.addWidget(self.zoomMinusB)
        right_layout.addWidget(self.showThemeC)
        right_layout.addWidget(self.clearTelemetryB)
        right_layout.addWidget(self.posL)
        right_layout.addWidget(self.posXL)
        right_layout.addWidget(self.posYL)
        right_layout.addWidget(self.posXRL)
        right_layout.addWidget(self.posYRL)
        right_layout.addWidget(self.posDRL)
        # FIXME : DEBUG : GOLDO
        #right_layout.addWidget(self.propulsionTestD)
        right_layout.addWidget(self.executePrematchB)
        right_layout.addWidget(self.simulStartB)
        right_layout.addWidget(self.simulPauseB)
        right_layout.addWidget(self.simulResumeB)
        right_layout.addWidget(self.testAstarB)
        right_layout.addWidget(self.testVerB)
        right_layout.addWidget(self.liftTempL)
        right_layout.addWidget(self.tempLeftL)
        right_layout.addWidget(self.tempRightL)
        right_layout.addStretch(16)
        self.setLayout(right_layout)

        self._table_view._scene.dbg_mouse_info.connect(self._update_mouse_dbg)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._on_timer)
        self._timer.start(5000)
        self._client.fpga_adc.connect(self._on_fpga_adc)
        self.adc_chan = 2
        self._client.nucleo_firmware_version.connect(self._on_nucleo_firmware_version)

    def _prematch(self):
        purple = 1
        yellow = 2
        self._client.publishTopic('gui/out/side', _sym_db.GetSymbol('google.protobuf.Int32Value')(value=yellow))
        self._client.publishTopic('gui/out/commands/prematch')

    def _start_match(self):
        self._client.publishTopic('gui/out/commands/debug_start_match')

    def _enable_theme_display(self):
        TableViewWidget.g_show_theme = self.showThemeC.isChecked()
        self._table_view.refreshTheme()

    def _update_mouse_dbg(self, x_mm, y_mm, rel_x_mm, rel_y_mm, d_mm):
        self.posXL.setText(" x: {:>6.1f}".format(x_mm))
        self.posYL.setText(" y: {:>6.1f}".format(y_mm))
        self.posXRL.setText(" xr: {:>6.1f}".format(rel_x_mm))
        self.posYRL.setText(" yr: {:>6.1f}".format(rel_y_mm))
        self.posDRL.setText(" dr: {:>6.1f}".format(d_mm))

    def _start_simulation(self):
        # FIXME : TODO : define "StartSimulation" properly
        #                for now use the "RobotStratDbgStartMatch=2048" message from the "Strat" project
        self._client.send_message_new_header(2048,b'')

    def _pause_simulation(self):
        # FIXME : TODO : define "PauseSimulation" properly
        #                for now use the "RobotStratDbgPauseMatch=2049" message from the "Strat" project
        self._client.send_message_new_header(2049,b'')

    def _resume_simulation(self):
        # FIXME : TODO : define "ResumeSimulation" properly
        #                for now use the "RobotStratDbgResumeMatch=2050" message from the "Strat" project
        self._client.send_message_new_header(2050,b'')

    def _test_astar(self):
        print ("Test A*")
        msg = _sym_db.GetSymbol('google.protobuf.Empty')()
        self._client.publishTopic('robot/test_astar', msg)

    def _test_firmware_ver(self):
        #print ("Test GetNucleoFirmwareVersion")
        msg = _sym_db.GetSymbol('google.protobuf.Empty')()
        self._client.publishTopic('nucleo/in/get_nucleo_firmware_version', msg)

    def _on_nucleo_firmware_version(self, fw_ver_str):
        print("Nucleo firmware version : {:s}".format(fw_ver_str))

    def _on_timer(self):
        msg = _sym_db.GetSymbol('goldo.nucleo.fpga.AdcRead')(chan = self.adc_chan)
        self._client.publishTopic('nucleo/in/fpga/adc/read', msg)
        if self.adc_chan == 2:
            self.adc_chan = 4
        elif self.adc_chan == 4:
            self.adc_chan = 2

    def _on_fpga_adc(self, adc_chan, adc_val):
        if adc_chan == 2:
            temp = conv_temp(adc_val)
            self.tempLeftL.setText(" L: {:>6.1f}°".format(temp))
        elif adc_chan == 4:
            temp = conv_temp(adc_val)
            self.tempRightL.setText(" R: {:>6.1f}°".format(temp))

