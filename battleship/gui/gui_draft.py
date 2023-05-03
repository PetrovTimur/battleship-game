from tkinter import *
from tkinter import ttk
from battleship.logic import game, ai

FIELD_SIZE = 10


def rotate(angle = 1):
    if current_button == None:
        print('No button')
    else:
        leave(current_button)
        testGame.rotate(angle)
        hover(current_button)


def get_rotated_cords(pos, size, rot):
        # rot = 0-up, 1-left, 2-down, 3-right
        pos_num = ([1,0,1,0])[rot]
        sign = ([1,1,-1,-1])[rot]

        coords = []
        
        for i in range(size):
            coords.append((pos[0], pos[1]))

            pos[pos_num] += sign
            if ((pos[0] >= FIELD_SIZE) or (pos[1] >= FIELD_SIZE)
                or (pos[0] < 0) or (pos[1] < 0)):
                break
        
        return coords



def hover(button):
    global current_button
    current_button = button
    if button.instate(['!disabled']):
        size = testGame.me.field.ships[testGame.me.field.placed].size
        position = button.grid_info()['column'], button.grid_info()['row']

        coords = []
        coords = get_rotated_cords(list(position), size, testGame.rotation_number)
        for i in coords:
            buttons1[i[0]][i[1]].state(['hover'])


def leave(button):
    if button.instate(['!disabled']):
        size = testGame.me.field.ships[testGame.me.field.placed].size
        position = button.grid_info()['column'], button.grid_info()['row']

        coords = []
        coords = get_rotated_cords(list(position), size, testGame.rotation_number)
        for i in coords:
            buttons1[i[0]][i[1]].state(['!hover'])


def place(button):
    if button.instate(['!disabled']):
        size = testGame.me.field.ships[testGame.me.field.placed].size
        position = button.grid_info()['column'], button.grid_info()['row']

        coords = []
        coords = get_rotated_cords(list(position), size, testGame.rotation_number)
        if (len(coords) < size):
            return

        for i in coords:
            buttons1[i[0]][i[1]].state(['disabled', 'pressed'])
            buttons1[i[0]][i[1]]['style'] = 'Ship.TButton'

        testGame.me.field.place(coords)
        testGame.me.field.placed += 1

        if testGame.me.field.check_placed():
            update_field()

# TODO check whether ship fits


def update_field():
    for i in range(FIELD_SIZE):
        for j in range(FIELD_SIZE):
            buttons1[i][j].state(['disabled'])
            buttons2[i][j].state(['!disabled'])


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

s = ttk.Style()
s.theme_use('default')
s.configure('Blue.TFrame', background='#406D96')
s.configure('Blue.TButton', width=3, background='#355C7D')
s.configure('Ship.TButton', width=3)
s.configure('Hit.TButton', width=3)
s.configure('Miss.TButton', width=3)
s.map('Blue.TButton', background=[('!pressed', 'disabled', '#26364a'), ('hover', 'pink')])
s.map('Ship.TButton', background=[('disabled', 'grey')])
s.map('Hit.TButton', background=[('disabled', 'orange')])
s.map('Miss.TButton', background=[('disabled', 'black')])

# TODO add different button styles

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
        # TODO add ship turning for scroll
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
