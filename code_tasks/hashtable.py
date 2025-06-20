import unittest

class Hashtable:

	'''hashtable implementation'''

	def __init__(self, size):
		'''core thing in hastables it's creation of right amount of buckets'''
		self.size = size
		self.buckets = [[] for i in range(size)]


	@staticmethod
	def _get_hash(key, size):
		'''second core thing - it's to determine right hash function'''
		return hash(key) % size


	def set_key_value(self, key, value):
		bucket_id = Hashtable._get_hash(key, self.size)

		found = False
		for index, pair in enumerate(self.buckets[bucket_id]):
			if pair[0] == key:
				found = True
				self.buckets[bucket_id][index] = (key, value)
				break

		if found == False:
			self.buckets[bucket_id].append((key, value))


	def get_by_key(self, key):
		bucket_id = Hashtable._get_hash(key, self.size)

		found = False
		for index, pair in enumerate(self.buckets[bucket_id]):
			if pair[0] == key:
				found = True
				return self.buckets[bucket_id][index][1]

		if found == False:
			raise ValueError('There is no such key in hashtable')


	def del_by_key(self, key):
		bucket_id = _get_hash(key, self.size)

		for index, pair in enumerate(self.buckets[bucket_id]):
			if pair[0] == key:
				found = True
				del self.buckets[bucket_id][index]
				break

	def __repr__(self):
		return str(self.buckets)


class HashtableTest(unittest.TestCase):

	def test_add(self):

		ht = Hashtable(10)
		ht.set_key_value('a', 'b')

		self.assertTrue(ht.get_by_key('a'), 'b') 


if __name__ == '__main__':
	unittest.main()













