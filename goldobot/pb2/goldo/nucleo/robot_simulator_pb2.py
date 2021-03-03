# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: goldo/nucleo/robot_simulator.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from goldo import pb2_options_pb2 as goldo_dot_pb2__options__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='goldo/nucleo/robot_simulator.proto',
  package='goldo.nucleo.robot_simulator',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\"goldo/nucleo/robot_simulator.proto\x12\x1cgoldo.nucleo.robot_simulator\x1a\x17goldo/pb2_options.proto\"\x9b\x01\n\x14RobotSimulatorConfig\x12\x13\n\x0bspeed_coeff\x18\x01 \x01(\x02\x12\x16\n\x0ewheels_spacing\x18\x02 \x01(\x02\x12\x18\n\x10\x65ncoders_spacing\x18\x03 \x01(\x02\x12\x1d\n\x15\x65ncoders_counts_per_m\x18\x04 \x01(\x02\x12\x1d\n\x0f\x65ncoders_period\x18\x05 \x01(\rB\x04\x80\xb5\x18\x05\x62\x06proto3'
  ,
  dependencies=[goldo_dot_pb2__options__pb2.DESCRIPTOR,])




_ROBOTSIMULATORCONFIG = _descriptor.Descriptor(
  name='RobotSimulatorConfig',
  full_name='goldo.nucleo.robot_simulator.RobotSimulatorConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='speed_coeff', full_name='goldo.nucleo.robot_simulator.RobotSimulatorConfig.speed_coeff', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='wheels_spacing', full_name='goldo.nucleo.robot_simulator.RobotSimulatorConfig.wheels_spacing', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='encoders_spacing', full_name='goldo.nucleo.robot_simulator.RobotSimulatorConfig.encoders_spacing', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='encoders_counts_per_m', full_name='goldo.nucleo.robot_simulator.RobotSimulatorConfig.encoders_counts_per_m', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='encoders_period', full_name='goldo.nucleo.robot_simulator.RobotSimulatorConfig.encoders_period', index=4,
      number=5, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\200\265\030\005', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=94,
  serialized_end=249,
)

DESCRIPTOR.message_types_by_name['RobotSimulatorConfig'] = _ROBOTSIMULATORCONFIG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

RobotSimulatorConfig = _reflection.GeneratedProtocolMessageType('RobotSimulatorConfig', (_message.Message,), {
  'DESCRIPTOR' : _ROBOTSIMULATORCONFIG,
  '__module__' : 'goldo.nucleo.robot_simulator_pb2'
  # @@protoc_insertion_point(class_scope:goldo.nucleo.robot_simulator.RobotSimulatorConfig)
  })
_sym_db.RegisterMessage(RobotSimulatorConfig)


_ROBOTSIMULATORCONFIG.fields_by_name['encoders_period']._options = None
# @@protoc_insertion_point(module_scope)
