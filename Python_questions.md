# Python questions

## Built-in Objects and 

## Sequences

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
- range (function)

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

## Links and literature

- https://docs.python.org/3/library/index.html
- Python for Data Analysis (Wes McKinney) 2nd edition




