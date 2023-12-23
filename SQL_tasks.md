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

Answer2: 
```sql
SELECT 
    price 
FROM price
WHERE 
    dt <= @dt 
    AND id = @id
ORDER BY dt DESC 
LIMIT 1
```

## we have tables ABBC и AABBE. What we got for INNER JOIN and RIGHT JOIN?

Answer:

inner:
AABBBB

right:
AABBBBE

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

## How to find suppliers, that didn't supply us anything, if we have suppliers dict nearby
DDL:
```sql
CREATE TABLE IF NOT EXISTS supplier (
      id bigint not null,
      name VARCHAR(200) not null 
  );
```

id |name         |
---|-------------|
 1 |  Supplier1  |
 2 |  Supplier2  |


Answer:
```sql
WITH revenue AS (
SELECT
  id_supplier
    SUM(quantity*price) as revenue
FROM deliveries
)
SELECT 
    id,
    name
FROM supplier
LEFT JOIN deliveries ON supplier.id = deliveries.id_supplier
WHERE 
    supplier.id IS NULL
```

## Question: We have two tables with item sstellites: address and price. We need to get last actual address and price for each item

```sql
create table s_item_address (
    item_id int,
    address varchar(100),
    actual_date timestamp
);

create table s_item_price (
    item_id int,
    price int,
    actual_date timestamp
);
```

Answer:

```sql
select coalesce(sia.item_id, sip.item_id) as item_id
     , address
     , price
from 
    (
    select item_id
         , address
         , row_number() over(partition by item_id order by actual_date desc) as rn
    s_item_address
    ) sia 
full outer join
    (
    select item_id
         , price
         , row_number() over(partition by item_id order by actual_date desc) as rn
    s_item_price
    ) sip 
    on 1=1
    and sia.rn = 1
    and sip.rn = 1
    and sia.item_id = sip.item_id
```

## Question: We have table with students marks. Get the students with less than 10 "2" marks , and more than 2 "5" marks

```sql
create table marks (
    student_id int,
    mark int
);
```

Answer:
```sql
select student_id
from (
    select student_id
        , sum(case when mark = 5 then 1 else 0 end) as num_5
        , sum(case when mark = 2 then 1 else 0 end) as num_2
    from marks
    group by student_id
    ) stg
where 1=1
    and num_2 < 10
    and num_5 > 2
```


## What is min and max value can be for different type of joins? Values in tables are unique!
```sql
a - 5 rows
b - 10 rows

select count(*)
from a
unknown join b on unknown (a.a=b.b)
```

Answer:
1. LEFT JOIN - min 5 max 5.
2. RIGHT JOIN- min 10 max 10.
3. INNER JOIN - min 0 max 5.
4. FULL JOIN - min 10 (largest(a,b)) max 15(a + b).
5. CROSS JOIN - min 50 max 50.

## There is a table with ~10 billion rows, which contains 10 last years of data, and which is really used by users. Data splitted by years evenly. You decided to left only two last years, because it's most used data. How you will perform that action, and how you do that in future?  

Answer:
You can insert last two years in separate table and send all queries to that table. It will be zero downtime, but it costs additional space.
In future it will be more convinient to partitionize table by years, and drop/detach and store somwhere outdated partitions  

## There is a huge table with 100+ columns. There is no primary key, but we have set of 30 columns, that combined can be used as key. How you can check if there is duplicates in table? Note, that group by by 30 columns will lasts forever, or even doesn't work

Answer:
You can concatenate that 30 columns and mashe hash of that concatenation. And group by that hashed field
