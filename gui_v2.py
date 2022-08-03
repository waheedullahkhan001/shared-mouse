# PyQt5 GUI App


import sys
import socket
from threading import Thread

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from client import SharedMouseClient
from machine import Machine
from server import SharedMouseServer


class GUI(QMainWindow):
    def __init__(self, port: int, height: int, width: int):
        super().__init__()

        self.rightMachine = None
        self.middleMachine = None
        self.leftMachine = None
        self.port = port
        self.screenHeight = height
        self.screenWidth = width

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

        self.create_menu()
        self.create_widgets()

        self.joining = False
        self.hosting = False
        self.server = None
        self.client = None
        self.serverThread = None
        self.clientThread = None

    def create_menu(self):
        menubar = self.menuBar()
        menubar.addMenu("Dashboard")
        menubar.addMenu("Settings")

    def create_widgets(self):
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

        self.checkBox.stateChanged.connect(self.security_key_checkbox_clicked)

        self.hBox1.addWidget(self.securityKeyLabel)
        self.hBox1.addWidget(self.securityKeyLineEdit)
        self.hBox1.addWidget(self.checkBox)
        self.hBox1.addWidget(self.newKeyButton)

        # Row 2
        imgPixmap = QPixmap("resources/images/machine.png")
        self.leftMachine = Machine(imgPixmap)
        self.leftMachine.set_machine_name_editable(False)
        self.hBox2.addLayout(self.leftMachine)
        self.middleMachine = Machine(imgPixmap)
        self.hBox2.addLayout(self.middleMachine)
        self.rightMachine = Machine(imgPixmap)
        self.rightMachine.set_machine_name_editable(False)
        self.hBox2.addLayout(self.rightMachine)

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
        self.newKeyButton.clicked.connect(self.new_key_button_clicked)
        self.joinButton.clicked.connect(self.join_button_clicked)
        self.hostButton.clicked.connect(self.host_button_clicked)

    def new_key_button_clicked(self):
        print(self.securityKeyLineEdit.text())

    def security_key_checkbox_clicked(self):
        self.securityKeyLineEdit.setEchoMode(QLineEdit.Normal) if self.checkBox.isChecked() \
            else self.securityKeyLineEdit.setEchoMode(QLineEdit.Password)

    def set_status(self, text: str):
        self.statusLabel.setText(f"Status: {text}")

    def join_button_clicked(self):
        if not self.joining:
            address = self.addressLineEdit.text()
            if address == "":
                address = "localhost"
            try:
                self.set_status("Connecting...")
                self.client = SharedMouseClient(address, self.port, self.screenWidth, self.screenHeight)
                clientMachineName = socket.gethostname()

                hostMachineName = self.client.recv_text()
                self.client.send_text(f"MN:{clientMachineName}")

                hostMachineName = hostMachineName.split(":")[1]
                self.set_status("Connected to " + hostMachineName)

                self.leftMachine.set_machine_name(clientMachineName)
                self.leftMachine.set_machine_name_editable(False)
                self.middleMachine.set_machine_name(hostMachineName)
                self.middleMachine.set_machine_name_editable(False)

                self.clientThread = Thread(target=self.client.clientLoop, daemon=True)
                self.clientThread.start()
                self.joining = True
                self.joinButton.setText("Stop")
                self.hostButton.setEnabled(False)
                self.addressLineEdit.setEnabled(False)
            except Exception:
                self.set_status("Something went wrong while connecting to server!")
        else:
            # kill clientThread here & test if it works
            self.client.close()  # This should cause exception in clientThread to kill it
            self.set_status("Waiting for user input...")
            self.joinButton.setText("Join")
            self.joinButton.setEnabled(True)
            self.hostButton.setEnabled(True)
            self.leftMachine.set_machine_name("")
            self.leftMachine.set_machine_name_editable(True)
            self.middleMachine.set_machine_name("")
            self.middleMachine.set_machine_name_editable(True)
            self.rightMachine.set_machine_name("")
            self.rightMachine.set_machine_name_editable(True)
            self.addressLineEdit.setEnabled(True)
            self.joining = False

    def host_button_clicked(self):
        if not self.hosting:
            machineName = self.middleMachine.get_machine_name()
            if machineName == "":
                machineName = socket.gethostname()
                self.middleMachine.set_machine_name(machineName)
            self.middleMachine.set_machine_name_editable(False)
            self.leftMachine.set_machine_name_editable(False)

            self.joinButton.setEnabled(False)
            self.addressLineEdit.setEnabled(False)
            self.server = SharedMouseServer("0.0.0.0", self.port, self.screenWidth, self.screenHeight)
            self.serverThread = Thread(target=self.wait_for_client, args=(self.server, machineName), daemon=True)
            self.serverThread.start()
            self.set_status("Waiting for client...")
            self.hostButton.setText("Stop")
            self.hosting = True
        else:
            # kill serverThread here & test if it works
            self.server.close()
            self.set_status("Waiting for user input...")
            self.joinButton.setEnabled(True)
            self.addressLineEdit.setEnabled(True)
            self.middleMachine.set_machine_name_editable(True)
            self.hostButton.setText("Host")
            self.leftMachine.set_machine_name("")
            self.leftMachine.set_machine_name_editable(True)
            self.middleMachine.set_machine_name_editable(True)
            self.rightMachine.set_machine_name("")
            self.rightMachine.set_machine_name_editable(True)
            self.hosting = False

    def wait_for_client(self, server: SharedMouseServer, machineName: str):
        try:  # debug
            server.wait_for_client()
            server.send_text(f"MN:{machineName}")
            clientMachineName = server.recv_text()
            self.leftMachine.set_machine_name(clientMachineName.split(":")[1])
            self.leftMachine.set_machine_name_editable(False)
            self.set_status("Connected to client!")
            server.start_mouse_listener()
        except Exception as e:  # debug
            print(f"DEBUG: serverThread: waitClient: Exception\nMSG: {e}")  # debug


if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    size = screen.size()
    gui = GUI(port=8901, height=size.height(), width=size.width())
    gui.show()
    sys.exit(app.exec_())
