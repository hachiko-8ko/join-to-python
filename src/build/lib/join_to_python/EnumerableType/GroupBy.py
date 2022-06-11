from collections import OrderedDict

from ..Types.EqualityComparer import *
from ..Types.Grouping import *
from ..Types.Exceptions import *

class GroupBy:
    """
    groupBy: Groups the elements of a sequence according to a specified key selector function and creates a result value from each group and its key.

    takes an optional element selection function
    takes an optional output projection function
    takes an optional equality comparer function

    >>> Enumerable<IGrouping<TKey, T | TElement | TOutput>> groupBy<T, TKey, TElement, TOutput>(Func<T, TKey> groupFunction,
            Func<T, TElement>? elementFunction = None,
            Func<TKey, Array<T | TElement>, TOutput>? outputFunction = None,
            IEqualityComparer<TKey>? comparer = None);
    >>> IEqualityComparer<T> = (Predicate<T, T> | { equals: Predicate<T, T> });
    >>> IGrouping<TKey, TValue> = { TKey key, TValue[] values, TValue[] __iter__() };
    """
    def groupBy(self, groupFunction, elementFunction = None, outputFunction = None, comparer = None):
        if not groupFunction:
            raise ArgumentNullException("Required argument is None")

        compare = extractEqualityComparer(comparer)

        def _groupBy(data):
            # Even though this is returning as if it's deferred execution, it's not really deferred. It has to process the full list
            # to know what times each individual key appears.

            cache = OrderedDict() # Use an ordered dict to preserve order that items appear

            for row in data:
                key = groupFunction(row)
                match = None
                if comparer:
                    for innerKey in cache.keys():
                        if comparer(innerKey, key):
                            match = cache.get(innerKey)
                            break
                else:
                    match = cache.get(key)

                if match:
                    match.add(row)
                else:
                    cache[key] = Grouping(key, row, elementFunction)

            for row in cache.items():
                if outputFunction:
                    yield outputFunction(row[0], row[1].values)
                else:
                    yield row[1]

        return self._extend(_groupBy)
