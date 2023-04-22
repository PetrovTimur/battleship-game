from tkinter import Tk
from menu import StartScreen, SettingsScreen


class App(Tk):
    def __init__(self):
        super().__init__()

        self.title('Battleship')

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.geometry('1280x720')
        self.resizable(False, False)

        self.bind('<<Main>>', lambda e: self.change_screen('Main'))
        self.bind('<<Settings>>', lambda e: self.change_screen('Settings'))

        self.screen = None
        self.session = None

        self.change_screen('Main')

    def change_screen(self, screen):
        self.screen = screen
        if self.session:
            self.session.destroy()
            self.session = None

        if self.screen == 'Main':
            self.session = StartScreen(self)
        elif self.screen == 'Settings':
            self.session = SettingsScreen(self)
