from ..Types.Exceptions import *

class Average:
    """
    average: computes the average of a sequence of numbers.
    optional transform function lets us calculate using values obtained by invoking afunction on each element of the sequence.
    if numbers can be None, then the None values are skipped

    >>> numeric? average<T>(Func<T, numeric>? outputFunction = None);
    >>> numeric = int | float | complex;
    """
    def average(self, outputFunction = None):
        sumval = 0
        count = 0
        containsNull = False
        for item in self:
            tmp = 0
            if outputFunction:
                tmp = outputFunction(item)
            else:
                tmp = item

            # Nullable number behaviour: if null, skip it
            if tmp is None:
                containsNull = True
                continue

            # Don't try to misuse the function by passing an object that implemented _radd_(). Not cool, dude.
            if not isinstance(tmp, (int, float, complex)):
                raise DataTypeException("Invalid data type for average")

            sumval += tmp
            count += 1

        if count == 0:
            # In the C# version, if the sequence is all null, this returns null instead of throwing
            if containsNull:
                return None
            raise EmptySequenceException("Sequence contains no elements")

        return sumval / count
