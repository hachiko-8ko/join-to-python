from ..Types.EqualityComparer import *
from ..Types.Exceptions import *

class Except:
    """
    except_: Produces the set difference (distinct) of two sequences.
    optional equality comparer can be used to compare values
    "Except" is already defined in python so JOIN had to add an underscore after the end. Limitation of the language.

    >>> Enumerable<T> except_<T>(Iterable<T> second, IEqualityComparer<T>? comparer = None);
    >>> IEqualityComparer<T> = (Predicate<T, T> | { equals: Predicate<T, T> });
    """
    def except_(self, second, comparer = None):
        if second is None:
            raise ArgumentNullException("Requried argument is None")

        compare = extractEqualityComparer(comparer)

        def _except(data):
            # No way around this, but we need to keep a history of every item returned. Both the first and second lists.
            # And the second might also be a generator, so we need to exhaust its values.

            # Start by loading the history with the second set. Then, we can do what we already did for distinct() and it'll pull out the matches

            history = set()
            for item in second:
                history.add(item)

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

        return self._extend(_except)
