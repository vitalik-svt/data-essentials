# Tools

## Airflow

### Key Objects

- **DAG** - Directed Acyclic Graph is the core concept of Airflow, collecting Tasks together, organized with dependencies and relationships to say how they should run.
- **Dag run** - A DAG Run is an object representing an instantiation of the DAG in time. Any time the DAG is executed, a DAG Run is created and all tasks inside it are executed. The status of the DAG Run depends on the tasks states. Each DAG Run is run separately from one another, meaning that you can have many runs of a DAG at the same time.
- **Task** - A Task is the basic unit of execution in Airflow. Tasks are arranged into DAGs, and then have upstream and downstream dependencies set between them into order to express the order they should run in.
- **Operator** - a template for a predefined Task, that you can just define declaratively inside your DAG
- **Sensor** - a special type of Operator that are designed to do exactly one thing - wait for something to occur. It can be time-based, or waiting for a file, or an external event, but all they do is wait until something happens, and then succeed so their downstream tasks can run
- **Hook** - A hook is an abstraction of a specific API that allows Airflow to interact with an external system. Hooks are built into many operators, but they can also be used directly in DAG code. Hooks wrap around APIs and provide methods to interact with different external systems. Hooks standardize how Astronomer interacts with external systems and using them makes your DAG code cleaner, easier to read, and less prone to errors. To use a hook, you typically only need a connection ID to connect with an external system. For more information about setting up connections, see Manage your connections in Apache Airflow. All hooks inherit from the BaseHook class, which contains the logic to set up an external connection with a connection ID. On top of making the connection to an external system, individual hooks can contain additional methods to perform various actions within the external system. These methods might rely on different Python libraries for these interactions. For example, the S3Hook relies on the boto3 library to manage its Amazon S3 connection.
- **XCom** - XComs (short for “cross-communications”) are a mechanism that let Tasks talk to each other, as by default Tasks are entirely isolated and may be running on entirely different machines.

An XCom is identified by a key (essentially its name), as well as the task_id and dag_id it came from. They can have any (serializable) value, but they are only designed for small amounts of data; do not use them to pass around large values, like dataframes.

### Key Components

- **Webserver** - A Flask server running with Gunicorn that serves the Airflow UI.
- **Scheduler** - A Daemon responsible for scheduling jobs. This is a multi-threaded Python process that determines what tasks need to be run, when they need to be run, and where they are run.
- **Database** - A database where all DAG and task metadata are stored. This is typically a Postgres database, but MySQL, MsSQL, and SQLite are also supported.
- **Executor** - The mechanism for running tasks. An executor is running within the scheduler whenever Airflow is operational.
- **Worker** - The process that executes tasks, as defined by the executor. Depending on which executor you choose, you may or may not have workers as part of your Airflow infrastructure.

### Types of executors

- Sequential Executor
- Local Executor
- Celery Executor
- Kubernetes Executer


## Hadoop

### Hadoop ecosystem ierarchy

├── HDFS <br>           
├──── HBase <br>                
├────── MapReduce <br>                    
├──────── Oozie    (Like ZooKeeper. Coordinates MR tasks)<br>
├──────── Pig      (high-level MR commands language)<br>
└──────── Hive 	   (high-level Sql-like MR commands lannguage)<br>

#### HDFS

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


#### HBase

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


#### MapReduce

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


#### Pig

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


#### Hive

SQL-like framework to MR tasks. HiveQL 

Works not so great for online or for small queries because of big overhead


### Map Reduce 2.0

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


## Spark

### Differences from Hadoop MR

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

### Pro's of Spark

- Can used for streaming and batching becuse don't have havy I/O operations
- Spark only for processing, not for storaging
- Spark can be connected to any source of data (HDFS, S3, Cassandra, HBase), beacuse of RDD abstraction
- Spark have plenty of libs (SparkSQL, MLib, GraphX, Spark Streaming)
- Works everywhere: HDFS, Mesos, Standalone (singlenode), in Cloud

### Key Concepts

#### RDD 

Sparks works on RDD, instead of HDFS

**RDD (Resilent Distributed Dataset)** - it's abstraction (API) to data.
It can be implemented over RAM, or HDFS, or any other source.
It's constructed by read different partitions/portions of the source

RDD not contains the actual data! It contains rules (lineage/dag) of HOW to calculate/get that data!

RDD can be :
- 1/2 dimensiinal - dataframe/dataset
- can be partitioned by different servers 
- Operation over RDD doesn't change RDD, they create new ones!
- All operations over RDD can be imagined as DAG (graph)

**Lineage** - it's RDD, that store chain of operations over RDD for each (!) RDD. it's DAG, in a nutshell.
If something get wrong, with some RDD, whle lineage restarts to that RDD.
When RDD is creates, lineage is updated (or created) and kept in-memory, by spark.
**Lineage** important part of *lazy evaluation*, that means, that Spark doesn't calculate evry step of transformation each time that you write it. It start execute whole plan only when one of the *actions* called.

Lineage essential for **Resilent** part in RDD's abbreviation, because it helps reprocess RDD, if something went wrong

**DAG** - very close to lineage ([medium](https://tsaiprabhanj.medium.com/spark-dag-and-rdd-lineage-cb41a0cdfc23#:~:text=In%20summary%2C%20RDD%20lineage%20provides,of%20tasks%20for%20improved%20performance.)), but represent more high-livel abstraction: RDD lineage provides the foundation for Spark’s fault tolerance by recording the sequence of transformations applied to data. The Spark DAG is a higher-level representation of the logical execution plan, incorporating RDD lineage and optimizing the execution of tasks for improved performance. Both concepts are crucial for Spark’s ability to efficiently process and recover from failures in distributed environments

There can be **Transformations** and **Actions** on RDDs:
**Transformations** - update the lineage
**Actions** - Execute actual lineage

**RDD Transformations**:
- **Narrow**:
	When each partition of parent RDD used only once (and no more) to create child partition:<br>
	A1 -> B1<br>
	A2 -> B2<br>
	A3 -> B3<br>
	That sort of dependencies let execute pipeline (lineage) on one node, without combining results<br>
	Example: filter operation<br>
- **Wide**:
	When each partition of parent RDD used by many child paririons<br>
	Example: groupbykey, reducebykey operation<br>
	**Join can be both Wide and NArrow: it depends on distribution of elements through partitions (like in MPP)**

So, because of that dependencies Scheduler make execution plan

#### Job
It's main 'calculation' object. It's called every time when you call an Action operation (means, when you actually need perform some calculation).
**№ of Jobs = № of Actions**

#### Stage
Stages are lays "inside" each job. Planner combine all narrow transformations together, so number of stages will be the same as number of wide-transormations in our rdd plus one
**№ of Stages = № of Wide Transformations + 1**

#### Task
Task lays under stages. And it's physicall calculation of stage over each partition of RDD. So there will be different task for different partitions, but there will be only one stage, for example
**№ of Stages depends on № of Partitions of RDD**

### Partitioner

It's process, that create "shuffle" operation in wide Transformations stage: it's reorganise partitions of parent rdd to child rdd.
It's important important to implement right logic of shuffling, to get rid of "skewed" data (imbalanced repartitioning)

There can be different algorithms in partitioner, to decide, in which partition which key should go:
- **Hash partitioner**: Just hash from key - as i.e. key%n (where n - number of partitions in child)
- **Range partitioner**: Where few "milestone" numbers (boundary points) are picked (which is most crucial part), and all key less than 1st number will be in first partition, all keys between 1st and snd - in second partition and so on (used for sorting tasks). Interesting part, that to determine that boundary points, Spark launches one more job (profiling), to scan your rdd (not full scan), and pick few pieces of data, to collect some statistic and determine boundary points for range partitioning

we can check what partitioner are last used:
'''python
some_rdd.partitioner.partitionFunc()
'''

### Spark Submit 
*What happens when we submit a Spark Job?*

- With spark-submit command user submits the Spark application to Spark cluster. This program invokes the main() method that is specified in the spark-submit command, which launches the **driver** program. 
- The **driver** program:
	- Converts the code into **DAG**, which will have plan of all the RDDs and transformations to be performed on them. During this phase driver also does some optimizations 
	- Then it converts the DAG to a physical execution plan with set of **stages**. 
	- After this physical plan, driver creates small execution units called **tasks**. 
- Then these tasks are sent to **Spark Cluster**.
- The driver program then talks to the cluster manager and **requests for the resources** for execution, which mentioned while calling spark-submit command
- Then the **cluster manger** launches the **executors** on the worker nodes. 
- **Executors** will **register** themselves with driver program so the driver program will have the complete knowledge about the executors. 
- Then **driver** program **sends** the tasks to the **executors** and starts the execution. 
- Driver program always monitors these tasks that are running on the executors till the completion of job. 
- When the job is completed or called stop() method in case of any failures, the driver program terminates and frees the allocated resources.

#### Vays to operate with data

- **RDD** - oldest API to manipulate on low-level. Not type-safe
- **DataFrame** (in Spark 2.0 or so), df - it's higher layer of abstraction than of RDD, and it's commonly used now. It's even faster than rdd due to low-level optimization
- **DataSet** - has reachest API, but not (!) availiable for python


#### Shared variables

- **Broadcast** - read-only variable
	it's file, that sent to **each executor** (not to the each task), cached, and can be accessed from inside task of that executor. It's created on spark driver, and sent to each node.
	It's ok for some relatevely small dictionaries/mappings , with which we can perfor, join without shuffle operation, because each partition of facts data will have acess to that common broadcasted dictionary.
	It's stored in serialiazble manner to lower memoru consumption

	Created by `brdcst = SparkContext.broadcast(v)`
	And can be accessed by `brdcst.value`

- **Accumulator** - write-only variable

	It's counters, that **each task** have, and after finishing their job, they send they result to driver programm, which accumulate them (simply sum-up)




### Operations on df

**Transformations** (Update lineage and returns new RDD):

- map - apply function for each element, returns changed elements
- filter - filter sub-rdd from rdd
- flatmap - apply function for each element, but can return group of elements for each element
- sample
- groupByKey 
- reduceByKey - grouping + function
- sortByKey
- union
- join
- cogroup
- crossproduct
- mapvalues
- sort
- partitionby

**Actions** (Execute lineage and returns value):

- collect
- reduce
- count
- lookup - get value by key
- save

Transformations operations are lazy - they don't compute while called.
Whole lineage started to compute only when Action operator called

### Architecture

- **Spark Session (Spark Context)** - Main entry point to Spark. It represents connection to Spark Cluster, and contains all information about that particular spark session. Which RDDs you have in that session, accumulators, Broadcast, etc.
It was context before Spark 2.0 presented. Now Session - more prefreable way. But in general they represent the same thing
	- **Spark Conf** - It's just configuration object, with wich you can create Spark Context, that you're really need
- **Worker nodes** - ???
- **Driver machine** - ???
- **Executor** - ???
- **Cluster Machine** - ???

### Caching

Because every time you call the action whole lineage executed, and it also may be needed to perform differnt actions over the same rdd, it's nice to have opportunity to precalculate rdd (perform reads, joins, etc), then save it (cached) and calculate needed actions then, without need to read all data again. You can do that with:

- `persist()` - which is have more options to store data in different ways 
- `cache()` - more widely used.

You can store cash on different storage levels:
- memory_only
- memory_and_disk
- memory_only_ser (serialized)
- memory_and_disk_ser
- disk_only
- ...

So you can cash rdd with that command (note, that it will cashed inly when first action will be called)
```python
from pyspark.storagelevel import StorageLevel

rdd.persist(StorageLevel.MEMORY_ONLY)
```

#### Memory Management 

- If it will lack of memory, LRU (Last recenty Used) meachanim will be launched, and deletes old RDDs
- Spark presents three storaging options:
	- memory storage, serialized Java objects
	- memory storage, deserialized Java objects
	- disk storage

#### Components
- Spark Application - Application itself, contains Driver and Executors
	- Spark Driver - coordination of whole process
	- Spark Executor - Execute process
- Spark Session - Initialize Spark Appliction, and create distibuted system
- Cluster Manager - Resource manager (YARN, Mesos, K8s, etc)


### Questions

- Difference between persist and cache?<br>
Cache() and persist() both the methods are used to improve performance of spark computation.<br>
These methods help to save intermediate results so they can be reused in subsequent stages.<br>
The only difference between cache() and persist() is:<br>
**Cache** technique we can save intermediate results in memory only
**Persist** we can save the intermediate results in 5 storage levels: MEMORY_ONLY, MEMORY_AND_DISK, MEMORY_ONLY_SER, MEMORY_AND_DISK_SER, DISK_ONLY).

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

### Links

1. https://youtube.com/playlist?list=PLHJp-gMPHvp9MDqV4qybL1FSBWcwMopcf&si=LVMlrr45tgwxIBja


## Kafka

### Base concepts

Kafka cluster consists of:
- Zookeper (DataBase whits all metadata about cluster)
- Broker-controller
- Brokers

Controller - it's just randomly selected cluster leader

messages for kafka:
- in bytes (serialized by producer)
- topic name
- key (optional) Messages with the same key will go to similar partition, which guarantee order (FIFO)

Topics phisically splitted for partitions, which is regular log files


### Reliability

Kafka guarantee that no one message will be lost, because of:
**replication_factor** - it's number of partition replication (to different brokers)

Each partition have their own leader, and Produce/Consume messages got through that leader.
Followers only check leader sometimes and ketchup changes from leader

**min.insync.replicas** - number of replicas that can be syncronized

**acks** - 0/1/-1(all) it's number of confirmation from broker, that he getting message (no confirmation, at least from leader, and from all)


### Produce 

1. Producer.send
2. Fetch metadata (from Zookeeper. Who is leader, where is Brokers)
3. Serialize message (key, value)
4. Define partition (based on key. if message didn't have key, that round-robin algorithm)
5. Compress message
6. Accumulate batch
7. Actual sending to broker

### Consume

1. Consumer.poll
2. Fetch metadata
3. Connect to partition-leaders and reading

Better to use consumer groups, when number of consumers equal to number of partitions in topic, so each consumer will read their own partition

Kafka commit reading, and there implemented two alghorithms of commits:
- AutoCommit (at most once) - but you can miss messages
- ManualCommit (at least once) - but you can duplicate messages

Exact once not implemented, but Kafka lets you do it yourself

## DBT

pass

## Terraform 

### General interaction sequence

- terraform init - *initializes project with terraform files. It's first command to do*
- terraform plan - *planning changes. Showing what will be done*
- terraform apply - *actually applies changes to real world*
- terraform destroy - *destroy all instances, created by terraform*

Backend of the terraform can be stored:

- locally: on the pc (ok for playground)
- remote: in terraform cloud (free up to 5 users)
- remote: selfhosted (in S3 + DynamoDB (in cloud, for instance))



