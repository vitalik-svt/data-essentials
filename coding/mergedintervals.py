#!/bin/python3

from typing import List, Tuple
import unittest
import math
import os
import random
import re
import sys

# Create the 'get_merged_intervals' function
# function need to merge intersected interwals and other intervals should be returned too
# The function is expected to return a 2D INTEGER ARRAY
# The function accepts 2D INTEGER ARRAY intervals as parameter
# Example: [(1, 2), (2, 3), (4, 5)] -> [(1, 3), (4, 5)]
 
class Schedule():
	
	def merge(self, intervals: List[Tuple]):

		# first of all let's rearrange (just in case) our intervals, so first element will be always less, than second
		# in the same time we generate new list, so passed parameter will be not changed
		intervals = [(min(x, y), max(x, y)) for x, y in intervals]

		# then let's order our intervals by start date
		intervals = sorted(intervals, key=(lambda x: x[0]))

		merged_intervals = []
		skip_next = False
		last_i = len(intervals) - 2

		for i, interval in enumerate(intervals[:-1]):

			if skip_next == True:
				if i == last_i:
					merged_intervals.append(intervals[i+1])
				else:
					skip_next = False
			else:
				if interval[1] >= intervals[i+1][0]:
					if i == last_i:
						merged_intervals.append((interval[0], intervals[i+1][1]))
					else:
						merged_intervals.append((interval[0], intervals[i+1][1]))
						skip_next = True
				else:
					if i == last_i:
						merged_intervals.append(interval)
						merged_intervals.append(intervals[i+1])
					else:
						merged_intervals.append(interval)
						skip_next = False


		return merged_intervals


class TestSolution(unittest.TestCase):

	def test_une(self):
		schedule = Schedule()
		self.assertEqual(schedule.merge([(1, 2), (2, 3), (4, 5)]), [(1, 3), (4, 5)])

	def test_deux(self):
		schedule = Schedule()
		self.assertEqual(schedule.merge([(1, 2), (4, 5)]), [(1, 2), (4, 5)])

	def test_troi(self):
		schedule = Schedule()
		self.assertEqual(schedule.merge([(2, 2), (2, 5)]), [(2, 5)])

	def test_quatre(self):
		schedule = Schedule()
		self.assertEqual(schedule.merge([(2, 2), (5, 2)]), [(2, 5)])

if __name__ == '__main__':
	unittest.main()
