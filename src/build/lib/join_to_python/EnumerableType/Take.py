from ..Generators.ExhaustIterable import drain
from ..Types.Exceptions import *

class Take:
    """
    take: Returns a specified number of contiguous elements from the start of a sequence.

    The C# version also allows you to pass a Range object which has a start and an end. In C#, this is start..end. In Python, this is equivalent to a slice object, which you can create using syntax "slice(start,end)" (you can't just say [start:end] as that'll give you a syntax error). In C#, ranges have no "step" property, so handling for the python step is being added.

    Be warned about the built-in slice constructor: slice(2) isn't slice(2, None) but slice (None, 2).

    The JavaScript version of this library takes start as a separate parameter, as a workaround for ranges not being a part of the
    language. For the sake of consistency, that will be supported also.

    >>> Enumerable<T> take<T>(int count, int skip = 0, slice sliceObject = None);
    """
    def take(self, count = None, skip = 0, sliceObject = None):
        if count is not None:
            if sliceObject is not None:
                raise ArgumentException("Incorrect overload: passed count and slice")
            if skip < 0:
                skip = 0

            def _take(data):
                nonlocal count
                nonlocal skip
                for item in data:
                    if skip > 0:
                        skip -= 1
                        continue
                    if count <= 0:
                        return
                    count -= 1
                    yield item

            return self._extend(_take)

        elif sliceObject is not None:
            start = sliceObject.start
            stop = sliceObject.stop
            step = sliceObject.step
            if start is None:
                start = 0
            if step == 0:
                raise ValueError("slice step cannot be zero")

            # I hate how there are three options here, but I decided to support the extra python options.
            # (1) reverse slice, (2) count and step are None, (3) either count or step is not none

            # If any of the values are negative, the slicing is reversed/based on the end. These require materialization of the
            # entire array because you can't get the last 2 items unless you've determined what the last item is.
            if (start < 0 or (stop is not None and stop < 0) or (step is not None and step < 0)):
                def _take(data):
                    arr = drain(data)[sliceObject]
                    yield from arr
                return self._extend(_take)

            # if stop is none, we want to take everything after the start index. the code for this is already written
            if stop is None and step is None:
                return self.skip(start)

            # of course our existing take doesn't have ability to set the step count
            def _takeWithStep(data):
                index = 0
                tmpStep = 0
                for item in data:
                    if index < start:
                        index += 1
                        continue

                    if stop is not None:
                        if index >= stop:
                            return

                    index += 1
                    if step is None:
                        yield item

                    else: # special step logic
                        if tmpStep == 0:
                            yield item

                        # Handle step
                        tmpStep += 1
                        if tmpStep == step:
                            tmpStep = 0

            return self._extend(_takeWithStep)

        else:
            raise ArgumentNullException("All required arguments are None")
