# Photolime metadata for GUI
METADATA = {
    "name": "Emboss",
    "id": "emboss",
    "icon": ("GtkIcon", "edit-symbolic"),
    "description": "Emboss filter"
}

import PIL
import numpy
from PIL import Image, ImageOps, ImageFilter


class Operation:
    def __init__(self, image: Image):
        self.image = image
        self.ready = False
        self.process()

    def process(self) -> Image:
        print("Modifying image!")

        image = self.image.filter(ImageFilter.EMBOSS)

        self.image = image
        self.ready = True
