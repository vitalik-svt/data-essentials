# Databases

## What is transaction?

transaction - it's atomic operation, which can be completed fully, or not. <br>
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
- begin
- end / commit
- rollback

## ACID (Properties of transaction)


**Atomicity** - means that operation (transaction) can be fully done or rollback'ed, yes or no, 1 or 0

**Consistency** - it's logical property. In previous example with bank transfer consistency means, that total amount of money will be the same after transaction. It's like law of conservation of energy

**Isolation** - it means, that each transaction independent of other transactions (see Isolation levels).
Isolation can be implemented in different ways, it's up to rdbms developers. Here some examples of **Isolation Levels**, from weakest, to strongest (approximately)

	- **Read Commited**: have two main parts:
		
		*Transaction can read only commited on changes, by the time that transaction started*
		
		- no dirty reads: other transactions don't read any uncommited changes
		- no dirty writes: other transaction, that wants to write need to wait until fist transaction commits

		It can be implemented by setting block for rows, that modified by transaction, so next transactions need to wait for their turn to modify some rows, when block will be released.
		Also, it will work for dirty reads: in case, when transaction try to read blocked row, she need to get pre-blocked state of that row

	- **Snapshot Isolation Level/Уepeatable read**: each transaction reads their own version of data, that commited when that transaction started

		It can be implemented by:
		- storing few versions of each data, which called MVCC (multiversion concurrency control)
		- each transaction must have monotoniously increased id (txid)
		- each piece of data should hold store metadata with information about created transaction, deleted, modified, so based on that information each transaction can understand: can it "see" that data, or not

	- **Serializability**: Most strict isolation level. Guarantees that result of concurrenttly executed transactions will be the same as if they are executed serially (one by one). But implement that hardest level of isolation can down speed.

	Serializibility implemented mainly in one of that ways:
		- sequential execution it's real isolation: when you have not so much transactions, and all of them fast you can just evaluate transactions really one by one
		- 2PL (2 phased lock): Transaction block some rows (by some predicat or something), and let it go after commit. It's quite slow, because in insert/update operations it's practicallly a sequential execution 
		- SSI (Serializable Snapshot Isolation): It use optimistic approach (while 2PL use pessimistic one). This approach based on Shapshot Isolation, but we also continously check transaction id (monotonically increasing value), and right before commiting transaction, transaction manager check, if there is transaction with bigger id commits some changes. If yes, our transaction should be rollbacked and rerunned

**Durability** - means, that if we get proof of end of transaction, that means, that there is can't happen something, to rollback that transaction, and it stored in database forever

## Consystency types:

**Isolation** is described in the context of transactions which consists of one or more read and write operations. On the other hand, **Consistency** is described in the context of atomic read or write operations.

- **Strict Consistency** - Full Consistency. Hard to achieve
- **Sequental consistency** - Guarantee, that latest processes will read/write newest value
- **Casual Consistency** - Data splits by dependend and independed. And Consistency exists only for Depended
- **Processor Consistency** - pass 
- **Weak Consistency** - pass
- **Eventual Consistency** - Means, that eventually (after some time) all data will be in consistent state 
- **Release Consistency** - pass
- **Entry Consistency** - pass

## CAP, BASE

it's concepts of how distributed system (not exactly database) should be made 

- Consistency
- Availiability
- Partitionability

Three of them almost impossible simaltaniously, and usually all picks Availiability and Partitionability
So there BASE approach:

- Basically availilale - In the end query will return result (but it can takes time)
- Soft State - All works without you
- Eventually Consistent - Eventual consistency

## What is Cursor. Types of Cursors

Area in memory, when result of query stored.
Can be client and server cursors.

## SQL vs NoSQL

by SQL it mostly means relational rowstored databases

No-SQL examples:

- **Column Store**: sparse matrix
	- CLickHouse
	- HBase
	- Google BigTable
	- Cassandra

- **Key:Value**: hash-table
	- S3
	- Voldemort

- **Document**: Tree
	- MongoDB

- **Graph**: graph
	- Allegro
	- InfinitieGraph

## How JOIN works

- **Nested Loop:**
For each row of the left table, iterate over whole right table
it's O(NxM)

- **Merge Join:**
At first we need to sort both tables, and after that
for first row of left table find all rows in right table and stops (remember place, where stop)
For second row of left table loop started from that place, where stopped.
So it's O(N+M)

- **Hash Join:**
At first we need to create hashmap from smallest table.
Then for each row from biggest table we calculate hash() and go to the hasmap.
so it's O(N)

## Indexes

### What is Index

**Index** - it's a separate data structure, that can perform select, but slow insert and update

In a nutshell - index it's like Table of contents for book. When you need particular chapter you don't need to fullscan all book. You can just look at TOC and see in which page range needed chapter are stored

Indexes can be clustered and nonclustered (In MSSQL, for example):

- **Clustered Index** - It's index, that part of the particular table. It can be only one clustered Index for each table, because Clustered index actually  (it's B-Tree in MSSQL)
- **Non-clustered Index** - It's separate from table "TOC". It can be many nonclustered indexes for each table

PostgreSQL doesn't have that concepts: all data stored in heaps, so all indexes are non-clustered.

It's more simpler to consider indexes as separate from data structure things, so clustered index - it's not really common thing

### Pro et contra

Pro: 
1. Faster select operations 
2. Phisycal sorting of data (but for clustered types of indexes only). If it will be unclustered index (most of it, tbh), it will be just additional data structure, that contains links to real data   

Contra: 
1. Slowyng DML operations (UPDATE, INSERT, DELETE) because you need to rebuild index each time
2. Increasing of size of database (for non-clustered indexes)
3. It takes time to rebuild indexes  


### Basic Data base index types

**B-Tree (Balanced)** - Most used type at that time. 

pass

**Hash Index** - Mostly used for key:value storage

It's a hasmap, that stored somewhere in ram (for fast response).
Let's assume, that our DB it's simple file that store some key:value, and we only append new values to the end of the file

So our file looks like:
data:		 key1: 'value1', key2: 'value2', key3: 'value3'... 
position:    12345678910111213141516171819202122232425262728...

And in that case we need to store somewhere hashmap, which will contain key and offset (in bytes or symbols for simplicity)
key1: 1
key2: 13
etc

So when we need to find some value, we just scan our hasmap and go directly to needed offset

**SS-Table**

pass

**LSM-Tree**

pass

### PostgreSQL Types of Indexes:

B-Tree (default), Hash, Generalized Inverted Index (GIN), Generalized Search Tree (GiST), SP-GiST (Space-Partitioned GiST), Block Range Index (BRIN)

### When should indexes be avoided?

- You should not use indexes on small tables
- You should not use indexes on tables that face large and frequent batch UPDATE and INSERT operations
- You should not use indexes on columns that have many NULL values
- You should not use indexes on columns that are frequently edited
- When column have small selectivity (too little unique values, or even worse - when we have disbalance)

### When it's better not to have indexes, instead of having them?

In a nutshell, that's how process looks like:
We go to the index, iterate over them, and go to particular data cells, with links, that mentioned in index.

In that case, if, for example, we have table with our employees, and if we quite old company, that means, that flag `active_employee` will be on 90% filled with `False`. So if we want to select some of old employee, and if we have that field indexed, so we need to get to index and select 90% of rows with links in index. That whole "go to index -> find value -> go to link - > find real value" will be more time consuming, than simple fullscan in actual data

### Why you can't just create as many indexes as possible, if then so great?

Because each index should be rebuild after any changes in table, which slow writes in database

## What is Database lock? 

*lock* - it's a "flag", that that particular object taken by some transaction, and that prevents other transactions perform operations over that object.
Because before starting operating, transaction should check if there is lock flag on object, or not. And if yes, transaction wont run.

Levels:
1. Database level - locks whole db.
2. Table level
3. Page level
4. Row level

Types:
1. Exclusive - just blocks any operations for that row/page/etc for other transactions
2. Shared - performed only for read transactions. That means, that object can get many shared locks, because all of that transactions only read it.
3. Predicate - It works with predicates as in where clause `where id > 100 and day_id = '2023-09-30'`

## RowStore and ColumnStore

### Rowstore

Data stored by rows, so DBMS iterate over rows and handle all the data.
Mostly used for operations, that involves whole raw

- **Pro**: 
	- It's cool for __OLTP__, because it's easy to append data at the end: you write in only one file (in general)
- **Contra**: 
	- In queries you need to handle all row with you, that fill memory

### Columnstore

Data stored by colummns, so RDBMS iterate over rows and handle all the data.<br>
Nice to have, when most of your operations involve not whole rows, but some columns only


- **Pro**:
	- It's cool for __OLAP__, because generally you select only some columns, so RDMBS need to take care only of that particular columns, and don't store additional data
	- It's simple to compress columns, for example you can compress column AAAAAAABBCCAAA to A7B2C2A3  (and then apply BitMap, for example)
- **Contra**:
	- It takes more time to insert data, becaues you need to insert data in all columns files


## Execution plan, Statistics (PostgrSQL)

### Execution plan

It's logical plan, which RDBMS will use to execute query. Can be run by two commands.

It's a tree where each leaf it's operation.
And each operation have their own cost, that can be changed by administrator (but default pretty ok for most cases)
PostgreSQL Planner select right plan by himself, and you can't "help" with that

- **Explain** - It's shows estimated (!) plan to given query
- **Explain Analyze** - It actually runs (!) query and then shows protocol of actually ised plan

Operations in execution plan:
- **Scan** - Selection of data
- **Bitmap** - Bit Maps construction
- **Sort, Aggregate, Append, Limit** - Actual operations with data
- **Intersect, Except** - Sets operations
- **Nested loop, hash join, merge join** - Joins
- **Init Plan, SubPlan** - Nested queries

Information that execution plan gives:
- **cost** - Operation cost
- **rows** - amount of rows
- **width** - width/weight (in bytes!)
- **output** - returned columns
- **actual** - actual data (shown only in analyze)
- **buffers** - weight of data
- **rows removed** - removed rows

Scan operations:
- **Sequential Scan** - sequential (full) scan
- **Index Scan** - scan of index
- **Index only Scan** - scan of index only
- **TID Scan** - scan for phisical row identifier
- **CTE Scan** - scan of CTE tables
- **Values Scan** - scan of constants
- **Function Scan** - scan of result of function

### Statistics

Stored in two tables, basically:

- **pg_class**
	- reltuples: amount of rows
	- relpages: amount of pages

- **pg_statistics**(table)/**pg_stats**(view)
Store data about fields/columns of table

	- null_frac: share of nulls
	- n_distinct: share of unique values
	- most_common_values: array of most frequent values (100 limit by default, but can be changed)
	- most_common_freqs: array of freauency of that most frequent values

### Weigth of some basic types in db

|type|bytes|
|----|-----|
|bool|1|
|int2|2|
|int4|4|
|int8|8|
|varchar(n)|n+4|
|char(n)|n+4|
|timestamp|8|

## How data stored (PostgreSQL)

Table consist of segments

Segment consist of pages

In each page stored actual data.
Write in each page performs in two directions:
from start of file added pointers to data
from end added actual data

Index data structure looks the same, but pointers in pages look not onto data, but on links to data

## Scalability, Distribution, Partition

Two main scalability options:
- Master-Slave:
	slaves hold copies of master, and clients send queries to less loaded slave

- Sharding:
	When you split data to different machines (like partitioning, but on machines)

- Distribution:
	Process, that distributes data by some key (random, preferrably), on smaller parts, so all nodes can perform query

- Partitions:
	Partition by monthes (for example)

## PostgreSQL Don'ts

[Nice link to explore](https://wiki.postgresql.org/wiki/Don%27t_Do_This)

## Files

### Unstructured

Fully no schema, so you need to parse it somehow.<br>
It's schema on-read.

- txt

### Semi-structured

Not really contains the schema, but it's the steps in the right direction.<br>
That data formats have some rules to create file, so it helps, but they are still **schema on-read**.

- csv/tsv/psv
- xml
- json

### Structured

Structured, means, that files have schemas, so you 100% shure, how you should handle each element in file.<br>
it's schema on-write.

- avro
- parquet
- etc...

## SQL tasks

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

## Can be such situation, where Left join will return more rows, than cross join?

Answer:

No, Maximum - same amount of rows

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

## Will that query run? 

```sql
sеlеct * 
frоm table1 
grоuр bу id
```

Answer: No

**Additional question:** In which case that query will run?

Answer: If we have only id column in that table

## Will that query run? 

```sql
uрdаtе table1 
sеt fiеld1 = rоw_numbеr() frоm table1
```

Answer: No, because row_number() can be accessible only in select, not in set. Also, it didn't finished syntactically


## Will that query run? 

```sql
sеlеct * frоm table1
whеrе null = null 
   оr null <> null 
   оr 123 <> null 
   оr null is null
```

Answer: yes, because of last condition. Other conditions will return either False, or None, because None can be compared only with None, by using is/is not 


## Links and literature

### Not sources of that page, but good sources in general

- Designing Data-Intensive Applications (Martin Kleppmann)
- https://seanhu93.medium.com/difference-of-isolation-and-consistency-cc9ddbfb88e0#:~:text=So%20what%20is%20the%20difference,clients%20of%20a%20distributed%20system
- https://www.youtube.com/watch?v=1j8SdS7s_NY
