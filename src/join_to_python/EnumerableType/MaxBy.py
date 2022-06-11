from ..Types.Comparer import *
from ..Types.Exceptions import *

class MaxBy:
    """
    maxBy: Returns the maximum value in a sequence using a key selector function.
    Takes an optional comparer, a function that takes two inputs and returns 1 if the first is higher, -1 is the second is higher, else 0.

    The difference between MaxBy and Max with a transformation function is that Max returns the output of the transformation while MaxBy
    returns the original value. This same result could be achieved with Max and a well-designed comparer function, of course.

    >>> T maxBy<T, TKey>(Func<T, TKey> keySelector, IComparer<TKey>? comparer = None);
    >>> IComparer<T> = (Func<T, T, 0 | 1 | -1> | { compare: Func<T, T, 0 | 1 | -1> });
    """
    def maxBy(self, keySelector, comparer = None):
        if not keySelector:
            raise ArgumentNullException("Required argument is None")

        compare = extractComparer(comparer)

        first = False
        for item in self:
            key = keySelector(item)
            if not first:
                maxkey = key
                maxvalue = item
                first = True
            elif compare:
                if compare(key, maxkey) > 0:
                    maxkey = key
                    maxvalue = item
            else:
                if key > maxkey:
                    maxkey = key
                    maxvalue = item

        if not first:
            raise EmptySequenceException("Sequence contains no elements")

        return maxvalue
