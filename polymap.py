from collections import defaultdict
from typing import Iterable

__all__ = ["PolyMap", "DefaultPolyMap"]


class _PolyMap:
    """Base class for PolyMaps."""

    # General object methods

    def __eq__(self, other) -> bool:
        """Compare two polymaps."""
        try:
            return super().__eq__(other) and self._groups == other._groups
        except AttributeError:
            return False

    # Common mapping methods

    def __setitem__(self, key, value) -> None:
        """Set an item and assign it to one or more groups."""
        if isinstance(key, tuple):
            key, *tags = key
            for tag in tags:
                self._groups[tag].add(key)
        super().__setitem__(key, value)

    def __delitem__(self, key) -> None:
        """Delete an item from the map and all groups."""
        self.ungroup(key)
        super().__delitem__(key)

    def update(self, other) -> None:
        """Update with the items (including groups) of another mapping."""
        super().update(other)
        if isinstance(other, _PolyMap):
            for group, keys in other._groups.items():
                self._groups[group].update(keys)

    def items(self, group=None) -> Iterable:
        """Iterate over items, optionaly filtering by group."""
        if group is None:
            return super().items()
        return ((k, self[k]) for k in self._groups[group])

    def keys(self, group=None) -> Iterable:
        """Iterate over keys, optionaly filtering by group."""
        if group is None:
            return super().keys()
        return iter(self._groups[group])

    def values(self, group=None):
        """Iterate over values, optionaly filtering by group."""
        if group is None:
            return super().values()
        return (self[k] for k in self._groups[group])

    def clear(self, group=None):
        """Remove all items, optionally filtered by group."""
        if group is None:
            return super().clear()
        keys = list(self.keys(group))
        for key in keys:
            del self[key]
        del self._groups[group]

    def copy(self, group=None):
        """Return a shallow copy, optionally filtered by group."""
        if group is None:
            return self.__class__(self)
        return self.__class__(self.items(group))

    def pop(self, key, default=None):
        """Pop key from the mapping with optional default."""
        self.ungroup(key)
        return super().pop(key, default)

    def popitem(self):
        """Remove and pop and return a (key, value) pair."""
        key, value = super().popitem()
        self.ungroup(key)
        return key, value

    def setdefault(self, key, default=None, group=None):
        """Return value if key exists, else insert and return default."""
        if group is not None:
            self._groups[group].add(key)
        return super().setdefault(key, default)

    # Unique PolyMap methods

    def groups(self, key=None):
        """Iterate over non-empty group keys, optionally filtering by key."""
        keys = self._groups.keys()
        if key is None:
            return (k for k in keys if self._groups[k])
        return (k for k in keys if key in self._groups[k])

    def grouped(self):
        """Iterate over the stored items per non-empty group."""
        for group, keys in self._groups.items():
            if keys:
                yield (group, ((k, self[k]) for k in keys))

    def group(self, key, *groups, replace=True):
        """Assign a key to one or more groups."""
        if not groups:
            raise ValueError("At least one group is required.")
        if key not in self:
            raise KeyError
        if replace:
            self.ungroup(key)
        for group in groups:
            self._groups[group].add(key)

    def ungroup(self, key, group=None):
        """Remove key from a group, or from all groups (default)."""
        for group in self.groups(key) if group is None else (group, ):
            self._groups[group].remove(key)


class PolyMap(_PolyMap, dict):
    """A mapping type whose items can be grouped."""

    def __new__(cls, value=None, **kwargs):
        poly = dict.__new__(cls, value, **kwargs)
        poly._groups = defaultdict(set)
        if isinstance(value, _PolyMap):
            poly._groups.update(value._groups)
        return poly


class DefaultPolyMap(_PolyMap, defaultdict):
    """A defaultdict-based version of PolyMap."""

    def __new__(cls, default_factory=None, value=None, **kwargs):
        poly = defaultdict.__new__(cls, default_factory, value, **kwargs)
        poly._groups = defaultdict(set)
        if isinstance(value, _PolyMap):
            poly._groups.update(value._groups)
        return poly
