# Python questions

## Built-in Sequences, Objects, Functions

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
r'string' - raw 
u'string' - unicode
b'string' - bytes

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
List containts links on particular object (can be different types) and link to next object.
So, when you add some element to the end of the list, for example.
Last element for now just accept the link for added element.

it's like
id(123) -> id(345) -> id(456) 

**Tuple**
Immutable object
Created in that particular time when declared, and stored in continuous place in memory.
So it's good for calling elements by index (it's O(1))

id(123), id(124), id(125)

**Array**
it's C-type array.
Like tuple, but containts only objects of one type, which takes much less space

```
import array
array.array('i', [1,2,3])
```

**Range**

Object, that returns by range function. It's not a generator
range(i, j)

Can be used in list comprehensions:

`[x for x in range(i, j)]`

**Comprehentions**

`[x for x in range(i, j)]` - returns list from i to j-1
`{x: y for x, i in enumerate(range(i, j))}` - returns dict from i to j-1 
`{x for x in range(i, j)}` - returns set from i to j-1

you can't define tuple comprehention, it need to be mabe like
`tuple([x for x in range(i, j)])`

**Generator**

Object, that can be called only once, because it stored only previous 
So you can restart it, because he is don't know where is start

You can implement generators by using yield instead of return

Simple generator expresstion:
`(x for x in range(i, j))`

it returns one x at a time, and don't stored anything else, so it can be used for infinite sequence without consuming memory


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

```
new_list = []
[new_list.append(x) for x in original_list if x not in new_list]
```

4. Or just good old loop:

```
new_list = []
for x in original_list:
	if x not new_list:
		new_list.append(x)
```

### multi assignment

nice thing in Python, that you can assign objects to multiple variables (tbh it's more link varibales with existing objects)

```
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

```
keys = ['a', 'b', 'c']
values = [1 ,2 ,3]
dct = dict(zip(keys, values))
```

`zip()` creates list of pairs (in that case), and `dict()` considers that pairs as key, value pairs

### hashmap

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

O(1) to find some element by key in Sets and Dicts
O(N) to find element in List and Tuples
O(1) to find element by index in Tuple
O(N) to find element by index in List

## Functions

function defines with def keyword

parameter is the variable listed inside the parentheses in the function definition.
argument is the value that are sent to the function when it is called.

```
def functionname(parameter):
	pass


functionname(argument)
```


### args and kwargs

it's agreement to use that particular words in function declaration.

```
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

```
python
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

### lambda functions

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

## Variables and Arguments

In Python every Variable it's pointer.

So when you 


Also, evety object contains link counter, and when it becomes equal to zero, object will be deleted


## Links and literature
### Not sources of that page, but good sources in general

- https://docs.python.org/3/library/index.html
- Python for Data Analysis (Wes McKinney) 2nd edition




