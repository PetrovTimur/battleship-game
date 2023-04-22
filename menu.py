from tkinter import VERTICAL
from tkinter import ttk


class StartScreen:
    def __init__(self, window):
        self.root = window

        self.frame = ttk.Frame(self.root)
        self.title = ttk.Label(self.frame, text='Welcome, player!')

        self.buttonsConfig = [
            {
                "text": "New Game",
                "command": lambda: print('hi'),
            },
            {
                "text": "Settings",
                "command": lambda: self.root.event_generate('<<Settings>>'),
            },
            {
                "text": "Quit",
                "command": self.root.destroy
            },
        ]

        self.buttons = []

        for buttonConfig in self.buttonsConfig:
            self.buttons.append(ttk.Button(self.frame, **buttonConfig))

        self.root.unbind('<Escape>')

        self.place()

    def place(self):
        self.frame.grid(column=0, row=0, sticky='nsew')
        self.frame.rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.frame.columnconfigure((0, 1, 2), weight=1)

        self.title.grid(column=0, row=0, columnspan=3)

        for i in range(len(self.buttons)):
            self.buttons[i].grid(column=1, row=(i + 1), sticky='nsew')

    def destroy(self):
        self.frame.destroy()


class SettingsScreen:
    def __init__(self, window):
        self.root = window

        self.frame = ttk.Frame(self.root, style='Blue.TFrame')
        self.title = ttk.Label(self.frame, text='Settings')

        self.separator = ttk.Separator(self.frame, orient=VERTICAL)

        self.buttonsConfig = [
            {
                "text": "Option 1",
                "command": lambda: print('hi'),
            },
            {
                "text": "Option 2",
                "command": lambda: print('hey'),
            }
        ]

        self.buttons = []

        for buttonConfig in self.buttonsConfig:
            self.buttons.append(ttk.Button(self.frame, **buttonConfig))

        self.root.bind('<Escape>', lambda e: self.root.event_generate('<<Main>>'))

        self.place()

    def place(self):
        self.frame.grid(column=0, row=0, sticky='nsew')
        self.frame.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        self.title.grid(column=1, row=0, columnspan=2)
        self.separator.grid(column=3, row=1, rowspan=2, sticky='ns')

        for i in range(len(self.buttons)):
            self.buttons[i].grid(column=1, row=(i + 1), columnspan=2, sticky='nsew')

    def destroy(self):
        self.frame.destroy()
