from ..Types.EqualityComparer import *
from ..Types.Exceptions import *

class Distinct:
    """
    distinct: Returns distinct elements from a sequence by using an optional equality comparer to compare values

    >>> Enumerable<T> distinct<T>(IEqualityComparer<T>? comparer = None);
    >>> IEqualityComparer<T> = (Predicate<T, T> | { equals: Predicate<T, T> });
    """
    def distinct(self, comparer = None):
        compare = extractEqualityComparer(comparer)

        def _distinct(data):
            # Keep a history of every item returned (no way around that) and only return if not in the list.
            history = set()
            for item in data:
                if compare:
                    found = False
                    for innerItem in history:
                        if compare(item, innerItem):
                            found = True
                            break
                    if not found:
                        history.add(item)
                        yield item
                else:
                    if item not in history:
                        history.add(item)
                        yield item

        return self._extend(_distinct)
