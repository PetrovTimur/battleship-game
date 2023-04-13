FIELD_SIZE = 10
SHIPS_PLACED = 0


class Ship:
    def __init__(self, size):
        self.size = size
        self.state = [0] * self.size
        self.afloat = True
        self.placed = False


class Field:
    def __init__(self):
        self.cells = [([0] * 10) for i in range(10)]
        self.ships = [Ship(2), Ship(3), Ship(4)]
        self.alive = True
    #     TODO add right amount of ships


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


class Game:
    def __init__(self, mode):
        self.mode = mode
        self.turn_number = 0
        self.player_field = Field()
        self.enemy_field = Field()

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
