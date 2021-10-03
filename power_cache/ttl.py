from sys import version_info
from time import monotonic
from typing import Generic, Optional, Tuple, TypeVar, Union

if version_info >= (3, 9):
    from collections import OrderedDict
elif version_info >= (3, 7):
    from typing import OrderedDict
else:
    raise ImportError("typed OrderedDict is not available in this version of Python")


_KT = TypeVar("_KT")
_VT = TypeVar("_VT")


class TTLCache(Generic[_KT, _VT]):
    """TTL Cache."""

    __slots__ = ("__cache", "__capacity", "__ttl")

    def __init__(self, capacity: int, ttl: Union[int, float]):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        if ttl <= 0:
            raise ValueError("ttl must be positive")
        self.__capacity = capacity
        self.__ttl = ttl
        self.__cache = OrderedDict[_KT, Tuple[float, _VT]]()

    def get(self, key: _KT, update_expiration: bool = False) -> Optional[_VT]:
        now = monotonic()
        if key in self.__cache:
            (key_expiration, value) = self.__cache.pop(key)
            if key_expiration > now:
                if update_expiration:
                    self.__cache[key] = (now + self.__ttl, value)
                else:
                    self.__cache[key] = (key_expiration, value)
                return value

        return None

    def set(self, key: _KT, value: _VT) -> None:
        # Warning: code replicated in .__setitem__()
        now = monotonic()

        if key in self.__cache:
            self.__cache.move_to_end(key)
            self.__cache[key] = (now + self.__ttl, value)
        else:
            if len(self.__cache) >= self.__capacity:
                self.__cache.popitem(last=False)
            self.__cache[key] = (now + self.__ttl, value)

    def evict_expired(self):
        now = monotonic()
        for key in tuple(self.__cache.keys()):
            if self.__cache[key][0] <= now:
                self.__cache.pop(key)

    # Dunder methods
    # --------------------------------------------------------------------------
    def __contains__(self, key: _KT) -> bool:
        return key in self.__cache

    def __delitem__(self, key):
        del self.__cache[key]

    def __getitem__(self, key: _KT) -> _VT:
        now = monotonic()
        if key in self.__cache:
            (key_expiration, value) = self.__cache.pop(key)
            if key_expiration > now:
                self.__cache[key] = (key_expiration, value)
                return value

        return self.__missing__(key)

    def __len__(self):
        return len(self.__cache)

    def __missing__(self, key):
        raise KeyError(key)

    def __repr__(self):
        return (
            "TTLCache(\n"
            f"\tcapacity={self.__capacity},\n"
            f"\tttl={self.__ttl},\n"
            f"\tcurrsize={len(self.__cache)},\n"
            f"\t{list(self.__cache.items())}\n)"
        )

    def __setitem__(self, key: _KT, value: _VT) -> None:
        # Warning: code copied from .set()
        now = monotonic()

        if key in self.__cache:
            self.__cache.move_to_end(key)
            self.__cache[key] = (now + self.__ttl, value)
        else:
            if len(self.__cache) >= self.__capacity:
                self.__cache.popitem(last=False)
            self.__cache[key] = (now + self.__ttl, value)


__all__ = ["TTLCache"]
