import tempfile
import os
from PIL import Image


class History():
    def __init__(self, maxSize, prefix="photolime-history_"):
        self.maxSize = maxSize
        self.prefix = prefix
        self.pos = -1
        self.currentSize = 0
        self.h = []

    def add(self, item: Image):
        file = tempfile.mkstemp(prefix=self.prefix)
        # write image using PNG format
        item.save(file[1], format="PNG")
        print(f"Saved history item as {file[1]}")
        if self.currentSize == self.maxSize and self.pos == self.maxSize - 1:
            os.remove(self.h.pop(0))
            self.pos -= 1
            self.currentSize -= 1

        while self.pos != self.currentSize - 1 and self.currentSize:
            os.remove(self.h.pop())
            self.currentSize -= 1

        self.h.append(file[1])
        self.pos += 1
        self.currentSize += 1
        print(f"Adding new item ({self.pos}/{self.currentSize})")

    def undo(self):
        self.pos = max(self.pos - 1, 0)
        image = Image.open(self.h[self.pos], formats=["PNG"])
        return image

    def redo(self):
        self.pos = min(self.pos + 1, self.currentSize - 1)
        image = Image.open(self.h[self.pos], formats=["PNG"])
        return image

    def isEmpty(self):
        return self.currentSize == 0

    def clear(self):
        for file in self.h:
            print(file)
            os.remove(file)
