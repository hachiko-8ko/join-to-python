from .MakeGenerator import makeGenerator

class RestartableGenerator:
    """
    Python doesn't give a way to restart a generator, which causes a great deal of trouble when you need to check it multiple times.
    For example, if you do an inner join, you need to check each element of the left with each element of the right.
    You need the ability to rebuild the generator from the original iterable. But there isn't a reference to the original iterable ANYWHERE.
    As a result, the only way to make this work is to make a copy of the data as you iterate it.
    This could double the amount of space needed, but it's a limitation of the technology.
    """
    def __init__(self, iterable, flexMemory = False):
        """
        Iterable must be an iterable. If flexMemory is true, then the backup list is cleared after restart.
        """
        self.backup = []
        self.iterator = cycleGenerator(iterable, self.backup)
        self.flexMemory = flexMemory

    def __iter__(self):
        yield from self.iterator

    def restart(self):
        """
        Restart the generator from the cache.
        """
        if (self.flexMemory):
            i = self.backup.copy()
            self.backup = []
            self.iterator = cycleGenerator(i, self.backup)
        else:
            self.iterator = makeGenerator(self.backup)

def cycleGenerator(iter, backup):
    for x in iter:
        backup.append(x)
        yield x
