def extractEqualityComparer(functionOrObject):
    """
    This was created for the javascript version's terrible function signatures, but it's being kept for the Python
    version so that developers who prefer to use compare functions can use them and those who prefer to use C# IEqualityComparer
    type objects can use them.

    >>> IEqualityComparer = (Predicate<T, T> | { compare: Predicate<T, T> });
    """
    if not functionOrObject:
        return
    if callable(functionOrObject):
        return functionOrObject
    return functionOrObject.equals
