from ..Types.EqualityComparer import *
from ..Types.Exceptions import *

class ExceptBy:
    """
    exceptBy: Produces the set difference of two sequences based on keys (distinct keys) returned by a key selector function.
    optional equality comparer can be used to compare values

    >>> Enumerable<T> exceptBy<T, TKey>(Iterable<T> second, Func<T, TKey> keySelector, IEqualityComparer<TKey>? comparer = None);
    >>> IEqualityComparer<T> = (Predicate<T, T> | { equals: Predicate<T, T> });
    """
    def exceptBy(self, second, keySelector, comparer = None):
        if second is None:
            raise ArgumentNullException("Required argument is None")

        compare = extractEqualityComparer(comparer)

        def _exceptBy(data):
            # No way around this, but we need to keep a history of every item returned. Both the first and second lists.
            # And the second might also be a generator, so we need to exhaust its values.

            # Start by loading the history with the second set. Then, we can do what we already did for distinct() and it'll pull out the matches

            history = set()
            for item in second:
                key = keySelector(item)
                history.add(key)

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

        return self._extend(_exceptBy)
