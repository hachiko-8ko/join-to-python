from ..Types.Exceptions import *

class ElementAtOrDefault:
    """
    elementAtOrDefault: Returns the element at a specified index in a sequence.
    Returns an optional default value if index is out of range, or None if not supplied.

    (Note that in Python, unlike C#, there's no way to know what type a sequence is supposed to have.)

    >>> T? elementAtOrDefault<T>(int index, T? defaultValue = None);
    """
    def elementAtOrDefault(self, index, defaultValue = None):
        i = 0
        for item in self:
            if i == index:
                return item
            i += 1
        return defaultValue
