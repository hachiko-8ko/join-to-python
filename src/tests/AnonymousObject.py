import inspect

"""
Quick and dirty function to create an anonymous object that can be printed. This is useful in general but very useful for unit tests.
"""
def Object(**kwargs):
    cls = type("Object", (), kwargs)
    def makeDict(self):
        result = {} # This would be more consistent as an OrderedDict but it doesn't look as good
        for prop, value in inspect.getmembers(self):
            if not prop.startswith('_'):
                result[prop] = value
        return str(result)
    cls.__str__ = makeDict
    cls.__repr__ = makeDict
    return cls()
