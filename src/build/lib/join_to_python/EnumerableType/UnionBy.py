from ..Types.EqualityComparer import *
from ..Types.Exceptions import *

class UnionBy:
    """
    unionBy: concatenates two sequences returning the set sequence based on keys returned by a key selector function.
    optional equality comparer can be supplied to compare values

    >>> Enumerable<T> unionBy<T, TKey>(Iterable<T> second, Func<T, TKey> keySelector, IEqualityComparer<TKey>? comparer = None);
    >>> IEqualityComparer<TKey> = (Predicate<T, T> | { equals: Predicate<T, T> });
    """
    def unionBy(self, second, keySelector, comparer = None):
        if second is None:
            raise ArgumentNullException("Required argument is None")
        if not keySelector:
            raise ArgumentNullException("Required argument is None")

        compare = extractEqualityComparer(comparer)

        def _unionBy(data):
            # No way around this, but we need to keep a history of every item returned. Both the first and second lists.
            history = set()
            for item in data:
                key = keySelector(item)
                if compare:
                    found = False
                    for innerItem in history:
                        if compare(innerItem, key):
                            found = True
                            break
                    if not found:
                        history.add(key)
                        yield item
                else:
                    if key not in history:
                        history.add(key)
                        yield item
            # a little bit of copypasta here but it's not worth making a sub-function for a single occurrence
            for item in second:
                key = keySelector(item)
                if compare:
                    found = False
                    for innerItem in history:
                        if compare(innerItem, key):
                            found = True
                            break
                    if not found:
                        history.add(key)
                        yield item
                else:
                    if key not in history:
                        history.add(key)
                        yield item

        return self._extend(_unionBy)
