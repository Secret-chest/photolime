import tempfile
import os


class History():
    def __init__(self, maxSize, prefix="photolime-history_"):
        self.maxSize = maxSize
        self.prefix = prefix
        self.pos = 0
        self.currentSize = 0
        self.h = []

    def add(self, item):
        item = item.tobytes()
        file = tempfile.mkstemp(prefix=self.prefix)
        with open(file[1], "wb") as f:
            f.write(item)
        if self.currentSize == self.maxSize and self.pos == self.maxSize - 1:
            del self.h[0]
            self.pos -= 1
            self.currentSize -= 1
        del self.h[self.pos + 1:]
        self.h.insert(self.pos, file[1])
        self.pos += 1
        self.currentSize += 1
        # FIXME

    def undo(self):
        self.pos = min(self.pos - 1, 0)
        return self.h[self.pos]

    def redo(self):
        self.pos = max(self.pos + 1, self.currentSize)
        return self.h[self.pos]

    def isEmpty(self):
        return self.currentSize == 0

    def clear(self):
        for i in self.h:
            os.remove(i)
