import tkinter as tk


class App(tk.Tk):

    def __init__(self):
        super().__init__()

        # configure the root window
        self.title('Mouse Without Borders')
        self.resizable(False, False)



if __name__ == '__main__':
    app = App()
    app.mainloop()
