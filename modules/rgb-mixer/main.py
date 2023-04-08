# Photolime metadata for GUI
METADATA = {
    "name": "RGB mixer",
    "id": "rgb-mixer",
    "icon": ("GtkIcon", "color-profile"),
    "description": "Set RGB channel values"
}

import PIL
import numpy
from PIL import Image, ImageDraw

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

        self.red = builder.get_object("red")
        self.green = builder.get_object("green")
        self.blue = builder.get_object("blue")

        def apply(event):
            self.process()

        def reset(event):
            self.red.set_value(0)
            self.green.set_value(0)
            self.blue.set_value(0)

        def cancel(event):
            window.destroy()

        handlers = {
            "reset": reset,
            "cancel": cancel,
            "apply": apply,
        }

        builder.connect_signals(handlers)

        window = builder.get_object("settings")
        window.show_all()
        self.window = window

    def process(self) -> Image:
        print("Modifying image!")

        red = self.builder.get_object("red")
        green = self.builder.get_object("green")
        blue = self.builder.get_object("blue")

        redValue = red.get_value() / 100 + 1
        greenValue = green.get_value() / 100 + 1
        blueValue = blue.get_value() / 100 + 1

        pixels = self.image.load()
        image = Image.new("RGB", self.image.size)
        draw = ImageDraw.Draw(image)

        # Recolour each pixel and draw it
        for x in range(image.width):
            for y in range(image.height):
                r, g, b = pixels[x, y]
                r = round(r * redValue)
                g = round(g * greenValue)
                b = round(b * blueValue)
                draw.point((x, y), (r, g, b))

        self.image = image
        self.ready = True
        self.window.destroy()
