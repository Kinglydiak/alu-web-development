#!/usr/bin/env python3
"""Base class for caching systems."""

class BaseCaching:
    """Base class for all caching systems."""

    MAX_ITEMS = 4

    def __init__(self):
        """Initialize the cache storage."""
        self.cache_data = {}

    def print_cache(self):
        """Print the current cache."""
        print("Current cache:")
        for key, value in self.cache_data.items():
            print(f"{key}: {value}")

    def get(self, key):
        """Retrieve an item from the cache."""
        raise NotImplementedError("Must be implemented in a subclass")

    def put(self, key, item):
        """Add an item to the cache."""
        raise NotImplementedError("Must be implemented in a subclass")
