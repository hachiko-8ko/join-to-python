from ..Types.ArgumentCountException import *
from ..Types.Exceptions import *

class Any:
    """
    any: Determines whether any elements of a sequence satisfy an optional condition
    This condition can optionally take the index as the second argument (this is not provided by the C# version)

    >>> bool any<T>(Predicate<T, T> | Predicate<T, T, int>)? filterFunction = None);
    """
    def any_(self, filterFunction = None):
        index = 0
        for item in self:
            if not filterFunction:
                return True

            try:
                checkArgumentCount(filterFunction, 2)
                if filterFunction(item, index):
                    return True
            except ArgumentCountException:
                if filterFunction(item):
                    return True
            index += 1

        return False

    def any(self, filterFunction = None):
        return self.any_(filterFunction)
