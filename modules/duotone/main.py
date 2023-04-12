# Photolime metadata for GUI
METADATA = {
    "name": "Duotone",
    "id": "duotone",
    "icon": ("GtkIcon", "fill-gradient"),
    "description": "Map the image to a gradient based on lightness"
}

import PIL
import numpy
from PIL import Image, ImageDraw

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, GLib
import matplotlib as mpl
import numpy as np


def colourMix(a, b, mix=0):
    c1 = np.array(mpl.colors.to_rgb(a))
    c2 = np.array(mpl.colors.to_rgb(b))
    return mpl.colors.to_rgb((1 - mix)*c1 + mix*c2)


class Operation:
    def __init__(self, image: Image):
        self.image = image
        self.ready = False
        builder = Gtk.Builder()
        builder.add_from_file(f"modules/{METADATA['id']}/settings.glade")

        self.builder = builder

        self.colour2 = builder.get_object("colour1")
        self.colour1 = builder.get_object("colour2")

        def apply(event):
            self.process()

        def cancel(event):
            window.destroy()

        handlers = {
            "cancel": cancel,
            "apply": apply,
        }

        builder.connect_signals(handlers)

        window = builder.get_object("settings")
        window.show_all()
        self.window = window

    def process(self) -> Image:
        print("Modifying image!")

        value1 = self.colour1.get_rgba()
        value2 = self.colour2.get_rgba()

        rgb1 = (value1.red, value1.green, value1.blue)
        rgb2 = (value2.red, value2.green, value2.blue)

        #hex1 = "#{:02x}{:02x}{:02x}".format(*c1)
        #hex2 = "#{:02x}{:02x}{:02x}".format(*c2)
        print(rgb1, rgb2, sep=" -> ")

        mapping = []
        for mix in range(0, 256):
            mapping.append(tuple(round(255 * i) for i in colourMix(rgb1, rgb2, mix / 255)))

        print(mapping)

        self.image = self.image.convert("L")
        pixels = self.image.load()
        image = Image.new("RGB", self.image.size)
        draw = ImageDraw.Draw(image)

        # Recolour each pixel and draw it
        for x in range(image.width):
            for y in range(image.height):
                l = pixels[x, y]
                draw.point((x, y), mapping[l])

        self.image = image
        self.ready = True
        self.window.destroy()
