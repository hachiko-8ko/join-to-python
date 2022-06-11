from ..Types.EqualityComparer import *
from ..Types.Exceptions import *

class SequenceEqual:
    """
    sequenceEqual: Determines whether two sequences are equal by comparing their elements.
    an optional equality comparer can be supplied

    >>> bool sequenceEqual<T>(Iterable<T> second, IEqualityComparer<T>? comparer = None);
    >>> IEqualityComparer<T> = (Predicate<T, T> | { equals: Predicate<T, T> });
    """
    def sequenceEqual(self, second, comparer = None):
        if second is None:
            raise ArgumentNullException("Required argument is None")

        compare = extractEqualityComparer(comparer)

        iter1 = iter(self)
        iter2 = iter(second)

        done1 = False
        done2 = False

        while True:
            try:
                val1 = next(iter1)
            except StopIteration:
                done1 = True
            try:
                val2 = next(iter2)
            except StopIteration:
                done2 = True

            if done1 != done2:
                return False # not the same length

            if done1: # both are True, iterator is done
                break

            if compare:
                if not compare(val1, val2):
                    return False # not the same value
            else:
                if val1 != val2:
                    return False # not the same value

        # same length and both items have same values
        return True
