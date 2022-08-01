from socket import socket, AF_INET, SOCK_STREAM
from pynput import mouse


class SharedMouseServer:
    def __init__(self, host: str, port: int, height: int, width: int):
        self.screenHeight = height
        self.screenWidth = width
        self.connection = None
        self.headerLength = 10

        self.host = host
        self.port = port

        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket.bind((self.host, self.port))
        self.serverSocket.listen(1)

    def waitForClient(self):
        self.connection, _ = self.serverSocket.accept()

    def onMouseMove(self, x: int, y: int):
        xPercent = (float(x) / float(self.screenWidth)) * float(100)
        yPercent = (float(y) / float(self.screenHeight)) * float(100)
        self.send_text(self.connection, f"MV:{xPercent},{yPercent}")

    def onMouseClick(self, x: int, y: int, button: mouse.Button, pressed: bool):
        xPercent = (float(x) / float(self.screenWidth)) * float(100)
        yPercent = (float(y) / float(self.screenHeight)) * float(100)
        self.send_text(self.connection, f"CL:{xPercent},{yPercent},{button.name},{int(pressed)}")

    def onMouseScroll(self, x: int, y: int, dx: int, dy: int):
        self.send_text(self.connection, f"SC:{dx},{dy}")

    def startMouseListener(self):
        listener = mouse.Listener(
            on_move=self.onMouseMove,
            on_click=self.onMouseClick,
            on_scroll=self.onMouseScroll)
        listener.start()

    def send_text(self, connection: socket, text: str):
        header = bytes(f"{len(text):<{self.headerLength}}", "utf-8")
        connection.sendall(header + bytes(text, "utf-8"))

    def recv_text(self, connection: socket):
        header = connection.recv(self.headerLength)
        while len(header) < self.headerLength:
            header += connection.recv(self.headerLength - len(header))

        messageLength = int(header.decode("utf-8").strip())
        message = connection.recv(messageLength).decode("utf-8")
        while len(message) < messageLength:
            message += connection.recv(messageLength - len(message)).decode("utf-8")

        return message

    def close(self):
        # temp fix for closing server
        try:
            temp_client = socket(AF_INET, SOCK_STREAM)
            temp_client.connect(("localhost", self.port))
            temp_client.close()
        except Exception:
            pass
        self.serverSocket.close()
