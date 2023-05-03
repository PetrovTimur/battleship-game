from tkinter import Tk, ttk
from .menu import StartScreen, SettingsScreen
from battleship.util import Config


class App(Tk):
    def __init__(self):
        super().__init__()

        self.title('Battleship')
        self.resizable(False, False)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.appOpts = Config.get()

        self.geometry(self.appOpts['resolution'])
        self.attributes('-fullscreen', self.appOpts.getboolean('fullscreen'))

        ttk.Style().theme_use('default')
        ttk.Style().configure('Blue.TFrame', background='#406D96')

        self.bind('<<Main>>', lambda e: self.change_screen('Main'))
        self.bind('<<Settings>>', lambda e: self.change_screen('Settings'))
        self.bind('<<SaveSettings>>', lambda e: Config.save(self.appOpts))

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