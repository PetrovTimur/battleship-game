"""All gameplay screens."""

from tkinter import ttk, BooleanVar, StringVar, Checkbutton, Toplevel
from battleship.logic import network
from battleship.logic.ai import get_coords, surrounding, BotThread
from battleship.resources import esc
from battleship.util.image import loadImage
from battleship.translation import _
import queue
import asyncio

FIELD_SIZE = 10


class ShipPlacementScreen:
    """Screen where player places ships."""

    def __init__(self, window):
        """Initialize all widgets."""
        self.root = window

        self.frame = ttk.Frame(self.root, style='Blue.TFrame')
        self.title = ttk.Label(self.frame, text=_('Place your ships'), style='Big.Blue.TLabel')

        self.message = StringVar()
        self.message_label = ttk.Label(self.frame, textvariable=self.message, justify='center',
                                       anchor='center', style='Blue.TLabel')

        self.return_label = ttk.Label(self.frame, text=_('Return'), justify='center',
                                      anchor='center', compound='left', style='Blue.TLabel')

        self.field_frame = ttk.Frame(self.frame)
        self.random_button = ttk.Button(self.frame, text=_('Random'), takefocus=False,
                                        command=self.random_place, style='Small.Blue.TButton')
        self.clear_button = ttk.Button(self.frame, text=_('Clear'), takefocus=False,
                                       command=self.clear, style='Small.Blue.TButton')
        self.is_ready = BooleanVar(value=False)
        self.ready_check = Checkbutton(self.frame, text=_('Ready'), takefocus=False,
                                       state='disabled', command=self.ready,
                                       variable=self.is_ready, onvalue=True, offvalue=False,
                                       background='#cfe2f3', activebackground='#cfe2f3')
        self.field_buttons: list[list[ttk.Button]] = []

        for i in range(FIELD_SIZE):
            self.field_buttons.append([])
            for j in range(FIELD_SIZE):
                self.field_buttons[i].append(ttk.Button(self.field_frame, takefocus=False,
                                                        style='Empty.TButton'))
                self.field_buttons[i][j].bind('<Enter>', lambda e, col=i, row=j:
                                              self.hover((col, row)))
                self.field_buttons[i][j].bind('<Leave>', lambda e, col=i, row=j:
                                              self.leave((col, row)))

                self.field_buttons[i][j].bind('<MouseWheel>', lambda e, col=i, row=j:
                                              self.rotate(e, (col, row)))
                self.field_buttons[i][j].bind('<Button-4>', lambda e, col=i, row=j:
                                              self.rotate(e, (col, row)))
                self.field_buttons[i][j].bind('<Button-5>', lambda e, col=i, row=j:
                                              self.rotate(e, (col, row)))

                self.field_buttons[i][j].configure(command=lambda col=i, row=j:
                                                   self.place_ship((col, row)))

        self.root.bind('<Escape>', lambda e: self.return_to_main())

        self.angle = 's'

        self.place()
        self.root.update_idletasks()

        self.image = loadImage(esc, (30, 30))
        self.return_label['image'] = self.image
        self.message_label.configure(wraplength=self.frame.winfo_width() // 8)

    def ready(self):
        """Prepare to start the game."""
        if self.is_ready.get():
            self.root.game.queue = queue.Queue()
            if self.root.game.mode == 'single':
                self.root.game.thread = BotThread(self.root.game, self)
            else:
                self.root.game.thread = network.AsyncioThread(self.root.game, self)
            self.root.game.thread.start()
        else:
            self.root.game.queue = None
            if self.root.game.mode == 'online':
                asyncio.run_coroutine_threadsafe(self.root.game.thread.put_in_erqueue('quit'),
                                                 self.root.game.thread.asyncio_loop)
            self.root.game.thread = None

    def connection_error(self):
        """Handle server unavailability error."""
        self.root.game.queue = None
        self.root.game.thread = None
        self.is_ready.set(False)
        self.message.set(_('Server is temporarily unavailable. Try later'))

    def start_game(self):
        """Switch to game screen."""
        self.root.event_generate('<<Game>>')

    def return_to_main(self):
        """Return to the start screen."""
        if self.root.game.mode == 'online' and self.is_ready.get():
            asyncio.run_coroutine_threadsafe(self.root.game.thread.put_in_erqueue('quit'),
                                             self.root.game.thread.asyncio_loop)

        self.root.game = None
        self.root.unbind('<Escape>')
        self.root.event_generate('<<Main>>')

    def random_place(self):
        """Generate random ship positions for player."""
        self.root.game.me.field.auto_place()

        for i in range(FIELD_SIZE):
            for j in range(FIELD_SIZE):
                self.field_buttons[i][j]['style'] = 'Ship.TButton' \
                    if self.root.game.me.field.cells[i][j] > 0 else 'Empty.TButton'
                self.field_buttons[i][j].state(['disabled'])

        self.ready_check.configure(state='normal')

    def clear(self):
        """Clear the field."""
        self.root.game.me.field.clear()

        for i in range(FIELD_SIZE):
            for j in range(FIELD_SIZE):
                self.field_buttons[i][j]['style'] = 'Empty.TButton'
                self.field_buttons[i][j].state(['!disabled'])

        self.is_ready.set(False)
        self.ready_check.configure(state='disabled')

    def place(self):
        """Place widgets on screen."""
        self.frame.grid(column=0, row=0, sticky='nsew')
        self.frame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1, minsize=40)
        self.frame.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15),
                                   weight=1, minsize=40)

        self.title.grid(column=5, row=0, columnspan=6, rowspan=2)
        self.field_frame.grid(column=5, row=2, columnspan=6, rowspan=6, sticky='nsew')
        self.random_button.grid(column=12, row=5, columnspan=3)
        self.clear_button.grid(column=12, row=4, columnspan=3)
        self.ready_check.grid(column=12, row=7, columnspan=3)
        self.message_label.grid(column=0, row=3, columnspan=5, rowspan=4)
        self.return_label.grid(column=0, row=0, columnspan=2)

        self.field_frame.grid_propagate(False)

        for i in range(FIELD_SIZE):
            for j in range(FIELD_SIZE):
                self.field_buttons[i][j].grid(column=i, row=FIELD_SIZE - j - 1, sticky='nsew')

        self.field_frame.rowconfigure('all', weight=1)
        self.field_frame.columnconfigure('all', weight=1)

    def hover(self, pos):
        """Highlight the cells on which the ship will be placed if this cell is selected."""
        col, row = pos
        current_button = self.field_buttons[col][row]
        current_button.state(['!hover'])
        if current_button.instate(['!disabled']):
            size = self.root.game.me.field.ships[self.root.game.me.field.placed].size

            coords = get_coords(pos, size, self.angle, self.root.game.me.field.cells)
            if len(coords) < size:
                if self.message.get() == '':
                    self.message.set(_('Can\'t put here. Try moving or rotating the ship'))
                return

            if self.message.get() != '':
                self.message.set('')

            for col, row in coords:
                self.field_buttons[col][row].state(['hover'])

    def leave(self, pos):
        """Return highlighted cells to normal color."""
        col, row = pos
        current_button = self.field_buttons[col][row]
        if current_button.instate(['!disabled']):
            size = self.root.game.me.field.ships[self.root.game.me.field.placed].size

            coords = get_coords(pos, size, self.angle, self.root.game.me.field.cells)
            if len(coords) < size:
                self.message.set('')
                return

            for col, row in coords:
                self.field_buttons[col][row].state(['!hover'])

    def rotate(self, event, pos):
        """Rotate the ship around the selected cell."""
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
        """Place a ship on the field."""
        size = self.root.game.me.field.ships[self.root.game.me.field.placed].size

        coords = get_coords(pos, size, self.angle, self.root.game.me.field.cells)
        if len(coords) < size:
            return

        around = surrounding(coords)

        for col, row in coords:
            self.field_buttons[col][row].state(['disabled', '!hover'])
            self.field_buttons[col][row]['style'] = 'Ship.TButton'

        for col, row in around:
            self.field_buttons[col][row].state(['disabled', '!hover'])

        self.root.game.me.field.place(coords)

        if self.root.game.me.field.check_placed():
            self.update_field()
            self.ready_check.configure(state='normal')

    def update_field(self):
        """Disable all buttons on the field."""
        for i in range(FIELD_SIZE):
            for j in range(FIELD_SIZE):
                self.field_buttons[i][j].state(['disabled'])

    def destroy(self):
        """Destroy main frame."""
        self.frame.destroy()


class GameScreen:
    """Screen of the main gameplay."""

    def __init__(self, window):
        """Initialize widgets."""
        self.root = window

        self.frame = ttk.Frame(self.root, style='Blue.TFrame')

        self.player_label = ttk.Label(self.frame, text='', style='Blue.TLabel')
        self.enemy_label = ttk.Label(self.frame, text='', style='Blue.TLabel')

        self.return_label = ttk.Label(self.frame, text=_('Return'), justify='center',
                                      anchor='center', compound='left', style='Blue.TLabel')

        self.activity = StringVar()
        self.activity_label = ttk.Label(self.frame, textvariable=self.activity, justify='center',
                                        anchor='center', style='Blue.TLabel')

        self.player_field = ttk.Frame(self.frame, style='Blue.TFrame')
        self.enemy_field = ttk.Frame(self.frame, style='Blue.TFrame')
        self.player_buttons: list[list[ttk.Button]] = []
        self.enemy_buttons: list[list[ttk.Button]] = []
        self.player_row_labels: list[ttk.Label] = []
        self.player_col_labels: list[ttk.Label] = []
        self.enemy_row_labels: list[ttk.Label] = []
        self.enemy_col_labels: list[ttk.Label] = []

        for i in range(FIELD_SIZE):
            self.player_buttons.append([])
            self.enemy_buttons.append([])
            self.player_row_labels.append(ttk.Label(self.player_field, text=str(i + 1), width=3,
                                                    anchor='center', style='Blue.TLabel'))
            self.player_col_labels.append(ttk.Label(self.player_field, text=chr(ord(_('A')) + i),
                                                    width=3, anchor='center', style='Blue.TLabel'))
            self.enemy_row_labels.append(ttk.Label(self.enemy_field, text=str(i + 1), width=3,
                                                   anchor='center', style='Blue.TLabel'))
            self.enemy_col_labels.append(ttk.Label(self.enemy_field, text=chr(ord(_('A')) + i),
                                                   width=3, anchor='center', style='Blue.TLabel'))
            for j in range(FIELD_SIZE):
                self.player_buttons[i].append(ttk.Button(self.player_field, takefocus=False,
                                                         style='Empty.TButton'))
                self.enemy_buttons[i].append(ttk.Button(self.enemy_field, takefocus=False,
                                                        style='Empty.TButton'))

                self.player_buttons[i][j]['style'] = 'Ship.TButton' \
                    if self.root.game.me.field.cells[i][j] > 0 else 'Empty.TButton'
                self.player_buttons[i][j].state(['disabled'])

                self.enemy_buttons[i][j].configure(command=lambda col=i, row=j:
                                                   self.player_turn((col, row)))

        self.root.bind('<Escape>', lambda e: self.quit())
        self.frame.bind('<<EnemyTurn>>', lambda e: self.enemy_turn())

        self.queue = self.root.game.queue
        self.root.game.thread.update_screen(self)

        self.root.game.turn = self.queue.get()
        if self.root.game.mode == 'online':
            self.root.game.enemy = self.queue.get()

        self.player_label['text'] = self.root.game.me.name
        self.enemy_label['text'] = self.root.game.enemy.name

        self.activity.set('{me!r} vs {enemy!r}'.format(me=self.root.game.me.name,
                                                       enemy=self.root.game.enemy.name))

        self.order()
        self.place()
        self.root.update_idletasks()

        self.image = loadImage(esc, (30, 30))
        self.return_label['image'] = self.image

    def return_to_main(self):
        """Return to main screen."""
        self.root.game = None
        self.root.unbind('<Escape>')
        self.root.event_generate('<<Main>>')

    def quit(self):
        """Raise quit warning window."""
        win = Toplevel()
        win.resizable(False, False)
        w = 200
        h = 100
        xs = self.root.winfo_rootx()
        ys = self.root.winfo_rooty()
        ws = self.root.winfo_width()
        hs = self.root.winfo_height()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        win.geometry('%dx%d+%d+%d' % (w, h, xs + x, ys + y))

        win.title(_('Warning'))
        win.rowconfigure((0, 1, 2, 3), weight=1)
        win.columnconfigure((0, 1), weight=1)

        question_label = ttk.Label(win, text=_('Quit to main?'))
        question_label.grid(column=0, row=0, columnspan=2, rowspan=2)

        yes_button = ttk.Button(win, text=_('Yes'), takefocus=False, command=lambda window=win:
                                self.handle_quit(window))
        no_button = ttk.Button(win, text=_('No'), takefocus=False, command=win.destroy)
        yes_button.grid(column=0, row=2, rowspan=2)
        no_button.grid(column=1, row=2, rowspan=2)

        win.grab_set()

    def handle_quit(self, w):
        """Handle quit scenario."""
        w.destroy()
        if self.root.game.mode == 'online':
            asyncio.run_coroutine_threadsafe(self.root.game.thread.put_in_erqueue('quit'),
                                             self.root.game.thread.asyncio_loop)
        else:
            self.queue.put('quit')
        self.return_to_main()

    def connection_error(self):
        """Raise connection error window."""
        win = Toplevel()
        win.resizable(False, False)
        w = 200
        h = 100
        xs = self.root.winfo_rootx()
        ys = self.root.winfo_rooty()
        ws = self.root.winfo_width()
        hs = self.root.winfo_height()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        win.geometry('%dx%d+%d+%d' % (w, h, xs + x, ys + y))

        win.title(_('Warning'))
        win.rowconfigure((0, 1, 2, 3), weight=1)
        win.columnconfigure((0, 1), weight=1)

        question_label = ttk.Label(win, text=_('Connection lost'))
        question_label.grid(column=0, row=0, columnspan=2, rowspan=2)

        ok_button = ttk.Button(win, text=_('Ok'), takefocus=False, command=lambda window=win:
                               self.handle_connection_error(window))
        ok_button.grid(column=0, row=2, rowspan=2, columnspan=2)

        win.protocol("WM_DELETE_WINDOW", lambda window=win: self.handle_connection_error(window))

        win.grab_set()

    def handle_connection_error(self, w):
        """Handle connection error."""
        w.destroy()
        self.return_to_main()

    def order(self):
        """Disable all buttons for the second player."""
        if self.root.game.turn == 'second':
            for i in range(FIELD_SIZE):
                for j in range(FIELD_SIZE):
                    self.enemy_buttons[i][j].state(['disabled'])

    def update_activity(self, coord, player, status):
        """Show last move as a text."""
        col, row = coord
        coord = chr(ord(_('A')) + col) + str(10 - row)

        if status == 'dead':
            if player == self.root.game.me.name:
                status = 'win'
            else:
                status = 'loss'
        statuses = {
            'miss': _('miss'),
            'hit': _('hit'),
            'sank': _('sank'),
            'win': _('You won!'),
            'loss': _('You lost!')
        }
        self.activity.set(_('{player!r} shoots at {coord}\n{status}')
                          .format(player=player, coord=coord, status=statuses[status]))

    def game_over(self):
        """Handle end of the game."""
        if self.root.game.mode == 'online':
            asyncio.run_coroutine_threadsafe(self.root.game.thread.put_in_erqueue('end'),
                                             self.root.game.thread.asyncio_loop)
        else:
            self.queue.put('end')
        self.root.bind('<Escape>', lambda e: self.return_to_main())

    def enemy_turn(self):
        """Process opponent's move."""
        pos = self.queue.get()
        col, row = pos
        status = self.root.game.enemy_turn((col, row))

        self.update_activity(pos, self.root.game.enemy.name, status)
        if status == 'hit':
            self.player_buttons[col][row]['style'] = 'Hit.TButton'
        elif status == 'sank' or status == 'dead':
            for coord in self.root.game.me.field.sank[-1].status.keys():
                self.player_buttons[coord[0]][coord[1]]['style'] = 'Sank.TButton'

            if status == 'dead':
                self.game_over()
        else:
            self.player_buttons[col][row]['style'] = 'Miss.TButton'
            for i in range(FIELD_SIZE):
                for j in range(FIELD_SIZE):
                    if self.enemy_buttons[i][j]['style'] == 'Empty.TButton':
                        self.enemy_buttons[i][j].state(['!disabled'])

        return status

    def player_turn(self, pos):
        """Process player's move."""
        col, row = pos
        status = self.root.game.player_turn((col, row))
        if self.root.game.mode == 'online':
            asyncio.run_coroutine_threadsafe(self.root.game.thread.put_in_queue(pos),
                                             self.root.game.thread.asyncio_loop)
        else:
            self.queue.put((pos, status))

        self.update_activity(pos, self.root.game.me.name, status)
        if status == 'hit':
            self.enemy_buttons[col][row]['style'] = 'Hit.TButton'
        elif status == 'sank' or status == 'dead':
            self.enemy_buttons[col][row]['style'] = 'Sank.TButton'
            for coord in self.root.game.enemy.field.sank[-1].status.keys():
                self.enemy_buttons[coord[0]][coord[1]]['style'] = 'Sank.TButton'

            if status == 'dead':
                for i in range(FIELD_SIZE):
                    for j in range(FIELD_SIZE):
                        if self.enemy_buttons[i][j]['style'] == 'Empty.TButton':
                            self.enemy_buttons[i][j].state(['disabled'])

                self.game_over()
        else:
            self.enemy_buttons[col][row]['style'] = 'Miss.TButton'
            for i in range(FIELD_SIZE):
                for j in range(FIELD_SIZE):
                    if self.enemy_buttons[i][j]['style'] == 'Empty.TButton':
                        self.enemy_buttons[i][j].state(['disabled'])

        self.enemy_buttons[col][row].state(['disabled'])

    def place(self):
        """Place widgets on screen."""
        self.frame.grid(column=0, row=0, sticky='nsew')
        self.frame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1, minsize=40)
        self.frame.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15),
                                   weight=1, minsize=40)

        self.player_label.grid(column=1, row=8, columnspan=6, rowspan=1)
        self.enemy_label.grid(column=9, row=8, columnspan=6, rowspan=1)

        self.return_label.grid(column=0, row=0, columnspan=2)

        self.activity_label.grid(column=5, row=0, columnspan=6, rowspan=2, sticky='nsew')

        self.player_field.grid(column=1, row=2, columnspan=6, rowspan=6, sticky='nsew')
        self.enemy_field.grid(column=9, row=2, columnspan=6, rowspan=6, sticky='nsew')
        self.player_field.grid_propagate(False)
        self.enemy_field.grid_propagate(False)

        for i in range(FIELD_SIZE):
            self.player_row_labels[i].grid(column=0, row=i + 1, sticky='nsew')
            self.player_col_labels[i].grid(column=i + 1, row=0, sticky='nsew')
            self.enemy_row_labels[i].grid(column=0, row=i + 1, sticky='nsew')
            self.enemy_col_labels[i].grid(column=i + 1, row=0, sticky='nsew')
            for j in range(FIELD_SIZE):
                self.player_buttons[i][j].grid(column=i + 1, row=FIELD_SIZE - j, sticky='nsew')
                self.enemy_buttons[i][j].grid(column=i + 1, row=FIELD_SIZE - j, sticky='nsew')

        self.player_field.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), weight=1,
                                       minsize=20)
        self.player_field.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), weight=1,
                                          minsize=20)
        self.enemy_field.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), weight=1,
                                      minsize=20)
        self.enemy_field.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), weight=1,
                                         minsize=20)

    def destroy(self):
        """Destroy main frame."""
        self.frame.destroy()
