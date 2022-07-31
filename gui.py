import sys

from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit, QPushButton, QLabel


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
        self.joinButton.clicked.connect(self.hostButtonClicked)

        self.grid.addWidget(self.ipLineEdit, 0, 0, 1, 2)
        self.grid.addWidget(self.joinButton, 0, 2)
        self.grid.addWidget(self.hostButton, 0, 3)
        self.grid.addWidget(self.statusLable, 1, 0, 1, 4)
        
        self.setLayout(self.grid)

    def joinButtonClicked(self):
        pass

    def hostButtonClicked(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
