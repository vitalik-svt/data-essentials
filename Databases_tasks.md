# Databases_tasks

## SQL basic questions

- Difference between Truncate and Delete: Delete delete row by row and log that. Truncate just drop whole table and recreates it
- What languages SQL has?: DDL (definition: create, alter), DML (manipulation: select), DCL (control: grant)
- Can you join with Null?: No, Null - not compatible, so Join Null on Null will be Null, so result will not appeared
- Difference between Union and Union ALL: Union drop duplicates in result query
- What types of window functions do you know?
    
    - lag(): previous row
    - lead(): next row
    - rownumber: just add rows number counter
    - rank: if there two rows with the same number, next number will be skipped
    - dense rank: no numbers skipped
    - min, max, etc.

- What is order of opertation:
    1. From
    2. Join
    3. Where
    4. Group by
    5. Having
    6. Select + Window functions
    7. Order by
    8. Limit

- What is normaliztion, which advantages it brings: Normalization in SQL is the process of organizing data to avoid duplication and redundancy. Some of the advantages are:
    - Better Database organization
    - More Tables with smaller rows
    - Efficient data access
    - Greater Flexibility for Queries
    - Quickly find the information
    - Easier to implement Security
    - Allows easy modification
    - Reduction of redundant and duplicate data
    - More Compact Database
    - Ensure Consistent data after modification

## Which query returns biggest number:

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

## How many rows will get same query but without distinct:
```sql
select distinct a, b, c
          , sum(d) as revenue 
from table
group by a, b, c
```
Answer: Same amount

## What you need to add, to get share of revenue from the same user, but in previous day?
```sql
select event_date, 
	   user_id, 
	   revenue, 
	   <?>
from revenue
order by event_date
```
Answer: revenue / lag(revenue) Over(Partition by user_id order by event_date desc)

## Write parametrised query which return price by day and id

| id | price | dt|
|----|-------|---|
|1   | 100   | 01.01.2021|
|1   | 110   | 05.05.2021|
|2   | 99    | 01.01.2021|
|2   | 95    | 01.03.2021|
|2   | 120   | 06.10.2021|

Answer:

```sql
declare @id int = 1
declare @dt date = '2021-02-02'

-- first of all wee need to add date_from and date_to columns, for convenient selection
select id
      , fromdate
      , todate
      , price
from
(
  select id
       , dt as fromdate
       , dateadd(dd, -1, lead(dt) over(partition by id order by dt asc)) as todate
       , price
  from prices
) tier1
where 1=1
and id = @id
and @dt between fromdate and todate
```

## Find suppliers, that supply us biggest amount of money in last month

|id |      dt    | id_supplier | id_product | quantity | price|
|---|------------|-------------|------------|----------|------|
|1  | 01.01.2021 |      1      |      1     |  100     | 100|
|2  | 01.01.2021 |      2      |      1     |  120     | 110|

Answer:
```sql
declare @month_id int = 202203

select id_supplier
from 
(
  select id_supplier
       , sum(quantity * price) as batch_cost
  from batch
  where year(dt) * 100 + month(dt) = @month_id
  group by id_supplier
  order by batch_cost desc
) tier1
where batch_cost = (select max(batch_cost) from ...)
```

