# Photolime metadata for GUI
METADATA = {
    "name": "Blur",
    "id": "blur",
    "icon": ("GtkIcon", "fill-gradient"),
    "description": "Blur the image"
}

import PIL
import numpy
from PIL import Image, ImageOps, ImageFilter

import gi
gi.require_version("Gtk", "3.0")
from gi.overrides import Gtk, GdkPixbuf, GLib


class Operation:
    def __init__(self, image: Image):
        self.image = image
        self.ready = False
        builder = Gtk.Builder()
        builder.add_from_file(f"modules/{METADATA['id']}/settings.glade")

        self.builder = builder

        self.radius = builder.get_object("radius")
        self.gaussian = builder.get_object("gaussian")

        def apply(event):
            self.process()

        def cancel(event):
            window.destroy()

        def reset(event):
            self.radius.set_value(0)

        handlers = {
            "cancel": cancel,
            "apply": apply,
            "reset": reset,
        }

        builder.connect_signals(handlers)

        window = builder.get_object("settings")
        window.show_all()
        self.window = window

    def process(self) -> Image:
        print("Modifying image!")

        blurFunction = None

        radius = self.radius.get_value()
        if self.gaussian.get_active():
            blurFunction = ImageFilter.GaussianBlur
        else:
            blurFunction = ImageFilter.BoxBlur

        image = self.image.filter(blurFunction(radius))

        self.image = image
        self.ready = True
        self.window.destroy()
