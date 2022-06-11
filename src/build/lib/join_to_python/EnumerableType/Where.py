from ..Types.ArgumentCountException import *
from ..Types.Exceptions import *

class Where:
    """
    where: Filters a sequence of values based on a predicate.
    Optionally, the filter function can receive the index as a second argument

    >>> Enumerable<T> where<T>((Predicate<T> | Predicate<T, int>) filterFunction);
    """
    def where(self, filterFunction):
        if not filterFunction:
            raise ArgumentNullException("Required argument is None")

        def _where(data):
            index = 0
            for item in data:
                try:
                    checkArgumentCount(filterFunction, 2)
                    if filterFunction(item, index):
                        yield item
                except ArgumentCountException:
                    if filterFunction(item):
                        yield item
                index += 1

        return self._extend(_where)
