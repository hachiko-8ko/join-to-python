from ..Types.ArgumentCountException import *
from ..Types.Exceptions import *

class TakeWhile:
    """
    takeWhile: Returns elements from a sequence as long as a specified condition is true.
    Optionally, the filter function can receive the index as a second argument

    >>> Enumerable<T> takeWhile<T>((IPredicate<T> | IPredicate<T, int>) filterFunction);
    """
    def takeWhile(self, filterFunction):
        if not filterFunction:
            raise ArgumentNullException("Required argument is None")

        def _takeWhile(data):
            index = 0
            triggered = False
            for item in data:
                # Whenever the filter goes false, triggered needs to go true, and it has to be sticky
                try :
                    checkArgumentCount(filterFunction, 2)
                    triggered = triggered or not filterFunction(item, index)
                except ArgumentCountException:
                    triggered = triggered or not filterFunction(item)
                index += 1
                if not triggered:
                    yield item

        return self._extend(_takeWhile)
