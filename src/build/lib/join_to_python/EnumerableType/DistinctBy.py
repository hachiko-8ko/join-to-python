from ..Types.EqualityComparer import *
from ..Types.Exceptions import *

class DistinctBy:
    """
    distinctBy: Returns distinct elements from a sequence based on keys returned by a key selector function.
    optional equality comparer can be supplied to compare values

    >>> Enumerable<T> distinctBy<T, TKey>(Func<T, TKey> keySelector, IEqualityComparer<TKey>? comparer = None);
    >>> IEqualityComparer<T> = (Predicate<T, T> | { equals: Predicate<T, T> });
    """
    def distinctBy(self, keySelector, comparer = None):
        if not keySelector:
            raise ArgumentNullException("Required argument is None")

        compare = extractEqualityComparer(comparer)

        def _distinctBy(data):
            # Keep a history of every item returned (no way around that) and only return if not in the list.
            history = set()
            for item in data:
                key = keySelector(item)
                if compare:
                    found = False
                    for innerItem in history:
                        if compare(key, innerItem):
                            found = True
                            break
                    if not found:
                        history.add(key)
                        yield item
                else:
                    if key not in history:
                        history.add(key)
                        yield item

        return self._extend(_distinctBy)
