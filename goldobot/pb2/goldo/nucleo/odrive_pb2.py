# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: goldo/nucleo/odrive.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='goldo/nucleo/odrive.proto',
  package='goldo.nucleo.odrive',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x19goldo/nucleo/odrive.proto\x12\x13goldo.nucleo.odrive\"\x88\x01\n\rRequestPacket\x12\x17\n\x0fsequence_number\x18\x01 \x01(\x05\x12\x13\n\x0b\x65ndpoint_id\x18\x02 \x01(\x05\x12\x1e\n\x16\x65xpected_response_size\x18\x03 \x01(\x05\x12\x0f\n\x07payload\x18\x04 \x01(\x0c\x12\x18\n\x10protocol_version\x18\x05 \x01(\x05\":\n\x0eResponsePacket\x12\x17\n\x0fsequence_number\x18\x01 \x01(\x05\x12\x0f\n\x07payload\x18\x04 \x01(\x0c\x62\x06proto3'
)




_REQUESTPACKET = _descriptor.Descriptor(
  name='RequestPacket',
  full_name='goldo.nucleo.odrive.RequestPacket',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='sequence_number', full_name='goldo.nucleo.odrive.RequestPacket.sequence_number', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='endpoint_id', full_name='goldo.nucleo.odrive.RequestPacket.endpoint_id', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='expected_response_size', full_name='goldo.nucleo.odrive.RequestPacket.expected_response_size', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='payload', full_name='goldo.nucleo.odrive.RequestPacket.payload', index=3,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='protocol_version', full_name='goldo.nucleo.odrive.RequestPacket.protocol_version', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=51,
  serialized_end=187,
)


_RESPONSEPACKET = _descriptor.Descriptor(
  name='ResponsePacket',
  full_name='goldo.nucleo.odrive.ResponsePacket',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='sequence_number', full_name='goldo.nucleo.odrive.ResponsePacket.sequence_number', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='payload', full_name='goldo.nucleo.odrive.ResponsePacket.payload', index=1,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
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
  serialized_start=189,
  serialized_end=247,
)

DESCRIPTOR.message_types_by_name['RequestPacket'] = _REQUESTPACKET
DESCRIPTOR.message_types_by_name['ResponsePacket'] = _RESPONSEPACKET
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

RequestPacket = _reflection.GeneratedProtocolMessageType('RequestPacket', (_message.Message,), {
  'DESCRIPTOR' : _REQUESTPACKET,
  '__module__' : 'goldo.nucleo.odrive_pb2'
  # @@protoc_insertion_point(class_scope:goldo.nucleo.odrive.RequestPacket)
  })
_sym_db.RegisterMessage(RequestPacket)

ResponsePacket = _reflection.GeneratedProtocolMessageType('ResponsePacket', (_message.Message,), {
  'DESCRIPTOR' : _RESPONSEPACKET,
  '__module__' : 'goldo.nucleo.odrive_pb2'
  # @@protoc_insertion_point(class_scope:goldo.nucleo.odrive.ResponsePacket)
  })
_sym_db.RegisterMessage(ResponsePacket)


# @@protoc_insertion_point(module_scope)
