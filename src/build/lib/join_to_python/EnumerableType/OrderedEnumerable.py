from functools import cmp_to_key

from .Enumerable import *
from .OrderBy import *
from ..Types.Comparer import *
from ..Generators.ExhaustIterable import drain
from ..Types.Exceptions import *

# Generators are already deferred, but ordering actions need to be extra deferred, because ThenBy() ordering actions
# that would normally happen on later steps need to be moved into this object. So rather than each step returning
# a generic built-in generator, OrderBy() and ThenBy() return this wrapper object, which has all the regular generator
# functions plus ThenBy().

# This matches C#. ThenBy() only exists on the IOrderedEnumerable, not on IEnumerable, even though it appears in
# the documentation for Enumerable. To make this simple for the user, I considered aliasing it to OrderBy, but that could
# lead to confusion.

"""
An enumerable class where sorting by multiple keys has a clean API and _actually works_.

The python sorted() and list.sort() methods do NOT work. Sorts are "_guaranteed_ to be stable." They are not. How do I do an RMA?
Python's failure can be demonstrated in 3 lines (or 1 if you put them all together):
wtf = [some array]
wtf2 = sorted(wtf, key=something)       # same behavior from wtf.sort() or if wtf is replaced
wtf3 = sorted(wtf2, key=somethingElse)  # same behavior from wtf.sort() or if wtf is replaced

Expected: wtf3 shows data sorted by something and then somethingElse.
Actual: wtf3 shows data sorted only by somethingElse.

For example, sorting by length then reverse alpha:
right: ["dog", "cat", "fish", "bird", "turtle", "iguana"] # JOIN to Python
wrong: ["turtle", "iguana", "fish", "dog", "cat", "bird"] # sorted() and list.sort() (only reverse alpha)
"""
class OrderedEnumerable(Enumerable):
    def __init__(self, data, orderBy, comparer = None, descending = False):
        Enumerable.__init__(self, data)
        self._sorters = [{"orderBy": orderBy, "comparer": extractComparer(comparer), "descending": descending}]

    def __iter__(self):
        # Lucky for us the combination of cmp() functions (1 or -1, -1 or 1, etc) works the same in Python as it does in JS
        # so we can build a single sort method, call cmp_to_key on it to get a key function, and sort once.
        sortingFunction = None
        for hat in self._sorters:
            sortingFunction = _buildSorter(hat['orderBy'], hat['comparer'], hat['descending'], sortingFunction)

        sortedData = sorted(drain(self._data()), key=cmp_to_key(sortingFunction))
        yield from sortedData

    def thenBy(self, keySelector = None, comparer = None):
        """
        thenBy: sorts a partially sorted enumerable by an optional key selector function, or by itself.
        takes an optional comparer function

        >>> OrderedEnumerable<T> thenBy(Func<T, TKey>? keySelector = None, IComparer<T> comparer = None);
        >>> IComparer<T> = (Func<T, T, 0 | 1 | -1> | { compare: Func<T, T, 0 | 1 | -1> });
        """
        if not keySelector:
            keySelector = lambda o: o
        self._sorters.append({ "orderBy": keySelector, "comparer": extractComparer(comparer), "descending": False })
        return self

    def thenByDescending(self, keySelector = None, comparer = None):
        """
        thenByDescending: reverse sorts a partially sorted enumerable by an optional key selector function, or by itself.
        takes an optional comparer function

        >>> OrderedEnumerable<T> thenByDescending(Func<T, TKey>? keySelector = None, IComparer<T> comparer = None);
        >>> IComparer<T> = (Func<T, T, 0 | 1 | -1> | { compare: Func<T, T, 0 | 1 | -1> });
        """
        if not keySelector:
            keySelector = lambda o: o
        self._sorters.append({ "orderBy": keySelector, "comparer": extractComparer(comparer), "descending": True })
        return self

def _buildSorter(keySelector, comparer, descending, initial = None):
    if not comparer:
        comparer = defaultComparer

    if initial:
        def _thenBy(x, y):
            key1 = keySelector(x)
            key2 = keySelector(y)
            if descending:
                return initial(x, y) or comparer(key2, key1)
            return initial(x, y) or comparer(key1, key2)
        return _thenBy
    else:
        def _orderBy(x, y):
            key1 = keySelector(x)
            key2 = keySelector(y)
            if descending:
                return comparer(key2, key1)
            return comparer(key1, key2)
        return _orderBy
