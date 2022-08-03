import sys

from threading import Thread

from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit, QPushButton, QLabel

from server import SharedMouseServer
from client import SharedMouseClient


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shared Mouse")
        self.setFixedSize(400, 80)
        self.createWidgets()
        self.show()
        self.server = None
        self.client = None
        self.hostThread = None
        self.clientThread = None

    def createWidgets(self):
        self.grid = QGridLayout()

        self.addressTextField = QLineEdit()
        self.joinButton = QPushButton("Join")
        self.hostButton = QPushButton("Host")
        self.statusLable = QLabel("Status: Waiting for user input...")
        self.hosting = False
        self.joining = False

        self.joinButton.clicked.connect(self.joinButtonClicked)
        self.hostButton.clicked.connect(self.hostButtonClicked)

        self.grid.addWidget(self.addressTextField, 0, 0, 1, 2)
        self.grid.addWidget(self.joinButton, 0, 2)
        self.grid.addWidget(self.hostButton, 0, 3)
        self.grid.addWidget(self.statusLable, 1, 0, 1, 4)
        
        self.setLayout(self.grid)

    def joinButtonClicked(self):
        # self.disableControlls()
        if not self.joining:
            address = self.addressTextField.text()
            if address == "":
                address = "localhost"
            try:
                self.setStatus("Connecting...")
                self.client = SharedMouseClient(address, 8901)
                self.setStatus("Connected to server!")
                self.clientThread = Thread(target=self.client.clientLoop, daemon=True)
                self.clientThread.start()
                self.joining = True
                self.joinButton.setText("Stop")
                self.hostButton.setEnabled(False)
                self.addressTextField.setEnabled(False)
            except Exception as e:
                self.setStatus("Something went wrong while connecting to server!")
        else:
            # kill clientThread here & test if it works
            self.client.close()
            self.setStatus("Waiting for user input...")
            self.joinButton.setText("Join")
            self.joinButton.setEnabled(True)
            self.hostButton.setEnabled(True)
            self.addressTextField.setEnabled(True)
            self.joining = False

    def hostButtonClicked(self):
        if not self.hosting:
            self.joinButton.setEnabled(False)
            self.addressTextField.setEnabled(False)
            self.server = SharedMouseServer('0.0.0.0', 8901)
            self.hostThread = Thread(target=self.waitClient, args=(self.server,), daemon=True)
            self.hostThread.start()
            self.setStatus("Waiting for client...")
            self.hostButton.setText("Stop")
            self.hosting = True
        else:
            # kill hostThread here & test if it works
            self.server.close()
            self.setStatus("Waiting for user input...")
            self.joinButton.setEnabled(True)
            self.addressTextField.setEnabled(True)
            self.hostButton.setText("Host")
            self.hosting = False

    def waitClient(self, server: SharedMouseServer):
        server.wait_for_client()
        self.setStatus("Connected to client!")
        server.start_mouse_listener()

    def setStatus(self, text: str):
        self.statusLable.setText(f"Status: {text}")

    def disableControlls(self):
        self.addressTextField.setEnabled(False)
        self.joinButton.setEnabled(False)
        self.hostButton.setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
