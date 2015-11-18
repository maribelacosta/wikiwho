from .limited_queue import LimitedQueue

__docformat__ = "restructuredtext en"

class LimitedDictLists(dict):
	"""
	Represents a limited size dictionary.  When the dictionary is full and 
	another item is added to it, the oldest item in the dictionary is thrown 
	away.
	"""
	
	def __init__(self, pairs=[], maxsize=None):
		"""
		Constructs a new LimitedDict.  If `maxsize` is not specified,
		it will be assumed to be len(pairs). 
		
		:Parameters:
			pairs : dict | iterable pairs
				A dict of (key->value) pairs or an iterator over pairs.
			maxsize : int
				The number of values that will be remembered
			
		"""
		#Create a clean iterator of pairs
		try:
			pairs = [(k,v) for (k, v) in pairs]
		except AttributeError:
			pairs = [(k,v) for (k, v) in pairs.iteritems()]
			
		#Determine how large the maxsize should be
		if maxsize != None:
			self.__maxsize = maxsize
		else:
			self.__maxsize = len(pairs)
			
		#Prime the queue
		self.__queue = LimitedQueue(maxlen=self.__maxsize)
		
		#Load in the pairs
		for k, v in pairs:
			self.__setitem__(k, v)
		
		
	
	def __getitem__(self, key):
		if dict.__contains__(self, key) and len(dict.__getitem__(self, key)) > 0:
			return dict.__getitem__(self, key)[0]
		else:
			raise KeyError(key)
	
	
	def __delitem__(self, key):
		if key in self and len(dict.__getitem__(self, key)) > 0:
			dict.__delitem__(self, key)
		else:
			raise KeyError(key)
	
	def __iter__(self):
		for pair in self.__queue:
			yield pair
	
	def __len__(self):
		return len(self.__queue)
	
	
	def __str__(self):
		return self.__repr__()
	
	
	def __repr__(self):
		return "%s(%r,%r)" % (
			self.__class__.__name__,
			self.__maxsize,
			[pair for pair in self]
		)
	
	def getMaxSize(self): return self.__maxsize
	def getQueue(self): return self.__queue
	
	def insert(self, key, value):
		"""
		Inserts a new key-value pair into the dictionary.  If the 
		dictionary is full, this function will return an expectorate;
		otherwise, it returns None. 
		
		:Parameters:
			key : hashable
				key to reference value
			value
				value to store
			
		:Return:
			A (key, value) pair expectorate if the dictionary is 
			full or None if it is not. 
		"""
		return self.__setitem__(key, value)
		
	
	def __setitem__(self, key, value):
		"""
		Inserts a new key-value pair into the dictionary.  If the 
		dictionary is full, this function will return an expectorate;
		otherwise, it returns None. 
		
		:Parameters:
			key : hashable
				key to reference value
			value
				value to store
			
		:Return:
			A (key, value) pair expectorate if the dictionary is 
			full or None if it is not. 
		"""
		#The queue will return something interesting if it is full
		expectorate = self.__queue.append((key,value))
		
		if expectorate != None and expectorate[0] in self:
			#Something got spit out of the queue
			#Take it out of the map
			if dict.__getitem__(self, expectorate[0])[-1] == expectorate[1]:
				retVal = dict.__getitem__(self, expectorate[0]).pop()
				
				if len(dict.__getitem__(self, expectorate[0])) == 0:
					dict.__delitem__(self, expectorate[0])
				
				return retVal
		
		if key in self:
			dict.__getitem__(self, key).insert(0, value)
		else:
			dict.__setitem__(self, key, [value])
			
	
	
	def getByIndex(self, index):
		"""
		Gets a pair based on the order it was added where 0 is the oldest and
		self.getLimit()-1 was most recently added.
		"""
		return self.__queue.get(index)[1]
	
	

