#!/usr/bin/env python3
"""LIFO caching system."""

BaseCaching = __import__('base_caching').BaseCaching


class LIFOCache(BaseCaching):
    """A caching system that discards the most recently added item."""

    def __init__(self):
        """Initialize the cache and track insertion order."""
        super().__init__()
        self.stack = []

    def put(self, key, item):
        """Add an item and discard the newest item if the cache is full."""
        if key is None or item is None:
            return

        if key not in self.cache_data:
            self.stack.append(key)

        self.cache_data[key] = item

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            discarded = self.stack.pop()
            del self.cache_data[discarded]
            print("DISCARD: {}".format(discarded))

    def get(self, key):
        """Return the value for a key, or None if the key is missing."""
        if key is None:
            return None
        return self.cache_data.get(key)
