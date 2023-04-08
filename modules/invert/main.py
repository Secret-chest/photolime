# Photolime metadata for GUI
METADATA = {
            "name": "Invert image",
            "id": "invert",
            "icon": ("GtkIcon", "image-invert-symbolic"),
            "description": "Invert the image's RGB values"
           }

import PIL
import numpy
from PIL import Image, ImageDraw


def process(image: Image) -> Image:
    w = image.width
    h = image.height

    pixels = image.load()
    draw = ImageDraw.Draw(image)

    for x in range(w):
        for y in range(h):
            r, g, b = pixels[x, y]
            r = 255 - r
            g = 255 - g
            b = 255 - b
            draw.point((x, y), (r, g, b))

    return image
