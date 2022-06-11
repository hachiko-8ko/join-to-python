from ..Types.EqualityComparer import *
from ..Types.Exceptions import *

class Contains:
    """
    contains: determines whether a sequence contains a specified element
    optional equalityComparer function to indicate if record matches

    >>> bool contains<T>(T value, IEqualityComparer<T>? comparer = None);
    >>> IEqualityComparer<T> = (Predicate<T, T> | { equals: Predicate<T, T> });
    """
    def contains(self, value, comparer = None):
        compare = extractEqualityComparer(comparer)
        for item in self:
            if not compare:
                if item == value:
                    return True
            else:
                if compare(item, value):
                    return True

        return False
