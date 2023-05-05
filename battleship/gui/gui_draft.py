from tkinter import *
from tkinter import ttk
from battleship.logic import game, ai
from battleship.logic.ai import get_coords

FIELD_SIZE = 10

if __name__ == '__main__':
    def step(button):
        position = button.grid_info()['column'], button.grid_info()['row']
        hit = testGame.player_turn((position[0], position[1]))
        if hit:
            buttons2[position[0]][position[1]]['style'] = 'Hit.TButton'
        else:
            buttons2[position[0]][position[1]]['style'] = 'Miss.TButton'
        buttons2[position[0]][position[1]].state(['disabled'])

        new_position = ai.shot(testGame.me.field.cells)
        hit = testGame.enemy_turn((new_position[0], new_position[1]))
        if hit:
            buttons1[new_position[0]][new_position[1]]['style'] = 'Hit.TButton'
        else:
            buttons1[new_position[0]][new_position[1]]['style'] = 'Miss.TButton'

    testGame = game.Game(mode=1)

    root = Tk()
    root.title("Battleship")
    root.geometry('1280x720')

    root.minsize(1280, 720)


    mainframe = ttk.Frame(root, style='Blue.TFrame')
    mainframe.grid(column=0, row=0, sticky='nsew')

    label1 = ttk.Label(mainframe, text='name 1', background='#355C7D', foreground='yellow')
    label1.grid(column=0, row=0, columnspan=3)
    label2 = ttk.Label(mainframe, text='name 2', background='#355C7D', foreground='yellow')
    label2.grid(column=3, row=0, columnspan=3)

    frame1 = ttk.Frame(mainframe, width=800, height=800)
    frame1.grid(column=1, row=2, sticky='nsew')
    frame2 = ttk.Frame(mainframe, width=800, height=800)
    frame2.grid(column=4, row=2, sticky='nsew')

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    mainframe.columnconfigure((0, 2, 3, 5), weight=1, minsize=80)
    mainframe.columnconfigure((1, 4), weight=0, minsize=480)
    mainframe.rowconfigure((0, 1, 3), weight=1, minsize=80)
    mainframe.rowconfigure(2, weight=0, minsize=480)

    buttons1 = [[ttk.Button(frame1, style='Blue.TButton') for i in range(FIELD_SIZE)] for j in range(FIELD_SIZE)]
    buttons2 = [[ttk.Button(frame2, style='Blue.TButton') for i in range(FIELD_SIZE)] for j in range(FIELD_SIZE)]

    current_button = None

    for i in range(FIELD_SIZE):
        for j in range(FIELD_SIZE):
            buttons1[i][j].grid(column=i, row=j, sticky='nsew')
            buttons1[i][j].configure(
                command=lambda b=buttons1[i][j]: place(b))
            buttons1[i][j].bind('<Return>', lambda e: rotate())

            buttons1[i][j].bind('<Enter>', lambda e, b=buttons1[i][j]: hover(b))
            buttons1[i][j].bind('<Leave>', lambda e, b=buttons1[i][j]: leave(b))

            buttons2[i][j].grid(column=i, row=j, sticky='nsew')
            buttons2[i][j].state(['disabled'])
            buttons2[i][j].configure(command=lambda b=buttons2[i][j]: step(b))

    frame2.rowconfigure('all', weight=1)
    frame2.columnconfigure('all', weight=1)

    frame1.rowconfigure('all', weight=1)
    frame1.columnconfigure('all', weight=1)

    root.mainloop()


class ShipPlacementScreen:
    def __init__(self, window):
        self.root = window

        self.frame = ttk.Frame(self.root)
        self.title = ttk.Label(self.frame, text='Ship placement', style='Red.TLabel')
        self.field_frame = ttk.Frame(self.frame)
        self.random_button = ttk.Button(self.frame, text='Random', command=lambda: print('random'))
        self.start_button = ttk.Button(self.frame, text='Ready',
                                       command=lambda: self.root.event_generate('<<GameScreen>>'))
        self.field_buttons: list[list[ttk.Button]] = []

        for i in range(FIELD_SIZE):
            self.field_buttons.append([])
            for j in range(FIELD_SIZE):
                self.field_buttons[i].append(ttk.Button(self.field_frame, style='Blue.TButton'))
                self.field_buttons[i][j].bind('<Enter>', lambda e, col=i, row=j: self.hover((col, row)))
                self.field_buttons[i][j].bind('<Leave>', lambda e, col=i, row=j: self.leave((col, row)))
                self.field_buttons[i][j].bind('<MouseWheel>', lambda e, col=i, row=j: self.rotate((col, row)))

                self.field_buttons[i][j].configure(command=lambda col=i, row=j: self.place_ship((col, row)))

        self.root.bind('<Escape>', lambda e: self.return_to_main())

        self.angle = 's'
        self.game = game.Game(mode=1)
        # TODO move game initialization to NewGameSetupScreen

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

        for i in range(len(self.field_buttons)):
            for j in range(len(self.field_buttons[0])):
                self.field_buttons[i][j].grid(column=i, row=FIELD_SIZE - j - 1, sticky='nsew')

        self.field_frame.rowconfigure('all', weight=1)
        self.field_frame.columnconfigure('all', weight=1)

    def hover(self, pos):
        col, row = pos
        current_button = self.field_buttons[col][row]
        current_button.state(['!hover'])
        if current_button.instate(['!disabled']):
            size = self.game.me.field.ships[self.game.me.field.placed].size

            coords = get_coords(pos, size, self.angle)
            for col, row in coords:
                self.field_buttons[col][row].state(['hover'])

    def leave(self, pos):
        col, row = pos
        current_button = self.field_buttons[col][row]
        if current_button.instate(['!disabled']):
            size = self.game.me.field.ships[self.game.me.field.placed].size

            coords = get_coords(pos, size, self.angle)
            for col, row in coords:
                self.field_buttons[col][row].state(['!hover'])

    def rotate(self, pos):
        angles = ['w', 'n', 'e', 's']

        self.leave(pos)
        self.angle = angles[(angles.index(self.angle) + 1) % 4]
        self.hover(pos)

    def place_ship(self, pos):
        size = self.game.me.field.ships[self.game.me.field.placed].size

        coords = get_coords(pos, size, self.angle)
        if len(coords) < size:
            return

        for col, row in coords:
            self.field_buttons[col][row].state(['disabled', 'pressed'])
            self.field_buttons[col][row]['style'] = 'Ship.TButton'

        self.game.me.field.place(coords)

        if self.game.me.field.check_placed():
            self.update_field()

    def update_field(self):
        for i in range(FIELD_SIZE):
            for j in range(FIELD_SIZE):
                self.field_buttons[i][j].state(['disabled'])

    def destroy(self):
        self.frame.destroy()
