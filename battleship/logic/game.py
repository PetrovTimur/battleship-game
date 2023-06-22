from .ai import random_ships, random_ships_matrix
from battleship.translation import _

FIELD_SIZE = 10
TOTAL_SHIPS = 10


class Ship:
    '''The class defining the ship'''
    def __init__(self, size):
        self.size = size
        self.status = {}
        self.afloat = True
        self.placed = False

    def hit(self, coord):
        '''Hit on this ship'''
        self.status[coord] = True
        self.afloat = not all(self.status.values())

    def place(self, coords):
        '''Installation of this ship'''
        for coord in coords:
            self.status[coord] = False

        self.placed = True


class Field:
    '''The class that defines the playing field'''
    def __init__(self):
        self.cells = [([0] * 10) for i in range(10)]
        self.ships = [Ship(4), Ship(3), Ship(3),
                      Ship(2), Ship(2), Ship(2),
                      Ship(1), Ship(1), Ship(1), Ship(1)]
        self.placed = 0
        self.sank = []

    def check(self, coord):
        '''Checking the hit on the ship'''
        hit = self.cells[coord[0]][coord[1]] > 0
        status = ''
        if hit:
            self.ships[self.cells[coord[0]][coord[1]] - 1].hit(coord)
            if self.ships[self.cells[coord[0]][coord[1]] - 1].afloat:
                status = 'hit'
            else:
                status = 'sank'
                self.sank.append(self.ships[self.cells[coord[0]][coord[1]] - 1])
            self.cells[coord[0]][coord[1]] = -1
        else:
            self.cells[coord[0]][coord[1]] = -2
            status = 'miss'

        return status

    def update(self, coord, status):
        '''Cell status updates when hit'''
        if status == 'hit' or status == 'sank':
            self.cells[coord[0]][coord[1]] = -1
        else:
            self.cells[coord[0]][coord[1]] = -2

        return status == 'hit' or status == 'sank'

    def auto_place(self):
        '''Automatic placement of ships'''
        self.placed = 0
        self.cells = random_ships_matrix()
        ships = random_ships(self.cells)
        for i in range(10):
            self.place(ships[i + 1])

    def check_placed(self):
        '''Checking whether the ship is placed'''
        for ship in self.ships:
            if not ship.placed:
                return False
        return True

    def clear(self):
        '''Clearing the list of delivered ships'''
        self.placed = 0
        self.cells = [([0] * 10) for i in range(10)]
        self.ships = [Ship(4), Ship(3), Ship(3),
                      Ship(2), Ship(2), Ship(2),
                      Ship(1), Ship(1), Ship(1), Ship(1)]

    def place(self, coords):
        '''Placing the ship on the playing field'''
        for coord in coords:
            self.cells[coord[0]][coord[1]] = self.placed + 1

        self.ships[self.placed].place(coords)

        self.placed += 1


class Player:
    def __init__(self, name):
        self.name = name
        self.field = Field()
        self.alive = True

    def update_status(self):
        self.alive = any(ship.afloat for ship in self.field.ships)

    def update_field(self, coord):
        hit = self.field.check(coord)

        self.update_status()

        if self.alive:
            return hit
        else:
            return 'dead'


class Bot(Player):
    def __init__(self):
        super().__init__(_('AI'))
        self.field.auto_place()


class Game:
    '''Organization of the sequence of moves'''
    def __init__(self, mode, name):
        self.mode = mode
        self.me = Player(name)
        if mode == 'online':
            self.enemy = None
        else:
            self.enemy = Bot()
        self.queue = None
        self.thread = None
        self.turn = None

    def player_turn(self, cell):
        return self.enemy.update_field(cell)

    def enemy_turn(self, cell):
        return self.me.update_field(cell)
