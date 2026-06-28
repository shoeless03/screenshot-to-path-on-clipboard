from PIL import ImageGrab


def grab_screen():
    return ImageGrab.grab(all_screens=True)


def crop(image, region):
    x1, y1, x2, y2 = region
    return image.crop((min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)))
