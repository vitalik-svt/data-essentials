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


## We have two sorted list. We need to merge them and get sorted result

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


## We have list with stock price over time (time series, let's say). We need to choose day to buy and to sell stock with maximum profit. If it's impossible - return 0

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

## What that code will return?

```sql
len(' '.join(list(map(str, [0, 1]))))
```

Answer: 3 (because it's len of `0 1` string)


## What print will return?

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

print will return 'd'. Because python will consider True, 1 and 1.0 as the same key (because they have similar hashes). So while dict will be constructed, at first, interpreter will add True:'a' pair, than 1:'b' pair will be replace first pair, as it would be update. But what's important here: python only replace value ('a' -> 'b'), but key will be the same, because why do you need to rewrite it, because Python thinks, that it's the same key, so in the end we will have that dict:

```python
a = {
  True : 'd', 
  1 : 'b', 
}
```

n.b., that in python 3.7+ order of keys guaranteed


## How that works?

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

## What that code will return?

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

## How to create class without class word

Answer: type



