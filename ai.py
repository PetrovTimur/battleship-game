from random import randint


def shot(cells) -> (int, int):
    coords = randint(0, 9), randint(0, 9)
    while cells[coords[0]][coords[1]] < 0:
        coords = randint(0, 9), randint(0, 9)

    return coords
