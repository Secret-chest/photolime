# Photolime metadata for GUI
METADATA = {
    "name": "Duotone",
    "id": "duotone",
    "icon": ("GtkIcon", "fill-gradient"),
    "description": "Map the image to a gradient based on lightness"
}

import PIL
import numpy
from PIL import Image, ImageOps

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, GLib


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

        rgb1 = (round(value1.red * 255), round(value1.green * 255), round(value1.blue * 255))
        rgb2 = (round(value2.red * 255), round(value2.green * 255), round(value2.blue * 255))

        #hex1 = "#{:02x}{:02x}{:02x}".format(*c1)
        #hex2 = "#{:02x}{:02x}{:02x}".format(*c2)
        print(rgb1, rgb2, sep=" -> ")

        image = self.image.convert("L")

        image = ImageOps.colorize(image, rgb1, rgb2)

        self.image = image
        self.ready = True
        self.window.destroy()
