Python_tasks

## function get some iterable, where all numbers included twice, except one, which included only once.
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
