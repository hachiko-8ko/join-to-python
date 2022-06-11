from ..Types.Exceptions import *

class Count:
    """
    count: returns a number that represents how many elements in the specified sequence satisfy an optional condition
    longCount also redirects here (the int class handles arbitrarily large numbers)

    >>> int count<T>(Predicate<T>? filterFunction = None);
    """
    def count(self, filterFunction = None):
        ctr = 0
        for item in self:
            if filterFunction:
                if filterFunction(item):
                    ctr += 1
            else:
                ctr += 1
        return ctr
