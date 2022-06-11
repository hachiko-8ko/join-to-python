"""
Fake monkey-patching to create functions that appear to be methods callable on any object, but actually aren't, because they can only be triggered by the / operator.
"""
import sys

# Ideally these imports wouldn't corrupt the global scope. They do, but unfortunately for me, the Python devs made the only way to pull from
# other files in the module using "from .something" instead of (import .something)
from .EnumerableType.Enumerable import *
from .EnumerableType.OrderBy import monkeyPatchOrderBy as _orderby
from .Extend import *
from .Types.Exceptions import *

def makeEnumerable(iterable):
    """
    Turn an object into an Enumerable. This is a regular Python function.

    >>> Enumerable<T> makeEnumerable(object iterable);
    """
    if iterable is None:
        raise NullReferenceException("NullReferenceException: Sequence is missing")
    return Enumerable(iterable)

@Extend
def asQueryable(*args, **kwargs):
    """
    Turn any object into an Enumerable. This is a slash function, so is called like obj/asQueryable().

    >>> static Enumerable<T> /asQueryable<T>(this object iterable);
    """
    iterable = kwargs.pop('__iterable__')
    if iterable is None:
        raise NullReferenceException("NullReferenceException: Sequence is missing")

    # The int/bool shortcuts were something I put in the JS version. Including them for consistency.
    if isinstance(iterable, (int, float)):
        return Enumerable.range(0, iterable)
    if isinstance(iterable, bool):
        if iterable:
            # true/asQueryable() is pretty useless: [false, true] ascending. Might be useful.
            return makeEnumerable([false, true])
        else:
            # false/asQueryable() is pretty useless: [true, false] descending. Might be useful.
            return makeEnumerable([true, false])

    return makeEnumerable(iterable)

# This needs special handling, because it isn't supposed to always call an enumerable method
@Extend
def tryGetNonEnumeratedCount(dictionary = None, **kwargs):
    """
    If the object is an enumerable, call the enumerable method.
    If it is a known type such as str, list, set, tuple, or dict, call len() on it.
    Otherwise make it an enumerable and call the enumerable method.

    There are too many things that act as generators or hide generators (map, filter for example) that do not show up
    under inspect.isgenerator() or inspect.isgeneratorfunction() to call len() on too many things.
    """
    iterable = kwargs.pop('__iterable__')

    if iterable is None:
        raise NullReferenceException("NullReferenceException: Sequence is missing")

    if isinstance(iterable, Enumerable):
        return iterable.tryGetNonEnumeratedCount(dictionary)

    if isinstance(iterable, (str, list, dict, set, tuple)):
        if dictionary:
            dictionary["value"] = len(iterable)
        return True

    enum = Enumerable(iterable)
    return enum.tryGetNonEnumeratedCount(dictionary)

"""
Default patching: reduce boilerplate
"""
def _patchTheMonkey():
    def callEnumerableMethod(methodName, *args, **kwargs):
        iterable = kwargs.pop('__iterable__')

        if iterable is None:
            raise NullReferenceException("NullReferenceException: Sequence is missing")

        # We only need to create a new enumerable the first time.
        # After that, we can call the method on the thing itself.
        if isinstance(iterable, Enumerable):
            enum = iterable
        else:
            enum = Enumerable(iterable)

        method = getattr(enum, methodName)
        return method(*args, **kwargs)

    # Has to be a separate function because otherwise somehow the Extend object bleeds out of the parentheses and braces and causes random errors.
    def _internal(module, name, methodName = None):
        setattr(module, name, Extend(lambda *args, **kwargs: callEnumerableMethod(methodName or name, *args, **kwargs)))

    thismodule = sys.modules[__name__]

    methods = (
        'aggregate',
        'all_',
        'any_',
        'append',
        'average',
        'chunk',
        'concat',
        'contains',
        'count',
        'crossJoin',
        'defaultIfEmpty',
        'distinct',
        'distinctBy',
        'elementAt',
        "elementAtOrDefault",
        'empty',
        'except_',
        'exceptBy',
        'first',
        'firstOrDefault',
        'forEach',
        'groupBy',
        'groupJoin',
        'innerJoin',
        'intersect',
        'intersectBy',
        'fullJoin',
        'join',
        'last',
        'lastOrDefault',
        'leftJoin',
        'max_',
        'maxBy',
        'maxOrDefault',
        'min_',
        'minBy',
        'minOrDefault',
        'ofType',
        'orderBy',
        'orderByDescending',
        'outerJoin',
        'prepend',
        'replicate',
        'reverse',
        'rightJoin',
        'select',
        'selectMany',
        'sequenceEqual',
        'single',
        'singleOrDefault',
        'skip',
        'skipLast',
        'skipWhile',
        'step',
        'sum_',
        'take',
        'takeLast',
        'takeWhile',
        'toArray',
        'toDictionary',
        'toHashSet',
        'toList',
        'toLookup',
        'union',
        'unionBy',
        'where',
        'zip_'
    )
    for m in methods:
        _internal(thismodule, m)

    # Aliased methods
    _internal(thismodule, 'cast', 'select')
    _internal(thismodule, 'longCount', 'count')

    # Monkey-patch the Enumerable with the two OrderBy methods
    # It's annoying that these have to be here, not even in OrderedEnumerable.py, but it does nothing there.
    _orderby(Enumerable)

_patchTheMonkey()
