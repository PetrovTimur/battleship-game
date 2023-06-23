"""AI features."""

from random import randint, uniform, choice
import threading
import time


def shot(cells) -> (int, int):
    """Shoot at random available cell."""
    time.sleep(uniform(1.5, 2.5))
    coords = randint(0, 9), randint(0, 9)
    while cells[coords[0]][coords[1]] < 0:
        coords = randint(0, 9), randint(0, 9)

    return coords


def get_coords(position, size, angle, field=None):
    """Get a list of coordinates for a ship."""
    angles = {'w': (-1, 0),
              'n': (0, 1),
              'e': (1, 0),
              's': (0, -1)}

    offset = angles[angle]
    coords = []

    for i in range(size):
        coord = (position[0] + i * offset[0], position[1] + i * offset[1])
        if 0 <= coord[0] < 10 and 0 <= coord[1] < 10:
            if field is not None:
                for surr in surrounding([coord]):
                    col, row = surr
                    if field[col][row] > 0:
                        return []

            coords.append(coord)

    return coords


def surrounding(coords):
    """Get neighboring coordinates of a ship."""
    surr = []
    for coord in coords:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                new_coord = (coord[0] + dx, coord[1] + dy)
                if 0 <= coord[0] + dx < 10 and 0 <= coord[1] + dy < 10 \
                        and new_coord not in coords and new_coord not in surr:
                    surr.append(new_coord)

    return surr


def random_ships_matrix():
    """Build a playing field with randomly placed ships."""
    sizes = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    number = 1
    cells = [[None]*10 for _ in range(10)]
    angles = {0: 'w',
              1: 'n',
              2: 'e',
              3: 's'}
    coords = []
    for size in sizes:
        f = True
        while f:
            pos = (randint(0, 9), randint(0, 9))
            angle = angles[randint(0, 3)]
            coords = get_coords(pos, size, angle)
            while len(coords) != size:
                pos = (randint(0, 9), randint(0, 9))
                angle = angles[randint(0, 3)]
                coords = get_coords(pos, size, angle)
            f = False
            for i in coords:
                if cells[i[0]][i[1]] is not None:
                    f = True
                    break
        for coord in coords:
            cells[coord[0]][coord[1]] = number
        for coord in coords:
            if coord[0] < 9 and cells[coord[0]+1][coord[1]] is None:
                cells[coord[0]+1][coord[1]] = 0
            if coord[1] < 9 and cells[coord[0]][coord[1]+1] is None:
                cells[coord[0]][coord[1]+1] = 0
            if coord[0] > 0 and cells[coord[0]-1][coord[1]] is None:
                cells[coord[0]-1][coord[1]] = 0
            if coord[1] > 0 and cells[coord[0]][coord[1]-1] is None:
                cells[coord[0]][coord[1]-1] = 0
            if coord[1] > 0 and coord[0] > 0 and cells[coord[0]-1][coord[1]-1] is None:
                cells[coord[0]-1][coord[1]-1] = 0
            if coord[1] < 9 and coord[0] > 0 and cells[coord[0]-1][coord[1]+1] is None:
                cells[coord[0]-1][coord[1]+1] = 0
            if coord[1] > 0 and coord[0] < 9 and cells[coord[0]+1][coord[1]-1] is None:
                cells[coord[0]+1][coord[1]-1] = 0
            if coord[1] < 9 and coord[0] < 9 and cells[coord[0]+1][coord[1]+1] is None:
                cells[coord[0]+1][coord[1]+1] = 0
        number += 1
    for i in range(len(cells)):
        for i2 in range(len(cells[i])):
            if cells[i][i2] is None:
                cells[i][i2] = 0
    return cells


def random_ships(cells):
    """Get coordinates of placed ships."""
    ships_coords = {}
    for i in range(10):
        coords = []
        for x in range(len(cells)):
            for y in range(len(cells)):
                if cells[x][y] == i+1:
                    coords.append((x, y))
        ships_coords[i+1] = coords
    return ships_coords


class BotThread(threading.Thread):
    """Playing thread for the AI."""

    def __init__(self, game, screen):
        """Initialize all params."""
        self.queue = game.queue
        self.screen = screen
        self.status = True
        self.game = game
        super().__init__(target=self.play, daemon=True)

    def update_screen(self, screen):
        """Get the new screen."""
        self.screen = screen

    def run(self):
        """Start the thread."""
        super().run()

    def shoot(self):
        """Shoot at the player."""
        try:
            pos, status = self.queue.get()
        except ValueError:
            self.status = False
            return False

        if status == 'dead':
            self.status = False

        return status == 'hit' or status == 'sank'

    def get_shot(self):
        """Get shot by the player."""
        pos = shot(self.game.me.field.cells)
        self.queue.put(pos)
        try:
            status = self.screen.enemy_turn()
        except ValueError:
            self.status = False
            return False

        if status == 'dead':
            self.status = False

        return status == 'hit' or status == 'sank'

    def play(self):
        """Start the game."""
        turn = choice(['first', 'second'])
        self.queue.put(turn)
        self.screen.start_game()

        if turn == 'first':
            while self.status:
                while self.shoot():
                    continue

                if not self.status:
                    break

                while self.get_shot():
                    continue
        else:
            while self.status:
                while self.get_shot():
                    continue

                if not self.status:
                    break

                while self.shoot():
                    continue
