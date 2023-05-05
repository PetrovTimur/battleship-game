import os


def setResource(root, path):
    return os.path.join(root, *path.split('/'))


PKGHOME = os.path.dirname(os.path.abspath(__file__ + f'{os.sep}..'))

config = setResource(PKGHOME, 'config.ini')