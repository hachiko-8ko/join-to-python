from ..Types.Comparer import *
from ..Types.Exceptions import *

class MinOrDefault:
    """
    minOrDefault: Returns the minimum value in a sequence.
    Takes an optional transformation function. If supplied, this transformation is applied to all values and the min result returned.

    If sequence is empty, returns the default value or None. This is a JOIN-specific method. There is no equivalent in C#.

    Takes an optional comparer, a function that takes two inputs and returns 1 if the first is higher, -1 is the second is higher, else 0.
    >>> (T | TResult)? minOrDefault<T, TResult>(Func<T, TResult>? outputFunction = None, IComparer<TResult>? comparer = None, TResult? defaultValue = None);
    >>> IComparer<T> = (Func<T, T, 0 | 1 | -1> | { compare: Func<T, T, 0 | 1 | -1> });
    """
    def minOrDefault(self, outputFunction = None, comparer = None, defaultValue = None):
        compare = extractComparer(comparer)
        if not outputFunction:
            outputFunction = lambda x: x # passthrough

        first = False
        for item in self:
            current = outputFunction(item)
            if not first:
                minval = current
                first = True
            elif compare:
                if compare(current, minval) < 0:
                    minval = current
            else:
                if current < maxval:
                    minval = current

        if not first:
            return defaultValue

        return minval
