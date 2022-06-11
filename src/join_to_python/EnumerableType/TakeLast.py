from ..Generators.ExhaustIterable import drain
from ..Types.Exceptions import *

class TakeLast:
    """
    takeLast: Returns a new enumerable collection that contains the last "count" elements from source

    >>> Enumerable<T> takeLast<T>(int count);
    """
    def takeLast(self, count):
        # This is another one which is technically deferred execution, but there's no way to take the last n items
        # if you don't count the list.
        def _takeLast(data):
            if count <= 0:
                return
            yield from drain(data)[-1 * count:]

        return self._extend(_takeLast)
