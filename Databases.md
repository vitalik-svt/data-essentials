# SQL and general databases questions

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

**Isolation** - it means, that each transaction independent of other transactions (see Isolation levels)

**Durability** - means, that if we get proof of end of transaction, that means, that there is can't happen something, to rollback that transaction, and it stored in database forever

## Isolation Levels



## Links and literature
### Not sources of that page, but good sources in general

- Designing Data-Intensive Applications (Martin Kleppmann)
