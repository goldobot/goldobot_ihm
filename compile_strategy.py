import struct

class RobotCommandSetPose:
	def __init__(self,compiler,args,blocking):
		self._point_id = args[0]
		self._point_idx = compiler._point_ids[self._point_id]
		self._angle = int(args[1])
		self._blocking = blocking

	def serialize(self):
		return struct.pack('<BBHh', 1, self._blocking, self._point_idx, self._angle)

	def __repr__(self):
		return '<SetPose {}, {} deg>'.format(self._point_id,self._angle)

class RobotCommandRotation:
	def __init__(self,compiler,args,blocking):
		self._angle = int(args[0])
		self._blocking = blocking

	def serialize(self):
		return struct.pack('<BBhBB', 2, self._blocking,  self._angle, 0, 0)

	def __repr__(self):
		return '<Rotation {} deg>'.format(self._angle)

class RobotCommandReposition:
	def __init__(self,compiler,args,blocking):
		self._angle = int(args[0])
		self._distance = int(args[1])
		self._blocking = blocking

	def serialize(self):
		return struct.pack('<BBhh', 4, self._blocking,  self._angle, self._distance)

	def __repr__(self):
		return '<Reposition {} deg, {} mm>'.format(self._angle, self._distance)

class RobotCommandArmsGoToPosition:
	def __init__(self,compiler,args,blocking):
		self._arm_id = args[0]
		self._position = int(args[1])
		self._blocking = blocking

	def serialize(self):
		return struct.pack('<BBBBH', 5, self._blocking,  self._arm_id,0,self._position)

	def __repr__(self):
		return '<arms.GoToPosition {}, {}>'.format(self._arm_id, self._position)

class RobotCommandArmsExecuteSequence:
	def __init__(self,compiler,args,blocking):
		self._arm_id = args[0]
		self._sequence = int(args[1])
		self._blocking = blocking

	def serialize(self):
		return b''

	def __repr__(self):
		return '<arms.ExecuteSequence {}, {}>'.format(self._arm_id, self._sequence)

_commands_dict ={
	'propulsion.set_pose': RobotCommandSetPose,
	'propulsion.rotation': RobotCommandRotation,
	'propulsion.reposition': RobotCommandReposition,
	'arms.go_to_position':RobotCommandArmsGoToPosition,
	'arms.execute_sequence':RobotCommandArmsExecuteSequence,
}
class StrategyCompiler:
	def __init__(self):
		self._points = []
		self._point_ids = {}
		self._trajectories_buffer = []

	def read_points(self):
		for l in open('robot_config/robot_positions.txt'):
			if l.startswith('//'):
				continue
			k,x,y = l.strip().split(',')
			self._point_ids[k] = len(self._points)
			self._points.append((int(x)*1e-3, int(y)*1e-3))

	def compile_strategy(self):
		self.read_points()
		#load sequences
		sequences = []
		sequence_ids = {}
		for l in open('robot_config/robot_sequences.txt'):
			if l.startswith('//'):
				continue
			if l.startswith('#begin '):
				args = l[7:].strip().split(',')
				cur_seq_id = args[0]
				cur_seq = []

			if l.startswith('#end'):
				sequence_ids[cur_seq_id] = len(sequences)
				sequences.append(cur_seq)
			fields = l.strip().split(',')
			if fields[0].endswith('$'):
				blocking = False
				fields[0] = fields[0][:-1]
			else:
				blocking = True
			if fields[0] in _commands_dict:				
				cur_seq.append(_commands_dict[fields[0]](self, fields[1:], blocking))
			
		self._commands = []
		self._sequences = []
		for s in sequences:
			beg = len(self._commands)
			for c in s:
				self._commands.append(c)
			self._sequences.append((beg, len(self._commands)))


sc = StrategyCompiler()
sc.compile_strategy()
print(sc.__dict__)