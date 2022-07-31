from socket import socket, AF_INET, SOCK_STREAM
from pynput import mouse


class SharedMouseServer:
    def __init__(self, host: str, port: int):
        self.headerLength = 10

        self.host = host
        self.port = port

        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket.bind((self.host, self.port))
        self.serverSocket.listen(1)
    
    def waitForClient(self):
        self.connection, _ = self.serverSocket.accept()

    def onMouseMove(self, x: int, y: int):
        self.send_text(self.connection, f"MV:{x},{y}")

    def onMouseClick(self, x: int, y: int, button: mouse.Button, pressed: bool):
        self.send_text(self.connection, f"CL:{x},{y},{button.name},{int(pressed)}")

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
        self.serverSocket.close()
