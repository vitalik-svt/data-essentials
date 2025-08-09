# Review algorithm

Me, personnaly divide review to three parts:

1. **Is code working as it is?**
	*In standalone environment. There i need to check all logic inside functions and so on. It's similar to unit-testing, and in test covered production maybe not so nessecary, because we assume, that code tested before pull request*

2. **Will code be working in production environment?**
	*How that code will interact with other things in production?*

	- Is the pipeline idempotent? 
	- Are they incorrectly using "current time" in the pipeline?
	- Are they using date > "start date" without a corresponding date < "end date" 
	- Are they doing JOINs with SCD (slowly changing dimension) tables that don't have the needed timeframe filters?
    - Is there "dtm", "source", another technical fields?

	- Is the data model efficient? 
	- Is there any excessive data duplication?
    - Is SQL efficient?
    - Is there nulls, how it handled?
	- Could they leverage complex data types for a better model?  
	- Are the column names reasonable and understandable? 

	- Do they have data quality checks at all?
	- Are they checking for NULLs, duplicates, and malformed values?
	- Are they doing row count anomaly detection?  
	- Will any of these quality checks be excessively noisy?

	- Can pipeline be less costy (in cloud solutions)?

3. **Refactoring**
	*Can code be cleaner, with the same functionality?*

   
# System Design questions

- You drive the process!
- You should clarify all requirements in the start!

    dev part:
    - How many users/data in the system?
    - is that system for company, or regional, global?
    - is data availiability crucial?
    - what about data latency?
    - OLTP/OLAP share
    - what features should be implemented?
    
    data part:
    - what is source of data?
    - Is it need to be batch or streaming? with which frequency, if batch?
    - size of data?
    - is it migration, or new system? 
    - who will use that system? BA, DS, OPS? 
    - What is target? BI?

- You should continiously ask, if your client understand your way of thinkning!

# Refactoring tips

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

### links
- https://www.youtube.com/watch?v=Be7INI_U6GY
- https://github.com/donnemartin/system-design-primer
- [Youtube channel "system design interview"](https://www.youtube.com/@SystemDesignInterview)
- [Youtube channel "IGotAnOffer-Engineering"](https://www.youtube.com/@IGotAnOffer-Engineering)

