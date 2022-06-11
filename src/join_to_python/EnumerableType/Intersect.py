from ..Types.EqualityComparer import *
from ..Types.Exceptions import *

class Intersect:
    """
    intersect: Returns distinct elements from a sequence by using an optional equality comparer to compare values

    >>> Enumerable<T> intersect<T>(Iterable<T> second, IEqualityComparer<T>? comparer = None);
    >>> IEqualityComparer<T> = (Predicate<T, T> | { equals: Predicate<T, T> });
    """
    def intersect(self, second, comparer = None):
        if second is None:
            raise ArgumentNullException("Required argument is None")

        compare = extractEqualityComparer(comparer)

        def _intersect(data):
            secondSet = set()
            for item in second:
                secondSet.add(item)

            # No way around this, but we need to keep a history of every item returned. Both the first and second lists.
            history = set()
            for item in data:
                if compare:
                    found = False
                    for innerItem in secondSet:
                        if compare(item, innerItem):
                            # It's in both sets...
                            found = True
                            break
                    if found:
                        for innerItem in history:
                            if compare(item, innerItem):
                                # But if it's been sent already, don't send it again.
                                found = False
                                break
                    # If found, track and send it
                    if found:
                        history.add(item)
                        yield item
                else:
                    if item in secondSet and item not in history:
                        history.add(item)
                        yield item

        return self._extend(_intersect)
