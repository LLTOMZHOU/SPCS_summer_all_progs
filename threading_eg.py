import time
from threading import Thread
'''
def worker1():
	for i in range(10):
		print "----------Thread1"
		time.sleep(2)

def worker2():
	for i in range(5):
		print "Thread2"
		time.sleep(3)

t1 = Thread(name = "Thread1", target = worker1)
t1.start()

t2 = Thread(name = "Thread2", target = worker2)
t2.start()

time.sleep(25)

'''
def t():
	print "thread t starts"
	print "thread t ends"

def d():
	print "thread d starts"
	time.sleep(5)
	print "thread d ends"

tt1 = Thread(name = "thread t", target = t)
tt2 = Thread(name = "thread t", target = d)

tt2.setDaemon(True)

tt1.start()
tt2.start()

tt2.join()



class MyThread(Thread):
	def run(self): #the function will be called by t.start()
		print "running"
		return

if __name__ == "__main__":
	for i in range(3):
		t = MyThread()
		t.start()

