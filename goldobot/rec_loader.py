import struct
import bisect

from google.protobuf.descriptor import MakeDescriptor
from google.protobuf.message_factory import MessageFactory
from google.protobuf.descriptor_pb2 import DescriptorProto,  FieldDescriptorProto, FileDescriptorProto
from google.protobuf.descriptor_pool import DescriptorPool
from google.protobuf.proto_builder import MakeSimpleProtoClass

import google.protobuf.empty_pb2
import google.protobuf.wrappers_pb2

from google.protobuf import descriptor_pool as _descriptor_pool

class RecLoader:
    def __init__(self):
        self._messages = []
        self._timestamps = []
        
    def __len__(self):
        return len(self._messages)

    def open(self, path):
        pool = DescriptorPool()
        # Add default protos for now
        d = _descriptor_pool.Default().FindFileByName('google/protobuf/descriptor.proto')
        dp = FileDescriptorProto()
        d.CopyToProto(dp)
        pool.AddSerializedFile(dp.SerializeToString())
        
        d = _descriptor_pool.Default().FindFileByName('google/protobuf/wrappers.proto')
        dp = FileDescriptorProto()
        d.CopyToProto(dp)
        pool.AddSerializedFile(dp.SerializeToString())
        
        d = _descriptor_pool.Default().FindFileByName('google/protobuf/empty.proto')
        dp = FileDescriptorProto()
        d.CopyToProto(dp)
        pool.AddSerializedFile(dp.SerializeToString())
        
        self._pool = pool
        descr = DescriptorProto(name='RecordFileHeader', field = [
            FieldDescriptorProto(
                name='data',
                number=1,
                label=FieldDescriptorProto.LABEL_REPEATED,
                type=FieldDescriptorProto.TYPE_BYTES)
            ]            
        )
        file_descriptor_proto = FileDescriptorProto()
        file_descriptor_proto.message_type.add().MergeFrom(descr)
        file_descriptor_proto.name = 'rec_file_header.proto'       
        pool.Add(file_descriptor_proto)
        descr = pool.FindFileByName('rec_file_header.proto').message_types_by_name['RecordFileHeader']
    
        message_factory = MessageFactory(pool=pool)
        RecFileHeader = message_factory.GetPrototype(descr)        
        
        with open(path, 'rb') as f:
            d = f.read(13)
            header_size, = struct.unpack('<I', d[9:])
            d = f.read(header_size)
            header = RecFileHeader()
            header.ParseFromString(d)
            file_protos = []
            for d in header.data:
                fdp = FileDescriptorProto()
                fdp.ParseFromString(d)
                pool.Add(fdp)
            try:
                self._messages = []
                self._timestamps = []
                while True:
                    h = struct.unpack('<IIII', f.read(16))
                    topic = f.read(h[1]).decode('utf8')
                    full_name = f.read(h[2]).decode('utf8')
                    payload = f.read(h[3])
                    msg = message_factory.GetPrototype(pool.FindMessageTypeByName(full_name))()
                    msg.ParseFromString(payload)
                    self._timestamps.append(h[0])
                    self._messages.append((topic, msg))
            except:
                pass
                

def reconstruct_stream(l):
    encoders_left = []
    encoders_right = []
    for topic, msg in l._messages:
        if topic == b'nucleo/out/propulsion/odometry_stream':
            timestamp = struct.unpack('<I', msg.value[0:4])
            vals = [struct.unpack('<HH', msg.value[i*4:(i+1)*4]) for i in range(1, len(msg.value)//4)]
            for v in vals:
                encoders_left.append(v[0])
    return encoders_left
#encoders_left = reconstruct_stream(l) 