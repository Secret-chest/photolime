# Photolime metadata for GUI
METADATA = {
    "name": "Invert image",
    "id": "invert",
    "icon": ("GtkIcon", "image-invert-symbolic"),
    "description": "Invert the image's RGB values"
}

import PIL
import numpy
from PIL import Image, ImageOps


class Operation:
    def __init__(self, image: Image):
        self.image = image
        self.ready = False
        self.process()

    def process(self) -> Image:
        print("Modifying image!")

        image = ImageOps.invert(self.image)

        self.image = image
        self.ready = True
