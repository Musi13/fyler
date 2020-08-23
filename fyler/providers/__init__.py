import pkg_resources
from functools import lru_cache

@lru_cache
def all_providers():
    return {
        k.name: k.load()() for k in
        pkg_resources.iter_entry_points('fyler.providers')
    }
