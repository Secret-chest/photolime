# Photolime metadata for GUI
METADATA = {
    "name": "Contour",
    "id": "contour",
    "icon": ("GtkIcon", "edit-symbolic"),
    "description": "Contour the image.\nUse with blur to create less lines"
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

        image = self.image.filter(ImageFilter.FIND_EDGES)

        self.image = image
        self.ready = True
