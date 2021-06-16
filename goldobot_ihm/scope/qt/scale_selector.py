from PyQt5.QtWidgets import QSpinBox

scales = [
    (0.01, '10m'),
    (0.02, '20m'),
    (0.05, '50m'),
    (0.1, '100m'),
    (0.2, '200m'),
    (0.5, '500m'),
    (1, '1'),
    (2, '2'),
    (5, '5'),
    (10, '10'),
    (20, '20'),
    (50, '50'),
    (100, '100'),
    (200, '200'),
    (500, '500'),
    (1000, '1k'),
    (2000, '2k'),
    (5000, '5k'),
    (10000, '10k'),
    (20000, '20k'),
    ]

class ScaleSelectorWidget(QSpinBox):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setRange(0,len(scales) - 1)
        
    def textFromValue(self, value):
        return scales[value][1]
        
    def valueFromText(self, text):
        print('vft')
        
    @property
    def scale(self):
        return scales[self.value()][0]