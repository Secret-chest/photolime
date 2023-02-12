import numpy
from PIL import Image
import math

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, GLib

builder = Gtk.Builder()
builder.add_from_file("main.glade")

window = builder.get_object("root")
window.show_all()

zoomFactor = 1

gtkImage = builder.get_object("image")
zoomValue = builder.get_object("zoomValue")
zoomIndicator = builder.get_object("zoomIndicator")

static = numpy.random.rand(512, 512, 3) * 256
image = Image.fromarray(static.astype("uint8")).convert("1").convert("RGB")


def render(event):
    zoomFactor = 2 ** zoomValue.get_value()
    scaledImage = image.resize((round(image.width * zoomFactor), round(image.height * zoomFactor)),
                               resample=Image.NEAREST)

    glibBytes = GLib.Bytes.new(scaledImage.tobytes())
    pixbuf = GdkPixbuf.Pixbuf.new_from_data(glibBytes.get_data(), GdkPixbuf.Colorspace.RGB, False, 8, scaledImage.width,
                                            scaledImage.height, len(scaledImage.getbands()) * scaledImage.width)
    zoomIndicator.set_text(f"{round(100 * zoomFactor)}%")
    gtkImage.set_from_pixbuf(pixbuf)


def zoomIn(event):
    zoomValue.set_value(zoomValue.get_value() + 0.25)
    render(None)


def zoomOut(event):
    zoomValue.set_value(zoomValue.get_value() - 0.25)
    render(None)


def zoomInitial(event):
    zoomValue.set_value(0)
    render(None)


def zoomFit(event):
    width = gtkImage.get_allocation().width
    height = gtkImage.get_allocation().height
    if height / image.height > width / image.width:
        zoom = math.log2(width / image.width)
    else:
        zoom = math.log2(height / image.height)
    zoomValue.set_value(zoom)
    render(None)


render(None)

handlers = {
    "destroy": Gtk.main_quit,
    "update-zoom": render,
    "zoom-in": zoomIn,
    "zoom-out": zoomOut,
    "zoom-initial": zoomInitial,
    "zoom-fit": zoomFit,
}
builder.connect_signals(handlers)

if __name__ == '__main__':
    Gtk.main()