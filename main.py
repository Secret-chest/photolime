import atexit
import numpy
from PIL import Image
import formats
import PIL
import math
import os
import importlib
import warnings
import history

warnings.filterwarnings("ignore")

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, GLib, Gdk

MAX_HISTORY_SIZE = 32
UPDATE_RATE = 20

print(f"Running Pillow {PIL.__version__}")

builder = Gtk.Builder()
builder.add_from_file("main.glade")

window = builder.get_object("root")

operation = None

zoomFactor = 1

ZOOM_FACTOR = 0.25

gtkImage = builder.get_object("image")
zoomValue = builder.get_object("zoomValue")
zoomIndicator = builder.get_object("zoomIndicator")

moduleList = builder.get_object("modules")

static = numpy.random.rand(16, 16, 3) * 256
image = Image.fromarray(static.astype("uint8")).convert("1").convert("RGB")

filePath = "Untitled"

imageHistory = history.History(MAX_HISTORY_SIZE)



def render(event):
    zoomFactor = 2 ** zoomValue.get_value()
    # scaledImage = image.resize((round(image.width * zoomFactor), round(image.height * zoomFactor)),
    #                            resample=Image.NEAREST)

    glibBytes = GLib.Bytes.new(image.tobytes())
    pixbuf = GdkPixbuf.Pixbuf.new_from_data(glibBytes.get_data(), GdkPixbuf.Colorspace.RGB, False, 8,
                                            image.width, image.height,
                                            len(image.getbands()) * image.width)
    pixbuf = pixbuf.scale_simple(image.width * zoomFactor, image.height * zoomFactor, GdkPixbuf.InterpType.NEAREST)

    zoomIndicator.set_text(f"{round(100 * zoomFactor)}%")
    gtkImage.set_from_pixbuf(pixbuf)
    window.set_title(f"{filePath} - photolime")


def loadFile(path):
    global image
    image = Image.open(path)
    imageHistory.add(image)
    render(None)


def saveFile(path):
    global image
    image.save(path)


def askForLoad(event):
    global filePath

    dialog = Gtk.FileChooserDialog(
        title="Open File",
        parent=window,
        action=Gtk.FileChooserAction.OPEN,
    )
    dialog.add_buttons(
        Gtk.STOCK_CANCEL,
        Gtk.ResponseType.CANCEL,
        Gtk.STOCK_OPEN,
        Gtk.ResponseType.OK,
    )

    imageFilter = Gtk.FileFilter()
    imageFilter.set_name("Supported images")
    supported = formats.SUPPORTED + formats.READONLY
    filters = []
    for i in supported:
        typeFilter = Gtk.FileFilter()
        typeFilter.add_mime_type(i)
        if i in formats.READONLY:
            typeFilter.set_name("(read-only) " + i)
        else:
            typeFilter.set_name(i)
        imageFilter.add_mime_type(i)
        filters.append(typeFilter)
    dialog.add_filter(imageFilter)

    anyFilter = Gtk.FileFilter()
    anyFilter.set_name("All files")
    anyFilter.add_pattern("*")
    dialog.add_filter(anyFilter)

    for i in filters:
        dialog.add_filter(i)

    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        filePath = dialog.get_filename()
        print(f"Loading {filePath}")
        loadFile(filePath)
        dialog.destroy()
        return filePath
    else:
        dialog.destroy()
        return None


def askForSave(event):
    dialog = Gtk.FileChooserDialog(
        title="Save File",
        parent=window,
        action=Gtk.FileChooserAction.SAVE,
    )
    dialog.add_buttons(
        Gtk.STOCK_CANCEL,
        Gtk.ResponseType.CANCEL,
        Gtk.STOCK_SAVE,
        Gtk.ResponseType.OK,
    )

    imageFilter = Gtk.FileFilter()
    imageFilter.set_name("Supported images")
    supported = formats.SUPPORTED + formats.WRITEONLY
    filters = []
    for i in supported:
        typeFilter = Gtk.FileFilter()
        typeFilter.add_mime_type(i)
        if i in formats.WRITEONLY:
            typeFilter.set_name("(write-only) " + i)
        else:
            typeFilter.set_name(i)
        imageFilter.add_mime_type(i)
        filters.append(typeFilter)
    dialog.add_filter(imageFilter)

    anyFilter = Gtk.FileFilter()
    anyFilter.set_name("All files")
    anyFilter.add_pattern("*")
    dialog.add_filter(anyFilter)

    for i in filters:
        dialog.add_filter(i)

    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        tempPath = dialog.get_filename()
        print(f"Saving {tempPath}")
        saveFile(tempPath)
        dialog.destroy()
        print(tempPath)
        return tempPath
    else:
        dialog.destroy()
        return None


def saveOver(event):
    print(filePath)
    saveFile(filePath)


def saveAs(event):
    global filePath
    tempPath = askForSave(None)
    if tempPath:
        filePath = tempPath


askForLoad(None)


def zoomIn(event):
    zoomValue.set_value(zoomValue.get_value() + ZOOM_FACTOR)
    render(None)


def zoomOut(event):
    zoomValue.set_value(zoomValue.get_value() - ZOOM_FACTOR)
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


def modifyImage():
    global image, operation
    if operation and operation.ready:
        print("Getting new image")
        image = operation.image
        imageHistory.add(image)
        operation = None
        render(None)
    return True


def undo(event):
    global image
    print(f"Undoing ({imageHistory.pos}/{imageHistory.currentSize})")
    if not imageHistory.isEmpty():
        image = imageHistory.undo()
    render(None)


def redo(event):
    global image
    print(f"Redoing ({imageHistory.pos}/{imageHistory.currentSize})")
    if not imageHistory.isEmpty():
        image = imageHistory.redo()
    render(None)


def openModule(trigger, module):
    global image, operation
    operation = getattr(module, "Operation")(image)
    render(None)


def refreshModules():
    print("Loading modules")
    for d in os.listdir("./modules"):
        print(f"Loading module {d}")
        module = importlib.import_module(f"modules.{d}.main")
        button = Gtk.Button.new_with_label(getattr(module, "METADATA")["name"])
        button.set_tooltip_text(getattr(module, "METADATA")["description"])

        button.connect("clicked", openModule, module)
        button.show()
        moduleList.insert(button, -1)


refreshModules()
render(None)

handlers = {
    "destroy": Gtk.main_quit,
    "update-zoom": render,
    "zoom-in": zoomIn,
    "zoom-out": zoomOut,
    "zoom-initial": zoomInitial,
    "zoom-fit": zoomFit,
    "save": saveOver,
    "save-as": saveAs,
    "save-copy": askForSave,
    "open": askForLoad,
    "undo": undo,
    "redo": redo,
}
builder.connect_signals(handlers)

window.show_all()

GLib.timeout_add(UPDATE_RATE, modifyImage)

atexit.register(lambda: print("Exit"))
atexit.register(imageHistory.clear)

if __name__ == '__main__':
    Gtk.main()
