
import threading as _threading
import ast as _ast
from pprint import pformat as _pformat
import os as _os
import codecs as _codecs
import pprint as _pprint


class MicroDB():
    """In-memory, Hash-mapping, Disk-writable, Thread-safe database."""

    def __init__(self, filename, partition_keys):
        self._rlock = _threading.RLock()
        self.partition_keys = partition_keys
        self.filename = filename
        self._load()

    def _load(self):
        self._dict = {}
        with self._rlock:
            if not _os.path.exists(self.filename):
                return
            with _codecs.open(self.filename, 'r', 'utf-8') as f:
                values = _ast.literal_eval(f.read())
            saved_as_grid = bool(isinstance(values[0], list))
            if saved_as_grid:
                list_of_list = values
                filenames = list_of_list[0]
                for row in list_of_list[1:]:
                    dictionary = {fn: v for fn, v in zip(filenames, row)}
                    key = self.gen_key(dictionary)
                    self._dict[key] = dictionary
            else:
                dictionaries = values
                self._dict = {self.gen_key(
                    dictionary): dictionary for dictionary in dictionaries}

    def save(self, filename=None):
        """
        writes data on disk as list of dictionaries.
        """
        with self._rlock:
            filename = filename or self.filename
            data = list(self._dict.values())
            self._write(filename, data)

    def _write(self, filename, data):
        """inside func of save method"""
        with self._rlock:
            with _codecs.open(filename, 'w', 'utf-8') as f:
                print(data, file=f, flush=True)

    def _get_fieldnames(self):
        """
        exacts keys from dictionaries. Good to fill before 'save_as_grid' method.
        """
        with self._rlock:
            fieldnames = set()
            for d in self._dict.values():
                fieldnames.update(d.keys())
            fieldnames = list(fieldnames)
            return fieldnames

    def _gen_grid(self):
        with self._rlock:

            fieldnames = self._get_fieldnames()
            grid = [fieldnames, ]
            for d in self._dict.values():
                try:
                    row = [d[k] for k in fieldnames]
                except KeyError as e:
                    lack_keys = [fn for fn in fieldnames if fn not in d]
                    raise Exception(
                        f"Dict {d} dosen't have these keys:{lack_keys}")
                grid.append(row)
            return grid

    def save_as_grid(self, filename=None):
        """
        same as 'save' method but as list of list. Good for decreasing amount of file when all dictionary has same keys.
        """
        with self._rlock:
            data = self._gen_grid()
            filename = filename or self.filename
            self._write(filename, data)

    def upsert(self, dictionary):
        """
        inserts new dictionary. if same partition_keys dictionary is already there, it will be overwritten.
        """
        with self._rlock:
            self._dict[self.gen_key(dictionary)] = dictionary

    def gen_key(self, dictionary):
        return tuple([dictionary.get(k) for k in self.partition_keys])

    def erase_all(self):
        "erase all data and write empty dict on disk"
        self._dict = {}
        self.save()

    def lock(self):
        return self._rlock

    def get(self, key, d=None):
        return self._dict.get(self.gen_key(key), d)

    def __str__(self):
        return str(list(self._dict.values()))

    def pprint_all(self):
        _pprint.pprint(list(self._dict.values()))

    def pprint_all_as_grid(self):
        _pprint.pprint(self._gen_grid())

    def all(self):
        yield from self._dict.values()

    def __len__(self):
        return len(self._dict)

    def __contains__(self, key):
        return bool(self.gen_key(key) in self._dict)

    def __delitem__(self, key):
        del self._dict[key]

    def __getitem__(self, key):
        return self._dict[key]
