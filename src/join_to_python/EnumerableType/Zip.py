from ..Types.Exceptions import *

class Zip:
    """
    zip_: Produces a sequence of tuples with elements from two or three specified sequences.
    In place of a third sequence, a function can be provided that combines the first two.

    Zip() already exists as part of the standard library so the slash function for this is zip_

    >>> Enumerable<(T, TSecond) | (T, TSecond, TThird)> zip<T, TSecond. TThird>(Iterable<TSecond> second, (Iterable<TThird> | Func<T, TSecond, TThird>)? third = None);
    """
    def zip_(self, second, third = None):
        if second is None:
            raise EmptySequenceException("Required argument is None")

        def _zip(data):
            iter1 = iter(data)
            iter2 = iter(second)

            val1 = None
            done1 = False

            val2 = None
            done2 = False

            iter3 = None
            func3 = None
            val3 = None
            done3 = False

            if third is not None and callable(third):
                func3 = third
            elif third is not None:
                iter3 = iter(third)

            while True:
                try:
                    val1 = next(iter1)
                except StopIteration:
                    done1 = True
                try:
                    val2 = next(iter2)
                except StopIteration:
                    done2 = True
                if iter3:
                    try:
                        val3 = next(iter3)
                    except StopIteration:
                        done3 = True

                # As soon as any of the sequences runs out of data, we halt.
                if done1 or done2 or done3:
                    break

                if iter3:
                    yield (val1, val2, val3)
                elif func3:
                    yield (val1, val2, func3(val1, val2))
                else:
                    yield (val1, val2)

        return self._extend(_zip)

    def zip(self, second, third = None):
        return self.zip(second, third)
