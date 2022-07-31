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

    def createWidgets(self):
        self.grid = QGridLayout()

        self.ipLineEdit = QLineEdit()
        self.joinButton = QPushButton("Join")
        self.hostButton = QPushButton("Host")
        self.statusLable = QLabel("Status: Waiting for user input...")

        self.joinButton.clicked.connect(self.joinButtonClicked)
        self.hostButton.clicked.connect(self.hostButtonClicked)

        self.grid.addWidget(self.ipLineEdit, 0, 0, 1, 2)
        self.grid.addWidget(self.joinButton, 0, 2)
        self.grid.addWidget(self.hostButton, 0, 3)
        self.grid.addWidget(self.statusLable, 1, 0, 1, 4)
        
        self.setLayout(self.grid)

    def joinButtonClicked(self):
        self.disableControlls()
        self.setStatus("Connecting...")

        client = SharedMouseClient(self.ipLineEdit.text(), 8901)
        self.setStatus("Connected to server!")

        Thread(target=client.clientLoop, daemon=True).start()

    def hostButtonClicked(self):
        self.disableControlls()
        server = SharedMouseServer('0.0.0.0', 8901)
        Thread(target=self.waitClient, args=(server,), daemon=True).start()
        self.setStatus("Waiting for client...")

    def waitClient(self, server: SharedMouseServer):
        server.waitForClient()
        self.setStatus("Connected to client!")
        server.startMouseListener()

    def setStatus(self, text: str):
        self.statusLable.setText(f"Status: {text}")

    def disableControlls(self):
        self.ipLineEdit.setEnabled(False)
        self.joinButton.setEnabled(False)
        self.hostButton.setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
