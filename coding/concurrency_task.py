'''
First have a look at concurrency.py to understand what's going on

Then let's try to solve some problem

1. You need to write function that takes string (username), and make some usernick based on that name (logic doesn't matter)
2. You need to create function, that take list of usernames, make nicks for them, and return list of nicks
	2.1. Now make that function asyncronious
	2.2. Now make that function return result in the same order, as input!
'''

from multiprocessing import Process
from multiprocessing.pool import ThreadPool
from threading import Thread
import queue
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed

import time

class User():

	SLEEP = 1
	NICK_FORMAT = 'xXx_{}_xXx'

	def __init__(self, username: str):
		self.name = username

	def get_nick(self):
		time.sleep(User.SLEEP)  # just to emulate some work
		return User.NICK_FORMAT.format(self.name)

	def put_nick_in_queue(self, queue):
		nick = self.get_nick()
		queue.put(nick)
		queue.task_done()

	def put_nick_in_results_list(self, results_list, place):
		nick = self.get_nick()
		results_list[place] = nick


class Community():

	def __init__(self, users: list[User]):
		self.users = users

	def get_nicks_sequentially(self):

		list_of_nicks = []
		for user in self.users:
			list_of_nicks.append(user.get_nick())

		print(list_of_nicks)

	def get_nicks_threading_random(self):

		'''
		Just for studing purposes lets create threading with no order guaranteed function, using Queue

		Here we will use Threading module and Queue (it's thread-safe structure to get results from Threads).
		So we create single Queue object, and pass it in each thread, while creating them.
		Then we need separate user function, that not only returns the nick, but put in in the Queue
		Then we start our Thread (n.b. start() - it's create fully new thread. run() - it's run existing thread)
		And join results later
		Then we iterate over Queue and get all of the results

		So, nevertherless tasks calculated in parallel - we should iterate over our users three times
		And order in results not guaranteed

		https://docs.python.org/3/library/threading.html
		https://docs.python.org/3/library/queue.html#Queue.Queue

		https://stackoverflow.com/questions/11968689/wait-until-all-threads-are-finished-in-python
		https://stackoverflow.com/questions/1886090/return-value-from-thread
		https://stackoverflow.com/questions/6893968/how-to-get-the-return-value-from-a-thread
		'''

		result = queue.Queue()
		threads = []

		for user in self.users:
			thread = Thread(target=user.put_nick_in_queue, args=(result, ))	
			threads.append(thread)	
			thread.start()

		for thread in threads:
			thread.join()

		list_of_nicks = []	
		for user in self.users:
			list_of_nicks.append(result.get())

		print(list_of_nicks)

	def get_nicks_threading_ordered_additional_structure(self):

		'''
		To get results in right order, we can create not Queue, but some structure
		It can be just list, and place result of each Thread just in right place.
		It's possible, parce que we start Threads in right order
		'''

		# at first we need to create structure, where we will store results. Because we can't just ger result from Thread!
		# We need to create something, where to put result, and it will be done inside the thread
		# regular append to list won't work, because result will be similar to queue - append order not guaranteed
		list_of_nicks = [None for user in range(len(self.users))]
		threads = []

		for i, user in enumerate(self.users):
			thread = Thread(target=user.put_nick_in_results_list, args=(list_of_nicks, i))
			threads.append(thread)	
			thread.start()

		for thread in threads:
			thread.join()

		print(list_of_nicks)


	def get_nicks_threading_ordered_threadpool(self):
		'''
		https://superfastpython.com/threadpool-python/
		'''

		list_of_nicks = []

		# first we create ThreadPool object (which is strangely part of multyprocessing lib)
		# Then we map (works like regular map) some func to each item in iterable
		# map - guarantees order
		# we can also use map_async function, which not guarantees order of func returns

		with ThreadPool(len(self.users)) as pool:
			for result in pool.map(User.get_nick, self.users):
				list_of_nicks.append(result)

		print(list_of_nicks)

	def get_nicks_threading_random_threadpool(self):
		'''
		the same as previous function, but with map_async
		'''

		list_of_nicks = []

		pool = ThreadPool(len(self.users))
		# we can't use same for loop, because result from map_async not iterable
		# so we need to asyncroniously launch pool with map_async, and then get all the results with get()
		async_result = pool.map_async(User.get_nick, self.users)

		# wait for the task to complete, or 10 sec for timeout
		async_result.wait(timeout=10)

		if async_result.ready():
			if async_result.successful():
				list_of_nicks = async_result.get()
			else:
				print('some error')
		else:
			print('not ready')

		# we need to close pool manually to free resourses, because we dont use with context manager
		pool.close()

		print(list_of_nicks)


	def get_nicks_threading_random_threadpoolexecutor(self):
		'''
		concurrent.futures it's lib on top of standard Threading and Multiprocessing libs,
		provides unified API for operating with threads and processes

		https://superfastpython.com/threadpool-python/
		https://docs.python.org/3/library/concurrent.futures.html

		https://www.tutorialspoint.com/concurrency_in_python/concurrency_in_python_pool_of_threads.htm#:~:text=With%20the%20help%20of%20concurrent,default,%20the%20number%20is%205
		'''

		list_of_nicks = []

		with ThreadPoolExecutor(len(self.users)) as executor:

			pool = []

			# at first we Sumbit (start) our threads
			for user in self.users:
				thread = executor.submit(user.get_nick)
				# and collect all threads in pool (we can do it with list comprehension also)
				pool.append(thread)

			# then we wait until all threads will be done:
			for thread in as_completed(pool):
				list_of_nicks.append(thread.result())

		print(list_of_nicks)


	def get_nicks_threading_ordered_threadpoolexecutor(self):
		'''
		We can use map functions (which guarantees order) with ThreadPoolExecutor
		'''

		list_of_nicks = []

		with ThreadPoolExecutor(len(self.users)) as executor:

			results = executor.map(User.get_nick, self.users)

		# then we wait until all threads will be done:
		for result in results:
			list_of_nicks.append(result)

		print(list_of_nicks)


	def get_nicks_threading_ordered_threadpoolexecutor_structure(self):
		'''
		We alse can use some dict (which will be orderd as input), while submitting threads, to map later results,
		no matter which thread end his work in which order
		'''

		list_of_nicks = []
		thread_to_user = {}
		with ThreadPoolExecutor(len(self.users)) as executor:

			thread_to_user = {user: executor.submit(user.get_nick) for user in self.users}

			# then we wait until all threads will be done:
			if as_completed(thread_to_user.values()):
				for _, future in thread_to_user.items():
					list_of_nicks.append(future.result())

		print(list_of_nicks)


	def get_nicks_multiprocessing_random(self):
		pass

	def get_nicks_multiprocessing_random(self):
		pass


if __name__ == '__main__':

	com = Community([User('user1'), User('user2'), User('user3'), User('user4'), User('user5')])

	def tester(method):
		start = time.time()
		method()
		end = time.time()
		print(f'{method.__name__} took: {end - start}')

	# tester(com.get_nicks_sequentially)
	# tester(com.get_nicks_threading_random)
	# tester(com.get_nicks_threading_ordered_additional_structure)
	# tester(com.get_nicks_threading_ordered_threadpool)
	# tester(com.get_nicks_threading_random_threadpool)
	# tester(com.get_nicks_threading_random_threadpoolexecutor)
	# tester(com.get_nicks_threading_ordered_threadpoolexecutor)
	# tester(com.get_nicks_threading_ordered_threadpoolexecutor_structure)
