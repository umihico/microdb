

class MicroDB():
    """In-memory, Hash-mapping, Disk-writable, Thread-safe database."""

    def __init__(self, filename):
        self.filename = filename
