from socket import socket, AF_INET, SOCK_STREAM

import pyperclip
from pynput import mouse
from pynput import keyboard


class SharedMouseServer:
    def __init__(self, host: str, port: int, height: int, width: int):
        self.screenHeight = height
        self.screenWidth = width
        self.connection = None
        self.headerLength = 10

        self.leftMachineEnabled = False
        self.middleMachineEnabled = True
        self.rightMachineEnabled = False

        self.host = host
        self.port = port

        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket.bind((self.host, self.port))
        self.serverSocket.listen(1)

    def wait_for_client(self):
        self.connection, _ = self.serverSocket.accept()

    def on_mouse_move(self, x: int, y: int):
        if self.leftMachineEnabled:
            xPercent = (float(x) / float(self.screenWidth)) * float(100)
            yPercent = (float(y) / float(self.screenHeight)) * float(100)
            self.send_text(f"MV:{xPercent},{yPercent}")

    def on_mouse_click(self, x: int, y: int, button: mouse.Button, pressed: bool):
        if self.leftMachineEnabled:
            xPercent = (float(x) / float(self.screenWidth)) * float(100)
            yPercent = (float(y) / float(self.screenHeight)) * float(100)
            self.send_text(f"CL:{xPercent},{yPercent},{button.name},{int(pressed)}")

    def on_mouse_scroll(self, x: int, y: int, dx: int, dy: int):
        if self.leftMachineEnabled:
            self.send_text(f"SC:{dx},{dy}")

    def on_key_press(self, key):
        if self.leftMachineEnabled:
            if hasattr(key, "name"):  # if key is a special key
                keyName = key.name
                self.send_text(f"PR:{keyName}")
            elif hasattr(key, "char"):  # if key is a character
                keyName = key.char
                self.send_text(f"PR:{keyName}")

    def on_key_release(self, key):
        if self.leftMachineEnabled:
            if hasattr(key, "name"):  # if key is a special key
                keyName = key.name
                self.send_text(f"RE:{keyName}")
            elif hasattr(key, "char"):  # if key is a character
                keyName = key.char
                self.send_text(f"RE:{keyName}")

    def on_middle_machine_hotkey(self):
        self.middleMachineEnabled = True
        self.leftMachineEnabled = False
        self.rightMachineEnabled = False

    def on_left_machine_hotkey(self):
        self.leftMachineEnabled = True
        self.middleMachineEnabled = False
        self.rightMachineEnabled = False

    def on_right_machine_hotkey(self):
        self.rightMachineEnabled = True
        self.leftMachineEnabled = False
        self.middleMachineEnabled = False

    def on_paste_hotkey(self):
        clipboard = pyperclip.paste()
        self.send_text(f"PC:{clipboard}")

    def start_event_listeners(self):
        mouseListener = mouse.Listener(
            on_move=self.on_mouse_move,
            on_click=self.on_mouse_click,
            on_scroll=self.on_mouse_scroll,
        )
        keyboardListener = keyboard.Listener(
            on_press=self.on_key_press,
            on_release=self.on_key_release,
        )
        hotkeys = keyboard.GlobalHotKeys({
            '<alt>+m': self.on_middle_machine_hotkey,
            '<alt>+l': self.on_left_machine_hotkey,
            '<alt>+r': self.on_right_machine_hotkey,
            '<alt>+v': self.on_paste_hotkey,
        })
        mouseListener.start()
        keyboardListener.start()
        hotkeys.start()

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
