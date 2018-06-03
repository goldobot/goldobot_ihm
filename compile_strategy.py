import struct

class RobotCommandDelay:
	def __init__(self,compiler,args,blocking):
		self._delay_ms = int(args[0])		
		self._blocking = blocking

	def serialize(self):
		return struct.pack('<BBH', 8, self._blocking, self._delay_ms)

	def __repr__(self):
		return '<Delay {} ms>'.format(self._delay_ms)

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

class RobotCommandTrajectory:
	def __init__(self,compiler,args,blocking):
		self._speed_settings = int(args[0])
		self._point_ids = [compiler._point_ids[a] for a in args[1:]]
		self._begin_idx = len(compiler._trajectory_buffer)
		self._num_points = len(self._point_ids)
		self._blocking = blocking
		compiler._trajectory_buffer += self._point_ids

	def serialize(self):
		return struct.pack('<BBHBB', 4, self._blocking,  self._begin_idx, self._num_points, 0)

	def __repr__(self):
		return '<Trajectory {},{}>'.format(self._speed_settings, self._point_ids)

class RobotCommandReposition:
	def __init__(self,compiler,args,blocking):
		self._angle = int(args[0])
		self._distance = int(args[1])
		self._blocking = blocking

	def serialize(self):
		return struct.pack('<BBhh', 5, self._blocking,  self._angle, self._distance)

	def __repr__(self):
		return '<Reposition {} deg, {} mm>'.format(self._angle, self._distance)

class RobotCommandArmsGoToPosition:
	def __init__(self,compiler,args,blocking):
		self._arm_id = _arm_ids[args[0]]
		self._position = int(args[1])
		self._blocking = blocking

	def serialize(self):
		return struct.pack('<BBBBH', 6, self._blocking,  self._arm_id,0,self._position)

	def __repr__(self):
		return '<arms.GoToPosition {}, {}>'.format(self._arm_id, self._position)

class RobotCommandArmsExecuteSequence:
	def __init__(self,compiler,args,blocking):
		self._arm_id = _arm_ids[args[0]]
		self._sequence = int(args[1])
		self._blocking = blocking

	def serialize(self):
		return struct.pack('<BBBBH', 7, self._blocking, self._arm_id,0,self._sequence)

	def __repr__(self):
		return '<arms.ExecuteSequence {}, {}>'.format(self._arm_id, self._sequence)

_commands_dict ={
	'propulsion.set_pose': RobotCommandSetPose,
	'propulsion.rotation': RobotCommandRotation,
	'propulsion.reposition': RobotCommandReposition,
	'propulsion.trajectory': RobotCommandTrajectory,
	'arms.go_to_position':RobotCommandArmsGoToPosition,
	'arms.execute_sequence':RobotCommandArmsExecuteSequence,
	'delay':RobotCommandDelay
}

_arm_ids = {
	'left': 0,
	'right': 1,
	'grabber': 2,
	'bascule': 3,
	'colonnes': 4,
}
class StrategyCompiler:
	def __init__(self):
		self._points = []
		self._point_ids = {}
		self._trajectory_buffer = []

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
		self._sequence_ids = sequence_ids
		for s in sequences:
			beg = len(self._commands)
			for c in s:
				self._commands.append(c)
			self._sequences.append((beg, len(self._commands)))


class ArmsStrategyCompiler:
	def __init__(self):
		pass
	def _load_sequences(self, file_path):
		for l in open(file_path):
			f = l.find('//')
			if f >= 0:
				l = l[:f]
			fields = l.strip('')
			pos_name = l[0]
		lines = [[int(e) for e in l.strip().split(',')] for l in open('robot_config/{}_positions.txt'.format(name)) if not l.startswith('//')]


sc = StrategyCompiler()
sc.compile_strategy()
print(sc.__dict__)
print(sc._trajectory_buffer)