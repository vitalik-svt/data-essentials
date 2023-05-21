# Spark

## Differences from Hadoop MR

1. In HAdoop MR each operation should be MR operation, so need to consist of two phases.
Even for MRR operation there is dummy Map operation between Maps, with their own I/O stages

So when we do in spark:
M -> R -> R -> R

We must do in hadoop:
M -> R -> M -> R -> M -> R

2. In Hadoop MR you need to save result of any MR operation to HDFS
Spark Use RDD, and it can be in memory, so without havy I/O operations

3. If some operations (three, for example) use the same dataset, in Hadoop you need to create MR for each operation
So you need read dataset from HDFS three times
But in Spark you can load that data in RDD (in RAM) and use it three times
So you read disk only once

## Key Concepts

### RDD 

Sparks works on RDD, instead of HDFS
**RDD (Resilent Distributed Dataset)** - it's abstraction (API) to data.
It can be implemented over RAM, or HDFS, or any other source

RDD can be :
	- 1/2 dimensiinal - dataframe/dataset
	- can be partitioned by different servers 
	- Operation over RDD doesn't change RDD, they create new ones!
	- All operations over RDD can be imagined as DAG (graph)

**Lineage** - it's RDD, that store chain of operations over RDD for each (!) RDD. it's DAG, in a nutshell.
If something get wrong, with some RDD, whle lineage restarts to that RDD

**RDD Transformations**:
	- **Narrow**:
		When each partition of parent RDD used only once (and no more) to create child partition:
		A1 -> B1
		A2 -> B2
		A3 -> B3
		That sort of dependencies let execute pipeline (lineage) on one node, without combining results
		Example: filter operation
	- **Wide**:
		When each partition of parent RDD used by many child paririons
		Example: groupbykey operation

So, because of that dependencies Scheduler make execution plan

### Pro's

- Can used for streaming and batching becuse don't have havy I/O operations
- Spark only for processing, not for storaging
- Spark can be connected to any source of data (HDFS, S3, Cassandra, HBase), beacuse of RDD abstraction
- Spark have plenty of libs (SparkSQL, MLib, GraphX, Spark Streaming)
- Works everywhere: HDFS, Mesos, Standalone (singlenode), in Cloud

### Shared variables

- Broadcast - read-only
- Accumulator - write-only

### Operation types

- Transformations - operations, that create new RDD in result
- Actions - operations, that return value

### Components
- Spark Application - Application itself, contains Driver and Executors
	- Spark Driver - coordination of whole process
	- Spark Executor - Execute process
- Spark Session - Initialize Spark Appliction, and create distibuted system
- Cluster Manager - Resource manager (YARN, Mesos, etc)

### Memory Management 

- If it will lack of memory, LRU (Last recenty Used) meachanim will be launched, and deletes old RDDs
- Spark presents three storaging options:
	- memory storage, serialized Java objects
	- memory storage, deserialized Java objects
	- disk storage

## Operations

Transformations (Returns new RDD):

- map - apply function for each element, returns changed elements
- filter - filter sub-rdd from rdd
- flatmap - apply function for each element, but can return group of elements for each element
- sample
- groupbykey 
- reducebykey - grouping + function
- union
- join
- cogroup
- crossproduct
- mapvalues
- sort
- partitionby

Actions (Returns value):

- count
- collect
- reduce
- lookup - get value by key
- save

Transformations operations are lazy - they don't compute while called.
Whole lineage started to compute only when Action operator called

## Questions

- Difference between persist and cache?
Cache() and persist() both the methods are used to improve performance of spark computation. These methods help to save intermediate results so they can be reused in subsequent stages.
The only difference between cache() and persist() is ,
Cache technique we can save intermediate results in memory only
Persist () we can save the intermediate results in 5 storage levels(MEMORY_ONLY, MEMORY_AND_DISK, MEMORY_ONLY_SER, MEMORY_AND_DISK_SER, DISK_ONLY).

- Hpw to create User defined functions?
```python
def square(val):
	return val * val

spark.udf.register('PythonSquareUDF', square)
```

- Explain Stages and Tasks creation in Spark?
1. Once the DAG is build, the Spark scheduler creates a physical execution plan. 
2. DAG scheduler splits the graph into multiple stages, the stages are created based on the transformations.
3. The narrow transformations will be grouped together into a single stage.
4. The DAG scheduler will then submit the stages into the task scheduler. 


