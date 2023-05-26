# Hadoop

## Hadoop ecosystem ierarchy

├── HDFS <br>           
├──── HBase <br>                
├────── MapReduce <br>                    
├──────── Oozie    (Like ZooKeeper. Coordinates MR tasks)<br>
├──────── Pig      (high-level MR commands language)<br>
└──────── Hive 	   (high-level Sql-like MR commands lannguage)<br>

### HDFS

Stands for Hadoop File System.
- Nicely works with quite big size files (more than 100mb), and whith not too big amount of files (up to 1 million).
- Pattern: write once / read many times
- Optimized for sequential (not scattered) read
- Doesn't supports multithreading write in one file!
- You can only append information to file
 
HDFS Daemons:

- **Namenode**:
	- in charge of namespace (all files)
	- contains metainformation about data
	- run on one machine (but it can have secondaty namenode, which is backup (not distribution))
- **Datanode**:
	- contains and works with data
	- sends heartbeat to namenode
	- runs on every machine in cluster 

Storage:

	- Files consist of blocks
	- Each datanode contain blocks from different files
	- Same blocks can be duplicated to different datanodes in reliability purposes (3 copies by default)
	- default block size 64 or 128 mb. blocks quite big to reduce seek time (phisical move of HDD head)


### HBase

It's will be too long to full scan HDFS each time, so HBase it's columnar database, which used like "index".<br>
It contain information about all files in HDFS.<br>
With HBase you can access to particular file/part of file in HDFS.<br>
Based on Google Big Table<br>

- Distributed (sharding) data Base
- Column based (Column-families)


Table consist of Regions<br>
Region - it's group of rows, which stored together<br>

Daemons:

- HMaster (Master server) - metadata and so on
- Region Server - handle with one or multiple regions. Each region can belongs to only one region server


### MapReduce

In terms of Hadoop It's framework, which actually works with HDFS Data, with HBase help

In general It's paradigm for distibuted calculations.
Mostly define two main stages:

1. **Map** - At that stage same function applied to each part of data.

	- Data, that given to MR must be splitted, so it can't handle .gz files or something
	- Splitted bunches of data must don't depends of each other
	- One split - One worker
	- Worker Launches at the same machine, where his split lies ("code to data" approach, because it's faster to copy code to different nodes.)

Python analogue:
`map(func, iterable)` "equal" to `[func(x) for x in iterable]`

2. **Intermediate save phase** - When you operates with big bunches of data it can be nice to save data after Map phase to HDFS, just in case

3. **Shuffle** - It's a phase when each block of result after mappers splitted between Reduce workers (by key value)

4. **Reduce** - At that stage all data after map function aggregaed in one place

	- each reducer node writes at their own file
	- amount of reducers set by user
	- save data in hdfs

Python analogue:
`reduce(func, iterable)` "equal" to `func(iterable)`

In hadoop every MR starts with HDFS and ends with HDFS.


In Hadoop, MR works over HDFS, and MR processes have their own trackers (daemons):

- **JobTracker** - main tracker with all metadata and so on
- **TaskTracker** - Process, that launches at the same node, as DataNode (HDFS)


### Pig

Have their own PigLatin language for MR tasks

Can be launched locally or on MR mode

Core components in Pig:

- **Field** - analogue of cell
- **Tuple** - analogue of row in a table
- **Bag** - analogut of table

Main commands:
- load
- describe
- dump
- d_grouped
- illustrate
- foreach
- tokenize
- flatten
- generate
- filter


### Hive

SQL-like framework to MR tasks. HiveQL 

Works not so great for online or for small queries because of big overhead


## Map Reduce 2.0

MR 1.0:
- API
- Framework
- Resource Manager

MR 2.0:
- MR API
- Framework
and
- YARN API
- Resource manager


So, resource manager became independent player in whole process

In MR1.0 client choose number of Mapper nodes, and Reducer nodes
And whtn all Mapper finished their works, they just rest

But in MR2.0 there is no fixed Mapper/Reducer positions to nodes: they can be Mappers or Reducers, based on load, and YARN desicion
