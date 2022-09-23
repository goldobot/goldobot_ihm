import zmq
import re
import struct
from PyQt5.QtCore import QObject, QSocketNotifier, pyqtSignal
from PyQt5.QtGui import QPixmap

from goldobot.messages import NucleoFirmwareVersion
from goldobot.messages import PropulsionTelemetryEx
from goldobot.messages import RplidarPlot
from goldobot.messages import RplidarRobotDetection
from goldobot.messages import OdometryConfig
from goldobot.messages import PropulsionControllerConfig

from goldobot import message_types

import goldobot.pb2 as _goldo_pb2

import google.protobuf as _pb
_sym_db = _pb.symbol_database.Default()

class ZmqClient(QObject):
    nucleo_firmware_version = pyqtSignal(str)
    message_received = pyqtSignal(object)
    heartbeat = pyqtSignal(int)
    start_of_match = pyqtSignal(int)
    match_state_change = pyqtSignal(int,int)
    comm_stats = pyqtSignal(object)
    propulsion_telemetry = pyqtSignal(object)
    propulsion_telemetry_ex = pyqtSignal(object)
    rplidar_plot = pyqtSignal(object)
    rplidar_robot_detection = pyqtSignal(object)
    astar_dbg_map = pyqtSignal(object)
    odometry_config = pyqtSignal(object)
    propulsion_controller_config = pyqtSignal(object)
    dynamixel_registers = pyqtSignal(int, int, object)
    fpga_registers = pyqtSignal(int, int)
    fpga_registers_crc = pyqtSignal(int, int, int)
    fpga_adc = pyqtSignal(int, float)
    asserv_plot = pyqtSignal(int, int)
    sensors = pyqtSignal(int)
    gpio = pyqtSignal(int)
    debug_goldo = pyqtSignal(int)
    robot_end_load_config_status = pyqtSignal(bool)
    sequence_event = pyqtSignal(int, object)
    odrive_response = pyqtSignal(object)
    camera_image = pyqtSignal(object)
    robot_state_change = pyqtSignal(object)

    def __init__(self, ip=None, parent = None):
        super(ZmqClient, self).__init__(None)
        self._context = zmq.Context()

        self._push_socket = self._context.socket(zmq.PUB)
        self._push_socket.connect('tcp://{}:3002'.format(ip))

        self._socket_main_sub = self._context.socket(zmq.SUB)
        self._socket_main_sub.connect('tcp://{}:3801'.format(ip))
        self._socket_main_sub.setsockopt(zmq.SUBSCRIBE,b'')

        self._socket_main_pub = self._context.socket(zmq.PUB)
        self._socket_main_pub.connect('tcp://{}:3802'.format(ip))

        self._notifier_main = QSocketNotifier(self._socket_main_sub.getsockopt(zmq.FD), QSocketNotifier.Read, self)
        self._notifier_main.activated.connect(self._on_socket_main_sub)

        self._callbacks = []
        self._goldo_log_fd = open("goldo_log.txt","wt")

    def send_message(self, message_type, message_body):
        self._push_socket.send_multipart([struct.pack('<H',message_type), message_body])

    def send_message_new_header(self, message_type, message_body):
        self._push_socket.send_multipart([struct.pack('<BBHIi',0,0,message_type,0,0), message_body])

    def publishTopic(self, topic, msg = None):
        if msg is None:
            msg = _sym_db.GetSymbol('google.protobuf.Empty')()
        self._socket_main_pub.send_multipart([topic.encode('utf8'),
                                              msg.DESCRIPTOR.full_name.encode('utf8'),
                                              msg.SerializeToString()])

    def registerCallback(self, pattern: str, callback, full=False):
        pattern = (
            pattern
            .replace('*', r'([^/]+)')
            .replace('/#', r'(/[^/]+)*')
            .replace('#/', r'([^/]+/)*')
            )
        self._callbacks.append((re.compile(f"^{pattern}$"), callback, full))

    def onMessage(self, topic, msg):
        callback_matches = ((regexp.match(topic), callback, full) for regexp, callback, full in self._callbacks)
        for match, callback, full in callback_matches:
            if match:
                if full:
                    callback(topic, msg)
                else:
                    callback(*match.groups(), msg)
        if topic == 'nucleo/out/os/heartbeat':
            self.heartbeat.emit(msg.timestamp)
        if topic == 'nucleo/out/robot/config/load_status':
            self.robot_end_load_config_status.emit(msg.status==0)
        if topic == 'nucleo/out/odrive/response':
            self.odrive_response.emit(msg)
        if topic == 'nucleo/out/odometry/config':
            self.odometry_config.emit(msg)
        if topic == 'nucleo/out/propulsion/telemetry':
            self.propulsion_telemetry.emit(msg)
        if topic == 'nucleo/out/propulsion/telemetry_ex':
            self.propulsion_telemetry_ex.emit(msg)
        if topic == 'nucleo/out/propulsion/config':
            self.propulsion_controller_config.emit(msg)
        if topic == 'nucleo/out/fpga/reg':
            self.fpga_registers.emit(msg.apb_address, msg.apb_value)
        if topic == 'nucleo/out/fpga/adc/read_out':
            self.fpga_adc.emit(msg.chan, msg.chan_val)
        if topic == 'rplidar/out/scan':
            self.rplidar_plot.emit(msg)
        if topic == 'gui/in/robot_state':
            self.robot_state = msg
            self.robot_state_change.emit(msg)
        if topic == 'nucleo/out/dbg_goldo':
            #print("nucleo/out/dbg_goldo : {:8x}".format(msg.value))
            val = msg.value
            ts = val & 0xffff0000
            ts = ts >> 16
            pos = val & 0x0000ffff
            if pos & 0x00008000 == 0x00008000: pos -= 0x10000
            self._goldo_log_fd.write("{} {}\n". format(ts,pos))
            self._goldo_log_fd.flush()
            self.asserv_plot.emit(ts, pos)

    def _on_socket_main_sub(self):
        self._notifier_main.setEnabled(False)
        socket = self._socket_main_sub
        flags = socket.getsockopt(zmq.EVENTS)
        while flags & zmq.POLLIN:
            topic, full_name, payload = socket.recv_multipart()
            flags = socket.getsockopt(zmq.EVENTS)
            topic = topic.decode('utf8')
            full_name = full_name.decode('utf8')
            try:
                msg_class = _sym_db.GetSymbol(full_name)
                if msg_class is not None:
                    msg = msg_class()
                    msg.ParseFromString(payload)
                else:
                    msg = None
                self.onMessage(topic, msg)
            except KeyError:
                pass
        self._notifier_main.setEnabled(True)
