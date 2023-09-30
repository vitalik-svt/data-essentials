import unittest
from collections.abc import Iterable

class Sorting:

	'''implementation of merge sorting algorithm, that takes iterable and sort it'''

	def __init__(self, values: Iterable):
		self.values = values


	def merge_sort(self):

		len = len(self.values)


	def merge(self):
		pass


	def __repr__(self):
		return str(self.values)