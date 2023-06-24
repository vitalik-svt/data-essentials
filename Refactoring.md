# Refactoring


## Review algorithm

Me, personnaly divide review to three parts:

1. **Is code working as it is?**
	*In standalone environment. There i need to check all logic inside functions and so on. It's similar to unit-testing, and in test covered production maybe not so nessecary, because we assume, that code tested before pull request*

2. **Will code be working in production environment?**
	*How that code will interact with other things in production?*

	- Is the pipeline idempotent? 
	- Are they incorrectly using "current time" in the pipeline?
	- Are they using date > "start date" without a corresponding date < "end date" 
	- Are they doing JOINs with SCD (slowly changing dimension) tables that don't have the needed timeframe filters

	- Is the data model efficient? 
	- Is there any excessive data duplication?
	- Could they leverage complex data types for a better model?  
	- Are the column names reasonable and understandable? 

	- Do they have data quality checks at all?
	- Are they checking for NULLs, duplicates, and malformed values?
	- Are they doing row count anomaly detection?  
	- Will any of these quality checks be excessively noisy?

	- Can pipeline be less costy (in cloud solutions)?

3. **Refactoring**
	*Can code be cleaner, with the same functionality?*



## Refactoring tips

0. **Use type hints everywhere!**

0. **Split functionality to functions for convinient maintaining and testing**

0. **Add testing wherever you can**

1. Merge nested if-statements:

```python
if a:
    if b:
        pass

# -> refactor
if a and b:
    pass
```

2. Use any/all instead of a loop

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

3. Pull statements/constants out of loop

```python
for building in buildings:
    city = 'London'
    addresses.append(building.street_address, city)

# -> refactor
city = 'London'
for building in buildings:
    addresses.append(building.street_address, city)
```

4. Try to remove variables, that used only once to be returned after.

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

5. Add a guard clause

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

6. Movs assignments closer to their usage

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

7. Sumplify check of sequence len. len(of zero len) will return False

```python
if len(list_of_hats) > 0:
    hat_to_wear = choose_hat(list_of_hats)

# -> refactor
if list_of_hats:
    hat_to_wear = choose_hat(list_of_hats)
```

8. Use enumerate, for god sake

```python
for i in range(len(players)):
    print(i, players[i])

# -> refactor
for i, player in enumerate(players, start=1): # also you can use additional start argument
    print(i, player)
```

9. Simplify condition into return statement

```python
def function():
    if isinstance(a, b) or issubclass(b, a):
        return True
    return False

# -> refactor
def function():
    return isinstance(a, b) or issubclass(b, a)
```

10. Merge duplicated blocks into one

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

11.Replace yield inside for loop with yield from

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


## System Design

- You drive the interview!
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
    - is it migration to cloud, or new system? 
    - who will use that system? BA, DS? 

- You should continiously ask, if interviewer understand your way of thinkning!

### links
- https://www.youtube.com/watch?v=Be7INI_U6GY
- https://github.com/donnemartin/system-design-primer
- Youtube channel "system design interview"

