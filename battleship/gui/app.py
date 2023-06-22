"""Main GUI module that draws all app attributes."""

from tkinter import Tk
from .menu import StartScreen, SettingsScreen, NewGameSetupScreen
from .game import ShipPlacementScreen, GameScreen
from battleship.util import Config
from battleship.util.image import loadImage
from battleship.resources import icon
from .styles import initialize_styles
from battleship.translation import setLang


class App(Tk):
    """GUI app class."""

    def __init__(self):
        """Initialize GUI app."""
        super().__init__()

        self.title('Battleship')
        self.resizable(False, False)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.appOpts = Config.get()
        setLang(self.appOpts["language"])

        self.icon = loadImage(icon, (64, 64))
        self.iconphoto(True, self.icon)
        self.geometry(self.appOpts['resolution'])
        self.attributes('-fullscreen', self.appOpts.getboolean('fullscreen'))

        initialize_styles()

        self.bind('<<Main>>', lambda e: self.change_screen('Main'))
        self.bind('<<Settings>>', lambda e: self.change_screen('Settings'))
        self.bind('<<SaveSettings>>', lambda e: Config.save(self.appOpts))
        self.bind('<<NewGame>>', lambda e: self.change_screen('NewGame'))
        self.bind('<<ShipPlacement>>', lambda e: self.change_screen('ShipPlacement'))
        self.bind('<<Game>>', lambda e: self.change_screen('Game'))

        self.screen = None
        self.session = None
        self.game = None

        self.change_screen('Main')

    def change_screen(self, screen):
        """Change current screen to another one."""
        self.screen = screen
        if self.session:
            self.session.destroy()
            self.session = None

        if self.screen == 'Main':
            self.session = StartScreen(self)
        elif self.screen == 'Settings':
            self.session = SettingsScreen(self)
        elif self.screen == 'NewGame':
            self.session = NewGameSetupScreen(self)
        elif self.screen == 'ShipPlacement':
            self.session = ShipPlacementScreen(self)
        elif self.screen == 'Game':
            self.session = GameScreen(self)
