FIELD_SIZE = 10
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

        self.placed = True


class Field:
    def __init__(self):
        self.cells = [([0] * 10) for i in range(10)]
        self.ships = [Ship(4), Ship(3), Ship(3),
                      Ship(2), Ship(2), Ship(2),
                      Ship(1), Ship(1), Ship(1), Ship(1)]
        self.alive = True
        self.placed = 0

    def update_field(self, coord):
        hit = self.cells[coord[0]][coord[1]] > 0
        if hit:
            self.ships[self.cells[coord[0]][coord[1]] - 1].hit(coord)
            self.cells[coord[0]][coord[1]] = -1
            self.update_status()
        else:
            self.cells[coord[0]][coord[1]] = -2

        return hit

    def auto_place(self, func):
        self.cells = func()

    def check_placed(self):
        for ship in self.ships:
            if not ship.placed:
                return False
        return True

    def update_status(self):
        self.alive = any(ship.afloat for ship in self.ships)

    def place(self, coords):
        for coord in coords:
            self.cells[coord[0]][coord[1]] = self.placed + 1

        self.ships[self.placed].place(coords)


class Game:
    def __init__(self, mode):
        self.mode = mode
        self.turn_number = 0
        self.rotation_number = 0
        self.player_field = Field()
        self.enemy_field = Field()

    def player_turn(self, cell):
        return self.enemy_field.update_field(cell)

    def enemy_turn(self, cell):
        return self.player_field.update_field(cell)
    
    def rotate(self, angle = 1):
        self.rotation_number = (self.rotation_number + angle)%4
