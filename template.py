from tkinter import Tk, Label
from tkinter import ttk


def start_button_pressed():
    global fields
    fields = place_ships()
    window.quit()


def exit_button_pressed():
    window.destroy()
    exit()


def shot_button_pressed():
    global fields, state
    cords = 'players or enemy shoot cords'
    state, fields = game_logic(fields, cords)
    if (state == WIN) or (state == LOSE):
        window.quit()


def game(win):
    destroy_all(win)
    shot_button = ttk.Button(window, text="Shot", command=shot_button_pressed)
    shot_button.pack()
    exit_button = ttk.Button(window, text="Exit", command=exit_button_pressed)
    exit_button.pack()
    global state
    state = PLAYERS_TURN

    win.mainloop()


def destroy_all(window):
    for widget in window.winfo_children():
        widget.destroy()


def place_ships():
    return 'two fields with ships and shots'


def game_logic(fields, cords):
    return WIN, fields


def wait_for_enemy_turn():
    return


WIN = 0
LOSE = 1
PLAYERS_TURN = 2
ENEMY_TURN = 3

fields = 'two fields with ships and shots'
state = None

txt = "Try game for the first time!"
window = Tk()
window.title('battleship-game')
window.geometry("300x250")
window.protocol('WM_DELETE_WINDOW', exit_button_pressed)
while True:
    destroy_all(window)
    start_batton = ttk.Button(text="Start", command=start_button_pressed)
    start_batton.pack()
    exit_button = ttk.Button(text="Exit", command=exit_button_pressed)
    exit_button.pack()
    lbl = Label(text=txt)
    lbl.pack()

    window.mainloop()
    game(window)
    if state == WIN:
        txt = 'Congratulations!!!'
