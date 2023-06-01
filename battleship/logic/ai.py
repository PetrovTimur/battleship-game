from random import randint


def shot(cells) -> (int, int):
    coords = randint(0, 9), randint(0, 9)
    while cells[coords[0]][coords[1]] < 0:
        coords = randint(0, 9), randint(0, 9)

    return coords


def get_coords(position, size, angle):
    '''Получить координаты которые занимает корабль в данной ориентации
Координаты корабля размера два направленного влево
>>> get_coords([1,1],2,'w')
[(1, 1), (0, 1)]

вниз
>>> get_coords([1,1],2,'s')
[(1, 1), (1, 0)]

вправо
>>> get_coords([1,1],2,'e')
[(1, 1), (2, 1)]

вверх
>>> get_coords([1,1],2,'n')
[(1, 1), (1, 2)]

Проверка на выход за края
>>> get_coords([9,9], 2, 'n')
[]

>>> get_coords([9,9], 2, 'e')
[]

>>> get_coords([0,0], 2, 's')
[]

>>> get_coords([0,0], 2, 'w')
[]

Проверка изменений длинны
>>> get_coords([5,5], 1, 'n')
[(5, 5)]

>>> get_coords([5,5], 2, 'n')
[(5, 5), (5, 6)]

>>> get_coords([5,5], 3, 'e')
[(5, 5), (6, 5), (7, 5)]

>>> get_coords([5,5], 4, 'e')
[(5, 5), (6, 5), (7, 5), (8, 5)]

>>> get_coords([5,5], 5, 's')
[(5, 5), (5, 4), (5, 3), (5, 2), (5, 1)]

>>> get_coords([5,5], 2, 's')
[(5, 5), (5, 4)]

>>> get_coords([5,5], 3, 'w')
[(5, 5), (4, 5), (3, 5)]

>>> get_coords([5,5], 4, 'w')
[(5, 5), (4, 5), (3, 5), (2, 5)]

Неверный ввод
>>> get_coords([5], 4, 'w')
Traceback (most recent call last):
...
IndexError: list index out of range

>>> get_coords([5,5,5], 5, 's')
[(5, 5), (5, 4), (5, 3), (5, 2), (5, 1)]

>>> get_coords([-1,-5], 2, 's')
[]

>>> get_coords([-1,5], 5, 'e')
[]

>>> get_coords([5,5], -3, 'e')
[]

>>> get_coords([5,5], 3, 'з')
Traceback (most recent call last):
...
KeyError: 'з'

>>> get_coords('b', 3, 'e')
Traceback (most recent call last):
...
TypeError: '<=' not supported between instances of 'int' and 'str'

>>> get_coords([5,5], 'b', 'e')
Traceback (most recent call last):
...
TypeError: '>' not supported between instances of 'str' and 'int'

>>> get_coords([5,5], 3, 3)
Traceback (most recent call last):
...
KeyError: 3

    '''
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
    doctest.testmod()

# TODO rework coords to prevent placing at already occupied and nearby spots
