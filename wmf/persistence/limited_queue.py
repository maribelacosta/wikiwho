
__docformat__ = "restructuredtext en"

class LimitedQueue:
	"""
	A limited size queue, instances of this class will have a limited
	amount of spaces to store items.  When the queue is full and a
	subsequent item is added, an expectorate will be returned.
	
	This class's internal representation is a sized "circular" queue.
	Essentially, no matter what is added, removed or popped from this
	queue, it's internal structure does not change in size from its
	creation.  For the most part, this detail can be ignored, but it
	may be an important when considering performance.
	
	This should eventually be depricated in favor of collections.deque.
	"""
	
	def __init__(self, iterable=[], maxlen=None):
		"""
		Constructor
		
		:Parameters:
			iterable : iterable
				An iterator of elements to load into the queue
			maxlen : int
				The size of the queue, i.e. the perimeter of the circle.
		"""
		self.__circle  = list(iterable)
		if maxlen != None:
			self.__maxlen = maxlen
			self.__circle = self.__circle[0:maxlen]
		else:
			self.__maxlen = len(self.__circle)
		
		self.__counter = 0
		self.__length  = 0
		
		for i in range(len(self.__circle), self.__maxlen):
			self.__circle.append(None)
		
	
	def __iter__(self):
		for i in range(0, self.__length):
			if self.get(i) != None:
				yield self.get(i)
	
	def __reversed__(self):
		for i in range(self.__length-1, -1, -1):
			if self.get(i) != None:
				yield self.get(i)
			
		
	
	
	def __len__(self):
		return self.__length
		
	
	def index(self, item, j=0, k=None):
		"""
		Find the index of an item in the queue
		"""
		
		if k == None:
			k = len(self)
		
		for i in range(j, k):
			if item == self.__getitem__(i):
				return i
			
		raise ValueError("%s not in queue" % item)
		
	
	
	def pop(self, index=0):
		"""
		Removes an item from the queue and returns it.
		
		:Parameters:
			index : int
				Index of the item to remove and return
		
		:Return:
			The item removed.
		"""
		if index >= 0 and index < self.__length:
			#Remove the item from the correct location
			value = self.__circle.pop(self.__getInternalIndex(index))
			
			#Add a None to the end to make up for the removed item
			self.__circle.insert(self.__getInternalIndex(0), None)
			
			#Decrement length
			self.__length -= 1
			
			return value
		else:
			raise IndexError("Index %s does not exist in the queue and cannot be popped." % index)
	
	def __getitem__(self, index):
		return self.get(index)
		
	
	def __delitem__(self, index):
		self.pop(index)
		
	
	def __str__(self):
		return self.__repr__()
	
	
	def __repr__(self):
		return "%s(%r, %r)" % (
			self.__class__.__name__,
			self.__maxlen,
			[item for item in self]
		)
		
	
	
	def append(self, item):
		"""
		Adds a new object into the queue.  The return value depends on the
		state of the queue.  If the queue is full, the value returned will be 
		the object that falls off of the end of the queue.  If the queue is
		
		:Parameters:
			item
				The item to append to the queue
			
		:Return:
			The expectorate.  None if nothing if there was room for 
			item or the oldest item in the queue if the queue was 
			full.
		"""
		oldItem = self.__circle[self.__getNextInternalIndex()]
		
		self.__circle[self.__getNextInternalIndex()] = item
		self.__counter += 1
		if self.__length < self.__maxlen:
			self.__length += 1
		
		return oldItem
	
	
	def get(self, index):
		"""
		Gets a value from the queue.  This method will throw an IndexError if
		the index is not in the queue.
		
		:Parameters:
			index : int
				The index of the item to retrieve
			
		:Return:
			The item
		"""
		if index >= self.__length*-1 and index < self.__length:
			if index < 0:
				posIndex = self.__length+index
			else:
				posIndex = index
			
			return self.__circle[self.__getInternalIndex(posIndex)]
		else:
			raise IndexError("Index %s out of range(%s-%s)" % (index, self.__length*-1, self.__length))
		
	
	def __getNextInternalIndex(self):
		"""
		Gets the next location in self.__circle where new values should be 
		stored.
		"""
		return self.__counter % self.__maxlen
	
	

	def __getInternalIndex(self, index):
		"""
		Generates the actual internal index based off of an abstract 
		external index.  Essentially, this function turns what someone
		using this class thinks is an index to the right one for 
		self.__circle.
		
		:Parameters:
			index : int
				the index to convert
		
		:Return:
			Internal index
		"""
		if index >= 0 and index < self.__maxlen:
			if self.__counter >= self.__maxlen:
				return ((self.__counter)+index) % self.__maxlen
			else:
				return index
			
		else:
			raise IndexError("Index %s out of range" % index)
	
	
	def clear(self):
		"""
		Resets the queue to its empty state.
		"""
		self.__counter = 0
		self.__circle = []
		
		for i in range(0,self.__maxlen):
			self.__circle.append(None)

