from ..Types.Exceptions import *

class OfType:
    """
    ofType: Filters the elements of an IEnumerable based on a specified type.
    In Python this is kind of meaningless. It's just where(lambda x: instanceof(x, param))

    >>> Enumerable<R> ofType<T, R>((type | Tuple<type>) filterType);
    """
    def ofType(self, filterType):
        if not filterType:
            raise ArgumentNullException("Required argument is None")

        def _ofType(data):
            for item in data:
                if isinstance(item, filterType): # takes either a type or a tuple of types
                    yield item

        return self._extend(_ofType)
