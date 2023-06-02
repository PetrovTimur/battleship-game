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


if __name__ == "__main__":
    import doctest
    doctest.testfile("ai_tests.txt")

# TODO rework coords to prevent placing at already occupied and nearby spots
