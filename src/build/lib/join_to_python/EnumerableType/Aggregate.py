from ..Types.Exceptions import *

"""
This has one error in C# that is only thrown in the overload where no seed value is passed.
Because there's a difference between using a default of None and explictly passing none,
we need a way to set them apart.
"""
class _undefined_: pass

class Aggregate:
    """
    aggregate: Applies an accumulator function over a sequence.
    optional initial value acts as seed value
    optional outputFunction selects the result

    Overload order is changed from C#. In C#, the optional initial value can come first. In Python, optional parameters must follow required ones. It of course would be possible to match the javascript version, which sometimes stores the accumulator in the first argument and sometimes in the second, but that would really dirty up this clean Python API. It's more important to have good code than to match C#.

    >>> (TAccumulated | TResult) aggregate<T, TAccumulated, TResult>(
            Func<TAccumulated, T, TAccumulated> accumulatorFunction,
            T? initialValue = None,
            Func<TAccumulated, TResult>? outputFunction = None);
    """
    def aggregate(self, accumulatorFunction, initialValue = _undefined_(), outputFunction = None):
        if isinstance(initialValue, _undefined_):
            seeded = False
            value = None
        else:
            seeded = True
            value = initialValue

        for item in self:
            # If there is no seed, then the first value is used as the seed. After the first item, it is populated.
            if not seeded:
                seeded = True
                value = item
            else:
                value = accumulatorFunction(value, item)

        # C# only throws an error in the overload without a seed value.
        if not seeded:
            raise EmptySequenceException("Sequence contains no elements")

        if outputFunction:
            return outputFunction(value)
        else:
            return value

