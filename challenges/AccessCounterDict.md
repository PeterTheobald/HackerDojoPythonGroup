DESIGN SPEC:

Write a class AccessCounterDict that extends dict to count accesses to keys.
It should count accesses in the form of `dict[key]` and `dict.get(key, default)`.
It should provide a method to get the access counts for each key.
It should also provide a method to reset the access counts.

Purpose:
Some reasons one would want to count accesses:
- To periodically delete items that are never used
- To provide stats on the most used items

---

Does `dict[key]` and `dict.get(key, default)` that cover everything we need to count accesses?
We check `dir(dict)` to see what other methods we might want to override.
dict has a lot of methods! They are implemented in C for efficiency and directly access the dict's keys and values.
We may need to implement all of these to accurately count access.

Here are other ways someone might access a dictionary that we should consider:

Should the initial creation of a key-value pair count as an access? eg: dict[key] = value

Other ways to access individual keys or values: (these do NOT call get() or __getitem__())
- Using `in` to check for key existence: `if key in dict` (uses `dict.__contains__()`)
      Should accessing a key without getting the value count as an access?
- Using `setdefault()` method: `dict.setdefault(key, default)` (returns value, inserts if not present)
      Should an insert count as an access if the key wasn't present originally?
- Using `pop()` method: `dict.pop(key, default)` (removes key and returns value, or default if not found)
- Using `setdefault()` method: `dict.setdefault(key, default)` (returns value, inserts if not present)
      Should it count as an access if the key wasn't present originally?
- Using `popitem()` method: `dict.popitem()` (removes and returns an arbitrary (key, value) pair)
      Should accessing a key without specifying which key count as an access?

Ways to bulk access all keys or values:
        Should bulk accesses count as accesses?
- Using `keys()`: (returns a view of keys)
- Using `values()`: (returns a view of values)
- Using `items()`: (returns a view of (key, value) pairs)
    - Using `dict(other-dict)` creates a new dictionary from another, uses `dict.items()`
    - Using `dict.copy()` creates a shallow copy of the dictionary, uses `dict.items()`
    - Using `copy.deepcopy(dict)` creates a deep copy of the dictionary, uses `dict.items()`
    - Using `dict1 | dict2` or `dict1 & dict2` creates a union or intersection dict, uses `dict.items()`
- Iterating over the dictionary: `for key in dict` (`uses dict.iter()`)
    - Using `list(dict)` (calls `dict.iter()` to create a list of keys)
- Using `update()` method: `dict.update(other_dict)` (accesses keys from otherdict)
- Using `dict1 == dict2` it uses `__eq__` to compare the dicts, also ` > < != >= <= ` which use `__gt__() __lt__() __ne__() __ge__() __le__()`

Should key deletion remove the count for that key?
- using `del` `pop` `popitem` `clear`

---

How do we know we handled everything correctly?
We need tests!
Write a bunch of pytest tests that try different variations of access dicts, then checking that the resulting access counters are what you expect them to be!

That way any time you update your code, you just run `pytest` and you know if you broke anything.

---

Wouldn't it be nice if all of those dict methods internally used `__getitem__()` to access the item instead of accessing it directly, so we could add our custom code in one place and everything works?

The library collections has a class UserDict that does this and is made specifically for writing custom dictionary classes.
