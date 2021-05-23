# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: goldo/nucleo.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from goldo.common import geometry_pb2 as goldo_dot_common_dot_geometry__pb2
from goldo.nucleo import hal_pb2 as goldo_dot_nucleo_dot_hal__pb2
from goldo.nucleo import odometry_pb2 as goldo_dot_nucleo_dot_odometry__pb2
from goldo.nucleo import propulsion_pb2 as goldo_dot_nucleo_dot_propulsion__pb2
from goldo.nucleo import robot_simulator_pb2 as goldo_dot_nucleo_dot_robot__simulator__pb2
from goldo.nucleo import servos_pb2 as goldo_dot_nucleo_dot_servos__pb2
from goldo import pb2_options_pb2 as goldo_dot_pb2__options__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='goldo/nucleo.proto',
  package='goldo.nucleo',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x12goldo/nucleo.proto\x12\x0cgoldo.nucleo\x1a\x1bgoldo/common/geometry.proto\x1a\x16goldo/nucleo/hal.proto\x1a\x1bgoldo/nucleo/odometry.proto\x1a\x1dgoldo/nucleo/propulsion.proto\x1a\"goldo/nucleo/robot_simulator.proto\x1a\x19goldo/nucleo/servos.proto\x1a\x17goldo/pb2_options.proto\"4\n\x0cSensorConfig\x12\x10\n\x02id\x18\x01 \x01(\x05\x42\x04\x80\xb5\x18\x03\x12\x12\n\x04name\x18@ \x01(\tB\x04\x80\xb5\x18\x0c\"\xc5\x03\n\x0cNucleoConfig\x12(\n\x03hal\x18\x01 \x01(\x0b\x32\x1b.goldo.nucleo.hal.HalConfig\x12K\n\x0frobot_simulator\x18\x02 \x01(\x0b\x32\x32.goldo.nucleo.robot_simulator.RobotSimulatorConfig\x12\x37\n\x08odometry\x18\x03 \x01(\x0b\x32%.goldo.nucleo.odometry.OdometryConfig\x12G\n\npropulsion\x18\x04 \x01(\x0b\x32\x33.goldo.nucleo.propulsion.PropulsionControllerConfig\x12\x46\n\x0fpropulsion_task\x18\x05 \x01(\x0b\x32-.goldo.nucleo.propulsion.PropulsionTaskConfig\x12\x30\n\x06servos\x18\x06 \x03(\x0b\x32 .goldo.nucleo.servos.ServoConfig\x12+\n\x07sensors\x18\x07 \x03(\x0b\x32\x1a.goldo.nucleo.SensorConfig\x12\x15\n\renabled_tasks\x18\x08 \x03(\tb\x06proto3'
  ,
  dependencies=[goldo_dot_common_dot_geometry__pb2.DESCRIPTOR,goldo_dot_nucleo_dot_hal__pb2.DESCRIPTOR,goldo_dot_nucleo_dot_odometry__pb2.DESCRIPTOR,goldo_dot_nucleo_dot_propulsion__pb2.DESCRIPTOR,goldo_dot_nucleo_dot_robot__simulator__pb2.DESCRIPTOR,goldo_dot_nucleo_dot_servos__pb2.DESCRIPTOR,goldo_dot_pb2__options__pb2.DESCRIPTOR,])




_SENSORCONFIG = _descriptor.Descriptor(
  name='SensorConfig',
  full_name='goldo.nucleo.SensorConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='goldo.nucleo.SensorConfig.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\200\265\030\003', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='goldo.nucleo.SensorConfig.name', index=1,
      number=64, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\200\265\030\014', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=237,
  serialized_end=289,
)


_NUCLEOCONFIG = _descriptor.Descriptor(
  name='NucleoConfig',
  full_name='goldo.nucleo.NucleoConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='hal', full_name='goldo.nucleo.NucleoConfig.hal', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='robot_simulator', full_name='goldo.nucleo.NucleoConfig.robot_simulator', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='odometry', full_name='goldo.nucleo.NucleoConfig.odometry', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='propulsion', full_name='goldo.nucleo.NucleoConfig.propulsion', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='propulsion_task', full_name='goldo.nucleo.NucleoConfig.propulsion_task', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='servos', full_name='goldo.nucleo.NucleoConfig.servos', index=5,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='sensors', full_name='goldo.nucleo.NucleoConfig.sensors', index=6,
      number=7, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='enabled_tasks', full_name='goldo.nucleo.NucleoConfig.enabled_tasks', index=7,
      number=8, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=292,
  serialized_end=745,
)

_NUCLEOCONFIG.fields_by_name['hal'].message_type = goldo_dot_nucleo_dot_hal__pb2._HALCONFIG
_NUCLEOCONFIG.fields_by_name['robot_simulator'].message_type = goldo_dot_nucleo_dot_robot__simulator__pb2._ROBOTSIMULATORCONFIG
_NUCLEOCONFIG.fields_by_name['odometry'].message_type = goldo_dot_nucleo_dot_odometry__pb2._ODOMETRYCONFIG
_NUCLEOCONFIG.fields_by_name['propulsion'].message_type = goldo_dot_nucleo_dot_propulsion__pb2._PROPULSIONCONTROLLERCONFIG
_NUCLEOCONFIG.fields_by_name['propulsion_task'].message_type = goldo_dot_nucleo_dot_propulsion__pb2._PROPULSIONTASKCONFIG
_NUCLEOCONFIG.fields_by_name['servos'].message_type = goldo_dot_nucleo_dot_servos__pb2._SERVOCONFIG
_NUCLEOCONFIG.fields_by_name['sensors'].message_type = _SENSORCONFIG
DESCRIPTOR.message_types_by_name['SensorConfig'] = _SENSORCONFIG
DESCRIPTOR.message_types_by_name['NucleoConfig'] = _NUCLEOCONFIG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SensorConfig = _reflection.GeneratedProtocolMessageType('SensorConfig', (_message.Message,), {
  'DESCRIPTOR' : _SENSORCONFIG,
  '__module__' : 'goldo.nucleo_pb2'
  # @@protoc_insertion_point(class_scope:goldo.nucleo.SensorConfig)
  })
_sym_db.RegisterMessage(SensorConfig)

NucleoConfig = _reflection.GeneratedProtocolMessageType('NucleoConfig', (_message.Message,), {
  'DESCRIPTOR' : _NUCLEOCONFIG,
  '__module__' : 'goldo.nucleo_pb2'
  # @@protoc_insertion_point(class_scope:goldo.nucleo.NucleoConfig)
  })
_sym_db.RegisterMessage(NucleoConfig)


_SENSORCONFIG.fields_by_name['id']._options = None
_SENSORCONFIG.fields_by_name['name']._options = None
# @@protoc_insertion_point(module_scope)
