from ..Types.Exceptions import *

class Prepend:
    """
    prepend: Appends a value to the start of the sequence

    >>> Enumerable<T> prepend<T>(T newItem);
    """
    def prepend(self, newItem):
        def _prepend(data):
            yield newItem
            yield from data

        return self._extend(_prepend)
