import time
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

from pynput import mouse, keyboard

connection = None
headerLength = 10
fixed_x = 682
fixed_y = 0

lock = True
mouseButtons = {
    "left": mouse.Button.left,
    "middle": mouse.Button.middle,
    "right": mouse.Button.right
}


def break_lock():
    print("Breaking lock in 30 seconds")
    time.sleep(30)
    global lock
    lock = False


def lock_mouse_position():
    Thread(target=break_lock).start()
    while lock:
        mouse_move(fixed_x, fixed_y)
        # time.sleep(0.1)
    print("Lock broken")


def send_text(con, message):
    header = bytes(f"{len(message):<{headerLength}}", "utf-8")
    con.sendall(header + bytes(message, "utf-8"))


def receive_text(con):
    header = con.recv(headerLength)
    while len(header) < headerLength:
        header += con.recv(headerLength - len(header))

    messageLength = int(header.decode("utf-8").strip())
    message = con.recv(messageLength).decode("utf-8")
    while len(message) < messageLength:
        message += con.recv(messageLength - len(message)).decode("utf-8")

    return message


def on_mouse_move(x: int, y: int):
    # print(f"Mouse moved to {x}, {y}")
    message = f"MV:{x},{y}"
    send_text(connection, message)


def mouse_move(x, y):
    cx, cy = mouse.Controller().position
    mouse.Controller().move(x - cx, y - cy)


def on_mouse_click(x: int, y: int, button: mouse.Button, pressed: bool):
    print(f"Mouse clicked at {x}, {y} with {button}")
    message = f"CL:{x},{y},{button.name},{int(pressed)}"
    send_text(connection, message)
    pass


def on_mouse_scroll(x: int, y: int, dx: int, dy: int):
    print(f"Mouse scrolled at {x}, {y} with {dx}, {dy}")
    message = f"SC:{dx},{dy}"
    send_text(connection, message)
    pass


def start_mouse_listener():
    listener = mouse.Listener(
        on_move=on_mouse_move,
        on_click=on_mouse_click,
        on_scroll=on_mouse_scroll)
    listener.start()
    keyboardListener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    keyboardListener.start()


def create_server(host: str, port: int):
    server = socket(AF_INET, SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    return server


def join_server(host: str, port: int):
    client = socket(AF_INET, SOCK_STREAM)
    client.connect((host, port))
    return client


def action(message):
    if message.startswith("MV:"):
        x, y = message[3:].split(",")
        x = int(x)
        y = int(y)
        mouse_move(x, y)
    elif message.startswith("CL:"):
        x, y, button, pressed = message[3:].split(",")
        x = int(x)
        y = int(y)
        mouse_move(x, y)
        button = mouseButtons[button]
        mouse.Controller().press(button) if pressed else mouse.Controller().release(button)
    elif message.startswith("SC:"):
        dx, dy = message[3:].split(",")
        dx = int(dx)
        dy = int(dy)
        mouse.Controller().scroll(dx, dy)
    elif message.startswith("PR:"):
        key = message[3:]
        keyboard.Controller().press(key)
    elif message.startswith("RE:"):
        key = message[3:]
        keyboard.Controller().release(key)


def on_press(key):
    message = f"PR:{key}"
    print(message)
    send_text(connection, message)


def on_release(key):
    message = f"RE:{key}"
    print(message)
    send_text(connection, message)


def main():
    # Thread(target=lock_mouse_position).start()
    print("Enter 1 to host, 2 to join")
    choice = input()
    if choice == "1":
        server = create_server("0.0.0.0", 9999)
        print("Waiting for connection...")
        global connection
        connection, _ = server.accept()
        print("Connected to client")
        start_mouse_listener()
    elif choice == "2":
        address = input("Enter address: ")
        if address == "N" or address == "n":
            address = "192.168.100.15"
        print("Connecting to server...")
        client = join_server(address, 9999)
        print("Connected!")
        while True:
            message = receive_text(client)
            action(message)
        pass
    else:
        print("Invalid input")
    main()


if __name__ == "__main__":
    main()
