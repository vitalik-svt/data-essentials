# Databases

## What is transaction?

transaction - it's atomic operation, which can be completed fully, or not
We can combine different operations into one transaction, when we need to be sure, that they completed/not completed together

For example, when we transfer money from one account to another, we need to make it one logical transaction:

```
BEGIN TRANSACTION;

UPDATE bank_accounts
SET amount = amount - 100
WHERE user_id = 123

UPDATE bank_accounts
SET amount = amount + 100
WHERE user_id = 321

END TRANSACTION;
```

Transaction have these main commands:
begin
end / commit
rollback

## Which properties transaction have?

**Atomicity** - means that operation (transaction) can be fully done or rollback'ed, yes or no, 1 or 0

**Consistency** - it's logical property. In previous example with bank transfer consistency means, that total amount of money will be the same after transaction. It's like law of conservation of energy

**Isolation** - it means, that each transaction independent of other transactions (see Isolation levels).
It'ssimilar to **Serializibility**, that means, that transactions runs like that runs serializably (one after one), even in real life they run concurrently

**Durability** - means, that if we get proof of end of transaction, that means, that there is can't happen something, to rollback that transaction, and it stored in database forever

## CAP, BASE

- `Consistency` 
- `Availiability`
- `Partitionability`

Three of them almost impossible, so there BASE approach:

- `Basically availilale`
- `Soft State`
- `Eventually Consistent`

## Isolation Levels

- `Read Commited`: have two main parts 
	- `no dirty reads`: other transactions don't read any uncommited writes
	- `no dirty writes`: other transaction, that wants to write need to wait until fist transaction commits

- `Snapshot Isolation Level`: whtn each transaction reads their own version of data, that commited when that transaction started

- `Serializability`: based on one of three approaches:
	- `real isolation`: when you have not so much transactions, and all of them fast you can just evaluate queries one by one
	- `2 phased commit`: quite slow
	- `Serializable Snapshot Isolation`

## What is Cursor. Types of Cursors

Area in memory, when result of query stored.
Can be client and server cursors 

## How JOIN works

- Nested Loop:
For each row of the left table, iterate over whole right table
it's O(NxM)

- Merge Join:
At first we need to sort both tables, and after that
for first row of left table find all rows in right table and stops (remember place, where stop)
For second row of left table loop started from that place, where stopped.
So it's O(N+M)

- Hash Join:
At first we need to create hashmap from smallest table.
Then for each row from biggest table we calculate hash() and go to the hasmap.
so it's O(N)

## SQL Questions

- Difference between Truncate and Delete: Delete delete row by row and log that. Truncate just drop whole table and recreates it
- What languages SQL has?: DDL (definition: create, alter), DML (manipulation: select), DCL (control: grant)
- Can you join with Null?: No, Null - not compatible, so Join Null on Null will be Null, so result will not appeared
- Difference between Union and Union ALL: Union drop duplicates in result query
- Which query returns biggest number:

```sql
-- a
select count(distinct first.counter_column) 
from first
left join second 
    on first.join_key = second.join_key 
where second.filter_column >= 5

-- b
select count(distinct first.counter_column) 
from first
left join second 
on first.join_key = second.join_key 
and second.filter_column >= 5

-- c
select count(distinct first.counter_column) 
from first
right join second
    on first.join_key = second.join_key
where second.filter_column >= 5

-- d
select count(distinct first.counter_column)
from first
right join second
on first.join_key = second.join_key 
and second.filter_column >= 5
```

Answer: b, because where condition filter result, but join - not (for left join)

- how many rows will get same query but without distinct:
```sql
select distinct a, b, c
          , sum(d) as revenue 
from table
group by a, b, c
```
Answer: Same amount

- What you need to add, to get share of revenue from the same user, but in previous day?
```sql
select event_date, 
	   user_id, 
	   revenue, 
	   <?>
from revenue
order by event_date
```
Answer: revenue / lag(revenue) Over(Partition by user_id order by event_date desc)

- What types of window functions do you know?
	
	- lag(): previous row
	- lead(): next row
	- rownumber: just add rows number counter
	- rank: if there two rows with the same number, next number will be skipped
	- dense rank: no numbers skipped
	

## Distribution, Partition

- `Distribution` - Process, that distributes data by some key (random, preferrably), on smaller parts, so all nodes can perform query
- `Partitions` - Partition by monthes


## Links and literature
### Not sources of that page, but good sources in general

- Designing Data-Intensive Applications (Martin Kleppmann)
