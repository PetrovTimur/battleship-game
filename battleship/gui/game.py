from tkinter import ttk
from battleship.logic import ai
from battleship.logic.ai import get_coords

FIELD_SIZE = 10


class ShipPlacementScreen:
    def __init__(self, window):
        self.root = window

        self.frame = ttk.Frame(self.root)
        self.title = ttk.Label(self.frame, text='Ship placement', style='Red.TLabel')
        self.field_frame = ttk.Frame(self.frame)
        self.random_button = ttk.Button(self.frame, text='Random', command=lambda: print('random'))
        self.start_button = ttk.Button(self.frame, text='Ready',
                                       command=lambda: self.root.event_generate('<<Game>>'))
        self.field_buttons: list[list[ttk.Button]] = []

        for i in range(FIELD_SIZE):
            self.field_buttons.append([])
            for j in range(FIELD_SIZE):
                self.field_buttons[i].append(ttk.Button(self.field_frame, style='Blue.TButton'))
                self.field_buttons[i][j].bind('<Enter>', lambda e, col=i, row=j: self.hover((col, row)))
                self.field_buttons[i][j].bind('<Leave>', lambda e, col=i, row=j: self.leave((col, row)))

                self.field_buttons[i][j].bind('<MouseWheel>', lambda e, col=i, row=j: self.rotate(e, (col, row)))
                self.field_buttons[i][j].bind('<Button-4>', lambda e, col=i, row=j: self.rotate(e, (col, row)))
                self.field_buttons[i][j].bind('<Button-5>', lambda e, col=i, row=j: self.rotate(e, (col, row)))

                self.field_buttons[i][j].configure(command=lambda col=i, row=j: self.place_ship((col, row)))

        self.root.bind('<Escape>', lambda e: self.return_to_main())

        self.angle = 's'

        self.place()

    def return_to_main(self):
        self.root.unbind('<Escape>')
        self.root.event_generate('<<Main>>')

    def place(self):
        self.frame.grid(column=0, row=0, sticky='nsew')
        self.frame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1, minsize=40)
        self.frame.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15),
                                   weight=1, minsize=40)

        self.title.grid(column=5, row=0, columnspan=6, rowspan=2)
        self.field_frame.grid(column=5, row=2, columnspan=6, rowspan=6, sticky='nsew')
        self.random_button.grid(column=12, row=5, columnspan=3)
        self.start_button.grid(column=12, row=7, columnspan=3)

        self.field_frame.grid_propagate(False)

        for i in range(FIELD_SIZE):
            for j in range(FIELD_SIZE):
                self.field_buttons[i][j].grid(column=i, row=FIELD_SIZE - j - 1, sticky='nsew')

        self.field_frame.rowconfigure('all', weight=1)
        self.field_frame.columnconfigure('all', weight=1)

    def hover(self, pos):
        col, row = pos
        current_button = self.field_buttons[col][row]
        current_button.state(['!hover'])
        if current_button.instate(['!disabled']):
            size = self.root.game.me.field.ships[self.root.game.me.field.placed].size

            coords = get_coords(pos, size, self.angle)
            for col, row in coords:
                self.field_buttons[col][row].state(['hover'])

    def leave(self, pos):
        col, row = pos
        current_button = self.field_buttons[col][row]
        if current_button.instate(['!disabled']):
            size = self.root.game.me.field.ships[self.root.game.me.field.placed].size

            coords = get_coords(pos, size, self.angle)
            for col, row in coords:
                self.field_buttons[col][row].state(['!hover'])

    def rotate(self, event, pos):
        angles = ['w', 'n', 'e', 's']

        sign = 0
        if event.num == 5 or event.delta == -120:
            sign = -1
        if event.num == 4 or event.delta == 120:
            sign = 1

        self.leave(pos)
        self.angle = angles[(angles.index(self.angle) + sign) % 4]
        self.hover(pos)

    def place_ship(self, pos):
        size = self.root.game.me.field.ships[self.root.game.me.field.placed].size

        coords = get_coords(pos, size, self.angle)
        if len(coords) < size:
            return

        for col, row in coords:
            self.field_buttons[col][row].state(['disabled'])
            self.field_buttons[col][row]['style'] = 'Ship.TButton'

        self.root.game.me.field.place(coords)

        if self.root.game.me.field.check_placed():
            self.update_field()

    def update_field(self):
        for i in range(FIELD_SIZE):
            for j in range(FIELD_SIZE):
                self.field_buttons[i][j].state(['disabled'])

    def destroy(self):
        self.frame.destroy()


class GameScreen:
    def __init__(self, window):
        self.root = window

        self.frame = ttk.Frame(self.root)

        self.player_label = ttk.Label(self.frame, text='name 1')
        self.enemy_label = ttk.Label(self.frame, text='name 2')

        self.player_field = ttk.Frame(self.frame, style='Blue.TFrame')
        self.enemy_field = ttk.Frame(self.frame, style='Blue.TFrame')
        self.player_buttons: list[list[ttk.Button]] = []
        self.enemy_buttons: list[list[ttk.Button]] = []

        for i in range(FIELD_SIZE):
            self.player_buttons.append([])
            self.enemy_buttons.append([])
            for j in range(FIELD_SIZE):
                self.player_buttons[i].append(ttk.Button(self.player_field, style='Blue.TButton'))
                self.enemy_buttons[i].append(ttk.Button(self.enemy_field, style='Blue.TButton'))

                self.player_buttons[i][j]['style'] = 'Ship.TButton'\
                    if self.root.game.me.field.cells[i][j] > 0 else 'Blue.TButton'
                self.player_buttons[i][j].state(['disabled'])

                self.enemy_buttons[i][j].configure(command=lambda col=i, row=j: self.step((col, row)))

        self.place()

    def step(self, pos):
        col, row = pos
        hit = self.root.game.player_turn((col, row))
        if hit:
            self.enemy_buttons[col][row]['style'] = 'Hit.TButton'
        else:
            self.enemy_buttons[col][row]['style'] = 'Miss.TButton'
        self.enemy_buttons[col][row].state(['disabled'])

        new_col, new_row = ai.shot(self.root.game.me.field.cells)
        hit = self.root.game.enemy_turn((new_col, new_row))
        if hit:
            self.player_buttons[new_col][new_row]['style'] = 'Hit.TButton'
        else:
            self.player_buttons[new_col][new_row]['style'] = 'Miss.TButton'

    def place(self):
        self.frame.grid(column=0, row=0, sticky='nsew')
        self.frame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1, minsize=40)
        self.frame.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15),
                                   weight=1, minsize=40)

        self.player_label.grid(column=1, row=0, columnspan=6, rowspan=2)
        self.enemy_label.grid(column=9, row=0, columnspan=6, rowspan=2)

        self.player_field.grid(column=1, row=2, columnspan=6, rowspan=6, sticky='nsew')
        self.enemy_field.grid(column=9, row=2, columnspan=6, rowspan=6, sticky='nsew')
        self.player_field.grid_propagate(False)
        self.enemy_field.grid_propagate(False)

        for i in range(FIELD_SIZE):
            for j in range(FIELD_SIZE):
                self.player_buttons[i][j].grid(column=i, row=FIELD_SIZE - j - 1, sticky='nsew')
                self.enemy_buttons[i][j].grid(column=i, row=FIELD_SIZE - j - 1, sticky='nsew')

        self.player_field.rowconfigure('all', weight=1)
        self.player_field.columnconfigure('all', weight=1)
        self.enemy_field.rowconfigure('all', weight=1)
        self.enemy_field.columnconfigure('all', weight=1)

    def destroy(self):
        self.frame.destroy()
