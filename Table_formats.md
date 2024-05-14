# Table formats

## Row vs Columnar file/data formats 

phisycal models to store data can be these:<br>
example table:<br>

|rows|col_a|col_b|col_c|
|----|-----|-----|-----|
|row0| a0  | b0  | c0  |
|row1| a1  | b1  | c1  |
|row2| a2  | b2  | c2  |
|row3| a3  | b3  | c3  |

- Row format (each file contains some rows). they can united in longer rows, but, in a nutshell it's a continuous amount of rows.<br>
It's cool to use at row-store formats/dbs, **for OLTP/Write data-access pattern**, where you need to insert you just append row, where you need update/delete, you just need to find start of row, and read all continiously , because equential reading better for disk.<br>
it can be like in an example as is:

|     |     |     |     |     |     |
|-----|-----|-----|-----|-----|-----|
| a0  | b0  | c0  |	a1  | b1  | c1  |
| a2  | b2  | c2  | a3  | b3  | c3  |


- Pure Columnar

When your store one column in sequence.<br>
So, you need to find start of needed columns and read sequentially all data.<br>

|     |     |     |     |     |     |
|-----|-----|-----|-----|-----|-----|
| a0  | a1  | a2  |	a3  | b0  | b1  |
| b2  | b3  | c0  | c1  | c2  | c3  |

Or you can use different file for each column. Also, it's neccessary to undeerstand offset (~index) of each elemnt in file.
But it can be hard to organise that files physycally. So real-life implenetation of Parquet looks not like that, despite it's columnar table foramt

Columnar format **better suited for OLAP load pattern**, when you need to read from file/db

- Columnar (Hybrid)

That means, that you have both columns (horizontal) and columns(vertical) partitioning.

|     |     |     |     |     |     |
|-----|-----|-----|-----|-----|-----|
| a0  | a1  | b0  |	b1  | c0  | c1  |
| a2  | a3  | b2  | b3  | c2  | c3  |

So it's pure-columnar, but splitted by chunks (here is chunk length equals 2)

## Row formats

### Apahe Avro ([doc1](https://avro.apache.org/docs/), [doc2](https://avro.apache.org/docs/1.11.1/getting-started-python/)) 

it's an row format.
It also can be understood as json, but serialised in binary (which is oversimplifies whole thing, but still)

[nice video about avro internals](https://www.youtube.com/watch?v=0HsMaiLbXFk)

## Columnar formats

### ORC (Optimized Row Columnar) ([docs](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+ORC))

![orc](./images/tf_orc_1_1.webp)

ORC it's pure Columnar storaging format

[Article about ORC](https://medium.com/data-and-beyond/exploring-the-orc-file-format-advantages-use-cases-and-best-practices-for-data-storage-and-79c607ee9289)

ORC **optimized for reading**, mostly, because it has predicate pushdown, which allows Spark to skip over irrelevant data when querying large datasets.

### Apache Parquet ([docs](https://parquet.apache.org/docs/file-format/), [overview](https://learncsdesigns.medium.com/understanding-apache-parquet-d722645cfe74))

Parquet uses Columnar (hybrid) storaging format

**So, high-level:**<br>

- Parquet file consits of one or more **Row group** (can be configured by user)
- **Row group** contains exactly one column chunk per column (it's batch of columns)
- **Column chunk** contains one or more pages (it's part of column data)
- **Page** it's individible part of parquet

**And example:**<br>

![Parquet file representation](./images/tf_parquet_1_1.gif)

- 4-byte magic number "PAR1"
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
	- Column N chunk 0
- Row-group 2 
	- Column A chunk 1
		- Page 0
		- ...
		- Page N
	- Column B chunk 1
	- ...
	- Column N chunk 1
- Row-group M
- Footer **(File metadata)**
	- file
	- row-group 
	- column metadata start locations

![Parquet Architecture Again](./images/tf_parquet_1_2.png)

**Parquet has 6 encoding schemes, but there basic:** <br>

- Plain
	- Fixed width: means, that values stored back-to-back. cool for integers, for example:<br>
		file example: 1, 5, 6, 3, ...
	- Non-fixed width: used for different length data (strings). in that case data have length prefix
		file example: 2, yo, 3, no, 8, hobahoba, ...

- RLE_Dictionary (run-length encoding)
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

Parquet is **optimized for write-heavy workloads**, as it includes features such as encoding and dictionary compression that can improve write performance.

### Apache Arrow ([docs](https://arrow.apache.org/overview/))

its in-memory columnar format, which makes easier and faster tranfser between compnents.

Without a standard columnar data format, every database and language has to implement its own internal data format. This generates a lot of waste. Moving data from one system to another involves costly serialization and deserialization. In addition, common algorithms must often be rewritten for each data format.

Arrow's in-memory columnar data format is an out-of-the-box solution to these problems. Systems that use or support Arrow can transfer data between them at little-to-no cost. Moreover, they don't need to implement custom connectors for every other system. On top of these savings, a standardized memory format facilitates reuse of libraries of algorithms, even across languages.

![before](./images/tf_arrow_1_1.png)
![after](./images/tf_arrow_1_2.png)

[Video about arrow from creator](https://www.youtube.com/watch?v=R4BIXbfKBtk&t=548s)

## Enconding

We talked about formats there, but most of them impossible without enconding.
We can determine two main types of encoding:
- **loseless** - compression without losing any data
- **lossy** - we don't consider it in dat world, because don't want to lose anything

Most frequently used type of loselss encoding is **Run-length Encoding (RLE)**
par example, your data is:
*aaabbcdddddeefggg*

then you can encode it as symbol+number of reprtitions
*a3b2c1d4e2f1g2*

which can save you a space

Obviously, RLE most effective in sorted data!
So, if you choose thr encoding type of your Parquet file, make sure, that it's sorted somehow, so you will actually get that bonuses of encoding. Because there can be such situation, where RLE-encoded file will take similar space or even more(!), than without encoding 

## Data exchange protocols

It's protocols of exchanging binary data between machines

- **Thrift**
- **ProtoBuf (Protocol buffers)**

