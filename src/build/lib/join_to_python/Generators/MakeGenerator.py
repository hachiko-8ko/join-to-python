def makeGenerator(iterable):
    """
    Make any object into an iterable. If not iterable, it will become a single-item iterable.
    """
    try:
        # Try to iterate it. If it doesn't work, then it's not iterable.
        # The Python philosophy is "it's better to ask forgiveness than permission."
        # Or put anohter way, "Well, son, a funny thing about regret is, that it's better to regret 
        # something you have done, than to regret something you haven't done."
        yield from iterable
    except TypeError:
        # Turn random non-iterables into apparent one-element iterables.
        yield iterable
