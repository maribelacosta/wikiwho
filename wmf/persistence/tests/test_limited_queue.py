import unittest
from ..limited_queue import LimitedQueue

def suite():
	suite = unittest.TestSuite(
		[
			unittest.TestLoader().loadTestsFromTestCase(LimitedQueueTestCase)
		]
	)
	
	return suite


##
# Limited Queue Test Case
#
class LimitedQueueTestCase(unittest.TestCase):
		
	def testIterator1(self):
		queue = LimitedQueue(maxlen=3)
		queue.append("1")
		queue.append("2")
		queue.append("3")
		queue.append("3")
		queue.append("3")
		for element in queue:
			self.failUnless(element == "3", "Iterator returns impossible value")
		
	def testIterator2(self):
		queue = LimitedQueue(maxlen=3)
		queue.append("1")
		queue.append("2")
		queue.append("3")
		queue.append("3")
		queue.append("3")
		queue.append(0)
		queue.append(1)
		queue.append(2)
		i = 0
		for element in queue:
			self.failUnless(element == i, "Iterator returns values in incorrect order")
			i += 1
		
	def testIterator3(self):
		queue = LimitedQueue(maxlen=100)
		queue.append(1)
		i = 0
		for element in queue:
			i += 1
			
		self.failUnless(i == 1, "Iterator yields incorrect number of values.")
		
	def testReverseIterator(self):
		queue = LimitedQueue(maxlen=90)
		queue.append(1)
		testList = []
		for element in queue:
			testList.append(element)
		
		testList.reverse()
		i = 0
		for element in reversed(queue):
			self.failUnless(testList[i] == element, "Iterator does not reverse correctly.")
			i +=1
			
		
	
	
	def testGet1(self):
		queue = LimitedQueue(maxlen=3)
		queue.append(1)
		queue.append(2)
		queue.append(3)
		for i in range(0, len(queue)):
			self.failUnless(queue[i] == queue.get(i), "get() and __getitem__ disagree on values")
			self.failUnless(queue[i] == i+1, "get() is not returning the correct item")
		
	def testGet2(self):
		queue = LimitedQueue(maxlen=3)
		queue.append(1)
		queue.append(2)
		queue.append(3)
		queue.append(4)
		queue.append(5)
		queue.append(6)
		for i in range(0, len(queue)):
			self.failUnless(queue[i] == queue.get(i), "get() and __getitem__ disagree on values")
			self.failUnless(queue[i] == i+4, "get() is not returning the correct item")
		
	
	def testGet3(self):
		queue = LimitedQueue(maxlen=3)
		queue.append(1)
		self.failUnless(queue.get(-1) == 1, "get() fails on negative numbers.  Expected %r, got %r" % (1, queue.get(-1)))
		queue.append(2)
		self.failUnless(queue.get(-1) == 2, "get() fails on negative numbers.  Expected %r, got %r" % (2, queue.get(-1)))
		queue.append(3)
		self.failUnless(queue.get(-1) == 3, "get() fails on negative numbers.  Expected %r, got %r" % (3, queue.get(-1)))
		queue.append(4)
		self.failUnless(queue.get(-1) == 4, "get() fails on negative numbers.  Expected %r, got %r" % (3, queue.get(-1)))
	
	def testGet4(self):
		queue = LimitedQueue(maxlen=3)
		queue.append(1)
		self.failUnless(queue.get(0) == 1, "get() fails on negative numbers.  Expected %r, got %r" % (1, queue.get(0)))
		queue.append(2)
		self.failUnless(queue.get(0) == 1, "get() fails on negative numbers.  Expected %r, got %r" % (1, queue.get(0)))
		queue.append(3)
		self.failUnless(queue.get(0) == 1, "get() fails on negative numbers.  Expected %r, got %r" % (1, queue.get(0)))
		queue.append(4)
		self.failUnless(queue.get(0) == 2, "get() fails on negative numbers.  Expected %r, got %r" % (2, queue.get(0)))
		
	
	def testLength(self):
		queue = LimitedQueue(maxlen=3)
		self.failUnless(len(queue) == 0, "Queue length on creation incorrect")
		expectorate = queue.append(1)
		self.failUnless(len(queue) == 1, "Queue length should be one, instead is %s" % len(queue))
		expectorate = queue.append(2)
		self.failUnless(len(queue) == 2, "Queue length should be two, instead is %s" % len(queue))
		expectorate = queue.append(3)
		self.failUnless(len(queue) == 3, "Queue length should be three, instead is %s" % len(queue))
		expectorate = queue.append(4)
		self.failUnless(len(queue) == 3, "Queue length should be three, instead is %s" % len(queue))
		
	def testAdd(self):
		queue = LimitedQueue(maxlen=3)
		expectorate = queue.append(1)
		self.failUnless(expectorate == None, "Expectorate is released prematurely")
		expectorate = queue.append(2)
		self.failUnless(expectorate == None, "Expectorate is released prematurely")
		expectorate = queue.append(3)
		self.failUnless(expectorate == None, "Expectorate is released prematurely")
		expectorate = queue.append(4)
		self.failUnless(expectorate == 1, "Expectorate should be %r, instead is %r" % (1, expectorate))
	
	
	def testPopSimple(self):
		queue = LimitedQueue(maxlen=4)
		queue.append(1)
		expectorate = queue.pop()
		self.failUnless(expectorate == 1, "Expected that %r would be popped out, instead was %r" % (1, expectorate))
		self.failUnless(len(queue) == 0, "Length should be zero after all elements are popped, has %s" % len(queue))
		
	def testPopSimpleError(self):
		queue = LimitedQueue(maxlen=4)
		self.assertRaises(IndexError, queue.pop)
		queue.append("derr")
		expectorate = queue.pop()
		self.failUnless(expectorate == "derr", "Expected that %r would be popped out, instead was %r" % ("derr", expectorate))
		
		self.assertRaises(IndexError, queue.pop)
		
	
	def testPopComplicatedPop(self):
		queue = LimitedQueue(maxlen=4)
		queue.append(1)
		queue.append(2)
		queue.append(3)
		queue.append(4)
		queue.append(5)
		value = queue.pop()
		self.failUnless(value == 2, "Incorrect value returned from pop.")
		self.failUnless(len(queue) == 3, "Length should be zero after all elements are popped, has %s" % len(queue))
		
		expectorate = queue.append(6)
		self.failUnless(expectorate == None, "%r was spit out even when the queue was not full." % expectorate)
		

if __name__ == "__main__":
	suite = suite()
	unittest.TextTestRunner(verbosity=2).run(suite)
