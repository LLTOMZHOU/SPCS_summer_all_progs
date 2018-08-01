class test():
	def __init__(self, num):
		self.number = num
		print self.output()

	def output(self):
		for i in range(10):
			return i


# Define an empty class:
class C:
   pass

# Define a global function:
def meth(myself, arg):
   myself.val = arg
   return myself.val



def main():
	'''
	aaa = test(4)
	print type(aaa)
	print aaa
	'''

	# Poke the method into the class:
	C.meth = meth


if __name__ == "__main__":
	main()
