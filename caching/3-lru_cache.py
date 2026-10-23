#!/usr/bin/env python3
"""LRU caching system."""

BaseCaching = __import__('base_caching').BaseCaching


class LRUCache(BaseCaching):
    """A caching system that discards the least recently used item."""

    def __init__(self):
        """Initialize the cache and usage order."""
        super().__init__()
        self.order = []

    def put(self, key, item):
        """Add an item and discard the least recently used if necessary."""
        if key is None or item is None:
            return

        # Move this key to the most-recently-used position.
        if key in self.order:
            self.order.remove(key)

        self.cache_data[key] = item
        self.order.append(key)

        # Remove the least recently used item if over capacity.
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            discarded = self.order.pop(0)
            del self.cache_data[discarded]
            print("DISCARD: {}".format(discarded))

    def get(self, key):
        """Return an item and mark it as recently used."""
        if key is None or key not in self.cache_data:
            return None

        self.order.remove(key)
        self.order.append(key)
        return self.cache_data[key]
