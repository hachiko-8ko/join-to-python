from ..Types.Exceptions import *

class DefaultIfEmpty:
    """
    defaultIfEmpty: returns the sequence or the (optional) default value if the sequence is empty.
    Default in is a paramter. IF it is left out, None is returned.

    (Note that in Python, unlike C#, there's no way to know what type a sequence is supposed to have, especially an empty one.)

    >>> Enumerable<T | None> defaultIfEmpty<T>(T? defaultValue = None);
    """
    def defaultIfEmpty(self, defaultValue = None):
        def _defaultIfEmpty(data):
            empty = True
            for item in data:
                empty = False
                yield item
            if empty:
                yield defaultValue

        return self._extend(_defaultIfEmpty)
