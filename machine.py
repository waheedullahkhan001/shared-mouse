from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Machine(QVBoxLayout):

    def __init__(self, imgPixmap: QPixmap):
        super().__init__()
        self.machineImageLabel = QLabel()
        self.machineNameLineEdit = QLineEdit()

        self.machineImageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.machineImageLabel.setPixmap(imgPixmap)
        self.machineNameLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.machineNameLineEdit.setFixedWidth(150)
        self.machineNameLineEdit.setPlaceholderText("Machine Name")

        self.addWidget(self.machineImageLabel)
        self.addWidget(self.machineNameLineEdit)

    def set_machine_name(self, name: str):
        self.machineNameLineEdit.setText(name)

    def get_machine_name(self):
        return self.machineNameLineEdit.text()

    def set_machine_name_editable(self, editable: bool):
        self.machineNameLineEdit.setReadOnly(not editable)
