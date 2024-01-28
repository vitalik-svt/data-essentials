'''
Simple example to undersatnd how concurrency in python works

In that example we will create code with two functions
1) spin - will show symbols \|/- one after one in infinite (simulate spinning in ascii)
2) slow - just slqqp for some amount of seconds
When slow function ends - we will stop our spin process and end programm

'''

# Base functions for Threading and Multiprocessing

import itertools
import time
from threading import Event

def spin(msg: str, done: Event) -> None:
	'''function, that accept some msg to show,
	and done-flag, which is Event object. 
	By that object we will rule our thread and stop that infinite cycle'''

	def _erase(length: int):
		print(f'\r{length}\r', end='')

	# itertools.cycle makes infinite cycle over some iterable
	for char in itertools.cycle(r'\|/-'):
		# we will print our spin "load" symbols and our message
		status = f'\r{char} {msg}'
		# end parameter by default is newline, but we want to show all of that in one line, so we set it to ""
		print(status, end='', flush=True)  # you can read a little bit about flush there https://realpython.com/python-flush-print-output/
		# we create set of blank symbols to "erase" our output
		blanks = ' ' * len(status)
		# by default Event.wait - False. But we can call Event.set(), and it will change done.wait for True, which will be our command to leave cycle
		# also we have timeout argument, which return False, if timeout reached. So here we create 0.1 per sec frequency of updating our output
		if done.wait(.1):
			# there we print blanks, to "erase" our output before exiting, because we 
			_erase(blanks)
			break
		# there we print blanks, to "erase" our output before next showing 
		_erase(blanks)

def slow(sleeping: int = 5) -> str:
	'''that function demonstrates any slow connection/io operation/etc. So it's just sleep without any processor'''
	time.sleep(sleeping)
	return 'some return from slow function'


# 1. Threading

# from threading import Thread, Event
# I import threading to place all Events in one .py file for convinient usage

import threading

def threading_main():

	'''
	Key things in Threading is:
	1) Thread object, that we can only start
	2) Event object - we will use it to rule threads
	3) Event.set() makes Event == True, and with that we will break our infinite cycle
	'''

	# "declaring" an event object, to pass it to our spin function
	done = threading.Event()
	# creating a Thread object as Thread (func, *args)
	spinner = threading.Thread(target=spin, args=('thinking!', done))
	print(f'spinner object is {spinner}')
	# start our spinning thread
	spinner.start()
	# then we launch slow function in that, main thread. So from now, both thread will work in "parallel". But our main thread only sleep
	result = slow()
	# when slow function ends, we can trigger done Event, to break the infinite cycle
	done.set()
	# and in the end we should "join" our threads, like, synchronize - let's say. In other words we will collect them in one, and continue in main thread
	spinner.join()
	
	return result



# Multiprocessing

# spin and slow functions are the same (except spin func definition should look like def spin(msg:str, done: synchronize.Event) -> None)

# from multiprocessing import Process, Event
# from multiprocessing import synchronize

import multiprocessing

def multiprocessing_main():

	# there is another, multiprocessing Event. But anything the same (except spinner is now Process object, not Thread)
	# api of threading and Multiprocessing looks nearly the same
	done = multiprocessing.Event()
	spinner = multiprocessing.Process(target=spin, args=('thinking!', done))
	print(f'spinner object is {spinner}')
	spinner.start()
	result = slow()
	done.set()
	spinner.join()

	return result


# Asyncio

import asyncio

async def async_spin(msg: str) -> None:

	def _erase(length: int):
		print(f'\r{length}\r', end='')

	for char in itertools.cycle(r'\|/-'):
		status = f'\r{char} {msg}'
		print(status, end='', flush=True)
		blanks = ' ' * len(status)
		try:
			# we need to use particularly asyncio.sleep to not block other coroutines, which will be blocked if we will use time.sleep
			await asyncio.sleep(.1)
		# if that exception raised by calling asyncio.Task.cancel we should break the cycle
		except asyncio.CancelledError:
			_erase(blanks)
			break
		_erase(blanks)


async def async_slow(sleeping: int = 5) -> str:
	# n.b.! we need to use particularly asyncio.sleep to not block other coroutines, which will be blocked if we will use time.sleep
	await asyncio.sleep(sleeping)
	return 'some return from slow function'


async def asyncio_supervisor() -> int:
	'''coroutine function declares with 'async def' words. '''

	# create_task method plans coroutine immediately (it return asyncio.Task object)
	spinner = asyncio.create_task(async_spin('thinking'))
	print(f'spinner object is {spinner}')
	# key word "await" blocks asyncio_supervisor until slow returns the control
	result = await async_slow()
	# with asyncio.Task.cancel we raise CancelledError inside spin function
	# so we cancel coroutine by ourselves, not with some Event object, as for threading or multiprocessing
	spinner.cancel()
	return result

	# so here is three main things to rule coroutines
	# 1. asyncio.run(some_func()) - it's stops main function, until some_func returns control
	# 2. asyncio.create_task(some_func()) - it doesn't stops main function, it returns asyncio.Task object (which is coroutine/coprogramm), 
	# and it immediately plan (but not immediately run!!!) that coroutine
	# 3. await some_func() - it block main programm until some_func retunrns control


def asyncio_main() -> None:
	'''The ONLY function in asyncio block. Others will be coroutines!'''

	# main function will be blocked until asyncio_supervisor returns the control
	result = asyncio.run(asyncio_supervisor())

	return result



if __name__ == '__main__':
	
	print('threading:')
	result = threading_main()
	print(result)

	print('multiprocessing:')
	result = multiprocessing_main()
	print(result)

	print('asyncio:')
	result = asyncio_main()
	print(result)





