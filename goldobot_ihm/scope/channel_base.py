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
        #self._timebase = timebase

        self.offset = 0
        self.scale = 1        
        
    def update_offset(self, offset):
        self.offset = offset
        
    def update_scale(self, scale):
        self.scale = scale
        
    def set_data(self, x, y):
        self._data_x = np.array(x, dtype=np.float32)
        self._data_y = np.array(y, dtype=np.float32)
        
    def append_data(self, x, y):
        if x.shape != y.shape:
            raise RuntimeError("x and y arrays must have the same dimensions")
        self._data_x = np.append(self._data_x, x)
        self._data_y = np.append(self._data_y, y)
        
    def refresh(self):
        """
        Recompute display coordinates and update display.        
        """
        self.min_value = self.offset - self.scale * 5
        self.max_value = self.offset + self.scale * 5
        
        x = self._data_x - self.timebase.reference_timestamp
        y = (self._data_y + self.offset) / self.scale
        self.update_display(x, y)
        
    def update_display(self, x, y):
        """Reimplemented in subclass"""
        pass
        
        