from functools import reduce
from pyspark import SparkContext
from pyspark.sql import SparkSession, functions as F
from pyspark.sql.functions import udf, col
from pyspark.sql.types import IntegerType, BooleanType


class Task_one():

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


class Task_two():

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





if __name__ == '__main__':

	# task_one = Task_one([10, 9, 8, 11, 12, 14, 2, 1])
	# task_one.sequential_run()
	# task_one.spark_run_old()
	# task_one.spark_run()

	# task_two = Task_two('./data/weather.csv')
	# task_two.spark_run_old()




