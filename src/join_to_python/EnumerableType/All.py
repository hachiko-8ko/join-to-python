from ..Types.ArgumentCountException import *
from ..Types.Exceptions import *

class All:
    """
    all: Determines whether all elements of a sequence satisfy a condition.
    This condition can optionally take the index as the second argument (this is not provided by the C# version)

    >>> bool all<T>(Predicate<T, T> | Predicate<T, T, int>) filterFunction);
    """
    def all_(self, filterFunction):
        if not filterFunction:
            raise ArgumentNullException("Required argument is None")

        index = 0
        for item in self:
            try:
                checkArgumentCount(filterFunction, 2)
                if not filterFunction(item, index):
                    return False
            except ArgumentCountException:
                if not filterFunction(item):
                    return False
            index += 1

        return True

    def all(self, filterFunction):
        return self.all(filterFunction)
