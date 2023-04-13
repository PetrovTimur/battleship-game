from random import randint


def shot() -> (int, int):
    return randint(0, 9), randint(0, 9)
