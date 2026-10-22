#!/usr/bin/env python3
"""Basic caching system."""

BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    """A basic caching system without a size limit."""

    def put(self, key, item):
        """Store an item in the cache."""
        if key is None or item is None:
            return
        self.cache_data[key] = item

    def get(self, key):
        """Retrieve an item from the cache."""
        if key is None:
            return None
        return self.cache_data.get(key)
