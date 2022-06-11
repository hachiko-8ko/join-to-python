# IQueryable interface

## Note on method signatures

The new static typing system for Python is still rather a trainwreck. Look at the mess that is the doc on python.org, how protocol (interface) members are required to have bodies (misses the point), and how most existing features were added in recent versions that would put a hard lower limit on this library for no really good. So I'm not going to statically type this library but just document it.

Python signatures are included, but I haven't gone through and tested them with mypy. To be honest, I haven't gotten static types working. I'm not sure the things I'm trying to express are even possible in the latest version of Python (3.11 at this writing). Hopefully it'll get the idea across. YMMV.

I'm also going to include C# style syntax, which have the benefit of making sense. However, keep in mind that in C#, you can call overloads that have different argument order using positional arguments. This isn't possible in Python. So the Python syntax will be more accurate. But the C# syntax will be more descriptive (3 overloads typically means "these are your three options").

## Frequently Referenced Types

These types are referenced throughout.

```
# Python-style

numeric = Union[int, float, complex]
class IGrouping[Protocol][TKey, TValue]:
    def key: TKey
    def values: List[TValue]
    def __iter__(): List[TValue]

class IEqualityComparerDotNetStyle[Protocol][T]:
    def equals: Predicate[T, T] # .net IEqualityComparer looks like {equals}
IEqualityComparer[T] = Union[Predicate[T, T], IEqualityComparerDotNetStyle[T])

class IComparerDotNetStyle[Protocol][T]:
    def compare: Func[T, T, Union[0, 1, -1]] # .net IComparer looks like {compare}
IComparer[T] = Union[Func[T, T, Union[0, 1, -1]], IComparerDotNetStyle[T]]

# C# style

compareValue = 0 | 1 | -1 ; // I'm cheating here ... unions don't exist in C#
numeric = int | float | complex; // I'm still cheating
IGrouping<TKey, TValue> = { TKey key, TValue[] values, TValue[] __iter__() };

interface IEqualityComparerDotNetStyle { equals: Predicate<T, T>; }
IEqualityComparer<T> = Predicate<T, T> | IEqualityComparerDotNetStyle; // union cheat

interface IComparerDotNetStyle { compare: Func<T, T, compareValue>; }
IComparer<T> = Func<T, T, compareValue> | IComparerDotNetStyle; // union cheat
```

## aggregate

Applies an accumulator function over a sequence. optional initial value acts as seed value. optional outputFunction selects the result.

Overload order is changed from C#. In C#, the optional initial value can come first. In Python, optional parameters must follow required ones. It of course would be possible to match the javascript version, which sometimes stores the accumulator in the first argument and sometimes in the second, but that would really dirty up this clean Python API. It's more important to have good code than to match C#.

```
def aggregate[T, TAccumulated, TResult](accumulatorFunction: Func[TAccumulated, T, TAccumulated],
    initialValue: T = None, outputFunction: Func[TAccumulated, TResult] = None) -> Union[TAccumulated, TResult]

TAccumulated aggregate<T, TAccumulated>(Func<TAccumulated, T, TAccumulated> accumulatorFunction, T? initialValue = None);
TResult aggregate<T, TAccumulated, TResult>(Func<TAccumulated, T, TAccumulated> accumulatorFunction,
    T? initialValue = None, Func<TAccumulated, TResult> outputFunction);
```

## all_

Determines whether all elements of a sequence satisfy a condition. This condition can optionally take the index as the second argument (this is not provided by the C# version).

```
def all_[T](filterFunction: Union[Predicate[T, T], Predicate[T, T, int]) -> boolean

bool all_<T>(Predicate<T, T>) filterFunction);
bool all_<T>(Predicate<T, T, int>) filterFunction);
bool all<T>(ETC); /* name exists on class method */
```

## any_
Determines whether any elements of a sequence satisfy an optional condition. This condition can optionally take the index as the second argument (this is not provided by the C# version).

```
def any_[T](filterFunction: Union[Predicate[T, T], Predicate[T, T, int]] = None) -> boolean

bool any_<T>();
bool any_<T>(Predicate<T, T> filterFunction);
bool any_<T>(Predicate<T, T, int> filterFunction);
bool any<T>(ETC); /* name exists on class method */
```

## append
Appends a value to the end of the sequence

```
def append[T](newItem: T) -> Enumerable[T]

Enumerable<T> append<T>(T newItem);
```

## average
computes the average of a sequence of numbers. optional transform function lets us calculate using values obtained by invoking afunction on each element of the sequence. if numbers can be None, then the None values are skipped

```
def average[T](outputFunction: Func[T, numeric] = None) -> numeric

numeric? average<T>();
numeric? average<T>(Func<T, numeric> outputFunction);
```

## chunk
splits the elements of a sequence into chunks of size at most "size"

```
def chunk[T](size: int) -> Enumerable[List[T]]

Enumerable<T[]> chunk<T>(int size);
```

## concat
concatenates two sequences

```
def concat[T](second: Iterable[T]) -> Enumerable[T]>

Enumerable<T> append<T>(Enumerable<T> second);
```

## contains
determines whether a sequence contains a specified element. optional equalityComparer function to indicate if record matches

```
def contains[T](value: T, comparer: IEqualityComparer[T] = None) -> boolean

bool contains<T>(T value);
bool contains<T>(T value, IEqualityComparer<T> comparer);
```

 ## count
returns a number that represents how many elements in the specified sequence satisfy an optional condition. longCount also redirects here (the int class handles arbitrarily large numbers)

```
def count[T](filterFunction: Predicate[T] = None) -> int

int count<T>();
int count<T>(Predicate<T> filterFunction);
```

## crossJoin
Create a simple cartesian join (every record from table 1 along with every record from table 2). This is JOIN-only (not in C#)

```
def crossJoin[T, TSecond, R](second: Iterable[T], outputFunction:  Func[T, TSecond, R] = None) -> Enumerable[R]

Enumerable<R> crossJoin<T, TSecond, R>(Iterable<TSecond> second, Func<T, TSecond, R> outputFunction);
Enumerable<(T, TSecond)> crossJoin<T, TSecond>(Iterable<TSecond> second);
```

## defaultIfEmpty
returns the sequence or the (optional) default value if the sequence is empty. Default in is a paramter. IF it is left out, None is returned. (Note that in Python, unlike C#, there's no way to know what type a sequence is supposed to have, especially an empty one.)

```
def defaultIfEmpty[T](defaultValue: T = None) -> Enumerable[Union[T, None]]

Enumerable<T?> defaultIfEmpty<T>();
Enumerable<T> defaultIfEmpty<T>(T defaultValue);
```

## distinct
Returns distinct elements from a sequence by using an optional equality comparer to compare values

```
def distinct[T](comparer: IEqualityComparer[T] = None) -> Enumerable[T]

Enumerable<T> distinct<T>();
Enumerable<T> distinct<T>(IEqualityComparer<T> comparer);
```

## distinctBy
Returns distinct elements from a sequence based on keys returned by a key selector function. optional equality comparer can be supplied to compare values

```
def distinctBy[T, TKey](keySelector: Func[T, TKey], comparer: IEqualityComparer[T] = None)  -> Enumerable[T]

Enumerable<T> distinctBy<T, TKey>(Func<T, TKey> keySelector);
Enumerable<T> distinctBy<T, TKey>(Func<T, TKey> keySelector, IEqualityComparer<TKey> comparer);
```

## elementAt
Returns the element at a specified index in a sequence

```
def elementAt[T](index: int) -> T

T elementAt<T>(int index);
```

## elementAtOrDefault
Returns the element at a specified index in a sequence. Returns an optional default value if index is out of range, or None if not supplied. (Note that in Python, unlike C#, there's no way to know what type a sequence is supposed to have.)

```
def elementAtOrDefault[T](index, defaultValue = None) -> T

T elementAtOrDefault<T>(int index, T defaultValue);
T? elementAtOrDefault<T>(int index);
```

## empty
Returns an empty IEnumerable<T> that doesn't have the specified type argument because this is Python

```
def empty[T]() -> Enumerable[T]

Enumerable<T> empty<T>();
```

## except_
Produces the set difference (distinct) of two sequences. optional equality comparer can be used to compare values "Except" is already defined in python so JOIN had to add an underscore after the end. Limitation of the language.

```
def except_[T](second: Iterable[T], comparer: IEqualityComparer[T] = None) -> Enumerable[T]

Enumerable<T> except_<T>(Iterable<T> second);
Enumerable<T> except_<T>(Iterable<T> second, IEqualityComparer<T> comparer);
```

## exceptBy
Produces the set difference of two sequences based on keys (distinct keys) returned by a key selector function. optional equality comparer can be used to compare values

```
def exceptBy[T](second: Iterable[T], keySelector: Func[T, TKey], comparer = None) -> Enumerable[T]

Enumerable<T> exceptBy<T, TKey>(Iterable<T> second, Func<T, TKey> keySelector);
Enumerable<T> exceptBy<T, TKey>(Iterable<T> second, Func<T, TKey> keySelector, IEqualityComparer<TKey> comparer);
```

## first
Returns the first element in a sequence, throwing an exception if the sequence is empty. optional filter condition can be supplied. This condition can optionally take the index as the second argument (this is not provided by the C# version)

```
def first[T](filterFunction: Union[Predicate[T], Predicate[T, int]] = None) -> T

T first<T>();
T first<T>(Predicate<T> filterFunction);
T first<T>(Predicate<T, int> filterFunction);
```

## firstOrDefault
Returns the first element in a sequence, throwing an exception if the sequence is empty. optional filter condition can be supplied. This condition can optionally take the index as the second argument (this is not provided by the C# version)

If the filtered sequence is empty, it returns the default value. The default value is provided by a parameter or is None. (Note that in Python, unlike C#, there's no way to know what type a sequence is supposed to have, especially not an empty sequence.)

```
def firstOrDefault[T](filterFunction: Union[Predicate[T], Predicate[T, int]] = None, defaultValue = None) -> T

T? firstOrDefault<T>(Predicate<T>? filterFunction = None, T? defaultValue = None);
T? firstOrDefault<T>(Predicate<T, int>? filterFunction = None, T? defaultValue = None);
```

## forEach
Execute a callback function on each row in the enumerable, returning no results. The function can optionally take the index as a second input.

Note for people coming here from JS: There is no magic "self" in Python like "this" in JS and C#. Method calls on classes are just syntactic sugar that translates foo.method(arg) into method(foo, arg). JOIN can't allow that AND an optional positional argument for index, because if you create a function "def someMethod(value, self)" or "def someMethod(self, value)" Python will happily call "someMethod(value, index)." So if you must reference a parent class, use a closure.

```
def forEach[T](Union[Action[T], Action[T, int]]) -> None

None forEach<T>((Action<T> actionFunction);
None forEach<T>(Action<T, int> actionFunction);
```

## fullJoin
A friendly helper to create a simple full outer join. This follows the pattern of innerJoin(), which combines the two key lookups and equality comparer into a single function input. This is JOIN-only (not in C#)

```
def fullJoin[T, TSecond, R](second: Iterable[T], outputFunction:  Func[T, TSecond, R] = None) -> Enumerable[R]

Enumerable<R> fullJoin<T, TSecond, R>(Iterable<TSecond> second, Func<T?, TSecond?, R> outputFunction);
Enumerable<(T?, TSecond?)> fullJoin<T, TSecond>(Iterable<TSecond> second);
```

## groupBy
Groups the elements of a sequence according to a specified key selector function and creates a result value from each group and its key. takes an optional element selection function. takes an optional output projection function. takes an optional equality comparer function

```
def groupBy[T, TKey, TElement, TOutput](groupFunction: Func[T, TKey], elementFunction: Func[T, TElement] = None, outputFunction: Func[TKey, Array<T>, TOutput] = None, comparer: IEqualityComparer[TKey] = None):

/* groupBy overloads are a MESS ... too many options */
Enumerable<IGrouping<TKey, TOutput>> groupBy<T, TKey, TElement, TOutput>(Func<T, TKey> groupFunction,
            Func<T, TElement>? elementFunction = None,
            Func<TKey, Array<TElement>, TOutput> outputFunction,
            IEqualityComparer<TKey>? comparer = None);
Enumerable<IGrouping<TKey, TOutput>> groupBy<T, TKey, TElement, TOutput>(Func<T, TKey> groupFunction,
            Func<TKey, Array<T>, TOutput> outputFunction,
            IEqualityComparer<TKey>? comparer = None);
Enumerable<IGrouping<TKey, TElement>> groupBy<T, TKey, TElement, TOutput>(Func<T, TKey> groupFunction,
            Func<T, TElement>? elementFunction = None,
            IEqualityComparer<TKey>? comparer = None);
Enumerable<IGrouping<TKey, T>> groupBy<T, TKey, TElement, TOutput>(Func<T, TKey> groupFunction,
            IEqualityComparer<TKey>? comparer = None);
```

## groupJoin
Correlates the elements of two sequences based on key equality and groups the results.

This is a sort of a combination of outer join and half a group by (only the second sequence is grouped). The output function, which determines the output, is required. This doesn't seem useful enough for me to come up with a default output.

```
def groupJoin[T, TKey, TSecond, TResult](second: Iterable[T], firstKeySelector: Func[T, TKey], secondKeySelector: Func[TSecond, TKey], 
    outputFunction: Func[T, List[TSecond], TResult], comparer: IEqualityComparer[T] = None) -> Enumerable[TResult]

Enumerable<TResult> groupJoin<T, TSecond, TKey, TResult>(Iterable<TSecond> second,
    Func<T, TKey> firstKeySelector, Func<TSecond, TKey> secondKeySelector,
    Func<T, TSecond[], TResult> outputFunction, IEqualityComparer<TKey>? comparer = None);
```

## innerJoin
A friendly helper to create a simple inner join. This combines the two key lookups and the custom equality comparer into a single function input. For most programmers, this is all the complexity you'll need. This is JOIN-only (not in C#)

```
def innerJoin[T, R](second: Iterable[T], on: Predicate[T, TSecond], outputFunction = None) -> Enumerable[R]

Enumerable<R> innerJoin<T, TSecond, R>(Iterable<TSecond> second, Predicate<T, TSecond> on, Func<T, TSecond, R> outputFunction);
Enumerable<(T, TSecond)> innerJoin<T, TSecond>(Iterable<TSecond> second, Predicate<T, TSecond> on);
```

## intersect
Returns distinct elements from a sequence by using an optional equality comparer to compare values

```
def intersect[T](second: Iterable[T], comparer: IEqualityComparer[T] = None) -> Enumerable[T]

Enumerable<T> intersect<T>(Iterable<T> second);
Enumerable<T> intersect<T>(Iterable<T> second, IEqualityComparer<T> comparer);
```

## intersectBy
Produces the set intersection of two sequences based on keys returned by a key selector function. optional equality comparer can be provided

```
def intersectBy[T, TKey](second: Iterable[T], keySelector: Func[T, TKey], comparer: IEqualityComparer[T] = None) -> Enumerable[T]

Enumerable<T> intersectBy<T, TKey>(Iterable<T> second, Func<T, TKey> keySelector);
Enumerable<T> intersectBy<T, TKey>(Iterable<T> second, Func<T, TKey> keySelector, IEqualityComparer<TKey> comparer);
```

## join
Correlates the elements of two sequences based on matching keys. Only records are returned when both sides match. optional equality comparer can be used to compare keys. If the output selector is left out, results are returned as (first row, second row). This is a change from C#, which requires the output selector.

```
def join[T, TSecond, R](second: Iterable[T], firstKeySelector: Func[T, TKey], secondKeySelector: Func<TSecond, TKey>, 
    outputFunction: Func[T, TSecond, R] = None, comparer: IEqualityComparer[T] = None) -> Enumerable[R]

Enumerable<R> join<T, TSecond, TKey, R>(Iterable<TSecond> second,
        Func<T, TKey> firstKeySelector, Func<TSecond, TKey> secondKeySelector,
        Func<T, TSecond, R> outputFunction, IEqualityComparer<TKey>? comparer = None);
Enumerable<(T, TSecond)> join<T, TSecond, TKey>(Iterable<TSecond> second,
        Func<T, TKey> firstKeySelector, Func<TSecond, TKey> secondKeySelector,
        IEqualityComparer<TKey>? comparer = None);
```

## last
Returns the last element in a sequence, throwing an exception if the sequence is empty. optional filter condition can be supplied. This condition can optionally take the index as the second argument (this is not provided by the C# version)

```
def last[T](filterFunction = None) -> T

T last<T>();
T last<T>(Predicate<T> filterFunction);
T last<T>(Predicate<T, int> filterFunction);
```

## last
Returns the last element in a sequence, throwing an exception if the sequence is empty. optional filter condition can be supplied. This condition can optionally take the index as the second argument (this is not provided by the C# version)

If the filtered sequence is empty, it returns the default value. The default value is provided by a parameter or is None. (Note that in Python, unlike C#, there's no way to know what type a sequence is supposed to have, especially not an empty sequence.)

```
def lastOrDefault[T](filterFunction: Union[Predicate[T], Predicate[T, int] = None, defaultValue: T = None) -> T

T? lastOrDefault<T>(Predicate<T>? filterFunction = None, T? defaultValue = None);
T? lastOrDefault<T>(Predicate<T, int> filterFunction = None, T? defaultValue = None);
```

## leftJoin
friendly helper to create a simple left outer join. This follows the pattern of innerJoin(), which combines the two key lookups and equality comparer into a single function input. This is JOIN-only (not in C#)

```
def leftJoin[T, TSecond, R](second: Iterable[T], on: Predicate[T, TSecond], outputFunction: Func[T, TSecond, R] = None) -> Enumerable[R]

Enumerable<R> leftJoin<T, TSecond, R>(Iterable<TSecond> second, Func<T, TSecond> on, Func<T, TSecond?, R> outputFunction);
Enumerable<(T, TSecond?)> leftJoin<T, TSecond>(Iterable<TSecond> second, Func<T, TSecond> on);
```

## max_
Returns the maximum value in a sequence. Takes an optional transformation function. If supplied, this transformation is applied to all values and the max result returned. Takes an optional comparer, a function that takes two inputs and returns 1 if the first is higher, -1 is the second is higher, else 0.

```
def max_[T, TResult](outputFunction: Func[T, TResult] = None, comparer: IComparer[TResult] = None) -> T

TResult max_<T, TResult>(Func<T, TResult> outputFunction, IComparer<TResult>? comparer = None);
T max_<T, TResult>(IComparer<TResult>? comparer = None);
TResult max<T, TResult>(ETC); /* name exists on class method */
```

## maxBy
Returns the maximum value in a sequence using a key selector function. Takes an optional comparer, a function that takes two inputs and returns 1 if the first is higher, -1 is the second is higher, else 0.

The difference between MaxBy and Max with a transformation function is that Max returns the output of the transformation while MaxBy returns the original value. This same result could be achieved with Max and a well-designed comparer function, of course.

```
def maxBy[T, TKey](keySelector: Func[T, TKey], comparer: IComparer[TKey] = None) -> T

T maxBy<T, TKey>(Func<T, TKey> keySelector);
T maxBy<T, TKey>(Func<T, TKey> keySelector, IComparer<TKey> comparer);
```

## maxOrDefault
Returns the maximum value in a sequence. Takes an optional transformation function. If supplied, this transformation is applied to all values and the max result returned. If sequence is empty, returns the default value or None. This is a JOIN-specific method. There is no equivalent in C#. Takes an optional comparer, a function that takes two inputs and returns 1 if the first is higher, -1 is the second is higher, else 0.

```
def maxOrDefault[T, TResult](outputFunction: Func[T, TResult] = None, comparer: IComparer[TResult] = None, defaultValue: T = None) -> T

TResult maxOrDefault<T, TResult>(Func<T, TResult> outputFunction, IComparer<TResult>? comparer = None, TResult defaultValue);
TResult? maxOrDefault<T, TResult>(Func<T, TResult> outputFunction, IComparer<TResult>? comparer = None);
T maxOrDefault<T, TResult>(IComparer<TResult>? comparer = None, TResult defaultValue);
T? maxOrDefault<T, TResult>(IComparer<TResult>? comparer = None);
```

## min_
Returns the minimum value in a sequence. Takes an optional transformation function. If supplied, this transformation is applied to all values and the min result returned. Takes an optional comparer, a function that takes two inputs and returns 1 if the first is higher, -1 is the second is higher, else 0.

```
def min_[T, TResult](outputFunction: Func[T, TResult] = None, comparer: IComparer[TResult] = None) -> T

TResult min_<T, TResult>(Func<T, TResult> outputFunction, IComparer<TResult>? comparer = None);
T min_<T, TResult>(IComparer<TResult>? comparer = None);
TResult min<T, TResult>(ETC); /* name exists on class method */
```

## minBy
Returns the minimum value in a sequence using a key selector function. Takes an optional comparer, a function that takes two inputs and returns 1 if the first is higher, -1 is the second is higher, else 0. The difference between MinBy and Min with a transformation function is that Min returns the output of the transformation while MinBy returns the original value. This same result could be achieved with Min and a well-designed comparer function, of course.

```
def minBy[T, TKey](keySelector: Func[T, TKey], comparer: IComparer[TKey] = None) -> T

T minBy<T, TKey>(Func<T, TKey> keySelector);
T minBy<T, TKey>(Func<T, TKey> keySelector, IComparer<TKey> comparer);
```

## minOrDefault
Returns the minimum value in a sequence. Takes an optional transformation function. If supplied, this transformation is applied to all values and the min result returned. If sequence is empty, returns the default value or None. This is a JOIN-specific method. There is no equivalent in C#. Takes an optional comparer, a function that takes two inputs and returns 1 if the first is higher, -1 is the second is higher, else 0.

```
def minOrDefault[T, TResult](outputFunction: Func[T, TResult] = None, comparer: IComparer[TResult] = None, defaultValue: T = None) -> T

TResult minOrDefault<T, TResult>(Func<T, TResult> outputFunction, IComparer<TResult>? comparer = None TResult defaultValue);
TResult? minOrDefault<T, TResult>(Func<T, TResult> outputFunction, IComparer<TResult>? comparer = None);
T minOrDefault<T, TResult>(IComparer<TResult>? comparer = None TResult defaultValue);
T? minOrDefault<T, TResult>(IComparer<TResult>? comparer = None);
```

## ofType
Filters the elements of an IEnumerable based on a specified type. In Python this is kind of meaningless. It's just where(lambda x: instanceof(x, param))

```
def ofType[T, R](filterType: Union[type[R], Tuple[type[R]]]) -> Enumerable[R]

Enumerable<R> ofType<T, R>(type<R> filterType);
Enumerable<R> ofType<T, R>(Tuple<type<R>> filterType);
```

## orderBy
Sorts the elements of a sequence in ascending order according to a key function. Takes an optional cmp() function, a function that takes two inputs and returns 1 if the first is higher, -1 is the second is higher, else 0. The key function is also optional. If you leave it out, it'll default to the identity. I got tired of writing orderBy(o => o) when sorting numbers or strings. This is a change from C#.

```
def orderBy[T, TKey](keySelector: Func[T, TKey] = None, comparer: IComparer[TKey] = None) -> OrderedEnumerable[T]

OrderedEnumerable<T> orderBy<T, TKey>(Func<T, TKey>? keySelector = None, IComparer<TKey>? comparer = None);
```

## orderByDescending
Sorts the elements of a sequence in ascending order according to a key function. Takes an optional cmp() function, a function that takes two inputs and returns 1 if the first is higher, -1 is the second is higher, else 0. The key function is also optional. If you leave it out, it'll default to the identity. I got tired of writing orderBy(o => o) when sorting numbers or strings. This is a change from C#.

```
def orderByDescending[T, TKey](keySelector: Func[T, TKey] = None, comparer: IComparer[TKey] = None) -> OrderedEnumerable[T]

OrderedEnumerable<T> orderByDescending<T, TKey>(Func<T, TKey>? keySelector = None, IComparer<TKey>? comparer = None);
```

## outerJoin
Correlates the elements of two sequences based on matching keys. If no matching record is find in the second sequence, None is sent to the output selector.
Outer Joins are not provided in LINQ. This is a new function, following the pattern of join(). optional equality comparer can be used to compare keys. If the output selector is left out, results are returned as (first row, second row).

```
def outerJoin[T, TSecond, R](second: Iterable[T], firstKeySelector: Func[T, TKey], secondKeySelector: Func<TSecond, TKey>, 
    outputFunction: Func[T, TSecond, R] = None, comparer: IEqualityComparer[T] = None) -> Enumerable[R]

Enumerable<R> outerJoin<T, TSecond, TKey, R>(Iterable<TSecond> second,
        Func<T, TKey> firstKeySelector, Func<TSecond, TKey> secondKeySelector,
        Func<T, TSecond?, R> outputFunction, IEqualityComparer<TKey>? comparer = None);
Enumerable<(T, TSecond?)> outerJoin<T, TSecond, TKey>(Iterable<TSecond> second,
        Func<T, TKey> firstKeySelector, Func<TSecond, TKey> secondKeySelector,
        IEqualityComparer<TKey>? comparer = None);
```

## prepend
Appends a value to the start of the sequence

```
def prepend(newItem: T) -> Enumerable[T]

Enumerable<T> prepend<T>(T newItem);
```

## replicate
Repeat the items in a sequence a specified number of times. JOIN-only method.

```
def replicate[T](times: int) -> Enumerable[T]

Enumerable<T> replicate<T>(int times);
```

## reverse
Inverts the order of the elements in a sequence. Reverse is really pointless. It is already found on the list class, and while this is technically
delayed execution, it can only work by going through to the end of the enumerable.

```
def reverse[T]() -> Enumerable[T]

Enumerable<T> reverse<T>();
```

## rightJoin
A friendly helper to create a right left outer join. This follows the pattern of innerJoin(), which combines the two key lookups and equality comparer into a single function input. This is JOIN-only (not in C#)

```
def rightJoin[T, TSecond, R](second: Iterable[T], on: Predicate[T, TSecond], outputFunction: Func[T, TSecond, R] = None) -> Enumerable[R]

Enumerable<R> rightJoin<T, TSecond, R>(Iterable<TSecond> second, Predicate<T, TSecond> on, Func<T?, TSecond, R> outputFunction);
Enumerable<(T?, TSecond)> rightJoin<T, TSecond>(Iterable<TSecond> second, Predicate<T, TSecond> on);
```

## select
projects each element of a sequence into a new form by calling a transformation function on each element. Optionally, the transformation function can receive the index as a second argument

cast() is mapped to select() because in Python, cast() doesn't exist

```
def select[T, TOut](outputFunction: Union[Func<[T, TOut], Func[T, int, TOut]]) -> Enumerable[TOut]

Enumerable<TOut> select<T, TOut>(Func<T, TOut> outputFunction);
Enumerable<TOut> select<T, TOut>(Func<T, int, TOut>) outputFunction);
```

## selectMany
Projects each element of a sequence to an IEnumerable<T>, and flattens the resulting sequences into one sequence using a selector function. optionally, the transformation function can receive the index as a second argument. an optional output transformation function processes the output of the selector function to produce an output

```
def selectMany[T, TElement, R](subSelectFunction: Union[Func[T, Iterable[TElement]], Func[T, int, Iterable[TElement]]], 
    outputFunction: Func[T, TElement, R] = None) -> Enumerable[Union[R, TElement]]

Enumerable<R> selectMany<T, TElement, R>(Func<T, Iterable<TElement>> subSelectFunction, Func<T, TElement, R> outputFunction);
Enumerable<R> selectMany<T, TElement, R>(Func<T, int, Iterable<TElement> subSelectFunction, Func<T, TElement, R> outputFunction);
Enumerable<TElement> selectMany<T, TElement>(Func<T, Iterable<TElement>> subSelectFunction);
Enumerable<TElement> selectMany<T, TElement>(Func<T, int, Iterable<TElement> subSelectFunction);
```

## sequenceEqual
Determines whether two sequences are equal by comparing their elements. an optional equality comparer can be supplied

```
def sequenceEqual[T](second: Iterable[T], comparer: IEqualityComparer[T] = None) -> boolean

bool sequenceEqual<T>(Iterable<T> second);
bool sequenceEqual<T>(Iterable<T> second, IEqualityComparer<T> comparer);
```

## single
Returns the last element in a sequence, throwing an exception if the sequence is empty. optional filter condition can be supplied. This condition can optionally take the index as the second argument (this is not provided by the C# version)

```
def single[T](filterFunction = None) -> T

T single<T>();
T single<T>(Predicate<T> filterFunction);
T single<T>(Predicate<T, int> filterFunction);
```

## singleOrDefault
Returns the last element in a sequence, throwing an exception if the sequence is empty. optional filter condition can be supplied. This condition can optionally take the index as the second argument (this is not provided by the C# version. 

If the filtered sequence is empty, it returns the default value. The default value is provided by a parameter or is None. (Note that in Python, unlike C#, there's no way to know what type a sequence is supposed to have, especially not an empty sequence.)

```
def singleOrDefault[T](filterFunction = None, defaultValue = None):

T? singleOrDefault<T>();
T singleOrDefault<T>(T defaultValue);
T? singleOrDefault<T>(Predicate<T> filterFunction, T? defaultValue = None);
T? singleOrDefault<T>(Predicate<T, int> filterFunction, T? defaultValue = None);
```

## skip
Bypasses a specified number of elements in a sequence and then returns the remaining elements

```
def skip[T](count: int) -> Enumerable[T]

Enumerable<T> skip<T>(int count);
```

## skipLast
Returns a new enumerable collection that contains the elements from source with the last count elements of the source collection omitted

```
def skipLast[T](count: int) -> Enumerable[T]

Enumerable<T> skipLast<T>(int count);
```

## skipWhile
Bypasses elements in a sequence as long as a specified condition is true and then returns the remaining elements. optionally, the filter function can receive the index as a second argument

```
def skipWhile[T](filterFunction: Union[Predicate[T], Predicate[T, int]]) -> Enumerable[T]

Enumerable<T> skip<T>(Predicate<T> filterFunction);
Enumerable<T> skip<T>(Predicate<T, int> filterFunction);
```

## step
returns every "step" items from a sequence. This is a new item that I added because I thought it might be useful. Python's negative steps, which reverse the order, are not supported. You can use take() with the sliceObject input or you can call reverse() first.

```
def step[T](step: int) -> Enumerable[T]

Enumerable<T> step<T>(int step);
```

## sum_
Computes the sum of the sequence of values that are obtained by invoking an optional transform function on each element of the sequence

```
def sum_[T](outputFunction = None) -> numeric

numeric sum_<T>());
numeric sum_<T>(Func<T, numeric> outputFunction);
numeric sum<T>(ETC); /* name exists on class method */
```

## take
Returns a specified number of contiguous elements from the start of a sequence. 

The C# version also allows you to pass a Range object which has a start and an end. In C#, this is start..end. In Python, this is equivalent to a slice object, which you can create using syntax "slice(start,end)" (you can't just say [start:end] as that'll give you a syntax error). In C#, ranges have no "step" property, so handling for the python step is being added.

Be warned about the built-in slice constructor: slice(2) isn't slice(2, None) but slice (None, 2).

The JavaScript version of this library takes start as a separate parameter, as a workaround for ranges not being a part of the language. For the sake of consistency, that will be supported also.

```
def take[T](count: int = None, skip: int = 0, sliceObject: slice = None) -> Enumerable[T]

Enumerable<T> take<T>(int count, int skip = 0);
Enumerable<T> take<T>(slice sliceObject);
```

## takeLast
Returns a new enumerable collection that contains the last "count" elements from source

```
def takeLast[T](count: int) -> Enumerable[T]

Enumerable<T> takeLast<T>(int count);
```

## takeWhile
Returns elements from a sequence as long as a specified condition is true. Optionally, the filter function can receive the index as a second argument

```
def takeWhile[T](filterFunction: Union[IPredicate[T], IPredicate[T, int]]) -> Enumerable[T]

Enumerable<T> takeWhile<T>(IPredicate<T> filterFunction);
Enumerable<T> takeWhile<T>(IPredicate<T, int> filterFunction);
```

## thenBy
sorts a partially sorted enumerable by an optional key selector function, or by it takes an optional comparer function

```
# only on OrderedEnumerable

def thenBy[T, TKey](keySelector: Func[T, TKey] = None, comparer: IComparer[TKey] = None) -> OrderedEnumerable[T]

OrderedEnumerable<T> thenBy<T, TKey>(Func<T, TKey>? keySelector = None, IComparer<TKey>? comparer = None);
```

## thenByDescending
reverse sorts a partially sorted enumerable by an optional key selector function, or by itself. takes an optional comparer function

```
# only on OrderedEnumerable

def thenByDescending[T, TKey](keySelector: Func[T, TKey] = None, comparer: IComparer[TKey] = None) -> OrderedEnumerable[T]

OrderedEnumerable<T> thenByDescending<T, TKey>(Func<T, TKey>? keySelector = None, IComparer<TKey>? comparer = None);
```

## toArray
Returns a Python list containing the sequence values

```
def toArray[T]() -> List[T]

List<T> toArray<T>();
```

## toDictionary
Returns a dict with specified keys and values based on a keySelector function and an optional element selector function. Note that in general, objects don't make good keys, but this will let you use them

The C# ability to send a non-default equality comparer is not included because Python dicts do not allow custom equality.
If you want, you can modify the __hash__, __eq__ methods on the items themselves, but that is not controlled by the collection.

```
def toDictionary[TKey, TElement](keySelector: Func[T, TKey], elementSelector: Func[T, TElement] = None) -> Dict[T, TKey, TElement]

Dict<TKey, TElement> toDictionary<T, TKey, TElement>(Func<T, TKey> keySelector, Func<T, TElement> elementSelector);
Dict<TKey, T> toDictionary<T, TKey, TElement>(Func<T, TKey> keySelector);
```

## toHashSet
Returns a Set from an enumerable. 

The C# ability to send a non-default equality comparer is not included because Python sets do not allow custom equality.
If you want, you can modify the __hash__, __eq__ methods on the items themselves, but that is not controlled by the collection.

```
def toHashSet[T]() -> Set[T]

Set<T> toHashSet<T>();
```

## toList
Returns a Python list containing the sequence values

```
def toList[T]() -> List[T]

List<T> toList<T>();
```

## toLookup
Returns a defaultdict(list) with specified keys and values, based on a keySelector function and an optional element selector function. A defaultdict(list) is like a dict except it allows multiple values to be set for a given key.

The C# ability to send a non-default equality comparer is not included because Python sets do not allow custom equality.
If you want, you can modify the __hash__, __eq__ methods on the items themselves, but that is not controlled by the collection.

Note that in general, objects don't make good keys, but this will let you use them

```
def toLookup<T, TKey, TElement>(keySelector: Func[T, TKey], elementSelector: Func[T, TElement] = None) -> DefaultDict[List][TKey, Union[T, TElement]]

DefaultDictList<TKey, T> toLookup<T, TKey, TElement>(Func<T, TKey> keySelector);
DefaultDictList<TKey, TElement> toLookup<T, TKey, TElement>(Func<T, TKey> keySelector, Func<T, TElement> elementSelector);
```

## tryGetNonEnumeratedCount
Try to return the length of the source. Only possible if exhausted.

```
def tryGetNonEnumeratedCount(dictionary: Dictionary["value", int] = None) -> boolean

bool tryGetNonEnumeratedCount();
bool tryGetNonEnumeratedCount(Dictionary<string, int> dictionary); /* only the key "value" is updated */
```

## union
concatenates two sequences returning the set sequence. optional equality comparer can be supplied to compare values

```
def union[T](second: Iterable[T], comparer: IEqualityComparer[T] = None) -> Enumerable[T]

Enumerable<T> union<T>(Iterable<T> second);
Enumerable<T> union<T>(Iterable<T> second, IEqualityComparer<T> comparer);
```

## unionBy
concatenates two sequences returning the set sequence based on keys returned by a key selector function. optional equality comparer can be supplied to compare values

```
def unionBy[T](second: Iterable[T], keySelector: Func[T, TKey], comparer: IEqualityComparer[T] = None) -> Enumerable[T]

Enumerable<T> unionBy<T, TKey>(Iterable<T> second, Func<T, TKey> keySelector, IEqualityComparer<TKey>? comparer = None);
```

## where
Filters a sequence of values based on a predicate. Optionally, the filter function can receive the index as a second argument

```
def where[T](filterFunction: Union[Predicate[T], Predicate[T, int]): -> Enumerable[T]

Enumerable<T> where<T>(Predicate<T> filterFunction);
Enumerable<T> where<T>(Predicate<T, int> filterFunction);
```

## zip_
Produces a sequence of tuples with elements from two or three specified sequences. In place of a third sequence, a function can be provided that combines the first two.

```
def zip_[T, TSecond](second: Iterable[TSecond], third: Union[Iterable[TSecond], Func[T, TSecond, TThird]] = None) -> Enumerable[Union[(T, TSecond), (T, TSecond, TThird)])]

Enumerable<(T, TSecond)> zip_<T, TSecond>(Iterable<TSecond> second);
Enumerable<(T, TSecond, TThird)> zip_<T, TSecond, TThird>(Iterable<TSecond> second, Iterable<TThird> third);
Enumerable<(T, TSecond, TThird)> zip_<T, TSecond, TThird>(Iterable<TSecond> second, Func<T, TSecond, TThird> third);
Enumerable<(T, TSecond, TThird)> zip(ETC); /* name available on class method */
```

## static Enumerable.range()
return an enumerable containing count number of integers in a range, starting with start

```
@staticmethod
def range(start: int, count: int) -> Enumerable[int]

static Enumerable<int> range(int start, int count);
```

## tatic Enumerable.repeat()
return an enumerable containing element count number of times

```
@staticmethod
def repeat[T](element: T, count: int) -> Enumerable[T]

static Enumerable<T> repeat(T element, int count);
```
