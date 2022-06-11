from ..Types.Exceptions import *

class Skip:
    """
    skip: Bypasses a specified number of elements in a sequence and then returns the remaining elements

    >>> Enumerable<T> skip<T>(int count);
    """
    def skip(self, count):
        def _skip(data):
            nonlocal count
            for item in data:
                if count <= 0:
                    yield item
                count -= 1
        return self._extend(_skip)
