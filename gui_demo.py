# PyQt5 GUI App


import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *


class GUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sahred Mouse")
        self.resize(600, 300)

        self.createMenu()
        self.createWidgets()

    def createMenu(self):
        menubar = self.menuBar()
        dashboardMenu = menubar.addMenu("Dasboard")
        settingsMenu = menubar.addMenu("Settings")

    def createWidgets(self):
        self.root = QWidget()
        self.vbox = QVBoxLayout()
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.hbox3 = QHBoxLayout()

        self.hbox2.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.hbox3.setAlignment(Qt.AlignmentFlag.AlignBottom)

        self.setCentralWidget(self.root)
        self.root.setLayout(self.vbox)
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        self.vbox.addLayout(self.hbox3)
        self.vbox.addLayout(self.hbox3)


        self.secrityKeyLabel = QLabel("Security Key:")
        self.securityKeyLineEdit = QLineEdit()
        self.checkBox = QCheckBox("Show text")
        self.newKeyButton = QPushButton("New Key")

        self.hbox1.addWidget(self.secrityKeyLabel)
        self.hbox1.addWidget(self.securityKeyLineEdit)
        self.hbox1.addWidget(self.checkBox)
        self.hbox1.addWidget(self.newKeyButton)


        for i in range(4):
            vbox = QVBoxLayout()

            self.hbox2.addLayout(vbox)

            
            imageLabel = QLabel()
            lineEdit = QLineEdit()
            imgPixmap = QPixmap("resources/images/computer.png")

            imgPixmap = imgPixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
            imageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            imageLabel.setPixmap(imgPixmap)
            lineEdit.setPlaceholderText("Machine Name")

            vbox.addWidget(imageLabel)
            vbox.addWidget(lineEdit)

        
        self.ipLineEdit = QLineEdit()
        self.joinButton = QPushButton("Join")
        self.hostButton = QPushButton("Host")

        self.ipLineEdit.setPlaceholderText("IP Address")

        self.hbox3.addWidget(self.ipLineEdit)
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())