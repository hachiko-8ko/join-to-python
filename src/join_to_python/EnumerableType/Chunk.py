from ..Types.Exceptions import *

class Chunk:
    """
    chunk: splits the elements of a sequence into chunks of size at most "size"

    >>> Enumerable<T[]> chunk<T>(int size);
    """
    def chunk(self, size):
        if size < 1:
            raise OutOfRangeException("Argument out of range")

        def _chunk(data):
            counter = size
            tmp = []
            for item in data:
                tmp.append(item)
                counter -= 1
                if counter <= 0:
                    yield tmp
                    tmp = []
                    counter = size

            # If anything left unsent, send it
            if len(tmp) > 0:
                yield tmp

        return self._extend(_chunk)
