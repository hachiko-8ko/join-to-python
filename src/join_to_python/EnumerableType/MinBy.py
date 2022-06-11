from ..Types.Comparer import *
from ..Types.Exceptions import *

class MinBy:
    """
    minBy: Returns the minimum value in a sequence using a key selector function.
    Takes an optional comparer, a function that takes two inputs and returns 1 if the first is higher, -1 is the second is higher, else 0.

    The difference between MinBy and Min with a transformation function is that Min returns the output of the transformation while MinBy
    returns the original value. This same result could be achieved with Min and a well-designed comparer function, of course.

    >>> T minBy<T, TKey>(Func<T, TKey> keySelector, IComparer<TKey>? comparer = None);
    >>> IComparer<T> = (Func<T, T, 0 | 1 | -1> | { compare: Func<T, T, 0 | 1 | -1> });
    """
    def minBy(self, keySelector, comparer = None):
        if not keySelector:
            raise ArgumentNullException("Required argument is None")

        compare = extractComparer(comparer)

        first = False
        for item in self:
            key = keySelector(item)
            if not first:
                minkey = key
                minvalue = item
                first = True
            elif compare:
                if compare(key, minkey) < 0:
                    minkey = key
                    minvalue = item
            else:
                if key < minkey:
                    minkey = key
                    minvalue = item

        if not first:
            raise EmptySequenceException("Sequence contains no elements")

        return minvalue
