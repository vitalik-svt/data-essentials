- [Python](#python)
  - [Built-in Sequences, Objects, Functions](#built-in-sequences-objects-functions)
  - [Functions](#functions)
  - [Iterable, Iterators, Generators](#iterable-iterators-generators)
  - [Classes, Objects](#classes-objects)
  - [Modules, Packages](#modules-packages)
  - [Exceptions](#exceptions)
  - [Decorators](#decorators)
  - [Descriptor (doc)](#descriptor-doc)
  - [Processes, Threads, AsyncIO  (nice video about async)](#processes-threads-asyncio--nice-video-about-async)
  - [Input/Output](#inputoutput)
  - [Python testing](#python-testing)
  - [Virtual Environment](#virtual-environment)
- [Refactoring](#refactoring)
- [Patterns](#patterns)
- [Python tasks](#python-tasks)
  - [Questions](#questions)
  - [Coding tasks](#coding-tasks)
- [Additional Info](#additional-info)


# Python

That document based on https://github.com/yakimka/python_interview_questions

## Built-in Sequences, Objects, Functions

### Data types in python:

- mutable
    - list
    - dict
    - set
- immutable
    - tuple
    - string
    - int/float
    - frozenset
    - bool

### What is difference between '==' and 'is'?

- '==' compare operands by value
- 'is' compare operands by addresses in memory


### How arguments sets in functions?

- mutable arguments transmitted in function by link on object
- immutable objects transfmitted by value 

There is two type of arguments in Python: positional and keyword (named) arguments.
Positional arguments must be included in the correct order. Keyword arguments are included with a keyword and equals sign. 

`*args` (tuple) - argument, that can contain unknown amount of positional arguments
`**kwargs` (dict) - same, but for keyword arguments

### What is sequence

Due to duck-typing in python - sequence is object, that supports this methds:
`__getitem__()` - access to elements by index
`__len__()` - get number of elements in object. this method called by built-in function len() (if implemented in object)

Some of the sequences can support other methods:
`__contains__()` - check if element presented in the sequence
`__resersed__()` - reverse elements order
etc.

General built-in sequences:
- list	(mutable)
- tuple	(immutable)
- str 	(immutable)
- range (immutable)

### General sequence operations

| Operation | Result |
| --------- | ------ |
| `x in s` | True if an item of s is equal to x, else False| 
| `x not in s`  | False if an item of s is equal to x, else True |
| `s + t` | the concatenation of s and t |
| `s * n` or `n * s` | equivalent to adding s to itself n times. That's why you canmultiple str by int 'aha' * 3 and get 'ahaahaaha'|
| `s[i]` | Slicing: i-th item of s, started from 0 |
| `s[i:j]` | slice of s from i to j |
| `s[i:j:k]` | slice of s from i to j with step k |
| `len(s)` | length of s |
| `min(s)` | smallest item of s |
| `max(s)` | largest item of s |
| `s.index(x[, i[, j]])` | index of the first occurrence of x in s (at or after index i and before index j) |
| `s.count(x)` | total number of occurrences of x in s|

And if sequence is mutable (list), they will probably support this operations

| Operation | Result |
| --------- | ------ |
| `s[i] = x` | i-th element of s will replaced by x |
| `s[i:j] = x` or `s[i:j:k] = x` | elements from i to j (with k step) replaced by elements of x (should be iterable) |
| `s.append(x)` | appends x as one element to s sequence. in-place operation |
| `s.extend(x)` | appends all elements of x (must be iterable) to the end of s sequence |
| `s.clear()` | delete all the elements |
| `s.insert(i, x)` | insert x on i'th position in s |
| `s.pop(i)` | delete i'th element from sequence and returns it |
| `s.remove(x)` | delete first x in sequence | 


### Strings in python

in Python 3 there is only regular unicode string, that can be represented in different ways:
- r'string' - raw 
- u'string' - unicode
- b'string' - bytes

Strings are immutable, so you can't remove or change something. So, whtn you format, concatenate or replace something in string, that function bring back to you new string (new object with different id)

Some useful operations with strings:
| Operation | Result |
| --------- | ------ |
| `', '.join([a, b, c]])` | `a, b, c`  |
| `somestring.split(x)` | splits string by x symbol and returns list |
| `somestring.encode()` | string -> bytes. Good practice is to provide encoding clearly! 'utf-8' or something like that|
| `somestring.decode()` | bytes -> string. Provide encoding! |

### Some examples around sequences

**list** 
Mutable object

Particulary in python Lists are not linked lists. They are Mutable arrays (C-like)
Created in that particular time when declared, and stored in continuous place in memory.
So it's good for calling elements by index (it's O(1))

When we left only few empty places, lists copied in another area of memory, simoultaniously with increasing size

**Tuple**
Immutable object
Under the hood it's the same as list, but immutable

**Array**
it's C-type array.
Like tuple, but containts only objects of one type, which takes much less space

```python
import array
array.array('i', [1,2,3])
```

**Range**

Object, that returns by range function. It's not a generator
range(i, j)

Can be used in list comprehensions:

`[x for x in range(i, j)]`

### How you can get rid of duplicates in your list?

1. Transform it to set (because set contains only unique values)

`new_list = list(set(original_list))`

But that's not guarantre order, because set it's just a heap of elements without indexes

2. From python 3.7 you can use dict, because it's like set (in sense that contains only unique keys), and also it's guarantee that data will stored in the same order as inserted, so:

`new_list = list(dict.fromkeys(original_list))`

But! 
You can only place hashable objects, so it's not 100% cases option

Before 3.7 you can use
from Collections import OrderedDict

3. You can use list comprehention:

```python
new_list = []
[new_list.append(x) for x in original_list if x not in new_list]
```

4. Or just good old loop:

```python
new_list = []
for x in original_list:
	if x not new_list:
		new_list.append(x)
```

### Multi assignment

nice thing in Python, that you can assign objects to multiple variables (tbh it's more link varibales with existing objects)

```python
def some_func():
	return (1, 2, 3)

a, b, c = some_func()
```

### Hashable objects

It's objects, that implenents `__hash__` method, that returns some value, that don't change over time.
for example, you can use only hashable objects in keys for dict, or store only hashable in sets
it's because under the hood of dicts and sets is hashmap

also, you need to implement `__eq__` method, which used for comparison with different objects

### Sets

regular set - mutable
frozenset - immutable

Usually sets used for some mathematical operations, like:
Union, Intersection, Differences

Sets counts like similar, when all elements of sets are similar

### Mappers, Dicts

Mapper (mapping) object - it's container object that supports access to elements by keys.
Dict - it's most understandable example of mapping, but there is also different mappers.

Note, that you can use numbers as key to dicts, but also note, that 
1 and 1.0 same number, which can be brake your dict

Nice dict functions:
| Operation | Result |
| --------- | ------ |
| `dct.items()` | it's like enumerate over key and value pairs at the same time  |
| `dct.keys()` | sequence of keys |
| `dct.values()` | sequence of values |
| `dct.get(key, default_value)` | doesn't call exception, if key doesn't exist, unlike `dct[key]` |

When you iterate over dict (`for x in dct`), you iterates over keys!

Also nice example of creating dict from two sequences (of the same length)

```python
keys = ['a', 'b', 'c']
values = [1 ,2 ,3]
dct = dict(zip(keys, values))
```

`zip()` creates list of pairs (in that case), and `dict()` considers that pairs as key, value pairs

### Hashmap

it's what under the hood of dicts.
hasmap it's sparse array (python usually reserves around 30% of space blank) for have place to adding new key:values in future.
When dict about to reach limit of space, it's copying into other place in memory

So, when you call `dct[key]`, python calls `hash(key)` and seeks result in hashmap

Also there is collision, when hash() returns same result for different values. 
In that case they stored, let's say, in the same cell:

| hash_key | dict_key |
| --------- | ------ |
| a | 'Anna' |
| a | 'Boris' |
| c | ['Carl', 'Charles'] |
| d | 'Denis' |


### Search in sequences

- O(1) to find some element by key in Sets and Dicts
- O(N) to find element in List and Tuples
- O(1) to find element by index in Tuple
- O(N) to find element by index in List

## Functions

function defines with def keyword

parameter is the variable listed inside the parentheses in the function definition.
argument is the value that are sent to the function when it is called.

```python
def functionname(parameter):
	pass


functionname(argument)
```

### Args and kwargs

it's agreement to use that particular words in function declaration.

```python
def some_func(*args, **kwargs):
	pass
```

That means, that you can pass to that function any value of arguments, and access them in function with that names
args - is for position arguments
kwargs - is for named arguments

if you don't pass anything, that can be unpacked to args and kwargs, they will be empty tuple and dict, not None

Note: 
It's crutial to use immutable objects as default to function!
Because when you call that function many times, it whill use the same object and change it

```python
def foo(bar=[]):
    bar.append(1)
    return bar
foo()
>>> [1]
foo()
[1, 1]
foo()
>>> [1, 1, 1]
``` 

### Lambda functions

It's functions, that doesn't reserve space in namespace, that means python don't need to search them to call.
So it's faster

Note!
You can use in lambda body only expressions

**expression**
it's operators and operands, `x = 3 + 2`, for example

**statement**
In particular instruction for interpreter
like `print`, `pass`, or something 
(*if someone can provide some meaningful description that would be great*) 

### Variables and Arguments

In Python every variable it is pointer.
So when you define variable with object:
`variable = object`

Python creates object, and than **assigns** it with variable

### copy() and deepcopy()

`from copy import copy, deepcopy`

Aaand we slightly go to **copy** (aka **shallow copy**) and **deepcopy** functions, which can be useful to know while working with mutable objects

`b = a.copy()`
returns shallow copy of b and assign it with a
So it returns new object, but with old elements in it

let's assume, that a is a list
if we create shallow copy, python create new list object with different id, but that list will contain links to elements of a list

And if we change that somehow (if list a containts mutable elements), then they will change for b list too

To avoid that you need to use **deepcopy**, function, that recursively copied all nested objects in that list

Also, every object contains link counter, and when it becomes equal to zero, object will be deleted

## Iterable, Iterators, Generators

### Iterable

iterable – Object, that can return values one by one

Implemented methods:

`__iter__()` - returns iterator for given object
OR
`__getitem__()` - old version, or something


Iterable can be used in for loop, or other functions, that expects sequence (sum, min, max, map)

```python
class SomeIterable1(collections.abc.Iterable):
    def __iter__(self):
        pass

class SomeIterable2:
    def __iter__(self):
        pass

print(isinstance(SomeIterable1(), collections.abc.Iterable))
# True
print(isinstance(SomeIterable2(), collections.abc.Iterable))
# True
```

`iter()` functions checks for `__iter__()` method first of all, but if there is no this method, it checks for `__getitem__` then. Thats why you can iterate through strings, even if they doesn't have `__iter__()`. If there is no this methods founded, then `TypeError` will be reisen.

```python
from string import ascii_letters

class SomeIterable3:
    def __getitem__(self, key):
        return ascii_letters[key]

for item in SomeIterable3():
    print(item)
```

### Iterator

Object, that provide data flow.
It has `__next__()` method, that defines how to calculate next value

If there is no data to calculate left, `StopIteration` raisen

Iterator must have `__iter__` methods, which returns self, so Iterator is Iterable, and, let's say, it's overhead onto Iterable

### Comprehentions

`[x for x in range(i, j)]` - returns list from i to j-1
`{x: y for x, i in enumerate(range(i, j))}` - returns dict from i to j-1 
`{x for x in range(i, j)}` - returns set from i to j-1

you can't define tuple comprehention, it need to be mabe like
`tuple([x for x in range(i, j)])`

### Generator

Object, that can be called only once, because it stored only previous 
So you can restart it, because he is don't know where is start

You can implement generators by using **yield** instead of **return**

Simple generator expresstion:
`(x for x in range(i, j))`

it returns one x at a time, and don't stored anything else, so it can be used for infinite sequence without consuming memory

### Yield

The **yield** keyword in Python controls the flow of a generator function. This is similar to a return statement used for returning values in Python. However, there is a difference.

When you call a function that has a **yield** statement, as soon as a **yield** is encountered, the execution of the function halts and returns a generator iterator object instead of simply returning a value. **The state of the function, which includes variable bindings, the instruction pointer, the internal stack, and a few other things, is saved.**

In other words, the **yield** keyword will convert an expression that is specified along with it to a generator iterator, and return it to the caller.

If you want to get the values stored inside the generator object, you need to iterate over it. You can iterate over it using for loops or special functions like **next()**.

### Yield from ([stackoverflow](https://stackoverflow.com/questions/9708902/in-practice-what-are-the-main-uses-for-the-yield-from-syntax-in-python-3-3))

**yield from** establishes a transparent, bidirectional connection between the caller and the sub-generator:

- The connection is "transparent" in the sense that it will propagate everything correctly, not just the elements being generated (e.g. exceptions are propagated).
- The connection is "bidirectional" in the sense that data can be both sent from and to a generator.

```python
def reader():
    """A generator that fakes a read from a file, socket, etc."""
    for i in range(4):
        yield '<< %s' % i

def reader_wrapper(g):
    # Manually iterate over data produced by reader
    for v in g:
        yield v

wrap = reader_wrapper(reader())
for i in wrap:
    print(i)

# Result
<< 0
<< 1
<< 2
<< 3

# So, instead of manually iterating over reader(), we can just yield from it

def reader_wrapper(g):
    yield from g

# And it's like syntacs sugar for for-loop, but let's have a look to other, more important (probably)
# part of yeild from construction
# it's sending information INSIDE (!) generator


def writer():
    """A coroutine that writes data *sent* to it to fd, socket, etc."""
    while True:
        w = (yield)
        print('>> ', w)

def writer_wrapper(coro):
    coro.send(None)  # prime the coro
    while True:
        try:
            x = (yield)  # Capture the value that's sent
            coro.send(x)  # and pass it to the writer
        except StopIteration:
            pass

w = writer()
wrap = writer_wrapper(w)
wrap.send(None)  # "prime" the coroutine
for i in range(4):
    wrap.send(i)

# Expected result
>>  0
>>  1
>>  2
>>  3

# but that also works for wtiter_wrapper!

def writer_wrapper(coro):
    yield from coro

```

### Clousers ([habr](https://habr.com/ru/amp/publications/781866/))

Closure - it's function, that **defined** and **returned** by other function. And also closure have access to objects and values inside parent scope, regarding from where you call clouser

```python
def outers(): 
    n = 2

    def closure(): 
        return n ** 2 
    return closure


closure_foo = outers()      # call main func. it will return closure, and assigns to variable
print(closure_foo)          # <function outers.<locals>.closure at 0x7f254d6fe170> 
num = closure_foo()         # call closure and assigns to variable

print(num)                  # first option to call closure
>> 4 

print(outers()())           # second option to call closure
>> 4
```

See, function still have access to `n` variable, despite it out of their scope

## Classes, Objects

### OOP Concepts

- **Class** - it's blueprint for creating objects, encapsulating data and methods that can operate on that data
- **Object** - it's an instance of class
- **Encapsulation** - Bundling data and methods operating on that data within a class, actually. It's like API
- **Inheritance** - Allows a class to inherit attributes and methods from another class
- **Polymorphism** - enables one interface or method to be used for different data types and classes

### Underscores and access modifiers

- `_foo`- Only a convention. A way for the programmer to indicate that the variable is **private**
- `__foo`- This has real meaning. The interpreter replaces this name with `_classname__foo` as a way to ensure that the name will not overlap with a similar name in another class. So it's like **protected** attribute
- `__foo__`- Only a convention. A way for the Python system to use names that won't conflict with user names.

### Dunder (Magic) methods

- `__init__` - object initializer
- `__add__`-  add to another object
- `__eq__`-  equality check with different object
- `__iter__`- returns iterator
- etc.

### Three types of Methods in class 

1. Object methods

Knows about object state, take *self* argument and modified only object itself

```python

class SomeClass:

    def object_method(self):
        pass
```

2. Class methods
can be defined by decorator @classmethod

Knows about whole class, take *cls* argumant and modified some things in whole class

```python

class SomeClass:

    @classmethod
    def class_method(cls):
        pass
```

3. Statis methods
can be defined by decorator @staticmethod

Knows nothing neither about object ot class. Can be caled without creating an object, from class directly.
Not modifiyng anything. Can be used for some general things, that make sense to put into that class

```python

class SomeClass:
    
    @staticmethod
    def static_method():
        pass
```

Difference:

- A **class method** takes *cls* as the first parameter while a **static method** needs no specific parameters.
- A **class method** can access or modify the class state while a **static method** can’t access or modify it.
- In general, **static methods** know nothing about the class state. They are utility-type methods that take some parameters and work upon those parameters. On the other hand **class methods** must have class (*cls*) as a parameter.

### What is super method in classes?

**Super()** allows you to call methods of the superclass in your subclass. The primary use case of this is to extend the functionality of the inherited method.


### Methods and super() examples

```python

class Human:

    def __init__(self, intro):
        print(f"i'm a {intro}, human being!")


class Employee(Human):

    rating = 10

    def __init__(self, age, name):
        self.age = age
        self.name = name

    # object method with calling super in it
    def introduct_yourself(self, intro):
        super().__init__(intro)

    @staticmethod
    def sample(x):
        print('Inside static method', x)

    @classmethod
    def change_rating(cls, new_rating):
        cls.rating = new_rating


# Static method

# call static method by class, without creating object
Employee.sample(10)

# can be called using object
emp = Employee()
emp.sample(10)

# Class method

ab = Employee(25, 'Alice')
cd = Employee(27, 'Bob')
print(ab.rating)   # will be 1o by default
print(cd.rating)   # will be 1o by default

ab.change_rating(15)
print(cd.rating)     # will be 15, even we change it through ab object

Employee.change_rating(20)
print(cd.rating)     # will be 20, even we change it through Class

# super() function
# If we call
ab.introduct_yourself('employee')

# we will get, because mother class will be called 
"i'm a employee, human being!"
```

### Property vs attribute ([stackoverflow](https://stackoverflow.com/questions/7374748/whats-the-difference-between-a-python-property-and-attribute))


Properties are a special kind of attribute. Basically, when Python encounters the following code:

```python
spam = SomeObject()
print(spam.eggs)
```

it looks up `eggs` in `SomeObject1`, and then examines `eggs` to see if it has a `__get__`, `__set__`, or `__delete__` metho.
If it does, its a property, and Python will call the `__get__` method (since we were doing lookup) and return whatever that
method returns. If it is not a property, then `eggs` is looked up in `spam`, and whatever is found there will be returned.


```python
class A(object):
    _x = 0
    '''A._x is an attribute'''

    @property
    def x(self):
        '''
        A.x is a property
        This is the getter method
        '''
        return self._x

    @x.setter
    def x(self, value):
        """
        This is the setter method
        where I can check it's not assigned a value < 0
        """
        if value < 0:
            raise ValueError("Must be >= 0")
        self._x = value

>>> a = A()
>>> a._x = -1
>>> a.x = -1
Traceback (most recent call last):
  File "ex.py", line 15, in <module>
    a.x = -1
  File "ex.py", line 9, in x
    raise ValueError("Must be >= 0")
ValueError: Must be >= 0
```

### Attribute (Obj vs Class) and Property (Obj vs Class)

```python
class Class:

    attr = 'data attribute of class'

    @property
    def prop(self):
        return('property value of class')

obj = Class()
vars(obj)
# {} - __dict__ of object are empty
obj.attr
# 'data attribute of class' - because object itself doesn't have that attribute
obj.attr = 'data attribute of object'
print(vars(obj))
# {'attr': 'data attribute of object'} - because we create object attribute
obj.attr
#'data attribute of object' - and we can call it
Class.attr
#'data attribute of class' - and class attribute will be the same

# So here we've seen, how object attributes redefines class attributes
# Properties works differently!
# Property - it's property of Class, first of all
# So when you call obj.attr, interpreter will seek it in object, then in class, then in superclass
# But when you call obj.prop, interpreter will seek it in Class first, and then in Object!

# lets see

Class.prop
# <property object as 0x1072b7408> - it's just object of property
obj.prop
# 'property value of class' - when we call property from object, it calculates
obj.prop = 'property value of object'
# AttributeError: can't set attribute - we cant create attribute, and we also cant redefine property, because there is no 
# property set method in our class 
obj.__dict__['prop'] = 'property value of object'
# but we can sett attribute (not property) that way, without calling property by obj.prop
vars(obj)
# {'attr': 'data attribute of object', 'prop': 'property value of object'} - we call it prop, but it's attribute of object!
obj.prop
# 'property value of object' - it's just value of attribute!
Class.prop = 'property value of class_new, but tbh its attribute'
# we can try to reset property of Class, but that will just delete property, and create regular attribute of Class

```

### What is abstract Class?

It's class, from which we can't create an object. Usually we need it to create some 'super' class and create there some needed methods, to necessarily need to be implemented by child classes

```python

from abc import ABC, abstractmethod

# from ABC only
def AbstractClass(ABC):

    # need to be decorated
    @abstractmethod
    def necessarymethod(self):
        pass


def ChildClass(AbstractClass):

    def necessarymethod(self):
        print("look, mom, i've implemented it!")


def AnotherChildClass(AbstractClass):

    def notimplementnecessarymethod(self):
        print("i'm a bad guy")


# so

# this will return error
AbstractClass()


# this will create an object
child = ChildClass()


# this will return error too
badchild = AnotherChildClass()

```

### Metaclass ([info](https://realpython.com/python-metaclasses/#old-style-vs-new-style-classes))

Classes it's instanse of object, but by creating a Metaclass you can change basic object behaviour.
By default, when new instanse of class created, interpreter call basic method `__call__`, which calls `__new__` and `__init__` methods. So you can change something by redefining that methods in your custom Metaclass

```python
def new(cls):
     x = object.__new__(cls)
     x.attr = 100
     return x

Foo.__new__ = new

f = Foo()
f.attr
# 100

g = Foo()
g.attr
# 100
```

But is it really nesessary? You can create same behavior using:
- Inheritance from some class
- Decorator


### Context Manager

it's `with` operator, that define methods:
- `__enter__` - after entering context manager
- `__exit__` - after leaving context manager (in case of exception too)

And in that methods you need to implement all the things. For example, in `with open(file) as f:` in `__exit__` implemented `close` method, so files are getting closed

### Comparing objects

Objects compare by their id mostly, if `__eq__` not reimplemented

## Modules, Packages

### Module

Module - it's element of whole programm, logically separated from another. File, usually

Modules can be united into Packages, and then, into Libraries

Name of module placed in  `__name__` variable. If module not imported, but runned itself `__name__` became `"__main__"`.

### How Python seeks modules

- in directories with launched scripts
- in env variable PYTHONPATH

### Package

It's folder with modules and `__init__.py` in it

### Global keyword

It's used to exactly determine, that variable should be global, so interpreter can not to seek it internal scope (inside function)

You can easily access global variable from function, but modifiying it can cause some problems

```python
a = 5
b = 10

def add():
    c = a + b
    print(c)

add()
# 15 - which is fine

a = 15

def replace():
    b = a + 5
    a = b
    print(a)

replace() 
# will cause the error, because interpreter sees, that we define local variable a (in a=b row), 
# but before that we update a (which we now - is global), so for us it's two different variables.
# but interpreter things it's the same variable, and it will throw exception:
# UnboundLocalError: local variable 'a' referenced before assignment

# So we can easily fix that by using global keyword

x = 15

def replace_global():

    global x

    x += 5
    print(x)

replace_global() 
# which will return 20

# another example is to modifiyng some structures

arr = [10, 20, 30]
 
 
def fun():
    global arr
    arr = [20, 30, 40]
    # nb: if we will not use global, that local arr will be created, and nothing happened in outer scope
 
 
print(arr)
# [10, 20, 30]
fun()
print(arr)
# [20, 30, 40]

```
 
## Exceptions

```python
try:
       # Some Code.... 

except:
       # optional block
       # Handling of exception (if required)
       # it can be multiple except code, so you need to handle exceptions from more specific on top, to more general below
else:
       # execute if no exception
finally:
       # always executed code

```

## Decorators

Object, that incapsulate logic of anything 

```python

def simple_decorator(func):

    def wrapper():
        print('do some before func')
        func()
        print('do some after func')

    return wrapper

# and we can modify our function two ways:

@simple_decorator
def our_func_to_decorate():
    pass


# or
def our_func_to_decorate():
    pass

decorated_function = simple_decorator(our_func_to_decorate)
```

If we want to pass arguments to our function through decorator

```python
def one_more_layer(a=2):
    def simple_decorator(func):
        def wrapper(*args, **kwargs):
            print('do some before func')
            func(*args, **kwargs)
            print('do some after func')
        return wrapper
    return simple_decorator

# and we can modify our function two ways:

@one_more_layer(a=2)
def our_func_to_decorate():
    pass


# or
def our_func_to_decorate( ):
    pass

first_layer_decorator = one_more_layer(a=2)
actually_decorated_function = first_layer_decorator(our_func_to_decorate)
```

## Descriptor ([doc](https://docs.python.org/3/howto/descriptor.html#descriptor-howto-guide))

It's class which defines their own methods `__get__(), __set__(), or __delete__()`. 
When a class attribute is a descriptor, its special binding behavior is triggered upon attribute lookup. 
Normally, using a.b to get, set or delete an attribute looks up the object named b in the class dictionary for a, but if b is a descriptor, the respective descriptor method gets called.  

```python

# The Ten class is a descriptor whose __get__() method always returns the constant 10:

class Ten:
    def __get__(self, obj, objtype=None):
        return 10

# To use the descriptor, it must be stored as a class variable in another class:

class A:
    x = 5                       # Regular class attribute
    y = Ten()                   # Descriptor instance


# An interactive session shows the difference between normal attribute lookup and descriptor lookup:

a = A()                         # Make an instance of class A
a.x                         # Normal attribute lookup
# 5

a.y                         # Descriptor lookup
# 10
```

In the a.x attribute lookup, the dot operator finds 'x': 5 in the class dictionary. In the a.y lookup, the dot operator finds a descriptor instance, recognized by its __get__ method. Calling that method returns 10.

Note that the value 10 is not stored in either the class dictionary or the instance dictionary. Instead, the value 10 is computed on demand.

**Usually descriptors used to perform things dynamically** (That's why they alled descriptors. But it's just my guess) 

```python
import os

# Interesting descriptors typically run computations instead of returning constants:

class DirectorySize:

    def __get__(self, obj, objtype=None):
        return len(os.listdir(obj.dirname))

class Directory:

    size = DirectorySize()              # Descriptor instance

    def __init__(self, dirname):
        self.dirname = dirname          # Regular instance attribute

# An interactive session shows that the lookup is dynamic — it computes different, updated answers each time:

s = Directory('songs')
g = Directory('games')
s.size                              # The songs directory has twenty files
# 20

g.size                              # The games directory has three files
# 3

os.remove('games/chess')            # Delete a game
g.size                              # File count is automatically updated
# 2
```

Besides showing how descriptors can run computations, this example also reveals the purpose of the parameters to __get__(). The self parameter is size, an instance of DirectorySize. The obj parameter is either g or s, an instance of Directory. It is the obj parameter that lets the __get__() method learn the target directory. The objtype parameter is the class Directory.

## Processes, Threads, AsyncIO  ([nice video about async](https://www.youtube.com/watch?v=iG6fr81xHKA))

**Process** - Independent things, that have (no-shared) separated memory, CPU etc. And it's different Python processes!
It doesn't make sense to create more processes than cores/machines

**Multiprocessing** - it's Pure parallelism. Each process launch their Python interpreter, and OS place that processes somehow (usually each per core). Processes doesn't share any memory. We have some additional costs, because launch few separate interpreters - quite heavy. Also we limited by number of cores, even we can add more processes, than cores, least will wait for core to get free to start doing something

**Multithreading** - Thread - it's "subprocess" inside one process. But still, switching between threads handles by OS. Also, because of Python have **GIL** - only one thread can be given by Python to OS to launch it at one time. Threads share memory. You can launch some Threads, and amount will be bigger than amount of processes, but still it's relatively heavy operation.

**GIL** - Global Lock Interpreter. It's Service, that let only one Thread execute Python at once.

**Async** - It's similar to multithreading, but all ruled by Async framework, and actually you. So all the things happend inside one Process, inside one Thread, but you (and Async framework) "simulate" work of OS. And because of that - adding that coroutines - pretty lightweight operations, and tbh - the only reason why you should use AsyncIO, or other similar frameworks: to build some server, that can handle heavy load, for example, because you can create **thousands of coroutines**
Also, you can't use regular python libraries, which have **blocking** functions, that just block flow. Regular time.sleep, for example just will block everything. You need to use special asyncio.sleep

Again: It's like threading, but all the thnigs (changes of threads and so on) you need to write by yourself.
So while in Multithreading are:
1 Process and Many threads (that created and maintained by OS)

But in AsyncIO are:
1 Process, 1 Thread, and "sub-threads", but that "sub-threads" you need to manage (create, kill, stop, get execution from one to another, etc) by yourself, with your code. 

So, AsyncIO it's more lightweight, than threading, but it's different code style, and programming approaches.
Also, it can be used for reducing non-CPU time (IO, like library named, for example)


### When Multiprocessing, and when Multithreading?

Processing - it's mostly for CPU-comsuming operations, but multithreading - it's for operations, that frquently wait for somthing (I/O, requests).

And AsyncIO when you need to do really high amount of things in Parallel (actually, not in parallel, but asyncroniously. So, you try to utlise as much CPU time as possible)

## Input/Output

### json

- `dump` - json -> file
- `dumps` - json -> string
- `load` - file -> json
- `loads` - string -> json

## Python testing

```python
import unittest

def upper(some):
    return some.upper()

class TestSomething(unittest.TestCase):

    def test_upper(self):
        self.assertEqual(upper('foo'), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()
```

## Virtual Environment

- `vitrualenv` - for Python2
- `venv` - from Python3

1. Create vitrual environment folder:
```python
python3 -m venv venv # second venv it's folder to install venv
source env/bin/activate # activate for mac
deactivate # deactivate
```

### Most used linux commands

- **ls** - list of all directory components. `ls -a` shows all files
- **cd** - change directory. `cd yourdirthatinparticulardir`
- **mkdir** - make directory. `mkdir newdir`
- **rm** - remove files and directories 
- **mv** - move/rename
- **cp** - copy
- **pwd** - print working directory
- **chmod** - change files/dirs permissions
- **sudo** - execute command as superuser
- **chown** - change owner
- **cat** - concatenate and show files
- **grep** - seeking info in files
- **top** - show system process
- **ps** - display running processes
- **tar** - create/extract archive files
- **kill** - terminate process
- **ping** - test network. `ping www.google.com`
- **du** - shows disk usage. `du -ha --max-depth=1` shows usage in dirname for all files only 1st level of nestedness

# Refactoring

- **Use type hints everywhere!**

- **Split functionality to functions for convinient maintaining and testing**

- **Add testing wherever you can**

- Merge nested if-statements:

```python
if a:
    if b:
        pass

# -> refactor
if a and b:
    pass
```

- Use any/all instead of a loop

```python
numbers = [-1, -2, -4, 0, 3, -7]
has_positives = False
for n in numbers:
    if n > 0:
        has_positives = True
        break

# -> refactor
has_positives = any(n > 0 for n in numbers)
```

- Use tuple and other immutables in def args!

Usually, you don't want hide logic of changing the data inplace, because you can forget about it at it maybe unpredictable

```python
my_list = []

# instead of
def appender(lst=[], some):
    lst.append(some)

appender(my_list, 42)

# do 
def appender(tpl=Iterable, some):
    return tuple(tpl) + (some,)

my_list = appender(my_list, 42)
``` 

- Pull statements/constants out of loop

```python
for building in buildings:
    city = 'London'
    addresses.append(building.street_address, city)

# -> refactor
city = 'London'
for building in buildings:
    addresses.append(building.street_address, city)
```

- Try to remove variables, that used only once to be returned after.

```python
def state_attributes(self):
    """Return the state attributes."""
    state_attr = {
        ATTR_CODE_FORMAT: self.code_format,
        ATTR_CHANGED_BY: self.changed_by,
    }
    return state_attr

# -> refactor
def state_attributes(self):
    """Return the state attributes."""
    return {
        ATTR_CODE_FORMAT: self.code_format,
        ATTR_CHANGED_BY: self.changed_by,
    }
```

- Use a guard clause

```python
def should_i_wear_this_hat(self, hat):
    if isinstance(hat, Hat):
        current_fashion = get_fashion()
        weather_outside = self.look_out_of_window()
        is_stylish = self.evaluate_style(hat, current_fashion)
        if weather_outside.is_raining:
            print("Damn.")
            return True
        else:
            print("Great.")
            return is_stylish
    else:
        return False

# -> refactor
def should_i_wear_this_hat(self, hat):
    if not isinstance(hat, Hat):
        return False

    current_fashion = get_fashion()
    weather_outside = self.look_out_of_window()
    is_stylish = self.evaluate_style(hat, current_fashion)
    if weather_outside.is_raining:
        print("Damn.")
        return True
    else:
        print("Great.")
        return is_stylish
```

- Movs assignments closer to their usage

```python
def should_i_wear_this_hat(self, hat):
    if not isinstance(hat, Hat):
        return False

    current_fashion = get_fashion()
    weather_outside = self.look_out_of_window()
    is_stylish = self.evaluate_style(hat, current_fashion)
    if weather_outside.is_raining:
        print("Damn.")
        return True
    else:
        print("Great.")
        return is_stylish

# -> refactor
def should_i_wear_this_hat(self, hat):
    if not isinstance(hat, Hat):
        return False

    weather_outside = self.look_out_of_window()
    if weather_outside.is_raining:
        print("Damn.")
        return True
    else:
        print("Great.")
        current_fashion = get_fashion()
        return self.evaluate_style(hat, current_fashion)
        # is_stylish = self.evaluate_style(hat, current_fashion)
        # return is_stylish
```

- Sumplify check of sequence len. len(of zero len) will return False

```python
if len(list_of_hats) > 0:
    hat_to_wear = choose_hat(list_of_hats)

# -> refactor
if list_of_hats:
    hat_to_wear = choose_hat(list_of_hats)
```

- Use enumerate, for god sake

```python
for i in range(len(players)):
    print(i, players[i])

# -> refactor
for i, player in enumerate(players, start=1): # also you can use additional start argument
    print(i, player)
```

-  Simplify condition into return statement

```python
def function():
    if isinstance(a, b) or issubclass(b, a):
        return True
    return False

# -> refactor
def function():
    return isinstance(a, b) or issubclass(b, a)
```

- Merge duplicated blocks into one

```python
def process_payment(payment, currency):
    if currency == "USD":
        process_standard_payment(payment)
    elif currency == "EUR":
        process_standard_payment(payment)
    else:
        process_international_payment(payment)

# -> refactor
def process_payment(payment, currency):
    if currency == "USD" or currency == "EUR":
        process_standard_payment(payment)
    else:
        process_international_payment(payment)
```

or replace it with in, where possible

```python
def process_payment(payment, currency):
    if currency == "USD" or currency == "EUR":
        process_standard_payment(payment)
    else:
        process_international_payment(payment)

# -> refactor
def process_payment(payment, currency):
    if currency in ["USD", "EUR"]:
        process_standard_payment(payment)
    else:
        process_international_payment(payment)
```

- Replace yield inside for loop with yield from

This is an advanced tip if you are already familiar with generators. 
One little trick that often gets missed is that Python’s yield keyword has a corresponding yield from for iterables.

If you have an iterable like a list, instead of saying for item in iterable: yield item, you can simply say yield from iterable. This is shorter and removes the manual looping over the iterable, which can also result in an improved performance.

```python
def get_content(entry):
    for block in entry.get_blocks():
        yield block

# -> refactor
def get_content(entry):
    yield from entry.get_blocks()
```

# Patterns

- [SOLID video](https://www.youtube.com/watch?v=uxwjXLjJOoM)
- [Refactoring](https://refactoring.guru/refactoring/catalog)
- [Design patterns](https://refactoring.guru/design-patterns/catalog)

# Python tasks

## Questions

### How to create class without class word

Answer: type

## Coding tasks

### function get some iterable, where all numbers included twice, except one, which included only once.
for example: `[1, 1, 2, 3, 4, 3, 2]`.
You need to find that only one number

Answer:

Basic algorithm:
Make dict: {'number': 'counter'}
Iterate over input iterable, and update dictionary: if we don't have that key, than adding it. If we have it, adding + 1 to the counter.
And in the end iterate over dict and get number with counter equals 1
Additionnaly, while iterating in main cycle, instead of increasing the counter on second enter of some number we can delete the key from dict completely, and in the end it will be dict with only one number, that contained in input only oce

```python
# or we can use builtin counter function
from collections import Counter
z = [1, 1, 2, 3, 4, 3, 2]
Counter(z)
```


### We have two sorted list. We need to merge them and get sorted result

```python
left_ids = [10, 20, 30, 40]
right_ids = [5, 25, 45]
res = [5, 10, 20, 25, 30, 40, 45]
```

Answer:

basic approach: just extend one list with another, and call sort() function over result list. But it will have O(Nlog(N))complexity.
Of course what we need here - is to implement "sort merge" algorithm with O(N) complexity: iterate over two lists and compare their pairs

```python
# "brutforce" approach
final_list = []
final_list.extend(left_ids)
final_list.extend(right_ids)
final_list.sort()

i = 0
j = 0
final_list = []

# n.b.: while loop here, because we need to rule our pointers by ourselves
while i <= len(left_ids) and j <= len(right_ids):

    if left_ids[i] < right_ids[j]:
        final_list.append(left_ids[i])
        i += 1
        if i == len(left_ids):
            final_list.extend(right_ids[j:])
    else: 
        final_list.append(right_ids[j])
        j += 1
        if j == len(right_ids):
            final_list.extend(left_ids[i:])

```


### We have list with stock price over time (time series, let's say). We need to choose day to buy and to sell stock with maximum profit. If it's impossible - return 0

```python
stocks = [7,1,5,1,3,6,4]
```

Answer:

Core thing here - is to have two pointers. One will check minimum value, second - maximum. But it's obvious. Another tricky part here: 
We should start from 0 and 1 position for min and max pointers, and:
if buy < sell:  go further, increase max, keep min, and compare with current margin
if sell < buy:  place min in current max place (n.b. it can outstand from current min on more than 1 step!), and increase max.

So in general max pointer will be always increasing one by one

```python
from collections import namedtuple

class Solution:

	def best_margin(stocks):

		Buy = namedtuple('Buy', ['date', 'price'])
		Sell = namedtuple('Sell', ['date', 'price'])
		Margin = namedtuple('Margin', ['date_buy', 'date_sell', 'profit'])

		# create start position 
		buy = Buy(0, stocks[0])
		sell = Sell(1, stocks[1])
		margin = Margin(0, 1, stocks[1] - stocks[0])

		days_on_market = len(stocks) - 1

		if days_on_market <= 1:
			return Margin(None, None, 0)

		while sell.date < days_on_market:

			if buy.price < sell.price:
				margin_potential = Margin(buy.date, sell.date, sell.price - buy.price)
				margin = margin_potential if margin_potential.profit > margin.profit else margin
				print(sell)
				sell = Sell(sell.date + 1, stocks[sell.date + 1])
			else: 
				buy = Buy(sell.date, stocks[sell.date])
				print(sell)
				sell = Sell(sell.date + 1, stocks[sell.date + 1])

		return margin


stocks = [7,1,5,1,3,6,4]

best_profit = Solution.best_margin(stocks)
print(best_profit)
```

### What that code will return?

```sql
len(' '.join(list(map(str, [0, 1]))))
```

Answer: 3 (because it's len of `0 1` string)


### What print will return?

```sql
a = {
  True : 'a', 
  1 : 'b', 
  '1' : 'c', 
  1.0 : 'd'
}

print(a[True])
```

Answer:

print will return 'd'. Because python will consider True, 1 and 1.0 as the same key (because they have similar hashes).<br>
So while dict will be constructed, at first, interpreter will add True:'a' pair, than 1:'b' pair will be replace first pair, as it would be update. <br>
But what's also important here: <br>
python only replace value ('a' -> 'b'), but key will be the same, because why do you need to rewrite it, because Python thinks that it's the same key, so in the end we will have that dict:

```python
a = {
  True : 'd', 
  '1' : 'c', 
}
```

n.b., that in python 3.7+ order of keys guaranteed


### How that works?

```python
a, b = b, a
```

In the nutshell - `a, b` it's similar as `(a, b)`, so we see just two tuples here

Remember return from functions?
```python
def func()
    return hue, moe


a = func()

print(type(a))
>> tuple
```

Similar mechanism here

### What that code will return?

```python
a = 'Hello'
msg = list(a)
print(msg)
```

Answer: it returns `[‘H’, ‘e’, ‘l’, ‘l’, ‘o’]`

Question 2: Add 3 symbols, so print will return regular 'hello' string

Answer:
```python
a = 'Hello'
msg = list([a])   # Here we make list of one elment, so list() gets another list as input iterable, but with one element, not string, which is iterable of 5 elements
print(*msg)  # Here we unpack iterable
```

Question 3: Add 2 symbols, so print will return regular 'hello' string

Answer:
```python
a = 'Hello', # here we add comma, and create tuple (but without parenthesys)
# becase python consider 'a, b' as '(a, b)'
msg = list([a])
print(*msg)  # Here we unpack iterable
```


# Additional Info

- [Official Python doc](https://docs.python.org/3/library/index.html)
- [Teach Yourself Computer Sciense](https://teachyourselfcs.com)
- Fluent Python. Clear, Concise, and Effective Programming (Luciano Ramalho)
- Designing Data-Intensive Applications (Martin Kleppmann)
- Python for Data Analysis (Wes McKinney) 2nd edition




