class Grouping:
    """
    The object returned by the groupBy method.

    >>> interface IGrouping<TKey, TValue> { TKey key, TValue[] values, TValue[] __iter__() };
    """
    def __init__(self, key, value, elementSelectFunction = None):
        self.key = key
        self._values = [value]
        if elementSelectFunction:
            self._selector = elementSelectFunction
        else:
            self._selector = lambda x: x

    def __iter__(self):
        yield from self.values

    @property
    def values(self):
        return [self._selector(x) for x in self._values]

    def add(self, value):
        self._values.append(value)

    def __str__(self):
        return str(self.values)

    def __repr__(self):
        return str(self.values)

    # Note: Again, not possible to have custom JSON serialization. Built-in json.dumps() doesn't look for any helper methods.
    # Some others like json_fix and simplejson do, but it's different for every one. Should I support them all or none of them?
