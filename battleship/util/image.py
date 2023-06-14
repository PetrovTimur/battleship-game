from PIL import Image, ImageTk


def loadImage(src, size):
    image = Image.open(src)
    image = image.resize(size, Image.ANTIALIAS)

    return ImageTk.PhotoImage(image)
