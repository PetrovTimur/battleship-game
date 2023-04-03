from tkinter import Tk, Label
from tkinter import ttk

class Shot:
    def __init__(self, cell, player):
        'Cell format letter and number for example "a1", player format is int, 0-ENEMY, 1-YOU'
        self.cell = cell
        self.player = player


    def cordx(self):
        return self.cell[0]
    

    def cordy(self):
        return int(self.cell[1])
    

    def cord(self):
        return self.cell
    

    def get_player(self):
        return self.player
    
class Fields:
    def __init__(self, your_field, enemy_field):
        'Two lists 8*8 with 0-Nothing; 1-ship; 2-nothing, shooted; 3-ship, shooted'
        self.your_field = your_field
        self.enemy_field = enemy_field

    
    def enemy(self):
        return self.enemy_field
    

    def player(self):
        return self.your_field
    

    def any_yours_ship(self):
        flag = False
        for i in self.your_field:
            if i==1:
                flag = True
                break
        return flag
    

    def any_enemys_ship(self):
        flag = False
        for i in self.enemy_field:
            if i==1:
                flag = True
                break
        return flag



    def shoot(self, cords):
        def make_shot(field, cord):
            x = ord(cord[0])-ord('a')
            y = int(cord[1])
            if field[x][y] == SHIP:
                field[x][y] = SHIP_SHOOTED
            elif field[x][y] == NOTHING:
                field[x][y] = NOTHING_SHOOTED
            else:
                pass


        if cords.get_player == ENEMY:
            make_shot(self.enemy_field, cords.cord())
        else:
            cords.cord()
            make_shot(self.your_field, cords.cord())

        


def start_button_pressed():
    global fields
    fields = place_ships()
    window.quit()


def exit_button_pressed():
    window.destroy()
    exit()


def shot_button_pressed():
    global fields, state
    cords = Shot('a1', PLAYER)
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
    global fields
    return fields


def send_to_enemy(cords):
    return


def game_logic(fields, cords):
    'gets cords (consists of string(cell) and int(who made a a shot)) process shots'
    global PLAYER, ENEMY
    fields.shoot(cords)
    send_to_enemy(cords)
    if cords.get_player() == ENEMY:
        if fields.any_yours_ship():
            return ENEMY_TURN, fields
        else:
            return LOSE, fields
    else:
        if fields.any_enemys_ship():
            return PLAYERS_TURN, fields
        else:
            return WIN, fields
        return PLAYERS_TURN, fields
    return WIN, fields


def wait_for_enemy_turn():
    return


NOTHING = 0
SHIP = 1
NOTHING_SHOOTED  = 2
SHIP_SHOOTED = 3

ENEMY = 0
PLAYER = 1

WIN = 0
LOSE = 1
PLAYERS_TURN = 2
ENEMY_TURN = 3

fields = Fields([[0]*8]*8, [[0]*8]*8)
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
