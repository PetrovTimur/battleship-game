"""Images workaround."""

from PIL import Image, ImageTk


def loadImage(src, size):
    """Load image for GUI."""
    image = Image.open(src)
    image = image.resize(size, Image.ANTIALIAS)

    return ImageTk.PhotoImage(image)
