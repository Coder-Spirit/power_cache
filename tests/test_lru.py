from power_cache.lru import LRUCache


class TestLRUCache:
    def test_that_least_recently_used_item_is_evicted_on_memory_pressure_but_not_before(
        self,
    ) -> None:
        cache = LRUCache(3)
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
        cache = LRUCache(3)

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
