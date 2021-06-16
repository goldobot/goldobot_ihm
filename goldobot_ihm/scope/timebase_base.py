




class ScopeTimeBase(QWidget):
    
    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent        
        layout = QGridLayout()
        self._listbox_select_variable = QComboBox()
        layout.addWidget(self._listbox_select_variable)        
        self.setLayout(layout)
        self.reference_timestamp = 5
        
        self.min_value = 0
        self.max_value = 10
        self.scale = 1
        self.time_per_div = 1
        
    def _on_scale(self):
        pass
        
    def _on_offset(self):
        pass