from ..Types.ArgumentCountException import *
from ..Types.Exceptions import *

class ForEach:
    """
    forEach: Execute a callback function on each row in the enumerable, returning no results.
    The function can optionally take the index as a second input.

    Note for people coming here from JS: There is no magic "self" in Python like "this" in JS and C#. Method calls on classes
    are just syntactic sugar that translates foo.method(arg) into method(foo, arg). JOIN can't allow that AND an optional positional 
    argument for index, because if you create a function "def someMethod(value, self)" or "def someMethod(self, value)" Python will 
    happily call "someMethod(value, index)." So if you must reference a parent class, use a closure.

    >>> None forEach<T>((Action<T> | Action<T, int>) actionFunction);
    """
    def forEach(self, actionFunction):
        if not actionFunction:
            raise ArgumentNullException("Required argument is None")
        index = 0
        for item in self:
            try:
                checkArgumentCount(actionFunction, 2)
                actionFunction(item, index)
            except ArgumentCountException:
                actionFunction(item)
            index += 1
