from functools import reduce
from pyspark import SparkContext
from pyspark.sql import SparkSession, functions as F
from pyspark.sql.functions import udf, col
from pyspark.sql.types import IntegerType, BooleanType


class Example_one():

	'''
	Let's imagine some task of sorting, filtering and calculating:
	We have the list of numbers, and we need to filter only odd, than sqare them, and then find max
	Of course we can find max odd number, and sqare it after, but for study purposes let's do it that way
	we will do it with help of basic mr operations: map, filter, reduce for that basic example
	'''

	def __init__(self, numbers: list):
		self.numbers = numbers

	# basic implementation of checking if it's odd number or not
	@staticmethod
	def is_odd(number):
		return True if number%2 != 0 else False

	@staticmethod
	def make_sqr(number):
		return number**2

	@staticmethod
	def find_max(a, b):
		return a if a >= b else b
		
	def sequential_run(self):

		'''Basic Python solution for that problem'''
		
		print(f'Our list is: {self.numbers}')

		# let's filter only odd numbers first
		odds = list(filter(self.is_odd, self.numbers))
		print(f'filtered odds is: {odds}')

		# Then let's sqare them up with map function (i'll do it with lambda, just to show that we obviously can use it here)

		sqrd = list(map(lambda x: x**2, odds))
		print(f'sqared odds is: {sqrd}')

		# And then let's find out maximum value with reduce (which is not really widely used rn, but anyway)

		maximum = reduce(self.find_max, sqrd)
		print(f'Max value is {maximum}')


	# And it's run perfectly, but it runs in sequential order!
	# We want parallelize things, and that's where we need spark

	def spark_run_old(self):

		print('STARTED')

		'''
		Let's do that old way first: with RDD and SparkContext (sc). Now it's not commonly used,
		because in Spark 2.0 introduced sparkSession and Dataframes, which is higher abstractions over scs and rdds
		'''

		# first of all we create Spark Context (which is main entry point object for Spark (at least before 2.0))
		sc = SparkContext()

		# Then we create rdd by calling parallelize function, which take some input, and create number of partition/slices (optional)
		rdd = sc.parallelize(self.numbers, numSlices = 2)

		print(f'Our rdd object is: {rdd}')
		print(f'Our rdd is partitoned by {rdd.getNumPartitions()} parts')  # Also let's check number of partitions

		# then we will call the Action! Only there calculation begins (we don't have any calculations, but still)
		print(f'Our actual data in rdd is: {rdd.collect()}')

		# and lets implement our logic
		odds = rdd.filter(self.is_odd)
		print(f'filtered odds is: {odds.collect()}')

		sqrd = odds.map(self.make_sqr)
		print(f'sqared odds is: {sqrd.collect()}')

		maximum = sqrd.reduce(self.find_max)
		print(f'Max value is {maximum}')

		del sc


	def spark_run(self):

		spark = (
			SparkSession
			.builder
			.appName("Python Spark SQL basic example")
			.config("spark.some.config.option", "some-value")
			.getOrCreate()
			)

		df = spark.createDataFrame(self.numbers, IntegerType()).toDF(*['value'])

		print(f'Our df object is: {df.show()}')

		# and lets implement our logic
		odd_func = udf(lambda row: self.is_odd(row), BooleanType())
		odds = (df
				.withColumn('is_odd', odd_func(col('value')))
				.filter(col('is_odd') == True))
		print(f'filtered odds is: {odds.show()}')


		sqr_func = udf(lambda row: self.make_sqr(row), IntegerType())
		sqrd = (odds
				.withColumn('sqrd_value', sqr_func(col('value'))))
		print(f'sqared odds is: {sqrd.show()}')

		# We can just use agg func
		maximum = sqrd.agg({'sqrd_value': 'max'}).collect()[0]
		print(f'Max value is {maximum}')

		del spark


class Example_two():

	'''
	Reading rdd from file 
	'''

	def __init__(self, file_path):
		self.file_path = file_path

	@staticmethod
	def find_max(a, b):
		return a if a >= b else b

	def spark_run_old(self):
		
		sc = SparkContext()

		raw_rdd = sc.textFile(self.file_path, 2)

		# Then let's get only year and temp from our raw_rdd
		def get_year_temp(row: tuple):

			new_row = (
				int(row.split(',')[0].split('-')[0]),
				int(row.split(',')[2])
				)

			return new_row


		select_rdd = raw_rdd.map(get_year_temp)

		max_rdd = select_rdd.reduceByKey(self.find_max)

		# n.b., that's because of lazy evaluation only there calculation begins!
		result = max_rdd.collect()

		print(result)

		del sc

class Example_three:

	'''
	Examples of different functions on RDDs
	'''

	def __init__(self):
		pass

	def spark_run_first(self):

		sc = SparkContext()

		# Create rdd in parallel 
		#(with few partitions, you can set that number by yourself with numSlices argument. default is None)
		rdd = sc.parallelize([1,2,3,4,5,6,7,8])

		# you can get number of partitions to be sure 
		rdd.getNumPartitions()

		# sort be descending order
		rdd.sortBy(lambda num: num * -1).collect()

		# Or we can take only take 2 first things
		rdd.sortBy(lambda num: num * -1).take(2)

		# Reduce function (remember - reduce is action& Means, that it's return result, not another RDD)
		rdd.reduce(lambda x, y: x + y)

		# Also we have map operation, that maps any function to each entering in partition.
		# But which is nice, we also have mapPartitions and mapPartitionsWithIndex functions
		# They perform map function on partition (!) level, not on row level (!)
		# it's useful for io operations: those you can open/close file once per partition, and not for each row in your RDD

		# Example of mapPartitions

		def partition_processing(iterable):
			result = []
			result.append('Start maping partition')
			result.extend([(i, -i) for i in iterable]) # let's just add negative column
			result.append('Finished maping partition')
			return result

		for i in rdd.mapPartitions(partition_processing).collect():
			print(i)

		# Example of mapPartitionsWithIndex
		def partition_indexer(index, iterable):
			return [f'partition number {index} contains {i}' for i in iterable]

		print(rdd.mapPartitionsWithIndex(partition_indexer).collect())

		# And some other examples of Functions
		rdd.collect()    					# entire rdd
		rdd.count()							# count of elements
		rdd.distinct().collect()			# distinct
		rdd.first()							# first element of the rdd
		rdd.take(2)							# two first elements
		rdd.countByValue()					# Frequency of each element
		rdd.max()								
		rdd.min()	
		rdd.takeOrdered(2)					# Bottom 2 elements of the rdd
		rdd.takeOrdered(2, lambda x: -x)	# Top 2 elements of the rdd

		del sc


	def spark_run_transformations(self):

		sc = SparkContext()

		# Create rdd in parallel 
		#(with few partitions, you can set that number by yourself with numSlices argument. default is None)
		kv_rdd = sc.parallelize([(1, 2), (3,4), (3,6), (1,3)])

		# multiple value by 10
		kv_rdd.mapValues(lambda x: x * 10).collect()

		# if map function will return some iterable, we can flatten it
		# for example, for first kv pair (1, 2) it will return two pairs(1, 0) and (1, 1), 
		# where 1 - is key, and 0 and 1 - it's flattend range
		kv_rdd.flatmMapValues(lambda x: range(0, x)).collect()

		# just to get key
		kv_rdd.keys().collect()

		# just to get values
		kv_rdd.values().collect()

		# sortByKey: it's an Transformation uses Range partitioner, that described in .md
		kv_rdd.sortByKey().collect()

		# reduceByKey - it's an Transformation too
		kv_rdd.reduceByKey(lambda x, y: x + y).collect()

		# groupByKey - it's only groups by key, and let you to perform any other custom aggregation function
		# nb, that it may bring some memory issues, because you collect all the data without any aggregation
		for k, v in kv_rdd.groupByKey().collect():
			print(f'for key {k} group will be {list(v)}')

		# transformations over the pair of kv_rdd

		# Create rdd in parallel 
		#(with few partitions, you can set that number by yourself with numSlices argument. default is None)
		rdd_first = sc.parallelize([(1, 2), (3,4), (3,6), (3,6), (1,3)])
		rdd_second = sc.parallelize([(3, 9), (2, 3)])

		# this take keys, that presented in first rdd, but not in second
		# so the answer will be [(1,2), (1,3)]
		rdd_first.substractByKey(rdd_second).collect()

		# cogroup it's sort of join operation, which returns pair of values from left and right rdd, grouped by key
		# (1, ([2, 3], []))
		# (3, ([4, 6, 6], [9]))
		# (2, ([], [3]))
		rdd_first.coGroup(rdd_second)

		del sc


	def spark_run_actions(self):

		sc = SparkContext()

		kv_rdd = sc.parallelize([(1, 2), (3,4), (3,6), (3,6), (1,3)])

		# it's operation of updating the dictionary, so it will show latest value
		# in our case answer will be {1: 3, 3, 6}
		kv_rdd.collectAsMap()

		# return all values from that key
		kv_rdd.lookup(3)

		# let's generate pairs from regular list rdd

		rdd = sc.parallelize(100, 2, 3, 3, 410, 3, 3, 3, 4, 104, 2)

		# first lets make pairs, with rule if number>100 then it's 'high', else 'low'

		kv_rdd = rdd.keyBy(lambda x: 'low' if x < 100 else 'high')

		# then we can reduce it to get the sum, or groupby to have something more in the future
		kv_rdd.reduceByKey(lambda x, y: x + y).collect()

		# or we can do similar, but with group by
		kv.groupBy(lambda x: 'low' if x < 100 else 'high').collect()

		del sc

	def words_counter(self, file_path):

		sc = SparkContext()

		# first - each line it's separate elemnt
		rdd_of_lines = sc.textFile(file_path)
		# second - we should split line to words, and flatten it! So make each new "row" of word for rdd
		rdd_of_words = rdd_of_lines.flatMap(lambda line: line.split(" "))
		# then we create paired rdd with word as key, and 1 - as value, which represents apperance of the word
		rdd_of_pairs = rdd_of_words.map(lambda x: (x, 1))
		# then we reduce it by key!
		counter_rdd = rdd_of_pairs.reduceByKey(lambda x, y: x + y)

		print(counter_rdd.collect())

		# or we can just use countByValue()

		print(rdd_of_words.countByValue())

		del sc

	def spark_joins(self, temp_path, city_dict_path):

		sc = SparkContext()

		first = sc.parallelize([(1, 2), (3,4), (3,6), (3,6), (1,3)])
		second = sc.parallelize([(3, 9), (2, 3)])

		print(first.join(second).collect())

		# it's inner join, result will be
		# [(3, (4, 9)), (3, (6, 9)), (3, (6, 9))]  

		# and left and right
		print(first.leftOuterJoin(second).collect())
		print(first.rightOuterJoin(second).collect())

		# lets do some real life example: find out max trmp for each city

		max_temp = (
			sc.textFile(temp_path)
			.map(lambda row: (row.split(',')[1], int(row.split(',')[2])))
			.reduceByKey(lambda x, y: max(x, y)) 
			)

		print(max_temp.collect())

		city_dict = (
			sc.textFile(city_dict_path)
			.map(lambda row: (row.split(',')[0], row.split(',')[1]))
			)

		print(city_dict.collect())

		joined = max_temp.join(city_dict)
		result = joined.map(lambda row: (row[1][1], row[1][0]))

		print(result.collect())

		del sc


	def broadcast_joins(self, stock_path, div_path):

		'''
		our stock rdd will have many data, and dividents only few. So we will broadacst it.
		We should understand difference between open and close price of stock for each day, where dividends were given
		'''

		sc = SparkContext()

		def getParsedDailyRecord(daily):
			daily_list = daily.split("\t")
			exchange = str(daily_list[0])
			symbol = str(daily_list[1])
			date = str(daily_list[2])
			opn = float(daily_list[3])
			high = float(daily_list[4])
			close = float(daily_list[6])
			return ((exchange, symbol, date), opn, close)

		def generateDividendsDictionary(dividend):
			dividend_list = dividend.split("\t")
			exchange = str(dividend_list[0])
			symbol = str(dividend_list[1])
			date = str(dividend_list[2])
			dividends = float(dividend_list[3])
			return ((exchange, symbol, date), dividends)


		daily_rdd = sc.textFile(stock_path)
		daily_pair_rdd = daily_rdd.map(getParsedDailyRecord)

		dividends = sc.textFile(div_path)
		dividends_pair_rdd = dividends.map(generateDividendsDictionary)
		# we construct dict from rdd, just to call .get by key in the future, for simplicity
		dividends_dict = dict(dividends_pair_rdd.collect())

		# and create broadcast
		dividends_bdct = sc.broadcast(dividends_dict)

		def getDiffAndDividends(daily_pair_iter):
			for daily_pair in daily_pair_iter:
				key, opn, close = daily_pair
				# to access broadcast, we shoult call broadcast.value method, because broadcast it's layer upon our object
				dividend = dividends_bdct.value.get(key)
				if dividend is None:
					continue
				else:
					exchange, symbol, date = key
					yield "{} {} {} {} {}".format(exchange, symbol, date, close - opn, dividend)


		result_rdd = daily_pair_rdd.mapPartitions(getDiffAndDividends)
		for result in result_rdd.take(5):
			print(result)


		# for df it's explain() method, that sows execution plan, but for rdd its toDebugString
		print(result_rdd.toDebugString())
		# initialize sparksessionm and then
		# print(result_rdd.toDF().explain())


		del sc



if __name__ == '__main__':

	example_one = Example_one([10, 9, 8, 11, 12, 14, 2, 1])
	example_one.sequential_run()
	example_one.spark_run_old()
	example_one.spark_run()

	example_two = Example_two('./data/weather.csv')
	example_two.spark_run_old()

	example_three = Example_three()
	example_three.spark_run_first()
	example_three.spark_run_transformations()
	example_three.spark_run_actions()
	example_three.words_counter('./data/ebook.txt')
	example_three.spark_joins('./data/weather.csv', './data/zips_city.csv')
	example_three.broadcast_joins('./data/nyse_daily.tsv', './data/nyse_dividends.tsv')



