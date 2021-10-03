from typing import Optional
from power_cache.memoize import Memoize


class TestMemoize:
    def test_basic_memoization(self) -> None:
        calls = []

        def my_function(prefix: str, suffix: str) -> str:
            calls.append((prefix, suffix))
            return f"{prefix} {suffix}"

        memoizer = Memoize(capacity=3, cache_type="lru")
        memoized = memoizer(my_function)

        assert memoized.__annotations__ == my_function.__annotations__

        result = my_function("hello", "world")
        assert len(calls) == 1
        assert memoized("hello", "world") == result
        assert len(calls) == 2
        assert memoized("hello", "world") == result
        assert len(calls) == 2  # my_function is not called anymore

    def test_results_to_discard(self) -> None:
        calls = []

        def my_function(a: int, b: int) -> Optional[int]:
            calls.append((a, b))
            if (a % 2 == 0) and (b % 2 == 0):
                return None
            return a * b

        memoizer = Memoize(capacity=3, cache_type="lru", results_to_discard=(None,))
        memoized = memoizer(my_function)

        assert len(calls) == 0
        assert memoized(3, 5) == 15
        assert len(calls) == 1
        assert memoized(3, 5) == 15
        assert len(calls) == 1

        assert memoized(4, 16) is None
        assert len(calls) == 2
        assert memoized(4, 16) is None
        assert len(calls) == 3 # We trigger the computation again
