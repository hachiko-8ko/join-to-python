from ..Types.EqualityComparer import *
from ..Types.Exceptions import *

class IntersectBy:
    """
    intersectBy: Produces the set intersection of two sequences based on keys returned by a key selector function.
    optional equality comparer can be provided

    >>> Enumerable<T> intersectBy<T, TKey>(Iterable<T> second, Func<T, TKey> keySelector, IEqualityComparer<TKey>? comparer = None);
    >>> IEqualityComparer<T> = (Predicate<T, T> | { equals: Predicate<T, T> });
    """
    def intersectBy(self, second, keySelector, comparer = None):
        if second is None:
            raise ArgumentNullException("Required argument is None")
        if not keySelector:
            raise ArgumentNullException("Required argument is None")

        compare = extractEqualityComparer(comparer)

        def _intersectBy(data):
            secondSet = set()
            for item in second:
                key = keySelector(item)
                secondSet.add(key)

            # No way around this, but we need to keep a history of every item returned. Both the first and second lists.
            history = set()
            for item in data:
                key = keySelector(item)
                if compare:
                    found = False
                    for innerItem in secondSet:
                        if compare(key, innerItem):
                            # It's in both sets...
                            found = True
                            break
                    if found:
                        for innerItem in history:
                            if compare(key, innerItem):
                                # But if it's been sent already, don't send it again.
                                found = False
                                break
                    # If found, track and send it
                    if found:
                        history.add(key)
                        yield item
                else:
                    if key in secondSet and key not in history:
                        history.add(key)
                        yield item

        return self._extend(_intersectBy)
