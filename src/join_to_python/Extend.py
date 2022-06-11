from functools import partial
from .EnumerableType.Enumerable import *

# This is going to bleed into the global scope and I can't control it.
# For reasons I cannot even begin to understand, prefixing this with underscore makes it impossible to reference it after import
class Extend:
    """
    A helper to modify the reverse / operator to call the method being extended.
    This makes new Enumerable(list).select(lambda x: x.name).toArray() into list/select(lambda x: x.name)/toArray().

    After the first enumerable, you can actually go to dot syntax, but you need parens to get around order of operations.
    (list/select(lambda x: x.name)).toArray() is fine but list/select(lambda x: x.name).toArray() is calling toArray() on the
    select function, not the result of select (which hasn't been called yet).

    (If we had promises, it might have been possible to .then() onto the function call and return the promise, but this isn't JS. You'd also have to await everything which would suck).
    """
    def __init__(self, function):
        self.function = function

    def __call__(self, *args, **kwargs):
        return Extend(partial(self.function, *args, **kwargs))

    def __rtruediv__(self, other):
        return self.function(__iterable__ = other)
