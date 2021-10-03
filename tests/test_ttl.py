from time import sleep

from power_cache.ttl import TTLCache


class TestTTLCache:
    def test_that_least_recently_used_item_is_evicted_on_memory_pressure_but_not_before(
        self,
    ) -> None:
        cache = TTLCache(3, 1000)  # We use a long ttl to check the lru-like behavior
        assert len(cache) == 0

        cache.set("a", 1)
        assert len(cache) == 1
        assert cache.get("a") == 1

        cache.set("b", 2)
        assert len(cache) == 2
        assert cache.get("b") == 2
        assert cache.get("a") == 1

        cache.set("c", 3)
        assert len(cache) == 3
        assert cache.get("c") == 3
        assert cache.get("b") == 2
        assert cache.get("a") == 1

        cache.set("d", 4)
        assert len(cache) == 3
        assert cache.get("d") == 4
        assert cache.get("c") is None
        assert cache.get("b") == 2
        assert cache.get("a") == 1

    def test_setitem_and_getitem_and_delitem(self) -> None:
        cache = TTLCache(3, 1000)  # We use a long ttl to check the lru-like behavior

        cache.set("a", 1)
        assert cache["a"] == 1

        try:
            cache["b"]
        except KeyError as e:
            assert e.args[0] == "b"

        del cache["a"]
        try:
            cache["a"]
        except KeyError as e:
            assert e.args[0] == "a"

    def test_ttl_expiration(self) -> None:
        cache = TTLCache(3, 0.001)

        cache["a"] = 1
        cache["b"] = 2

        assert cache.get("a") == 1
        assert cache.get("b") == 2

        sleep(0.001)

        assert cache.get("b") is None
        assert cache.get("a") is None

    def test_ttl_expiration_eviction(self) -> None:
        cache = TTLCache(3, 0.001)

        cache["a"] = 1
        cache["b"] = 2

        assert len(cache) == 2  # Nothing strange
        sleep(0.001)
        assert len(cache) == 2  # Expiration does not trigger eviction
        cache.evict_expired()
        assert len(cache) == 0  # Eviction was performed

        cache["c"] = 3
        cache["d"] = 4
        assert len(cache) == 2  # Nothing strange
        sleep(0.001)
        assert len(cache) == 2  # Expiration does not trigger eviction
        cache["e"] = 5
        assert len(cache) == 3  # Expiration does not trigger eviction
        cache.evict_expired()
        assert len(cache) == 1  # Eviction was performed preserving "e"
