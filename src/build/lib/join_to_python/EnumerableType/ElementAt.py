from ..Types.Exceptions import *

class ElementAt:
    """
    elementAt: Returns the element at a specified index in a sequence

    >>> T elementAt<T>(int index);
    """
    def elementAt(self, index):
        i = 0
        for item in self:
            if i == index:
                return item
            i += 1
        raise OutOfRangeException("Index out of range")
