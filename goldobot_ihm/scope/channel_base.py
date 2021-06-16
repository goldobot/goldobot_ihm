import numpy as np

class ChannelBase(object):
    scale: float
    offset: float
    lim_min: float
    lim_max: float
    timebase: object
    
    def __init__(self):
        self._data_x = np.array([],dtype=np.float32)
        self._data_y = np.array([],dtype=np.float32)
        self.variable = ''
        #self._timebase = timebase

        self.offset = 0
        self.scale = 1       
        self.max_points = 10000
        
    def update_offset(self, offset):
        self.offset = offset
        self.lim_min = self.offset - self.scale * 5
        self.lim_max = self.offset + self.scale * 5
        
        
    def update_scale(self, scale):
        self.scale = scale
        self.lim_min = self.offset - self.scale * 5
        self.lim_max = self.offset + self.scale * 5
        
    def set_data(self, x, y):
        self._data_x = np.array(x, dtype=np.float32)
        self._data_y = np.array(y, dtype=np.float32)
        
    def append_data(self, x, y):
        if x.shape != y.shape:
            raise RuntimeError("x and y arrays must have the same dimensions")
        self._data_x = np.append(self._data_x, x)
        self._data_y = np.append(self._data_y, y)
        
        if self._data_x.shape[0] > self.max_points:
            self._data_x = self._data_x[-self.max_points:]
            self._data_y = self._data_y[-self.max_points:]

        
    def refresh(self):
        """
        Recompute display coordinates and update display.        
        """        
        
        x = (self._data_x - self.timebase.reference_timestamp - self.timebase.offset) / self.timebase.time_per_div
        y = (self._data_y + self.offset) / self.scale
        self.update_display(x, y)
        
    def update_display(self, x, y):
        """Reimplemented in subclass"""
        pass
        
        