from socket import socket, AF_INET, SOCK_STREAM
from pynput import mouse


class SharedMouseClient:
    def __init__(self, ip: str, port: int, height: int, width: int):
        self.screenHeight = height
        self.screenWidth = width
        self.headerLength = 10

        self.ip = ip
        self.port = port

        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect((self.ip, self.port))

        self.mouseController = mouse.Controller()

        self.mouseButtons = {
            "left": mouse.Button.left,
            "middle": mouse.Button.middle,
            "right": mouse.Button.right
        }

    def clientLoop(self):
        while True:
            text = self.recv_text(self.clientSocket)

            if text.startswith("MV:"):
                xPercent, yPercent = text[3:].split(",")
                x = int((float(xPercent) / float(100)) * float(self.screenWidth))
                y = int((float(yPercent) / float(100)) * float(self.screenHeight))
                self.mouseMove(x, y)

            elif text.startswith("CL:"):
                xPercent, yPercent, button, pressed = text[3:].split(",")
                x = int((float(xPercent) / float(100)) * float(self.screenWidth))
                y = int((float(yPercent) / float(100)) * float(self.screenHeight))
                button = self.mouseButtons[button]
                pressed = bool(int(pressed))

                self.mouseMove(x, y)
                self.mouseController.press(button) if pressed else self.mouseController.release(button)

            elif text.startswith("SC:"):
                dx, dy = text[3:].split(",")
                dx = int(dx)
                dy = int(dy)

                self.mouseController.scroll(dx, dy)
    
    def mouseMove(self, x, y):
        cx, cy = self.mouseController.position
        self.mouseController.move(x-cx, y-cy)

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
        self.clientSocket.close()
