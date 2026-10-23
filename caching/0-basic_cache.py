#!/usr/bin/env python3
"""Basic dictionary caching system."""

BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    """A basic cache with no size limit."""

    def put(self, key, item):
        """Store an item in the cache."""
        if key is None or item is None:
            return
        self.cache_data[key] = item

    def get(self, key):
        """Return a value by key, or None if the key is missing."""
        if key is None:
            return None
        return self.cache_data.get(key)
