from tkinter import StringVar, BooleanVar
from tkinter import ttk


class StartScreen:
    def __init__(self, window):
        self.root = window

        self.frame = ttk.Frame(self.root)
        self.title = ttk.Label(self.frame, text=f"Welcome, {self.root.appOpts['name']}!")

        self.buttonsConfig = [
            {
                "text": "New Game",
                "command": lambda: self.root.event_generate('<<NewGame>>'),
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

        self.frame = ttk.Frame(self.root)
        self.title = ttk.Label(self.frame, text='Settings')

        self.settings_frame = ttk.Frame(self.frame, style='Blue.TFrame')

        self.name = StringVar(self.settings_frame, self.root.appOpts['name'])
        self.name_entry = ttk.Entry(
            self.settings_frame,
            justify='center',
            textvariable=self.name
        )

        self.resolution = StringVar(self.frame, self.root.appOpts['resolution'])
        self.resolution_options = ['640x360', '960x540', '1280x720', '1600x900', '1920x1080', '2560x1440']
        self.resolution_menu = ttk.OptionMenu(
            self.settings_frame,
            self.resolution,
            self.resolution.get(),
            *self.resolution_options,
            command=lambda res: self.root.geometry(res)
        )

        self.fullscreen = BooleanVar(self.settings_frame, self.root.appOpts.getboolean('fullscreen'))
        self.fullscreen_button = ttk.Checkbutton(
            self.settings_frame,
            variable=self.fullscreen,
            command=lambda: self.root.attributes('-fullscreen', self.fullscreen.get())
        )

        self.language = StringVar(self.settings_frame, self.root.appOpts['language'])
        self.language_options = ['English', 'Русский']
        self.language_menu = ttk.OptionMenu(
            self.settings_frame,
            self.language,
            self.language.get(),
            *self.language_options,
            command=lambda lang: print('lang change')
        )

        self.labelsConfig = [
            {
                "text": "Name"
            },
            {
                "text": "Resolution"
            },
            {
                "text": "Fullscreen"
            },
            {
                "text": "Language"
            },
        ]

        self.labels = []

        for labelConfig in self.labelsConfig:
            self.labels.append(ttk.Label(self.settings_frame, **labelConfig))

        self.root.bind('<Escape>', lambda e: self.return_to_main())

        self.place()

    def return_to_main(self):
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
        self.frame.grid(column=0, row=0, sticky='nsew')
        self.frame.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        self.title.grid(column=1, row=0, columnspan=4)

        self.settings_frame.grid(column=1, row=1, columnspan=4, rowspan=2, sticky='nsew')
        self.settings_frame.rowconfigure((0, 1, 2, 3), weight=1)
        self.settings_frame.columnconfigure((0, 1, 2, 3), weight=1)

        self.name_entry.grid(column=3, row=0)
        self.resolution_menu.grid(column=3, row=1)
        self.fullscreen_button.grid(column=3, row=2)
        self.language_menu.grid(column=3, row=3)

        for i in range(len(self.labels)):
            self.labels[i].grid(column=0, row=i)

    def destroy(self):
        self.frame.destroy()


class NewGameScreen:
    def __init__(self, window):
        self.root = window

        self.frame = ttk.Frame(self.root)

        self.title = ttk.Label(self.frame, text='New Game')

        self.buttonsConfig = [
            {
                "text": "Single",
                "command": lambda: print('single'),
            },
            {
                "text": "Online",
                "command": lambda: print('online'),
            },
        ]

        self.buttons = []

        for buttonConfig in self.buttonsConfig:
            self.buttons.append(ttk.Button(self.frame, **buttonConfig))

        self.root.bind('<Escape>', lambda e: self.return_to_main())

        self.place()

    def return_to_main(self):
        self.root.unbind('<Escape>')
        self.root.event_generate('<<Main>>')

    def place(self):
        self.frame.grid(column=0, row=0, sticky='nsew')
        self.frame.rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.frame.columnconfigure((0, 1, 2, 3), weight=1)

        self.title.grid(column=1, row=1, columnspan=2)

        for i in range(len(self.buttons)):
            self.buttons[i].grid(column=(i + 1), row=2, sticky='nsew')

    def destroy(self):
        self.frame.destroy()
