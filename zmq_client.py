import zmq
import struct
from PyQt5.QtCore import QObject, QSocketNotifier, pyqtSignal

from messages import PropulsionTelemetry
from messages import PropulsionTelemetryEx
from messages import OdometryConfig
from messages import PropulsionControllerConfig

class ZmqClient(QObject):
    heartbeat = pyqtSignal(int)
    match_started = pyqtSignal(int)
    propulsion_telemetry = pyqtSignal(object)
    propulsion_telemetry_ex = pyqtSignal(object)
    odometry_config = pyqtSignal(object)
    propulsion_controller_config = pyqtSignal(object)

    def __init__(self, parent = None):
        super(ZmqClient, self).__init__(None)
        self._context = zmq.Context()

        self._sub_socket = self._context.socket(zmq.SUB)
        self._sub_socket.connect('tcp://localhost:3001')
        self._sub_socket.setsockopt(zmq.SUBSCRIBE,b'')

        self._push_socket = self._context.socket(zmq.PUSH)
        self._push_socket.connect('tcp://localhost:3002')

        self._notifier = QSocketNotifier(self._sub_socket.getsockopt(zmq.FD), QSocketNotifier.Read, self)
        self._notifier.activated.connect(self._on_sub_socket_event)

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

    def _on_message_received(self, msg):
        msg_type = struct.unpack('<H', msg[0:2])[0]

        if msg_type == 1:
            timestamp = struct.unpack('<I', msg[2:6])[0]
            self.heartbeat.emit(timestamp)
        if msg_type == 3:
            telemetry = PropulsionTelemetry(msg[2:])
            self.propulsion_telemetry.emit(telemetry)
        if msg_type == 4:
            timestamp = struct.unpack('<I', msg[2:6])[0]
            self.match_started.emit(timestamp)
        if msg_type == 6:
            telemetry = PropulsionTelemetryEx(msg[2:])
            self.propulsion_telemetry_ex.emit(telemetry)
        if msg_type == 7:
            print(struct.unpack('<HH', msg[2:]))
        if msg_type == 32:
            self.odometry_config.emit(OdometryConfig(msg[2:]))
        if msg_type == 33:
            self.propulsion_controller_config.emit(PropulsionControllerConfig(msg[2:]))