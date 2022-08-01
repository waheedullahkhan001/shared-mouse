# PyQt5 GUI App


import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *


class GUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Shared Mouse")
        self.resize(600, 300)

        self.createMenu()
        self.createWidgets()

        self.hosting = False
        self.joining = False

    def createMenu(self):
        menubar = self.menuBar()
        dashboardMenu = menubar.addMenu("Dashboard")
        settingsMenu = menubar.addMenu("Settings")

    def createWidgets(self):
        self.root = QWidget()
        self.vbox = QVBoxLayout()
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.hbox3 = QHBoxLayout()

        self.hbox2.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.hbox3.setAlignment(Qt.AlignmentFlag.AlignBottom)

        self.hbox2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hbox2.setSpacing(30)

        self.setCentralWidget(self.root)
        self.root.setLayout(self.vbox)
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        self.vbox.addLayout(self.hbox3)
        self.vbox.addLayout(self.hbox3)

        self.secrityKeyLabel = QLabel("Security Key:")
        self.securityKeyLineEdit = QLineEdit()
        self.securityKeyLineEdit.setText("Demo Security Key")
        self.securityKeyLineEdit.setEchoMode(QLineEdit.Password)
        self.securityKeyLineEdit.setReadOnly(True)
        self.checkBox = QCheckBox("Show text")
        self.checkBox.stateChanged.connect(self.showSecurityKeyCheckBoxSubmit)
        self.newKeyButton = QPushButton("New Key")

        self.hbox1.addWidget(self.secrityKeyLabel)
        self.hbox1.addWidget(self.securityKeyLineEdit)
        self.hbox1.addWidget(self.checkBox)
        self.hbox1.addWidget(self.newKeyButton)
        imgPixmap = QPixmap("resources/images/computer.png")
        imgPixmap = imgPixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)

        for i in range(3): # we will only work with 3 computers for now
            vbox = QVBoxLayout()
            self.hbox2.addLayout(vbox)

            machineImageLabel = QLabel()
            machineNameLineEdit = QLineEdit()

            machineImageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            machineImageLabel.setPixmap(imgPixmap)
            machineNameLineEdit.setPlaceholderText("Machine Name")
            machineNameLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
            machineNameLineEdit.setFixedWidth(150)

            vbox.addWidget(machineImageLabel)
            vbox.addWidget(machineNameLineEdit)


        self.addressLineEdit = QLineEdit()
        self.joinButton = QPushButton("Join")
        self.hostButton = QPushButton("Host")
        self.joinButton.clicked.connect(self.joinButtonSubmit)
        self.hostButton.clicked.connect(self.hostButtonSubmit)

        self.addressLineEdit.setPlaceholderText("IP Address")

        self.hbox3.addWidget(self.addressLineEdit)
        self.hbox3.addWidget(self.joinButton)
        self.hbox3.addWidget(self.hostButton)


        # self.statusLabel = QLabel("Status:")
        # self.statusLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)


        # self.ipLineEdit.deleteLater()
        # self.joinButton.deleteLater()
        # self.hostButton.deleteLater()

        # self.hbox3.addWidget(self.statusLabel)


        self.newKeyButton.clicked.connect(self.newkeyButtonSubmit)

    def newkeyButtonSubmit(self):
        print(self.securityKeyLineEdit.text())
    
    def showSecurityKeyCheckBoxSubmit(self):
        if self.checkBox.isChecked():
            self.securityKeyLineEdit.setEchoMode(QLineEdit.Normal)
        else:
            self.securityKeyLineEdit.setEchoMode(QLineEdit.Password)
    
    def hostButtonSubmit(self):
        if self.hosting:
            
            self.addressLineEdit.setEnabled(False)
            self.joinButton.setEnabled(False)
            self.newKeyButton.setEnabled(False)
            self.hostButton.setText("Stop")
            self.hosting = False
        else:

            self.addressLineEdit.setEnabled(True)
            self.joinButton.setEnabled(True)
            self.newKeyButton.setEnabled(True)
            self.hostButton.setText("Host")
            self.hosting = True
    
    def joinButtonSubmit(self):
        if self.joining:

            self.addressLineEdit.setEnabled(False)
            self.hostButton.setEnabled(False)
            self.newKeyButton.setEnabled(False)
            self.joinButton.setText("Stop")
            self.joining = False
        else:

            self.addressLineEdit.setEnabled(True)
            self.hostButton.setEnabled(True)
            self.newKeyButton.setEnabled(True)
            self.joinButton.setText("Join")
            self.joining = True

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())