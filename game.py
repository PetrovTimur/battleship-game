FIELD_SIZE = 10
SHIPS_PLACED = 0
TOTAL_SHIPS = 10


class Ship:
    def __init__(self, size):
        self.size = size
        self.status = {}
        self.afloat = True
        self.placed = False

    def hit(self, coord):
        self.status[coord] = True
        self.afloat = not all(self.status.values())

    def place(self, coords):
        for coord in coords:
            self.status[coord] = False


class Field:
    def __init__(self):
        self.cells = [([0] * 10) for i in range(10)]
        self.ships = [Ship(4), Ship(3), Ship(3),
                      Ship(2), Ship(2), Ship(2),
                      Ship(1), Ship(1), Ship(1), Ship(1)]
        self.alive = True

    def update_field(self, coord):
        self.cells[coord[0]][coord[1]] = -1
        self.ships[self.cells[coord[0]][coord[1]]].hit(coord)
        self.update_status()

    #     TODO check for empty/non empty -> different number

    def auto_place(self, func):
        self.cells = func()

    def check_placed(self):
        for ship in self.ships:
            if not ship.placed:
                return False
        return True

    def update_status(self):
        self.alive = any(ship.afloat for ship in self.ships)


class Game:
    def __init__(self, mode):
        self.mode = mode
        self.turn_number = 0
        self.player_field = Field()
        self.enemy_field = Field()

    def turn(self, cell):
        self.enemy_field.update_field(cell)
        if not self.enemy_field.alive:
            return 'WIN'
        #
        self.player_field.update_field(cell)
        if not self.player_field.alive:
            return 'LOSS'
