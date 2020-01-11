from collections import defaultdict
import weakref

__all__ = ["PolyMap", "DefaultPolyMap"]


class _PolyMap:
    """Base class for PolyMaps."""

    def __setitem__(self, key, value):
        """Set an item and assign it to one or more groups."""
        if isinstance(key, tuple):
            key, *tags = key
            for tag in tags:
                self._groups[tag].add(key)
        super().__setitem__(key, value)

    def __delitem__(self, key):
        """Delete an item from the dict and all groups."""
        for group in self._groups:
            if key in group:
                del group[key]
        super().__delitem__(key)

    def update(self, other):
        """Update with the items (including groups) of another mapping."""
        super().update(other)
        if isinstance(other, _PolyMap):
            for group, keys in other._groups.items():
                self._groups[group].update(keys)

    def items(self, group=None):
        """Iterate over items, optionaly filtering by group."""
        if group is None:
            return super().items()
        return ((k, self[k]) for k in self._groups[group])

    def keys(self, group=None):
        """Iterate over keys, optionaly filtering by group."""
        if group is None:
            return super().keys()
        return iter(self._groups[group])

    def values(self, group=None):
        """Iterate over values, optionaly filtering by group."""
        if group is None:
            return super().values()
        return (self[k] for k in self._groups[group])

    def groups(self, key=None):
        """Iterate over available group keys, optionally filtering by key."""
        keys = self._groups.keys()
        if key is None:
            return keys
        return (k for k in keys if key in self._groups[k])

    def grouped(self):
        """Iterate over the stored items per group."""
        for group, keys in self._groups.items():
            yield (group, ((k, self[k]) for k in keys))

    def clear(self, group=None):
        """Remove all items, optionally filtered by group."""
        if group is None:
            return super().clear()
        for key in self.keys(group):
            del self[key]
        del self._groups[group]

    def copy(self, group=None):
        """Return a shallow copy, optionally filtered by group."""
        if group is None:
            return self.__class__(self)
        return self.__class__(self.items(group))


class PolyMap(_PolyMap, dict):
    """A mapping type whose items can be grouped."""

    def __new__(cls, value=None, **kwargs):
        poly = dict.__new__(cls, value, **kwargs)
        poly._groups = defaultdict(set)
        return poly


class DefaultPolyMap(_PolyMap, defaultdict):
    """A defaultdict-based version of PolyMap."""

    def __new__(cls, default_factory=None, value=None, **kwargs):
        poly = defaultdict.__new__(cls, default_factory, value, **kwargs)
        poly._groups = defaultdict(set)
        return poly
