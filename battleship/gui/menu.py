"""All menu screens."""

from tkinter import StringVar, BooleanVar, Checkbutton
from tkinter import ttk
from battleship.logic.game import Game
from battleship.resources import esc
from battleship.util.image import loadImage
from battleship.translation import _, setLang


class StartScreen:
    """Main screen of the app."""

    def __init__(self, window):
        """Initialize all widgets."""
        self.root = window

        self.frame = ttk.Frame(self.root, style='Blue.TFrame')
        self.title = ttk.Label(self.frame, text=_('Welcome, {name}!')
                               .format(name=self.root.appOpts['name']), style='Big.Blue.TLabel')

        self.buttonsConfig = [
            {
                "text": _("New Game"),
                "command": lambda: self.root.event_generate('<<NewGame>>'),
            },
            {
                "text": _("Settings"),
                "command": lambda: self.root.event_generate('<<Settings>>'),
            },
            {
                "text": _("Exit"),
                "command": self.root.destroy
            },
        ]

        self.buttons = []

        for buttonConfig in self.buttonsConfig:
            self.buttons.append(ttk.Button(self.frame, takefocus=False,
                                           style='Big.Blue.TButton', **buttonConfig))

        self.place()

    def place(self):
        """Place widgets on screen."""
        self.frame.grid(column=0, row=0, sticky='nsew')
        self.frame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1, minsize=40)
        self.frame.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15),
                                   weight=1, minsize=40)

        self.title.grid(column=5, row=0, columnspan=6, rowspan=2)

        for i in range(len(self.buttons)):
            self.buttons[i].grid(column=5, row=2 * (i + 1), columnspan=6, rowspan=2, sticky='nsew')

    def destroy(self):
        """Destroy main frame."""
        self.frame.destroy()


class SettingsScreen:
    """Screen to choose preferred settings."""

    def __init__(self, window):
        """Initialize all widgets."""
        self.root = window

        self.frame = ttk.Frame(self.root, style='Blue.TFrame')
        self.title = ttk.Label(self.frame, text=_('Settings'), style='Big.Blue.TLabel')
        self.return_label = ttk.Label(self.frame, text=_('Return'), justify='center',
                                      anchor='center', compound='left', style='Blue.TLabel')

        self.settings_frame = ttk.Frame(self.frame, style='Bluer.TFrame', relief='groove')

        self.name = StringVar(self.settings_frame, self.root.appOpts['name'])
        self.name_entry = ttk.Entry(
            self.settings_frame,
            justify='center',
            textvariable=self.name)

        self.resolution = StringVar(self.frame, self.root.appOpts['resolution'])
        self.resolution_options = ['640x360', '960x540', '1280x720', '1600x900', '1920x1080',
                                   '2560x1440']
        self.resolution_menu = ttk.OptionMenu(
            self.settings_frame,
            self.resolution,
            self.resolution.get(),
            *self.resolution_options,
            style='Blue.TMenubutton',
            command=lambda res: self.root.geometry(res))

        self.resolution_menu['menu'].config(bg='#cfe2f3', activebackground='#6fa8dc')

        self.fullscreen = BooleanVar(self.settings_frame,
                                     self.root.appOpts.getboolean('fullscreen'))
        self.fullscreen_button = Checkbutton(
            self.settings_frame,
            variable=self.fullscreen,
            takefocus=False,
            command=self.set_fullscreen,
            background='#9fc5e8',
            activebackground='#9fc5e8')

        self.language = StringVar(self.settings_frame, self.root.appOpts['language'])
        self.language_options = ['English', 'Русский']
        self.language_menu = ttk.OptionMenu(
            self.settings_frame,
            self.language,
            self.language.get(),
            *self.language_options,
            style='Blue.TMenubutton',
            command=lambda lang: self.set_language())

        self.language_menu['menu'].config(bg='#cfe2f3', activebackground='#6fa8dc')

        self.labelsConfig = [
            {
                "text": _("Name")
            },
            {
                "text": _("Resolution")
            },
            {
                "text": _("Fullscreen mode")
            },
            {
                "text": _("Language")
            }]

        self.labels = []

        for labelConfig in self.labelsConfig:
            self.labels.append(ttk.Label(self.settings_frame, style='Bluer.TLabel', **labelConfig))

        self.root.bind('<Escape>', lambda e: self.return_to_main())

        self.place()
        self.root.update_idletasks()

        self.image = loadImage(esc, (30, 30))
        self.return_label['image'] = self.image

    def set_fullscreen(self):
        """Change fullscreen mode setting."""
        if self.fullscreen.get():
            width = self.root.winfo_screenwidth()
            height = self.root.winfo_screenheight()
            self.root.geometry(f"{width}x{height}")
            self.resolution.set(f"{width}x{height}")
            self.root.attributes('-fullscreen', True)
        else:
            self.root.attributes('-fullscreen', False)

    def set_language(self):
        """Change language."""
        self.root.appOpts['language'] = self.language.get()
        setLang(self.root.appOpts["language"])
        self.root.event_generate('<<Settings>>')

    def return_to_main(self):
        """Return to the main screen."""
        self.root.unbind('<Escape>')

        settings = {'name': self.name.get(),
                    'resolution': self.resolution.get(),
                    'fullscreen': 'yes' if self.fullscreen.get() else 'no',
                    'language': self.language.get()}

        for key, value in settings.items():
            self.root.appOpts[key] = value

        self.root.event_generate('<<SaveSettings>>')
        self.root.event_generate('<<Main>>')

    def place(self):
        """Place widgets on screen."""
        self.frame.grid(column=0, row=0, sticky='nsew')
        self.frame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1, minsize=40)
        self.frame.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15),
                                   weight=1, minsize=40)

        self.title.grid(column=5, row=0, columnspan=6, rowspan=2)
        self.return_label.grid(column=0, row=0, columnspan=2)

        self.settings_frame.grid(column=3, row=2, columnspan=10, rowspan=6, sticky='nsew')
        self.settings_frame.rowconfigure((0, 1, 2, 3), weight=1)
        self.settings_frame.columnconfigure((0, 1, 2, 3), weight=1)

        self.name_entry.grid(column=3, row=0, columnspan=2)
        self.resolution_menu.grid(column=3, row=1, columnspan=2)
        self.fullscreen_button.grid(column=3, row=2, columnspan=2)
        self.language_menu.grid(column=3, row=3, columnspan=2)

        for i in range(len(self.labels)):
            self.labels[i].grid(column=0, row=i, columnspan=2)

    def destroy(self):
        """Destroy main frame."""
        self.frame.destroy()


class NewGameSetupScreen:
    """Screen to choose the game mode."""

    def __init__(self, window):
        """Initialize all widgets."""
        self.root = window

        self.frame = ttk.Frame(self.root, style='Blue.TFrame')

        self.title = ttk.Label(self.frame, text=_('Choose game mode'), style='Big.Blue.TLabel')
        self.return_label = ttk.Label(self.frame, text=_('Return'), justify='center',
                                      anchor='center', compound='left', style='Blue.TLabel')

        self.buttonsConfig = [
            {
                "text": _("Single"),
                "command": lambda: self.start_game('single'),
            },
            {
                "text": _("Online"),
                "command": lambda: self.start_game('online'),
            }]

        self.buttons = []

        for buttonConfig in self.buttonsConfig:
            self.buttons.append(ttk.Button(self.frame, takefocus=False, style='Big.Blue.TButton',
                                           **buttonConfig))

        self.root.bind('<Escape>', lambda e: self.return_to_main())

        self.place()
        self.root.update_idletasks()

        self.image = loadImage(esc, (30, 30))
        self.return_label['image'] = self.image

    def return_to_main(self):
        """Return to main screen."""
        self.root.unbind('<Escape>')
        self.root.event_generate('<<Main>>')

    def start_game(self, mode):
        """Initialize the game and switch screens."""
        self.root.game = Game(mode, self.root.appOpts['name'])

        self.root.event_generate('<<ShipPlacement>>')

    def place(self):
        """Place widgets on screen."""
        self.frame.grid(column=0, row=0, sticky='nsew')
        self.frame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1, minsize=40)
        self.frame.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15),
                                   weight=1, minsize=40)

        self.title.grid(column=5, row=0, columnspan=6, rowspan=2)
        self.return_label.grid(column=0, row=0, columnspan=2)

        for i in range(len(self.buttons)):
            self.buttons[i].grid(column=(5 * i + 3), row=3, columnspan=5, rowspan=2, sticky='nsew')

    def destroy(self):
        """Destroy main frame."""
        self.frame.destroy()
