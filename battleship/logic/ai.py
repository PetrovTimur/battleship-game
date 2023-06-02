from random import randint


def shot(cells) -> (int, int):
    coords = randint(0, 9), randint(0, 9)
    while cells[coords[0]][coords[1]] < 0:
        coords = randint(0, 9), randint(0, 9)

    return coords


def get_coords(position, size, angle):
    angles = {'w': (-1, 0),
              'n': (0, 1),
              'e': (1, 0),
              's': (0, -1)}

    offset = angles[angle]
    coords = []

    if (0 <= position[0] < 10 and 0 <= position[1] < 10
        and size > 0
        and 0 <= position[0] + (size - 1) * offset[0] < 10
        and 0 <= position[1] + (size - 1) * offset[1] < 10):
        for i in range(size):
            coords.append((position[0] + i * offset[0], position[1] + i * offset[1]))

    return coords

def random_ships_matrix():
    sizes = [4,3,3,2,2,2,1,1,1,1]
    number = 1
    cells = [[None]*10 for _ in range(10)]
    angles = {  0: 'w',
                1: 'n',
                2: 'e',
                3: 's'}
    coords = []
    for size in sizes:
        f = True
        while f:
            pos = (randint (0, 9), randint (0, 9))
            angle = angles[randint(0,3)]
            coords = get_coords(pos, size, angle)
            while len(coords) != size:
                pos = (randint (0, 9), randint (0, 9))
                angle = angles[randint(0,3)]
                coords = get_coords(pos, size, angle)
            f = False
            for i in coords:
                if cells[i[0]][i[1]] != None:
                    f = True
                    break
        for coord in coords:
            cells[coord[0]][coord[1]] = number
        for coord in coords:
            if coord[0]<9 and cells[coord[0]+1][coord[1]] == None:
                cells[coord[0]+1][coord[1]] = 0
            if coord[1]<9 and cells[coord[0]][coord[1]+1] == None:
                cells[coord[0]][coord[1]+1] = 0
            if coord[0]>0 and cells[coord[0]-1][coord[1]] == None:
                cells[coord[0]-1][coord[1]] = 0
            if coord[1]>0 and cells[coord[0]][coord[1]-1] == None:
                cells[coord[0]][coord[1]-1] = 0
        number += 1
    for i in range(len(cells)):
        for i2 in range(len(cells[i])):
            if cells[i][i2] == None:
                cells[i][i2] = 0
    return cells


def random_ships(cells):
    ships_coords = {}
    for i in range(10):
        coords = []
        for x in range(len(cells)):
            for y in range(len(cells)):
                if cells [x][y] == i+1:
                    coords.append((x,y))
        ships_coords[i+1] = coords
    return ships_coords


if __name__ == "__main__":
    import doctest
    doctest.testfile("ai_tests.txt")

# TODO rework coords to prevent placing at already occupied and nearby spots
