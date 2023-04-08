# Photolime metadata for GUI
METADATA = {
            "name": "Static generator",
            "id": "static-generator",
            "icon": ("GtkIcon", "image-denoise-symbolic"),
            "description": "Generate random static noise image"
           }

import PIL
import numpy
from PIL import Image


def process(image: Image) -> Image:
    w = image.width
    h = image.height
    static = numpy.random.rand(h, w, 3) * 256
    image = Image.fromarray(static.astype("uint8")).convert("1").convert("RGB")

    return image