from socket import socket, AF_INET, SOCK_STREAM
from pynput import mouse
from pynput import keyboard
from pynput.keyboard import Key, KeyCode

from special_keys import special_keys


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
        self.keyboardController = keyboard.Controller()

        self.mouseButtons = {
            "left": mouse.Button.left,
            "middle": mouse.Button.middle,
            "right": mouse.Button.right
        }

    def clientLoop(self):
        while True:
            text = self.recv_text()

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

            elif text.startswith("PR:"):
                keyName = text[3:]
                if keyName in special_keys:
                    self.keyboardController.press(special_keys[keyName])
                else:
                    try:
                        self.keyboardController.press(keyName)
                    except ValueError as e:
                        print(f"Key {keyName} not found")

            elif text.startswith("RE:"):
                keyName = text[3:]
                if keyName in special_keys:
                    self.keyboardController.press(special_keys[keyName])
                else:
                    try:
                        self.keyboardController.release(keyName)
                    except ValueError as e:
                        print(f"Key {keyName} not found")

    def mouseMove(self, x, y):
        cx, cy = self.mouseController.position
        self.mouseController.move(x - cx, y - cy)

    def send_text(self, text: str):
        header = bytes(f"{len(text):<{self.headerLength}}", "utf-8")
        self.clientSocket.sendall(header + bytes(text, "utf-8"))

    def recv_text(self):
        header = self.clientSocket.recv(self.headerLength)
        while len(header) < self.headerLength:
            header += self.clientSocket.recv(self.headerLength - len(header))

        messageLength = int(header.decode("utf-8").strip())
        message = self.clientSocket.recv(messageLength).decode("utf-8")
        while len(message) < messageLength:
            message += self.clientSocket.recv(messageLength - len(message)).decode("utf-8")

        return message

    def close(self):
        self.clientSocket.close()
