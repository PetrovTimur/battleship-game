import os


def setResource(root, path):
    return os.path.join(root, *path.split('/'))


PKGHOME = os.path.dirname(os.path.abspath(__file__ + f'{os.sep}..'))
RSCPATH = os.path.join(PKGHOME, 'resources')
IMGPATH = os.path.join(RSCPATH, 'images')

config = setResource(PKGHOME, 'config.ini')
esc = setResource(IMGPATH, 'escape.png')
