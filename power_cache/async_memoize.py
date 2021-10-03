from sys import version_info
from typing import Any, Callable, Literal, Tuple, TypeVar, Union

if version_info >= (3, 9):
    from collections.abc import Coroutine
else:
    from typing import Coroutine

from .key import Key
from .lru import LRUCache
from .ttl import TTLCache

# TODO: Once Python 3.10 is here, rely on ParamSpec specified in PEP 612
_AF = TypeVar("_AF", bound=Callable[..., Coroutine[Any, Any, Any]])


class AsyncMemoize:
    """Memoization async function decorator."""

    def __init__(
        self,
        capacity: int,
        cache_type: Literal["lru", "ttl"] = "lru",
        ttl: Union[int, float] = 0.0,
        results_to_discard: Tuple[Any, ...] = (),
    ):
        if cache_type == "lru":
            self.__cache: Union[LRUCache[Key, Any], TTLCache[Key, Any]] = LRUCache[
                Key, Any
            ](capacity)
        elif cache_type == "ttl":
            self.__cache = TTLCache[Key, Any](capacity, ttl)
        else:
            raise ValueError(f"Unknown cache type: {cache_type}")

        self.__results_to_discard = results_to_discard

    def __call__(self, func: _AF) -> _AF:
        # We return a simpler wrapper when __values_to_discard is empty
        if len(self.__results_to_discard) > 0:

            async def wrapper(*args: Any, **kwargs: Any) -> Any:
                key = Key(args, kwargs)
                result = self.__cache.get(key)
                if result is None:
                    result = await func(*args, **kwargs)
                    if result not in self.__results_to_discard:
                        self.__cache[key] = result
                return result

        else:

            async def wrapper(*args: Any, **kwargs: Any) -> Any:
                key = Key(args, kwargs)
                result = self.__cache.get(key)
                if result is None:
                    result = await func(*args, **kwargs)
                    self.__cache[key] = result
                return result

        # We do this for runtime-type-checking
        wrapper.__annotations__ = func.__annotations__

        return wrapper  # type: ignore


__all__ = ["AsyncMemoize"]
