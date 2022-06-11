import inspect

"""
An exception that specifically indicates that the number of arguments is wrong.
"""
class ArgumentCountException(TypeError):
    pass

"""
Here's something uniquely difficult in Python. Nowhere is it described how to add *args and *kwargs when you aren't the one writing
the function. If someone gives you myFunc(value), not myFunc(value, *args). and you call myfunc(value, index) it will throw.

In C#, you can use method signatures to go only to valid methods. Func<TItem, TOut> or Func<TItem, int, TOut>. Simple.
In JavaScript, you can pass all the arguments you want, used or not. Also simple.

In Python, you can try it and check for TypeError, but TypeError is used for so many different things. Concatenate an integer and
a string? TypeError, resulting in a completely confusing error message when the program logic things the # of arguments was off.

This is a function that checks the total number of positional arguments. In the Pythonic style, rather than returning the
count, it throws if it doesn't match the expected count.
"""
def checkArgumentCount(func, expected):
    argcount = len(inspect.getargspec(func).args)
    if argcount != expected:
        raise ArgumentCountException("method takes exactly {0} argument(s) ({1} given)".format(argcount, expected))
