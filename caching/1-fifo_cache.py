#!/usr/bin/env python3
"""FIFO caching system."""

BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    """A caching system that discards the oldest item first."""

    def __init__(self):
        """Initialize the cache and FIFO order."""
        super().__init__()
        self.queue = []

    def put(self, key, item):
        """Add an item and discard the oldest if the cache is full."""
        if key is None or item is None:
            return

        if key not in self.cache_data:
            self.queue.append(key)

        self.cache_data[key] = item

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            discarded = self.queue.pop(0)
            del self.cache_data[discarded]
            print("DISCARD: {}".format(discarded))

    def get(self, key):
        """Return the value for a key, or None if missing."""
        if key is None:
            return None
        return self.cache_data.get(key)
