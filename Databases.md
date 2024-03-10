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

## Links and literature

### Not sources of that page, but good sources in general

- Designing Data-Intensive Applications (Martin Kleppmann)
- https://seanhu93.medium.com/difference-of-isolation-and-consistency-cc9ddbfb88e0#:~:text=So%20what%20is%20the%20difference,clients%20of%20a%20distributed%20system
- https://www.youtube.com/watch?v=1j8SdS7s_NY
