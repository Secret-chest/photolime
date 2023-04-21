# Photolime metadata for GUI
METADATA = {
    "name": "Automatic contrast",
    "id": "autocontrast",
    "icon": ("GtkIcon", "fill-gradient"),
    "description": "Maximise (normalise) image contrast"
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

        self.preserve = builder.get_object("preserve")

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

        image = ImageOps.autocontrast(self.image, preserve_tone=self.preserve.get_active())

        self.image = image
        self.ready = True
        self.window.destroy()
