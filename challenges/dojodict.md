What is Python did have the dict data type? How would we build it for ourselves?

dict recap:

d = { 'key1': 10, 'key2': 20, 'key3': 8}

Very fast! d['key2'] is O(1) lookup, one operation, no searching.
Very different than scanning through a list. O(n)
Even faster than a binary search. O(log n)

If Python didn't have this, how would we build it?

```
from typing import Any, List, Tuple, Optional

class DojoDict:
    def __init__(self, capacity: int = 16) -> None:
        self._buckets = [None for _ in range(capacity)]

    def _find_index(self, key: str) -> int:
        # return number from 0 to len(_buckets)-1
        keys_index = sum( ord(char) for char in key)
        return keys_index % len(self._buckets)

    def set(self, key: str, value: Any) -> None:
        i = self._find_index(key)
        self._buckets(i) = value
        # PROBLEM! What do we do if two keys have the same index?!
 
    def get(self, key: str, default: Optional[Any] = None) -> Any:
        i = self._find_index(key)
        v = self._buckets[i]
        return v
        # or simply: return self._buckets[ self._find_index(key)]

```
- talk about the hashing function
- talk about bucket collisions
- talk about auto extending the list size


Let's fix the error that keys can have the same index
by making each bucket a LIST of (key,value) s
that share the same index

```
from typing import Any, List, Tuple, Optional

class DojoDict:
    def __init__(self, capacity: int = 16) -> None:
        self._buckets: List = [[] for _ in range(capacity)]

    def _find_index(self, key: str) -> int:
        # return number from 0 to len(_buckets)-1
        keys_index = sum( ord(char) for char in key)
        return keys_index % len(self._buckets)

    def set(self, key: str, value: Any) -> None:
        i = self._find_index(key)
        bucket = self._buckets[i]
        for idx, (k, _) in enumerate(bucket):
            if k == key:
                bucket[idx] = (key, value)  # update
                return
        bucket.append((key, value))        # otherwise, insert

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        i = self._find_index(key)
        for k, v in self._buckets[i]:
            if k == key:
                return v
        return default
```

Now it will work even if two keys share an index. But the hashing algorithm _find_index
is poor. Some bucket indexes will be more common than others causing values to bunch up
in "popular" buckets and "unpopular" buckets going empty.

- discuss hash() and hashlib: md5() sha1() sha256()

Let's add a better hash function and some error checking:

```
from typing import Any, List, Tuple, Optional

class MyDict:
    def __init__(self, capacity: int = 16) -> None:
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        self._buckets: List[List[Tuple[str, Any]]] = [[] for _ in range(capacity)]

    def _index(self, key: str) -> int:
        if not isinstance(key, str):
            raise TypeError("key must be a string")
        return hash(key) % len(self._buckets)

    def set(self, key: str, value: Any) -> None:
        i = self._index(key)
        bucket = self._buckets[i]
        for idx, (k, _) in enumerate(bucket):
            if k == key:
                bucket[idx] = (key, value)  # update
                return
        bucket.append((key, value))        # insert

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        i = self._index(key)
        for k, v in self._buckets[i]:
            if k == key:
                return v
        return default
```

The last thing to add would be automatically increasing the size of the list
when it gets crowded.

