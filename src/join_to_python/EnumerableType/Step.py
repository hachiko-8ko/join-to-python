from ..Types.Exceptions import *

class Step:
    """
    step: returns every "step" items from a sequence

    This is a new item that I added because I thought it might be useful. Python's negative steps, which reverse the order, are not
    supported. You can use take() with the sliceObject input or you can call reverse() first.

    >>> Enumerable<T> step<T>(int step);
    """
    def step(self, step):
        if step <= 0:
            raise ArgumentException("Required argument is invalid")

        def _step(data):
            tmpStep = 0
            for item in data:
                if tmpStep == 0:
                    yield item

                # Handle step
                tmpStep += 1
                if tmpStep == step:
                    tmpStep = 0

        return self._extend(_step)
