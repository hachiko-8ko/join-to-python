def extractComparer(functionOrObject):
    """
    This was created for the javascript version's terrible function signatures, but it's being kept for the Python
    version so that developers who prefer to use compare functions can use them and those who prefer to use C# IComparer
    type objects can use them.

    >>> IComparer = (Func<T, T, 0 | 1 | -1> | { compare: Func<T, T, 0 | 1 | -1> });
    """
    if not functionOrObject:
        return
    if callable(functionOrObject):
        return functionOrObject
    return functionOrObject.compare

def defaultComparer(x, y):
    """
    This is the default cmp(x,y) function that used to exist but now is not needed, now that cmp functions have been removed.
    """
    if x > y:
        return 1
    if x < y:
        return -1
    return 0
