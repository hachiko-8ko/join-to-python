from ..Types.Comparer import *
from ..Types.Exceptions import *

class MaxOrDefault:
    """
    maxOrDefault: Returns the maximum value in a sequence.
    Takes an optional transformation function. If supplied, this transformation is applied to all values and the max result returned.

    If sequence is empty, returns the default value or None. This is a JOIN-specific method. There is no equivalent in C#.

    Takes an optional comparer, a function that takes two inputs and returns 1 if the first is higher, -1 is the second is higher, else 0.
    >>> (T | TResult)? maxOrDefault<T, TResult>(Func<T, TResult>? outputFunction = None, IComparer<TResult>? comparer = None, TResult? defaultValue = None);
    >>> IComparer<T> = (Func<T, T, 0 | 1 | -1> | { compare: Func<T, T, 0 | 1 | -1> });
    """
    def maxOrDefault(self, outputFunction = None, comparer = None, defaultValue = None):
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
            return defaultValue

        return maxval
