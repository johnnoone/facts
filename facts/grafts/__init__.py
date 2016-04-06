import asyncio
import functools
import logging
import os.path
from collections import namedtuple
from facts.conf import settings
from pkgutil import extend_path, walk_packages
from pkg_resources import iter_entry_points

__path__ = extend_path(__path__, __name__)
__all__ = ['graft', 'Graft', 'Namespace']

Namespace = namedtuple('Namespace', 'namespace value')


class Graft:

    def __init__(self, func, *, namespace=None):
        self.func = asyncio.coroutine(func)
        self.namespace = namespace

    async def __call__(self, *arg, **kwargs):
        response = await self.func(*arg, **kwargs)
        return Namespace(self.namespace, response)


def graft(func=None, *, namespace=None):
    """Decorator for marking a function as a graft.

    Parameters:
        namespace (str): namespace of data, same format as targeting.
    Returns:
        Graft

    For example, these grafts::

        @graft
        def foo_data:
            return {'foo', True}

        @graft(namespace='bar')
        def bar_data:
            return False

    will be redered has::

        {
            'foo': True,
            'bar': False
        }
    """

    if not func:
        return functools.partial(graft, namespace=namespace)

    if isinstance(func, Graft):
        return func

    return Graft(func, namespace=namespace)


def is_graft(func):
    """Tells if func is a graft.
    """
    return isinstance(func, Graft)


class Loader:

    def __init__(self):
        self.GRAFTS = set([])

    def run(self, force=False):
        if self.GRAFTS and not force:
            return self.GRAFTS

        # insert missing paths
        # this could be a configurated item
        self.add_userpath(settings.userpath)

        # autoload decorated functions
        self.load_decorated()

        # append setuptools modules
        self.load_setuptools(settings.entry_point)

        return self.GRAFTS

    def add_userpath(self, userpath):
        if os.path.isdir(userpath) and userpath not in __path__:
            __path__.append(userpath)

    def notify_error(self, name):
        logging.error('unable to load %s package' % name)

    def load_decorated(self):
        root_pkg = '%s.' % __name__
        walker = walk_packages(__path__, root_pkg, onerror=self.notify_error)
        for module_finder, name, ispkg in walker:
            # if not name.endswith('_grafts'):  # TODO remove this
            #     continue
            loader = module_finder.find_module(name)
            mod = loader.load_module(name)
            for func in mod.__dict__.values():
                if is_graft(func):
                    self.GRAFTS.add(func)

    def load_setuptools(self, group):
        for entry_point in iter_entry_points(group=group):
            try:
                func = entry_point.load()
                if is_graft(func):
                    self.GRAFTS.add(func)
                else:
                    self.notify_error(entry_point.name)
            except Exception as error:
                logging.exception(error)
                self.notify_error(entry_point.name)
