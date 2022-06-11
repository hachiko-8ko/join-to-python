from ..Generators.MakeGenerator import makeGenerator
from ..Types.Exceptions import *

class BaseEnumerable:
    def __init__(self, data):
        self._cache = []
        self._isClosed = False

        # Normally, we'd go ahead and say the data should be an array, nothing but.
        # But let's be flexible and allow anything. If it's not iterable, then it'll become a one-item iterator.
        self._source = self._ensureBackup(makeGenerator(data))

    def tryGetNonEnumeratedCount(self, dictionary = None):
        """
        tryGetNonEnumeratedCount: Try to return the length of the source. Only possible if exhausted.
        >>> bool tryGetNonEnumeratedCount(out Dictionary<"value", int>? dictionary = None);
        """
        if self._isClosed:
            # We don't have out vars in Python either so we have to use a dictionary reference.
            if dictionary:
                dictionary["value"] = len(self._cache)

            return True

        # If not closed, this is a generator, and we can't count it without enumerating it.
        return False

    def __iter__(self):
        # Need to materialize the full list to sort it
        for item in self._data():
            yield item

    def _data(self):
        # There's not a lot of call for selecting from an enumerable more than once, but someone might
        # want to do it. In C# the only real time this happens is when you use the debugger, but it does happen.

        # But when data has been fetched from the generator, it becomes closed, and every generator in its
        # source is also closed. This is built in to Python and not something we can change.
        # But we can cache the data when we fetch it and return the cache if closed.

        if self._isClosed:
            return self._cache

        return self._source

    def _ensureBackup(self, data):
        for item in data:
            self._cache.append(item)
            yield item

        self._isClosed = True

    # Note: Not possible to have custom JSON serialization. Built-in json.dumps() doesn't look for any helper methods.
    # Some others like json_fix and simplejson do, but it's different for every one. Should I support them all or none of them?
