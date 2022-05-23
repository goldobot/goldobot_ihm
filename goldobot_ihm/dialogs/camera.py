from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QPixmap

from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel, QPushButton

class CameraDialog(QDialog):
   
    
    def __init__(self, parent = None):
        super().__init__(parent)
        self._client = None
       
        layout = QGridLayout()
        self._label = QLabel()
        self._button = QPushButton()


        
        layout.addWidget(self._label)
        layout.addWidget(self._button)
        self.setLayout(layout)      

        self._button.clicked.connect(self._on_capture_clicked)        


    def set_client(self, client: ''):
        self._client = client
        self._client.registerCallback('camera/video/frame', self._on_camera_frame)
        self._client.registerCallback('camera/detections', self._on_detections)
        
    def _on_camera_frame(self, msg):
        pixmap= QPixmap()
        pixmap.loadFromData(msg.value)
        self._label.setPixmap(pixmap)
        
    def _on_capture_clicked(self):
        self._client.publishTopic('camera/in/capture')
        
    def _on_detections(self,msg):
        print('camera', msg)

