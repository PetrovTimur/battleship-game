"""App resources module."""

import os


def set_resource(root, path):
    """Determine resource path."""
    return os.path.join(root, *path.split('/'))


PKGHOME = os.path.dirname(os.path.abspath(__file__ + f'{os.sep}..'))
RSCPATH = os.path.join(PKGHOME, 'resources')
IMGPATH = os.path.join(RSCPATH, 'images')

config = set_resource(PKGHOME, 'config.ini')
esc = set_resource(IMGPATH, 'escape.png')
icon = set_resource(IMGPATH, 'icon.png')
translation = set_resource(PKGHOME, 'translation')
