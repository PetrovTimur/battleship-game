from tkinter import *
from tkinter import ttk
import ai
import game

FIELD_SIZE = 10


def hover(button):
    size = testGame.player_field.ships[game.SHIPS_PLACED].size
    position = button.grid_info()['column'], button.grid_info()['row']
    for i in range(size):
        buttons1[position[0]][position[1] + i].state(['hover'])


def leave(button):
    size = testGame.player_field.ships[game.SHIPS_PLACED].size
    position = button.grid_info()['column'], button.grid_info()['row']
    for i in range(size):
        buttons1[position[0]][position[1] + i].state(['!hover'])


def place(button):
    size = testGame.player_field.ships[game.SHIPS_PLACED].size
    position = button.grid_info()['column'], button.grid_info()['row']
    for i in range(size):
        buttons1[position[0]][position[1] + i].state(['disabled'])

    testGame.player_field.ships[game.SHIPS_PLACED].placed = True
    game.SHIPS_PLACED += 1

# TODO check whether ship fits
# TODO change style of the button after hit


def step(button):
    print(button.state())
    print(button.state(['pressed', 'disabled']))
    print(button.state())
    buttons1[ai.shot()[0]][ai.shot()[1]].state(['disabled'])


testGame = game.Game(mode=1)

root = Tk()
root.title("Battleship")
root.geometry('1280x720')

s = ttk.Style()
s.theme_use('default')
s.configure('Blue.TFrame', background='#406D96')
s.configure('Blue.TButton', width=3, background='#355C7D')
s.map("Blue.TButton", background=[('pressed', 'disabled', 'red'),
                                  ('!pressed', 'disabled', 'black'),
                                  # ('disabled', 'hover', 'yellow'),
                                  ('hover', 'pink')])

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

for i in range(FIELD_SIZE):
    for j in range(FIELD_SIZE):
        buttons1[i][j].grid(column=i, row=j, sticky='nsew')
        buttons1[i][j].configure(
            command=lambda b=buttons1[i][j]: place(b))
        buttons1[i][j].bind('<MouseWheel>', lambda e: print('scroll'))
        # TODO add ship turning for scroll
        buttons1[i][j].bind('<Enter>', lambda e, b=buttons1[i][j]: hover(b))
        buttons1[i][j].bind('<Leave>', lambda e, b=buttons1[i][j]: leave(b))

        buttons2[i][j].grid(column=i, row=j, sticky='nsew')
        buttons2[i][j].configure(command=lambda b=buttons2[i][j]: step(b))

frame2.rowconfigure('all', weight=1)
frame2.columnconfigure('all', weight=1)

frame1.rowconfigure('all', weight=1)
frame1.columnconfigure('all', weight=1)

root.mainloop()
