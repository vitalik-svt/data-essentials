
attribute = 'outside of class'

class Example:

	# here we define class attributes, which we can use in our methods
	attr_1 = 'class attr 1'
	attr_2 = ['class', 'attr', 2]

	# and here is tha attribute, which not be stored in instances
	attr_3 = 'pure class attribute'

	def __init__(self):

		# we can call class attrbiutes either with self (with instance) 
		self.some_1 = self.attr_1
		# or with classname
		self.some_2 = Example.attr_2


def run():
	
	exmpl_1 = Example()
	print(f'exmpl_1.some_1: {exmpl_1.some_1}')
	print(f'exmpl_1.some_2: {exmpl_1.some_2}')

	Example.attr_1 = 'class attr 1 changed'
	Example.attr_2 = ['class', 'attr', 2, 'changed']

	print(f'exmpl_1.some_1: {exmpl_1.some_1}')
	print(f'exmpl_1.some_2: {exmpl_1.some_2}')

	exmpl_2 = Example()

	print(f'exmpl_2.some_1: {exmpl_2.some_1}')
	print(f'exmpl_2.some_2: {exmpl_2.some_2}')


	print(f'exmpl_2.attr_3: {exmpl_2.attr_3}')
	Example.attr_3 = 'pure class attribute changed'
	print(f'exmpl_2.attr_3: {exmpl_2.attr_3}')


if __name__ == '__main__':
	run()
	