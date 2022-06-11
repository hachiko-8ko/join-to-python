from ..Types.Exceptions import *

class Sum:
    """
    sum: Computes the sum of the sequence of values that are obtained by invoking an optional transform function on each element of the sequence

    >>> numeric sum<T>(Func<T, numeric>? outputFunction = None);
    >>> numeric = int | float | complex;
    """
    def sum_(self, outputFunction = None):
        sumval = 0
        for item in self:
            if outputFunction:
                valueToAdd = outputFunction(item)
                # Don't try to misuse the function by passing an object that implemented _radd_(). Not cool, dude.
                if not isinstance(valueToAdd, (int, float, complex)):
                    raise DataTypeException("Sequence contains invalid number after transformation")
                sumval += valueToAdd
            else:
                if not isinstance(item, (int, float, complex)):
                    raise DataTypeException("Sequence contains invalid number")
                sumval += item

        return sumval

    def sum(self, outputFunction = None):
        return self.sum_(outputFunction);
