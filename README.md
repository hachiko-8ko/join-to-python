# JOIN to Python
## Implemention of LINQ to Objects in Python

JOIN to Python is a python implementation of [JOIN to Javascript](https://github.com/hachiko-8ko/join-to-javascript), a library that allows you to join lists to other lists, select, order, etc. It also adds a few methods that I wanted to do myself (outer joins are painful and hacky in LINQ so I made better methods). There are other ways to do most of these things, using filter(), map(), list comprehensions, and so on, but as far as I know there's not a complete fluent API, partly because it's very difficult to do fluent APIs based on the Python array.

When possible, JOIN defers execution in the same way that LINQ provides deferred execution, waiting until you fetch the data by iterating it, calling toArray(), or fetching a single item. This means, for example, if you fetch `integers/where(row => isPrime(row))/first()` it will halt on the first prime, unlike `drain(filter(lambda: row => isPrime(row), integers))[0]` which processes every row in the array.

Only LINQs fluent syntax is included. You would need to be able to make custom operators to do query syntax, and that's not allowed in Python.

[System.Linq Documentation](https://docs.microsoft.com/sv-SE/dotnet/api/system.linq.enumerable?view=net-6.0)

### Caveats

#### Slash functions used in place of dot methods

Python has nothing like C#'s extension methods (syntatic sugar that turns `enumerable.Select(func)` into `StaticClass.Select(enumerable, func)`). It also doesn't allow you to monkey-patch built-ins like List (I'm ignoring forbiddenfruit here, because it has a dependency on CPython, and I don't want to limit it in that way). It also doesn't allow you to create custom operators. When you take all these things, it appears that it's impossible to write queries like `list1.join(list2, lambda l: l.id, lambda r: r.id, lambda l, r: { "Name": l.Name, "Address": r.Street + " " + r.City })` without wrapping list1 in `Enumerable(list1)` which is messy especially if you're doing it more than once.

But wait. It does allow you to override the behavior on a handful of built-in operators, so if you're OK with using a different symbol, you can make it happen. The symbol I decided on is / (forward slash) because it's the only single-key operator available that did not require pressing shift or moving up to the top row. Admittedly, this is only true in QWERTY and might not be true everywhere. So choosing slash is a bit selfish. It's also right next to the period so it doesn't require a lot of change to write `list1/join(list2, lambda l: l.id, lambda r: r.id, lambda l, r: { "Name": l.Name, "Address": r.Street + " " + r.City })`. 

`/join()` calls a function named "join" that creates an enumerable if necessary, and then calls the method `join()` on it.

You can avoid the slashy nonsense by taking time to build your enumerables first. The slash functions are only necessary to query non-Enumerables (and optional otherwise).

```
enum = makeEnumerable(myList) # or myList/asEnumerable()
return enum.where(lambda x: x.isActive).select(lambda person: { "name": person.name }).toList() # much cleaner but takes 2 lines
```

#### Python order of operations: dots come before slashes

You probably don't want to mix slashes and dots. (list/join()).toArray() will work but list/join().toArray() will not (note the parenthesis). The reason is order of operations. Python calls toArray() on the join function, NOT the OUTPUT of the join function, because . is considered first. There is no way to intercept this. It's called before the call method that does all the preceding work, so JOIN would need to be able to look into the future to see what to return.

This is a kick in the teeth because it messes up a common C# idiom: `foo = query.first().foo` but there's nothing I can do about it aside from using forbiddenfruit to monkeypatch the C library. In general, one-liners aren't considered Pythonic. Of course, C# itself breaks the C# idiom at times (`var foo = await something().foo; /* compilation error */`) so it's not really special to Python.

#### Name conflicts

Seven functions needed new names: _all, any, max, min, sum, except, zip_. Making new functions with those names would overwrite global functions, and except can't be used for anything. They have had an underscore appended. But it's not enough to require changing everything from the linq method names, especially since in all but escept, the Enumerable methods still exist under the matching names (`Enumerable(data).any()` works as expected).

### Installation and use

1. Download the repository to the machine where you want to install JOIN to Python.
2. From inside the directory where you downloaded the files, execute `python3 setup.py build`.
3. Execute `python3 setup.py install` to install as system (requires root) or `python3 setup.py install --user` to install under your user. This, of course, is assuming you have python3 aliased to your python 3, to allow you to have python2 and python3 living side by side.

To use it, include this in your python script:
```
from join_to_python import *
```

### Documentation and examples

See [IQueryable.README.md](https://github.com/hachiko-8ko/join-to-python/blob/master/src/IQueryable.README.md) for complete documentation. See the test cases in the [tests](https://github.com/hachiko-8ko/join-to-python/blob/master/src/tests) folder for detailed examples of all the methods.
