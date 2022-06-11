from ..Generators.ExhaustIterable import drain
from ..Types.Exceptions import *

class SkipLast:
    """
    skipLast: Returns a new enumerable collection that contains the elements from source with the last count elements of the source collection omitted

    >>> Enumerable<T> skipLast<T>(int count);
    """
    def skipLast(self, count):
        # This is another one which is technically deferred execution, but there's no way to skip the last n items
        # if you don't count the list.
        def _skipLast(data):
            nonlocal count
            if count <= 0:
                toReturn = data
            else:
                toReturn = drain(data)[0:count*-1]
            yield from toReturn
        return self._extend(_skipLast)
