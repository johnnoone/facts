"""
    Workflow
    --------

    All discovered grafts are kept into ANNOTATIONS set.
    Loader explores filesystem and entry points and contributes to
    ANNOTATIONS.
    But it exposes only his own discovered grafts.
"""

import logging
import os.path
import sys
from .bases import Namespace, Graft, ANNOTATIONS, graft
from .helpers import is_graft
from .exceptions import ConflictError
from pkgutil import extend_path, walk_packages
from pkg_resources import iter_entry_points

__path__ = extend_path(__path__, __name__)
__all__ = ['graft', 'Graft', 'ConflictError', 'Namespace']


class Loader:

    def __init__(self, settings):
        self.GRAFTS = set([])
        self.settings = settings

    def run(self, force=False):
        if self.GRAFTS and not force:
            return self.GRAFTS

        # insert missing paths
        # this could be a configurated item
        self.add_userpath(self.settings.userpath)

        # autoload decorated functions
        self.load_decorated()

        # append setuptools modules
        self.load_setuptools(self.settings.entry_point)

        return self.GRAFTS

    def add_userpath(self, userpath):
        if os.path.isdir(userpath) and userpath not in __path__:
            __path__.append(userpath)

    def notify_error(self, name):
        logging.error('unable to load %s package', name)

    def load_decorated(self):
        root_pkg = '%s.' % __name__
        walker = walk_packages(__path__, root_pkg, onerror=self.notify_error)

        for module_finder, name, ispkg in walker:
            parts = name.split('.')
            if any(part.startswith('_') for part in parts):
                logging.info('ignore %s', name)
            try:
                mod = sys.modules[name]
                logging.info('use %s', name)
            except KeyError:
                loader = module_finder.find_module(name)
                logging.info('load %s', name)
                mod = loader.load_module(name)
            for func in mod.__dict__.values():
                if is_graft(func):
                    self.GRAFTS.add(ANNOTATIONS[func])

    def load_setuptools(self, group):
        for entry_point in iter_entry_points(group=group):
            try:
                func = entry_point.load()
                if is_graft(func):
                    self.GRAFTS.add(ANNOTATIONS[func])
                else:
                    self.notify_error(entry_point.name)
            except Exception as error:
                logging.exception(error)
                self.notify_error(entry_point.name)
