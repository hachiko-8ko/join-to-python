from ..Types.Comparer import *
from ..Types.Exceptions import *

class Max:
    """
    max: Returns the maximum value in a sequence.
    Takes an optional transformation function. If supplied, this transformation is applied to all values and the max result returned.

    Takes an optional comparer, a function that takes two inputs and returns 1 if the first is higher, -1 is the second is higher, else 0.
    >>> (T | TResult) max<T, TResult>(Func<T, TResult>? outputFunction = None, IComparer<TResult>? comparer = None);
    >>> IComparer<T> = (Func<T, T, 0 | 1 | -1> | { compare: Func<T, T, 0 | 1 | -1> });
    """
    def max_(self, outputFunction = None, comparer = None):
        compare = extractComparer(comparer)
        if not outputFunction:
            outputFunction = lambda x: x # passthrough

        first = False
        for item in self:
            current = outputFunction(item)
            if not first:
                maxval = current
                first = True
            elif compare:
                if compare(current, maxval) > 0:
                    maxval = current
            else:
                if current > maxval:
                    maxval = current

        if not first:
            raise EmptySequenceException("Sequence contains no elements")

        return maxval

    def max(self, outputFunction = None, comparer = None):
        return self.max_(outputFunction, comparer)
