from typing import Any, Callable, Literal, Tuple, TypeVar, Union

from .key import Key
from .lru import LRUCache
from .ttl import TTLCache

# TODO: Once Python 3.10 is here, rely on ParamSpec specified in PEP 612
_F = TypeVar("_F", bound=Callable[..., Any])


class Memoize:
    """Memoization function decorator."""

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

    def __call__(self, func: _F) -> _F:
        # We return a simpler wrapper when __values_to_discard is empty
        if len(self.__results_to_discard) > 0:

            def wrapper(*args: Any, **kwargs: Any) -> Any:
                key = Key(args, kwargs)
                result = self.__cache.get(key)
                if result is None:
                    result = func(*args, **kwargs)
                    if result not in self.__results_to_discard:
                        self.__cache[key] = result
                return result

        else:

            def wrapper(*args: Any, **kwargs: Any) -> Any:
                key = Key(args, kwargs)
                result = self.__cache.get(key)
                if result is None:
                    result = func(*args, **kwargs)
                    self.__cache[key] = result
                return result

        # We do this for runtime-type-checking
        wrapper.__annotations__ = func.__annotations__

        return wrapper  # type: ignore


__all__ = ["Memoize"]
