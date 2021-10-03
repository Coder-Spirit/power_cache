# Power Cache

[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Simple (but powerful) Caching Tools.

## Why another caching library

There are many libraries out there to deal with the same problem that this
library tries to solve, but most of them fall short on at least one of the
following points:

- Minimalism.
- Providing proper type hints to ease the user's life when using the library.
- Providing out-of-the-box support for asynchronous functions.
- Simplicity. One clear example is how cache's capacity is measured. In
  `power_cache`, capacity is measured just counting items, and not using their
  size, as other libraries do. There are legitimate reasons to avoid the "sizes
  approach": it heavily affects performance, and it's highly error prone.
- Correctness:
  - Some popular implementations incorrectly implement `__eq__` by just
    comparing object hashes.
  - Some popular implementations implement `__hash__` in a way that collisions
    will be more frequent than desirable.

## Usage

### LRU Cache

```python
from power_cache import LRUCache

cache = LRUCache(capacity=3)

# We can also specify key & value types if we are using `mypy` or `pytypes`
cache = LRUCache[str, int](capacity=3)

cache['the answer to everything'] = 42
cache['the answer to everything']  # returns 42

cache['a'] = 1
cache['b'] = 2
cache['c'] = 3

# Raises KeyError, because the key was the least recently used, and the capacity
# is only 3, so the previous value was evicted.
cache['the answer to everything']
```

## TTL Cache

`TTLCache` is very similar to `LRUCache`, with the distinction that it marks
values as expired if they are too old.

```python
from time import sleep
from power_cache import TTLCache

cache = TTLCache(capacity=3, ttl=120)  # Values valid only for 2 minutes

# We can also specify key & value types if we are using `mypy` or `pytypes`
cache = TTLCache[str, int](capacity=3, ttl=120)

cache['the answer to everything'] = 42
cache['the answer to everything']  # returns 42

cache['a'] = 1
cache['b'] = 2
cache['c'] = 3

# Raises KeyError, because the key was the least recently used, and the capacity
# is only 3, so the previous value was evicted.
cache['the answer to everything']

assert len(cache) == 3

cache.evict_expired()  # We can manually evict all expired values
assert len(cache) == 3  # Nothing was evicted because values are too recent

sleep(121)

# Now all values are marked as expired, but not evicted automatically, because
# that would spend too much CPU time.
assert len(cache) == 3

cache.evict_expired()  # We can manually evict all expired values
assert len(cache) == 0
```

## Memoize

```python
from power_cache import Memoize

# Runtime annotations are preserved.
# `capacity` must be always specified, while `cache_type` is "lru" by default.
@Memoize(capacity=3, cache_type="lru")
def my_function(): ...

@Memoize(capacity=3, cache_type="ttl", ttl=120)
def another_function(): ...
```

## AsyncMemoize

```python
from power_cache import AsyncMemoize

# Runtime annotations are preserved.
# `capacity` must be always specified, while `cache_type` is "lru" by default.
@AsyncMemoize(capacity=3, cache_type="lru")
async def my_function(): ...

@AsyncMemoize(capacity=3, cache_type="ttl", ttl=120)
async def another_function(): ...
```
