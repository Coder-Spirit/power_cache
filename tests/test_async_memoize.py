from typing import Optional

import pytest

from power_cache.async_memoize import AsyncMemoize


class TestAsyncMemoize:
    @pytest.mark.asyncio
    async def test_basic_memoization(self) -> None:
        calls = []

        async def my_function(prefix: str, suffix: str) -> str:
            calls.append((prefix, suffix))
            return f"{prefix} {suffix}"

        memoizer = AsyncMemoize(capacity=3, cache_type="lru")
        memoized = memoizer(my_function)

        assert memoized.__annotations__ == my_function.__annotations__

        result = await my_function("hello", "world")
        assert len(calls) == 1
        assert await memoized("hello", "world") == result
        assert len(calls) == 2
        assert await memoized("hello", "world") == result
        assert len(calls) == 2  # my_function is not called anymore

    @pytest.mark.asyncio
    async def test_results_to_discard(self) -> None:
        calls = []

        async def my_function(a: int, b: int) -> Optional[int]:
            calls.append((a, b))
            if (a % 2 == 0) and (b % 2 == 0):
                return None
            return a * b

        memoizer = AsyncMemoize(
            capacity=3, cache_type="lru", results_to_discard=(None,)
        )
        memoized = memoizer(my_function)

        assert len(calls) == 0
        assert await memoized(3, 5) == 15
        assert len(calls) == 1
        assert await memoized(3, 5) == 15
        assert len(calls) == 1

        assert await memoized(4, 16) is None
        assert len(calls) == 2
        assert await memoized(4, 16) is None
        assert len(calls) == 3  # We trigger the computation again
