from ..Extend import Extend
from .OrderedEnumerable import *
from ..Types.Exceptions import *

# WARNING!
# These two methods must be added to Enumerable using monkey-patching because declaring them in the Enumerable class cause the
# OrderedEnumerable class to not recognize Enumerable, its own base class. This is because it's creating an instance of the
# OrderedEnumerable (its own child).

"""
orderBy: Sorts the elements of a sequence in ascending order according to a key function.
Takes an optional cmp() function, a function that takes two inputs and returns 1 if the first is higher, -1 is the second is higher, else 0.

The key function is also optional. If you leave it out, it'll default to the identity. I got tired of writing orderBy(o => o)
when sorting numbers or strings. This is a change from C#.

>>> OrderedEnumerable<T> orderBy<T, TKey?(Func<T, TKey>? keySelector = None, IComparer<TKey>? comparer = None);
>>> IComparer<T> = (Func<T, T, 0 | 1 | -1> | { compare: Func<T, T, 0 | 1 | -1> });
"""
def orderBy(self, keySelector = None, comparer = None):
    if not keySelector:
        keySelector = lambda o: o
    return OrderedEnumerable(self, keySelector, comparer)

"""
orderByDescending: Sorts the elements of a sequence in ascending order according to a key function.
Takes an optional cmp() function, a function that takes two inputs and returns 1 if the first is higher, -1 is the second is higher, else 0.

The key function is also optional. If you leave it out, it'll default to the identity. I got tired of writing orderBy(o => o)
when sorting numbers or strings. This is a change from C#.

>>> OrderedEnumerable<T> orderByDescending<T, TKey?(Func<T, TKey>? keySelector = None, IComparer<TKey>? comparer = None);
>>> IComparer<T> = (Func<T, T, 0 | 1 | -1> | { compare: Func<T, T, 0 | 1 | -1> });
"""
def orderByDescending(self, keySelector = None, comparer = None):
    if not keySelector:
        keySelector = lambda o: o
    return OrderedEnumerable(self, keySelector, comparer, True)

"""
Enumerable cannot directly reference either order by method, because they return OrderedEnumerable, it's child class.
This function simplies the process of adding those methods after the fact.
"""
def monkeyPatchOrderBy(cls):
    cls.orderBy = orderBy
    cls.orderByDescending = orderByDescending

@Extend
def thenBy(*args, **kwargs):
    return _callOrderedEnumerable('thenBy', *args, **kwargs)

@Extend
def thenByDescending(*args, **kwargs):
    return _callOrderedEnumerable('thenByDescending', *args, **kwargs)

"""
The normal creation of /thenBy() in MonkeyPoxing.py does not work with OrderedEnumerable. Suddenly code that was working begins to fail.
It's not possible for files in that directory to import from OrderedEnumerable.py, which is necessary to throw a better message than
the confusing one that happens if you call Enumerable.thenBy(). So here's some unavoidable code duplication.

I chose not to alias thenBy() to orderBy() because a programmer could mix them up and end up with bad data.
"""
def _callOrderedEnumerable(methodName, *args, **kwargs):
    enum = kwargs.pop('__iterable__')
    if enum is None:
        raise NullReferenceException("NullReferenceException: Sequence is missing")

    # I considered making thenBy an alias for orderBy, but that could lead to program errors if programmers do it by accident
    if not isinstance(enum, OrderedEnumerable):
        raise NullReferenceException("ThenBy may only be called on an OrderedEnumerable")

    method = getattr(enum, methodName)
    return method(*args, **kwargs)
