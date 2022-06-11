from ..Types.Exceptions import *

class Concat:
    """
    concat: concatenates two sequences

    >>> Enumerable<T> append<T>(Enumerable<T> second);
    """
    def concat(self, second):
        def _concat(data):
            yield from data
            yield from second

        return self._extend(_concat)
