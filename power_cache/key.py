from typing import Any, Dict, Tuple


class Key:
    __slots__ = ("__args", "__kwargs")

    def __init__(self, args: Tuple[Any, ...], kwargs: Dict[str, Any]) -> None:
        self.__args = args
        self.__kwargs = tuple(kwargs.items())

    def __eq__(self, o: object) -> bool:
        return (
            isinstance(o, Key)
            and (self.__args == o.__args)
            and (self.__kwargs == o.__kwargs)
        )

    def __hash__(self) -> int:
        return hash(("Key", self.__args, self.__kwargs))
