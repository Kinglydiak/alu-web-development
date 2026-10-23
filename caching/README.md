# Caching

Python caching system assignments.

## Basic dictionary cache

BasicCache inherits from BaseCaching and stores key-value pairs
in cache_data without a maximum size. The put method ignores
None keys and items. The get method returns None for missing keys.
