from ..Types.Exceptions import *

class Append:
    """
    append: Appends a value to the end of the sequence

    >>> Enumerable<T> append<T>(T newItem);
    """
    def append(self, newItem):
        def _append(data):
            yield from data
            yield newItem

        return self._extend(_append)
