from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QLineEdit
from widgets.properties_editor import PropertiesEditorWidget

from messages import OdometryConfig
import message_types



class SequencesDialog(QDialog):
    def __init__(self, parent = None):
        super(SequencesDialog, self).__init__(None)
        self._client = None
        wid = QLineEdit()

        self._get_button = QPushButton('Get')

    def set_client(self, client):
        self._client = client