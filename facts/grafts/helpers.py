from .bases import ANNOTATIONS
from contextlib import suppress


def as_graft(func):
    """Return func as a graft.
    """
    return ANNOTATIONS[func]


def is_graft(func):
    """Tells if func is a graft.
    """
    with suppress(TypeError):
        return func in ANNOTATIONS
    return False
