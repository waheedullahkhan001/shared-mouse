# PyQt5 GUI App


import sys
from threading import Thread

from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from client import SharedMouseClient
from server import SharedMouseServer


class GUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.port = 8901
        self.root = None
        self.vBox = None

        self.hBox1 = None
        self.hBox2 = None
        self.hBox3 = None
        self.hBox4 = None
        self.hBox5 = None

        self.checkBox = None
        self.statusLabel = None
        self.hostButton = None
        self.joinButton = None
        self.securityKeyLineEdit = None
        self.securityKeyLabel = None
        self.newKeyButton = None
        self.addressLineEdit = None

        self.setWindowTitle("Shared Mouse")
        self.setFixedSize(550, 275)

        self.createMenu()
        self.createWidgets()

        self.joining = False
        self.hosting = False
        self.server = None
        self.client = None
        self.serverThread = None
        self.clientThread = None

    def createMenu(self):
        menubar = self.menuBar()
        menubar.addMenu("Dashboard")
        menubar.addMenu("Settings")

    def createWidgets(self):
        # Setting up basic layout
        self.root = QWidget()
        self.vBox = QVBoxLayout()
        self.vBox.setSpacing(15)

        self.setCentralWidget(self.root)
        self.root.setLayout(self.vBox)

        # Working area
        self.hBox1 = QHBoxLayout()
        self.hBox2 = QHBoxLayout()
        self.hBox3 = QHBoxLayout()
        self.hBox4 = QHBoxLayout()
        self.hBox5 = QHBoxLayout()

        self.vBox.addLayout(self.hBox1)
        self.vBox.addLayout(self.hBox2)
        self.vBox.addLayout(self.hBox3)
        self.vBox.addLayout(self.hBox3)
        self.vBox.addLayout(self.hBox4)
        self.vBox.addLayout(self.hBox5)

        # there are 5 entries (all hbox) in self.vBox each having stretch priority 0 (0,0,0,0,0)
        # 1, 2, 4, 5 are used to contain widgets and 3 is used as seperator
        # this line will set stretch priority of 3 to 1 (0,0,1,0,0) so other don't stretch
        # and make it look ugly
        self.vBox.setStretch(2, 1)

        # Row 1
        self.securityKeyLabel = QLabel("Security Key:")
        self.securityKeyLineEdit = QLineEdit()
        self.securityKeyLineEdit.setText("Demo Security Key")
        self.securityKeyLineEdit.setEchoMode(QLineEdit.Password)
        self.securityKeyLineEdit.setReadOnly(True)
        self.checkBox = QCheckBox("Show text")
        self.newKeyButton = QPushButton("New Key")

        self.checkBox.stateChanged.connect(self.securityKeyCheckBoxClicked)

        self.hBox1.addWidget(self.securityKeyLabel)
        self.hBox1.addWidget(self.securityKeyLineEdit)
        self.hBox1.addWidget(self.checkBox)
        self.hBox1.addWidget(self.newKeyButton)

        # Row 2
        imgPixmap = QPixmap("resources/images/machine.png")

        for _ in range(3):  # we will only work with 3 computers for now
            vBox = QVBoxLayout()
            self.hBox2.addLayout(vBox)
            machineImageLabel = QLabel()
            machineNameLineEdit = QLineEdit()

            machineImageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            machineImageLabel.setPixmap(imgPixmap)
            machineNameLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
            machineNameLineEdit.setFixedWidth(150)
            machineNameLineEdit.setPlaceholderText("Machine Name")

            vBox.addWidget(machineImageLabel)
            vBox.addWidget(machineNameLineEdit)

        # Row 3
        self.addressLineEdit = QLineEdit()
        self.joinButton = QPushButton("Join")
        self.hostButton = QPushButton("Host")

        self.addressLineEdit.setPlaceholderText("IP Address")

        self.hBox4.addWidget(self.addressLineEdit)
        self.hBox4.addWidget(self.joinButton)
        self.hBox4.addWidget(self.hostButton)

        # Row 4
        self.statusLabel = QLabel("Status: Waiting for user input...")
        self.statusLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.hBox5.addWidget(self.statusLabel)

        # Connecting signals
        self.newKeyButton.clicked.connect(self.newKeyButtonClicked)
        self.joinButton.clicked.connect(self.joinButtonClicked)
        self.hostButton.clicked.connect(self.hostButtonClicked)

    def newKeyButtonClicked(self):
        print(self.securityKeyLineEdit.text())

    def securityKeyCheckBoxClicked(self):
        self.securityKeyLineEdit.setEchoMode(QLineEdit.Normal) if self.checkBox.isChecked() \
            else self.securityKeyLineEdit.setEchoMode(QLineEdit.Password)

    def setStatus(self, text: str):
        self.statusLabel.setText(f"Status: {text}")

    def joinButtonClicked(self):
        if not self.joining:
            address = self.addressLineEdit.text()
            if address == "":
                address = "localhost"
            try:
                self.setStatus("Connecting...")
                self.client = SharedMouseClient(address, self.port, self.getScreenHeight(), self.getScreenWidth())
                self.setStatus("Connected to server!")
                self.clientThread = Thread(target=self.client.clientLoop, daemon=True)
                self.clientThread.start()
                self.joining = True
                self.joinButton.setText("Stop")
                self.hostButton.setEnabled(False)
                self.addressLineEdit.setEnabled(False)
            except Exception:
                self.setStatus("Something went wrong while connecting to server!")
        else:
            # kill clientThread here & test if it works
            self.client.close()  # This should cause exception in clientThread to kill it
            self.setStatus("Waiting for user input...")
            self.joinButton.setText("Join")
            self.joinButton.setEnabled(True)
            self.hostButton.setEnabled(True)
            self.addressLineEdit.setEnabled(True)
            self.joining = False

    def hostButtonClicked(self):
        if not self.hosting:
            self.joinButton.setEnabled(False)
            self.addressLineEdit.setEnabled(False)
            self.server = SharedMouseServer("0.0.0.0", self.port, self.getScreenHeight(), self.getScreenWidth())
            self.serverThread = Thread(target=self.waitClient, args=(self.server,), daemon=True)
            self.serverThread.start()
            self.setStatus("Waiting for client...")
            self.hostButton.setText("Stop")
            self.hosting = True
        else:
            # kill serverThread here & test if it works
            self.server.close()
            self.setStatus("Waiting for user input...")
            self.joinButton.setEnabled(True)
            self.addressLineEdit.setEnabled(True)
            self.hostButton.setText("Host")
            self.hosting = False

    def waitClient(self, server: SharedMouseServer):
        try:  # debug
            server.waitForClient()
            self.setStatus("Connected to client!")
            server.startMouseListener()
        except Exception as e:  # debug
            print(f"DEBUG: serverThread: waitClient: Exception\nMSG: {e}")  # debug

    def getScreenHeight(self):
        return QtWidgets.QApplication(sys.argv).primaryScreen().size().height()

    def getScreenWidth(self):
        return QtWidgets.QApplication(sys.argv).primaryScreen().size().width()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())
