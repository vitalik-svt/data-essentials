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

## Basic Data base data types

**Hash Index**

pass

**SS-Table**

pass

**LSM-Tree**

pass

**B-Tree**

pass


## ACID (Properties of transaction)


**Atomicity** - means that operation (transaction) can be fully done or rollback'ed, yes or no, 1 or 0

**Consistency** - it's logical property. In previous example with bank transfer consistency means, that total amount of money will be the same after transaction. It's like law of conservation of energy

**Isolation** - it means, that each transaction independent of other transactions (see Isolation levels).
Isolation can be implemented in different ways, it's up to rdbms developers. Here some examples of **Isolation Levels**, from weakest, to strongest (approximately)

	- **Read Commited**: have two main parts:
		
		*Transaction can read only commited on changes, by the time that transaction started*
		
		- no dirty reads: other transactions don't read any uncommited changes
		- no dirty writes: other transaction, that wants to write need to wait until fist transaction commits

	- **Snapshot Isolation Level/repeatable read**: each transaction reads their own version of data, that commited when that transaction started

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

### Types of Indexes

Indexes can be implemented with different data structures

- **B-Tree** - Most used type at that time. 
- **Hash Index** - Mostly used for key:value storage
- **SS-Table** - tbh i don't get that fully. need to be filled later
- **LSM-Tree** - tbh i don't get that fully. need to be filled later

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

## RowStore and ColumnStore

### Rowstore

Data stored by rows, so DBMS iterate over rows and handle all the data.
Mostly used for operations, that involves whole raw

**Pro**:
	- It's cool for __OLTP__, because it's easy to append data at the end: you write in only one file (in general)
**Contra**:
	- In querits you need to handle all row with you, that fill memory

### Columnstore

Data stored by colummns, so RDBMS iterate over rows and handle all the data.<br>
Nice to have, when most of your operations involve not whole rows, but some columns only


**Pro**:
	- It's cool for __OLAP__, because generally you select only some columns, so RDMBS need to take care only of that particular columns, and don't store additional data
	- It's simple to compress columns, for example you can compress column AAAAAAABBCCAAA to A7B2C2A3  (and then apply BitMap, for example)
**Contra**:
	- It takes more time to insert data, becaues you need to insert data in all columns files

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

### Weigth of some basid types

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
	Partition by monthes

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

- **Avro**

pass

- **Parquet**

	phisycal models to store data can be thest:<br>
	example table:<br>
	|rows|col_a|col_b|col_c|
	|----|-----|-----|-----|
	|row0| a0  | b0  | c0  |
	|row1| a1  | b1  | c1  |
	|row2| a2  | b2  | c2  |
	|row3| a3  | b3  | c3  |

	- Row-wise (each file contains some rows). they can united in longer rows, but, in a nutshell it's a continuous amount of rows.<br>
	It's cool to use at row-store databases (obviously), for OLTP data-access pattern, so where you need to insert you just append row, where you need update/delete, you just need to find start of row, and read all continiously , because equential reading better for disk.<br>
	it can be like in an example as is:

	|     |     |     |     |     |     |
	|-----|-----|-----|-----|-----|-----|
	| a0  | b0  | c0  |	a1  | b1  | c1  |
	| a2  | b2  | c2  | a3  | b3  | c3  |


	- Column-wise.

	When your store one column in sequence.<br>
	So, you need to find start of needed columns and read sequentially all data.<br>
	It's used for OLAP pattern

	|     |     |     |     |     |     |
	|-----|-----|-----|-----|-----|-----|
	| a0  | a1  | a2  |	a3  | b0  | b1  |
	| b2  | b3  | c0  | c1  | c2  | c3  |

	Or you can use different file for each column. Also, it's neccessary to undeerstand offset (~index) of each elemnt in file

	- Hybrid. _Parquet use that type_

	That means, that you have both columns (horizontal) and columns(vertical) partitioning.

	|     |     |     |     |     |     |
	|-----|-----|-----|-----|-----|-----|
	| a0  | a1  | b0  |	b1  | c0  | c1  |
	| a2  | a3  | b2  | b3  | c2  | c3  |

	**Under the hood Parquet file has:**<br>

	- Row-group 1 (128mb by default)
		- Column A chunk 0
			- Page 0
				- Page metadata<br>
					_min_, _max_, _count_
				- Repetition levels
				- Definition levels<br>
					_for nested schemas_
				- Encoded values<br>
					_actual data in encoding state_
			- ...
			- Page N
		- Column B chunk 0
		- ...
		- Column N chunk N
	- ...
	- Row-group N
	- Footer
		- file
		- row-group 
		- column metadata


	**Parquet has 6 encoding schemes, but there basic:** <br>

	- Plain
		- Fixed with: means, that values stored back-to-back. cool for integers, for example:<br>
			file example: 1, 5, 6, 3, ...
		- Non-fixed with: used for different length data (strings). in that case data have length prefix
			file example: 2, yo, 3, no, 8, hobahoba, ...

	- RLE_Dictionary
		- Run-length encoding + bit-packing + dictionary compression
		- Assumes duplicate and repeated values

			example data:
			a, b, c, a, a, a, f, f, b, a

			dictionary-compression stage:
			_it's just creation of hashmap_
			a: 0, b:1, and so on

			so data will be
			0, 1, 2, 0, 0, 0, 6, 6, 1, 0

			RLE+Bit packaging stage:
			0, 1, 2, (3, 0), (2, 6), 1, 0

	_Note1:_ beacuse of all that metadata things stored in file, and rowgroups, you shoukd avoid use small files
	_Note2:_ Also avoid to use hufe files, because that means huge footer, but algorythms for foorer managment not optimized for speed.
	_Note3:_ So, size of 1gb is ok

	#### Conclusion about Parquet:

	- Redused I/O
		- because of size (compression to RLE_Dictionary)
		- because of avoioding read irrelevant data (based on metadata min max and dictionary filtering)
	- Redused overhead
		- if you avoid using small files


## Links and literature

### Not sources of that page, but good sources in general

- Designing Data-Intensive Applications (Martin Kleppmann)
- https://seanhu93.medium.com/difference-of-isolation-and-consistency-cc9ddbfb88e0#:~:text=So%20what%20is%20the%20difference,clients%20of%20a%20distributed%20system
- https://www.youtube.com/watch?v=1j8SdS7s_NY
