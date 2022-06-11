from ..Generators.RestartableGenerator import *
from ..Types.Exceptions import *

class Replicate:
    """
    replicate: Repeat the items in a sequence a specified number of times.
    JOIN-only method.

    >>> Enumerable<T> replicate<T>(int times);
    """
    def replicate(self, times):
        def _replicate(data):
            nonlocal times
            loop = RestartableGenerator(data)
            while times > 0:
                yield from loop
                loop.restart()
                times -= 1

        return self._extend(_replicate)
