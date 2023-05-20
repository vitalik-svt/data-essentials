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

- Difference between Truncate and Delete:



## Distribution, Partition

- `Distribution` - Process, that 
- `Partitions` - Partition by monthes


## Links and literature
### Not sources of that page, but good sources in general

- Designing Data-Intensive Applications (Martin Kleppmann)
