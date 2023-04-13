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

    def update(self, coord):
        self.cells[coord[0]][coord[1]] = 1
    #     TODO update ships, check status

    def auto_place(self, func):
        self.cells = func()

    def check_placed(self):
        for ship in self.ships:
            if not ship.placed:
                return False
        return True


class Game:
    def __init__(self, mode):
        self.mode = mode
        self.turn_number = 0
        self.player_field = Field()
        self.enemy_field = Field()

    def turn(self, cell):
        self.enemy_field.update(cell)
        if not self.enemy_field.alive:
            return 'WIN'
        #
        self.player_field.update(cell)
        if not self.player_field.alive:
            return 'LOSS'
