from socket import socket, AF_INET, SOCK_STREAM
from pynput import mouse
from pynput import keyboard


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

    def wait_for_client(self):
        self.connection, _ = self.serverSocket.accept()

    def on_mouse_move(self, x: int, y: int):
        xPercent = (float(x) / float(self.screenWidth)) * float(100)
        yPercent = (float(y) / float(self.screenHeight)) * float(100)
        self.send_text(f"MV:{xPercent},{yPercent}")

    def on_mouse_click(self, x: int, y: int, button: mouse.Button, pressed: bool):
        xPercent = (float(x) / float(self.screenWidth)) * float(100)
        yPercent = (float(y) / float(self.screenHeight)) * float(100)
        self.send_text(f"CL:{xPercent},{yPercent},{button.name},{int(pressed)}")

    def on_mouse_scroll(self, x: int, y: int, dx: int, dy: int):
        self.send_text(f"SC:{dx},{dy}")

    def on_press(self, key):
        if hasattr(key, "vk"):
            self.send_text(f"PR:{key.vk}")

    def on_release(self, key):
        if hasattr(key, "vk"):
            self.send_text(f"RE:{key.vk}")

    def start_mouse_listener(self):
        mouseListener = mouse.Listener(
            on_move=self.on_mouse_move,
            on_click=self.on_mouse_click,
            on_scroll=self.on_mouse_scroll)
        keyboardListener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        mouseListener.start()
        keyboardListener.start()

    def send_text(self, text: str):
        header = bytes(f"{len(text):<{self.headerLength}}", "utf-8")
        self.connection.sendall(header + bytes(text, "utf-8"))

    def recv_text(self):
        header = self.connection.recv(self.headerLength)
        while len(header) < self.headerLength:
            header += self.connection.recv(self.headerLength - len(header))

        messageLength = int(header.decode("utf-8").strip())
        message = self.connection.recv(messageLength).decode("utf-8")
        while len(message) < messageLength:
            message += self.connection.recv(messageLength - len(message)).decode("utf-8")

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
