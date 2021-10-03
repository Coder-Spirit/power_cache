from sys import version_info
from typing import Generic, Optional, TypeVar

if version_info >= (3, 9):
    from collections import OrderedDict
elif version_info >= (3, 7):
    from typing import OrderedDict
else:
    raise ImportError("typed OrderedDict is not available in this version of Python")


_KT = TypeVar("_KT")
_VT = TypeVar("_VT")


class LRUCache(Generic[_KT, _VT]):
    """LRU Cache."""

    __slots__ = ("__capacity", "__cache")

    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.__capacity = capacity
        self.__cache = OrderedDict[_KT, _VT]()

    def get(self, key: _KT) -> Optional[_VT]:
        # WARNING: Code replicated in  .__setitem__()
        if key in self.__cache:
            self.__cache.move_to_end(key)
        return self.__cache.get(key)

    def set(self, key: _KT, value: _VT) -> None:
        self.__cache[key] = value
        self.__cache.move_to_end(key)
        if len(self.__cache) > self.__capacity:
            self.__cache.popitem(last=False)

    # Dunder methods
    # --------------------------------------------------------------------------
    def __contains__(self, key: _KT) -> bool:
        return key in self.__cache

    def __delitem__(self, key):
        del self.__cache[key]

    def __getitem__(self, key: _KT) -> _VT:
        if key in self.__cache:
            self.__cache.move_to_end(key)
        return self.__cache[key]

    def __len__(self):
        return len(self.__cache)

    def __missing__(self, key):
        raise KeyError(key)

    def __repr__(self):
        return (
            "LRUCache(\n"
            f"\tcapacity={self.__capacity},\n"
            f"\tcurrsize={len(self.__cache)},\n"
            f"\t{list(self.__cache.items())}\n)"
        )

    def __setitem__(self, key: _KT, value: _VT) -> None:
        # WARNING: Code copied from .set()
        self.__cache[key] = value
        self.__cache.move_to_end(key)
        if len(self.__cache) > self.__capacity:
            self.__cache.popitem(last=False)


__all__ = ["LRUCache"]
