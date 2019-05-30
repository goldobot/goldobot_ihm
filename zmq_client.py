import zmq
import struct
from PyQt5.QtCore import QObject, QSocketNotifier, pyqtSignal

from messages import PropulsionTelemetry
from messages import PropulsionTelemetryEx
from messages import RplidarRobotDetection
from messages import OdometryConfig
from messages import PropulsionControllerConfig

import message_types

class ZmqClient(QObject):
    message_received = pyqtSignal(object)
    heartbeat = pyqtSignal(int)
    start_of_match = pyqtSignal(int)
    match_state_change = pyqtSignal(int,int)
    comm_stats = pyqtSignal(object)
    propulsion_telemetry = pyqtSignal(object)
    propulsion_telemetry_ex = pyqtSignal(object)
    rplidar_robot_detection = pyqtSignal(object)
    odometry_config = pyqtSignal(object)
    propulsion_controller_config = pyqtSignal(object)
    dynamixel_registers = pyqtSignal(int, int, object)
    fpga_registers = pyqtSignal(int, int)
    sensors = pyqtSignal(int)
    gpio = pyqtSignal(int)
    robot_end_load_config_status = pyqtSignal(bool)

    def __init__(self, ip=None, parent = None):
        super(ZmqClient, self).__init__(None)
        self._context = zmq.Context()

        self._sub_socket = self._context.socket(zmq.SUB)
        self._sub_socket.connect('tcp://{}:3001'.format(ip))
        self._sub_socket.setsockopt(zmq.SUBSCRIBE,b'')

        self._sub_socket_rplidar = self._context.socket(zmq.SUB)
        self._sub_socket_rplidar.connect('tcp://{}:3101'.format(ip))
        self._sub_socket_rplidar.setsockopt(zmq.SUBSCRIBE,b'')

        self._push_socket = self._context.socket(zmq.PUB)
        self._push_socket.connect('tcp://{}:3002'.format(ip))

        self._notifier = QSocketNotifier(self._sub_socket.getsockopt(zmq.FD), QSocketNotifier.Read, self)
        self._notifier.activated.connect(self._on_sub_socket_event)

        self._notifier_rplidar = QSocketNotifier(self._sub_socket_rplidar.getsockopt(zmq.FD), QSocketNotifier.Read, self)
        self._notifier_rplidar.activated.connect(self._on_sub_socket_rplidar_event)

    def send_message(self, message_type, message_body):
        self._push_socket.send_multipart([struct.pack('<H',message_type), message_body])

    def _on_sub_socket_event(self):        
        self._notifier.setEnabled(False)

        flags = self._sub_socket.getsockopt(zmq.EVENTS)

        while flags & zmq.POLLIN:
            received = self._sub_socket.recv_multipart()
            self._on_message_received(b''.join(received))
            flags = self._sub_socket.getsockopt(zmq.EVENTS)
        self._notifier.setEnabled(True)

    def _on_sub_socket_rplidar_event(self):        
        self._notifier_rplidar.setEnabled(False)
        flags = self._sub_socket_rplidar.getsockopt(zmq.EVENTS)
        while flags & zmq.POLLIN:
            received = self._sub_socket_rplidar.recv_multipart()
            self._on_message_received(b''.join(received))
            flags = self._sub_socket_rplidar.getsockopt(zmq.EVENTS)
        self._notifier_rplidar.setEnabled(True)

    def _on_message_received(self, msg):
        self.message_received.emit(msg)
        msg_type = struct.unpack('<H', msg[0:2])[0]

        if msg_type == 20:
            self.sensors.emit(struct.unpack('<I',msg[2:])[0])
        if msg_type == 21:
            self.gpio.emit(struct.unpack('<I',msg[2:])[0])
        if msg_type == 22:
            print('sequence event', struct.unpack('<BB',msg[2:]))
        if msg_type == 403:
            self.robot_end_load_config_status.emit(bool(struct.unpack('<B',msg[2:])))
        if msg_type == message_types.Heartbeat:
            timestamp = struct.unpack('<I', msg[2:6])[0]
            self.heartbeat.emit(timestamp)
            
        if msg_type == message_types.MatchStateChange:
            state,side = struct.unpack('<BB', msg[2:4])
            self.match_state_change.emit(state,side)

        if msg_type == message_types.PropulsionTelemetry:
            telemetry = PropulsionTelemetry(msg[2:])
            self.propulsion_telemetry.emit(telemetry)

        if msg_type == message_types.PropulsionTelemetryEx:
            telemetry = PropulsionTelemetryEx(msg[2:])
            self.propulsion_telemetry_ex.emit(telemetry)

        if msg_type == message_types.RplidarRobotDetection:
            other_robot = RplidarRobotDetection(msg[2:])
            self.rplidar_robot_detection.emit(other_robot)

        if msg_type == message_types.StartOfMatch:
            timestamp = struct.unpack('<I', msg[2:6])[0]
            self.start_of_match.emit(timestamp)

        if msg_type == message_types.CommStats:
            self.comm_stats.emit(struct.unpack('<HH', msg[2:]))
            pass

        if msg_type == message_types.DbgGetOdometryConfig:
            self.odometry_config.emit(OdometryConfig(msg[2:]))

        if msg_type == message_types.DbgGetPropulsionConfig:
            self.propulsion_controller_config.emit(PropulsionControllerConfig(msg[2:]))

        if msg_type == message_types.DbgDynamixelGetRegisters:
            id_, address = struct.unpack('<BB', msg[2:4])
            self.dynamixel_registers.emit(id_, address, msg[4:])

        if msg_type == message_types.FpgaDbgReadReg:
            apb_addr, apb_data = struct.unpack('<II', msg[2:])
            self.fpga_registers.emit(apb_addr, apb_data)
            
        if msg_type == 90:
            print(struct.unpack('<BB', msg[2:]))

