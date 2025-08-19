"""
This module provides AccessCounterDict, a dictionary subclass that counts accesses to each key.
"""

class AccessCounterDict(dict):
    """
    A dictionary subclass that counts the number of accesses to each key.
    Accesses are counted for __getitem__ and get().
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the AccessCounterDict.
        Accepts all arguments that a standard dict does.
        """
        super().__init__(*args, **kwargs)
        self._access_counts = {}

    def __getitem__(self, key):
        """
        Retrieve the value for the given key and increment its access count if the key exists.
        Handles accesses in the form `dict[key]`.
        """
        if key in self:
            self._access_counts[key] = self._access_counts.get(key, 0) + 1
        return super().__getitem__(key)

    def get(self, key, default=None):
        """
        Retrieve the value for the given key (or default if not found) and increment its access count if the key exists.
        Handles accesses in the form `dict.get(key, default)`.
        """
        if key in self:
            self._access_counts[key] = self._access_counts.get(key, 0) + 1
        return super().get(key, default)

    def get_access_counts(self):
        """
        Return a dictionary mapping each key to its access count.
        """
        return dict(self._access_counts) # return copy to protect internal state from user modifications
    
    def reset_access_counts(self):
        """
        Reset all access counts to zero.
        """
        self._access_counts.clear()

# A demonstration if this module is run directly instead of imported:
def main():
    # Create an AccessCounterDict and populate it
    acd = AccessCounterDict({'a': 1, 'b': 2, 'c': 3})

    # Access keys using bracket notation
    print("acd['a']:", acd['a'])
    print("acd['b']:", acd['b'])

    # Access key using get()
    print("acd.get('a'):", acd.get('a'))
    print("acd.get('c'):", acd.get('c'))
    print("acd.get('d', 0):", acd.get('d', 0))  # Non-existent key

    # Show access counts
    print("Access counts:", acd.get_access_counts())

    # Reset access counts
    acd.reset_access_counts()
    print("Access counts after reset:", acd.get_access_counts())

if __name__ == "__main__":
    main()