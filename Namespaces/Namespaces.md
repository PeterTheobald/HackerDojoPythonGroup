# Namespaces, Scope, Closures and Decorators
## Variables recap

In Python all variables are names that point to values. Picture the values in little boxes in memory. Two variables (names) can point to the same value (same box) or to two different boxes.

``` python

>>> x=300
>>> y=x    # assign y to the same box as x
>>> z=300
>>> 
>>> x==y
True
>>> x==z
True
>>> x is y
True
>>> x is z  # same value but different box
False
```

Python tries to save space by making all variables that point to small ints (256 or under) and small strings point to the same box in memory.

``` python

>>> x=100
>>> y=100
>>> x is y
True
# Python was smart enough to reuse the same box in memory for numbers less than 257
>>> x="hello"
>>> y="hello"
>>> x is y
True
# Also smart enough to reuse the same box in memory for small literal strings
>>> a=x+y
>>> b=x+y
>>> a==b
True
>>> a is b
False
# But this was too complicated to recognize they are the same value (because string interning is done at compile time not run time)
```

Any time you reassign a variable it makes a new box. It does NOT change the value in the box.

``` python

>>> x=5
>>> id(x)
9784992
>>> y=x
>>> id(y)
9784992
>>> x=x+1
>>> id(x)
9785024
>>> x
6
>>> y
5
```

## Mutable vs Immutable

There are certain data types such as List, Dict, Set, and custom Classes that have multiple values inside them. These types follow the same rule that assigning them makes a new box. But you CAN change one of the values inside them without creating a new box.

``` python

>>> x=[1,2,3]
>>> y=x
>>> x is y
True
>>> id(x), id(y)
(140569748543872, 140569748543872)
# Both x and y point to the same box

>>> y=[1,2,3]
# reassign y to a new value; Even though it has the same values it gets a NEW BOX
>>> x==y
True
>>> x is y
False
>>> id(x), id(y)
(140569748543872, 140569748467200)

>>> y=x
>>> x is y
True
# Both x and y point to the same box again

>>> y[1]="changed value"
# Don't reassign the value of y; Change the value of one of it's items
>>> x
[1, 'changed value', 3]
>>> y
[1, 'changed value', 3]
>>> x is y
True
```

Data types that can ONLY be reassigned to a new value in a new box are called IMMUTABLE. These data types include int, float, str, bool, frozenset, and interestingly tuple which looks like a list but the items can't be changed.
Data types that allow you to change one of their items are called MUTABLE. These data types include list, dict, set and custom class objects.

Usually you don't have be aware of this. It only matters when you pass a value as an argument to a function, and that function changes the value inside it. If the function reassigns it's local variable it doesn't affect the caller's variable. If the function changes one of the items inside a MUTABLE data type it changes the caller's copy as well, since they both point to the same box.

``` python

>>> def ch_ch_ch_changes1( l):
...     l=[ 1, 2, 3, "new values"]
...
>>> def ch_ch_ch_changes2( l):
...     l[2]="new value"
...
>>> x=[1,2,3]
>>> ch_ch_ch_changes1(x)
>>> x
[1, 2, 3]
>>> ch_ch_ch_changes2(x)
>>> x
[1, 2, 'new value']
```

## Namespaces

Namespaces are how Python organizes all of the variable names and function names in your program. There are 5 types of namespaces:

1. Built-in
2. Global
3. Module
4. Local
5. Enclosing or non-local

Built-in: Built-in names are all of the variables and functions that are built into Python and always available to you at any place in the code. These are kept in the dictionary-like object `__builtins__`. We can look inside it with `dir(__builtins__)`.

Global: Global names are all of the variables and functions that are defined at the top level of your main Python file. These are kept in the dictionary returned by `globals()`. We can look inside it with `dir()` or with `globals().keys()`.

Module: Module names are all of the variables and functions that are defined at the top level of any other python modules (files) used by your program. You gain access to them by importing them.

``` python
module.py:

mod_var=1
def mod_function():
  pass

>>> import module      <-- import module into it's own MODULE namespace
>>> dir(module)
['__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'mod_function', 'mod_var']

>>> mod_var
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'mod_var' is not defined
>>> module.mod_var
1
>>> from module import mod_var    <-- import it into the GLOBAL namespace
>>> mod_var
1
```

Local: Local names are all of the variables and functions that are defined INSIDE a function definition. They are kept in the dictionary returned by `locals()`. We can look inside it with `locals().keys()`. This namespace is created when the function begins and cleaned up when the function returns. This means all of the local variables in a function disappear when the function returns. Python keeps track if any global or caller variables are pointing to the same values as the local variables. When the function returns if nothing is referencing the values anymore they are freed.

``` python
>>> def inc(a):
...   a=a+1
...   print(a)
...
>>> x=10
>>> inc(x)
11
>>> x
10
>>> a
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'a' is not defined

>>> def inc(a):
...   a=a+1
...   print(locals())
...
>>> inc(10)
{'a': 11}
```

You can list the names in the local namespace with `dir(locals())`

Enclosing or non-local: In Python you can defined a function inside another function. This is called an INNER FUNCTION.
Enclosing or non-local names are the variables and functions that are defined in a function definition that is one level higher than the INNER FUNCTION.

``` python

>>> global_var = "global"

>>> def outer_func():
...     # Nonlocal scope
...     nonlocal_var = "nonlocal"
...     def inner_func():
...         # Local scope
...         local_var = "local"
...         print(f"In the '{local_var}' scope!")
...         print(f"In the '{nonlocal_var}' scope!")
...         print(f"In the '{global_var}' scope!")
...     inner_func()
...

>>> outer_func()
In the 'local' scope!
In the 'nonlocal' scope!
In the 'global' scope!
```

In Python functions are "first-class citizens" and their definitions can be assigned to variables and passed around just like any other data type. This means the outer function can return the inner function to the caller so it can be used after outer function has finished and been cleaned up.

``` python

>>> def outer():
...     def inner(a):
...       return a*-1
...     return inner
...
>>> f=outer()     <-- the name "inner" has been lost, but the definition lives on
>>> f(100)
-100
```

## Scope

When you reference a variable name, which one will Python use? It will first look for the variable in the LOCAL scope, then the ENCLOSING (non-local) scope, then the GLOBAL scope, then the BUILT-IN scope in that order.  Variables in MODULE scopes are only accessible when references directly using their module names.

``` python

>>> x = "global"

>>> def outer():
...     x = "enclosing"
...     def inner():
...         x = "local"
...         print(x)
...     inner()
...

>>> outer()
local
```

Careful! You can define a name in the global or local scope that will be found first before a built-in!

``` python

>>> max(10,99,1)
99
>>> def max(*l):
...   return "Nyah nyah you can't max"
...
>>> max(10,99,1)
"Nyah nyah you can't max"
```

But you can still access the built-in name explicitly:

``` python

>>> import builtins
>>> builtins.max(10,99,1)
99
```

or delete your conflicting name:

``` python

>>> del max
>>> max(10,99,1)
99
```

You can access GLOBAL and NON-LOCALS from inside a function.

``` python

>>> def f():
...   global x
...   x="new value"
...
>>> x=3
>>> f()
>>> x
'new value'
```

``` python

>>> def outer():
...   x=99
...   def inner():
...     nonlocal x
...     x=1
...   inner()
...   print(x)
...
>>> outer()
1
```

## Closures

If you return an inner function from an outer function, the caller can use the inner function but there can be a tricky problem. What if your inner function uses enclosing nonlocal variables from the outer function? When the outer function returns, normally it would clean up and free it's variables. But the inner function it returned is still in use and needs those enclosing nonlocal variables. 

Python will detect this and it won't clean up the outer function's variables. It will keep them in a *closure* , which is a space for all of the outer function's variable's to live until all references to the inner function are gone and the inner function and the closure can be freed.

``` python

>>> def inc_by_x( x):
...   inc=x
...   def inner( n):
...     return n+inc
...   return inner
...
>>> f=inc_by_x(10)
>>> f(1)
11
>>> f(100)
110
```

_Note: the variable 'inc' wasn't necessary. I could have just used 'x' because arguments count as enclosing nonlocal variables._

``` python

>>> def counter():
...   count=0
...   def inner(n):
...     nonlocal count
...     count+=n
...     return count
...   return inner
...
>>> f=counter()
>>> f(10)
10
>>> f(5)
15
>>> f(100)
115
>>> g=counter()
>>> g(2)
2
>>> g(2)
4
>>> f(0)
115
```

Note: the second call to `g=counter()` created a NEW closure.

We don't need to give the inner function a name, since we never use it.

``` python

>>> def inc_by_x(x):
...   return lambda n: n+x   # <-- lambda anonymous function
...
>>> f=inc_by_x(10)
>>> f(21)
31
```

Some languages call these examples "factory functions" because they are functions that build new functions.

Where does Python keep a closure in memory? It attaches an `__closure__` attribute to the closure function. This `__closure__` attribute holds all of the enclosed nonlocal variables (in a mostly non useful way for us).

``` python

>>> f=inc_by_x(10)
>>> f(21)
31
>>> f.__closure__
(<cell at 0x7fc4a62b44c0: int object at 0x954f40>,)
```

## Decorators

A decorator is a way to modify a function without altering it's source code. You write it as a closure that takes an input function and does extra behaviors before and after calling the input function to give it extra functionality. Python adds a nice syntax to use decorators.

``` python

>>> def timed(func):
...     def wrapper(*args, **kwargs):
...         start = time.perf_counter()
...         result = func(*args, **kwargs)
...         end = time.perf_counter()
...         print(f"{func.__name__} took {end - start:.6f} seconds")
...         return result
...     return wrapper

>>> @timed
... def slow_function():
...     time.sleep(1)
...

>>> slow_function()
slow_function took 1.001686 seconds
```



## Closures vs. Classes

Closures are a way to retain state between function calls and you can see there are many similarities between Closures and Classes. In functional programming languages Closures are used to do very similar work as Classes in Object Oriented Languages. Python supports both.

Here is an example of writing a Stack as a Closure instead of as a Class:

``` python

def Stack():
  _items = []

  def push(item):
    _items.append(item)

  def pop():
    return _items.pop()

  def closure():   # <-- create a dummy placeholder to attach the "methods"
    pass

  closure.push = push
  closure.pop = pop
  return closure

>>> stack = Stack()
>>> stack.push(1)
>>> stack.push(2)
>>> stack.push(3)
>>> stack.pop()
3
>>> stack._items
Traceback (most recent call last):
    ...
AttributeError: 'function' object has no attribute '_items'
```

Interestingly, Python Classes don't really enforce private class variables being private. A caller can break the encapsulation by directly accessing instance.\_items , but with a Closure we have real enforced privacy. There is no way for a caller to access \_items because the name isn't available to the caller.


