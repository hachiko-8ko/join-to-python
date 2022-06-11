from ..Types.ArgumentCountException import *
from ..Types.Exceptions import *

class SkipWhile:
    """
    skipWhile: Bypasses elements in a sequence as long as a specified condition is true and then returns the remaining elements.
    optionally, the filter function can receive the index as a second argument

    >>> Enumerable<T> skip<T>((Predicate<T>, Predicate<T, int>) filterFunction);
    """
    def skipWhile(self, filterFunction):
        if not filterFunction:
            raise ArgumentNullException("Required argument is None")

        def _skipWhile(data):
            index = 0
            triggered = False
            for item in data:
                # Whenever the filter goes false, triggered needs to go true, and it has to be sticky
                try:
                    checkArgumentCount(filterFunction, 2)
                    triggered = triggered or not filterFunction(item, index)
                except ArgumentCountException:
                    triggered = triggered or not filterFunction(item)
                index += 1
                if triggered:
                    yield item

        return self._extend(_skipWhile)
