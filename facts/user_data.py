from facts.serializer import dump, load
from facts.targeting import Target
from pathlib import Path

__all__ = ['UserFacts']


class UserFacts:

    def __init__(self, filename):
        self.filename = Path(filename)

    @property
    def data(self):
        try:
            return load(self.filename.read_text())
        except FileNotFoundError:
            return {}

    def read(self, target):
        return Target(target).read(self.data)

    def write(self, target, value, merge=False):
        data = Target(target).write(self.data, value, merge)
        self._write(data)

    def delete(self, target):
        data = Target(target).delete(self.data)
        self._write(data)

    def _write(self, data):
        self.filename.parent.mkdir(parents=True, exist_ok=True)
        self.filename.write_text(dump(data))
