'''
First have a look at concurrency.py to understand what's going on

Then let's try to solve some problem

1. You need to write function that takes string (username), and make some usernick based on that name (logic doesn't matter)
2. You need to create function, that take list of usernames, make nicks for them, and return list of nicks
	2.1. Now make that function asyncronious
	2.2. Now make that function return result in the same order, as input!
'''

from multiprocessing import Process
from threading import Thread
import queue
import time

class User():

	SLEEP = 1
	NICK_FORMAT = 'xXx_{}_xXx'

	def __init__(self, username: str):
		self.name = username

	def get_nick(self):
		time.sleep(User.SLEEP)  # just to emulate something
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
		result_list = [None for user in range(len(self.users))]
		threads = []

		for i, user in enumerate(self.users):
			thread = Thread(target=user.put_nick_in_results_list, args=(result_list, i))
			threads.append(thread)	
			thread.start()

		for thread in threads:
			thread.join()

		print(result_list)


	def get_nicks_threading_ordered_threadpoolexecutor(self):
		pass

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
		print(f'{method.__name__} takes: {end - start}')

	tester(com.get_nicks_sequentially)
	tester(com.get_nicks_threading_random)
	tester(com.get_nicks_threading_ordered_additional_structure)

