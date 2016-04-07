import asyncio
import functools
from .exceptions import ConflictError
from collections import namedtuple
from weakref import WeakKeyDictionary

ANNOTATIONS = WeakKeyDictionary()

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

    if func in ANNOTATIONS:
        raise ConflictError('%s already registered!' % func)

    if isinstance(func, Graft):
        ANNOTATIONS[func] = func
    else:
        ANNOTATIONS[func] = Graft(func, namespace=namespace)
    return func
