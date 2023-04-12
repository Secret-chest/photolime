# Photolime metadata for GUI
METADATA = {
    "name": "Adjustments",
    "id": "adjustments",
    "icon": ("GtkIcon", "image"),
    "description": "Contrast, saturation, lightness and more"
}

import PIL
import numpy
from PIL import Image, ImageDraw, ImageEnhance

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

        self.brightness = builder.get_object("brightness")
        self.contrast = builder.get_object("contrast")
        self.saturation = builder.get_object("saturation")
        self.sharpness = builder.get_object("sharpness")

        def apply(event):
            self.process()

        def reset(event):
            self.brightness.set_value(0)
            self.contrast.set_value(0)
            self.saturation.set_value(0)
            self.sharpness.set_value(0)

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

        brightness = self.builder.get_object("brightness").get_value() / 100 + 1
        contrast = self.builder.get_object("contrast").get_value() / 100 + 1
        saturation = self.builder.get_object("saturation").get_value() / 100 + 1
        sharpness = self.builder.get_object("sharpness").get_value() / 100 + 1

        pixels = self.image.load()
        image = self.image.copy()

        brightnessEnhancer = ImageEnhance.Brightness(image)
        image = brightnessEnhancer.enhance(brightness)

        contrastEnhancer = ImageEnhance.Contrast(image)
        image = contrastEnhancer.enhance(contrast)

        saturationEnhancer = ImageEnhance.Color(image)
        image = saturationEnhancer.enhance(saturation)

        sharpnessEnhancer = ImageEnhance.Sharpness(image)
        image = sharpnessEnhancer.enhance(sharpness)

        self.image = image
        self.ready = True
        self.window.destroy()
