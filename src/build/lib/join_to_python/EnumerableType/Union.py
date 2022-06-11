from ..Types.EqualityComparer import *
from ..Types.Exceptions import *

class Union:
    """
    union: concatenates two sequences returning the set sequence.
    optional equality comparer can be supplied to compare values

    >>> Enumerable<T> union<T>(Iterable<T> second, IEqualityComparer<T>? comparer = None);
    >>> IEqualityComparer<T> = (Predicate<T, T> | { equals: Predicate<T, T> });
    """
    def union(self, second, comparer = None):
        if second is None:
            raise ArgumentNullException("Required argument is None")

        compare = extractEqualityComparer(comparer)

        def _union(data):
            # No way around this, but we need to keep a history of every item returned. Both the first and second lists.
            history = set()
            for item in data:
                if compare:
                    found = False
                    for innerItem in history:
                        if compare(innerItem, item):
                            found = True
                            break
                    if not found:
                        history.add(item)
                        yield item
                else:
                    if item not in history:
                        history.add(item)
                        yield item
            # a little bit of copypasta here but it's not worth making a sub-function for a single occurrence
            for item in second:
                if compare:
                    found = False
                    for innerItem in history:
                        if compare(innerItem, item):
                            found = True
                            break
                    if not found:
                        history.add(item)
                        yield item
                else:
                    if item not in history:
                        history.add(item)
                        yield item

        return self._extend(_union)
