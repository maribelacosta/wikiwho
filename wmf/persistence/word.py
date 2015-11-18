
__docformat__ = "restructuredtext en"

class Word:
	__slots__ = (
		'__content',
		'__revision_id',
		'__revision_user',
		'__revision_timestamp',
		'__visible'
	)
	
	def __init__(self, content=None, revision=None):
		"""
		Constructor
		
		:Parameters:
			content : unicode
				Content of the actual word
			revision : Revision
				Revision that the word was added by
			
		"""
		if content != None and revision != None:
			self.__content            = content
			self.__revision_id        = revision.getId()
			self.__revision_user      = revision.getUsername()
			self.__revision_timestamp = revision.getTimestamp()
			self.__visible            = 0
		else:
			self.__content            = content
			self.__revision_id        = None
			self.__revision_user      = None
			self.__revision_timestamp = None
			self.__visible            = 0
	
	def deflate(self):
		"""
		Produces a JSONable version of the instance.
		
		:Return:
			A JSONable dictionary
		"""
		return {
			'content': self.__content,
			'revision': {
				'id':        self.__revision_id,
				'user':      self.__revision_user,
				'timestamp': self.__revision_timestamp
			},
			'visible': self.__visible
		}
	
	@staticmethod
	def inflate(json):
		"""
		Creates a Word identical to the one whose deflate() call 
		produced json.
		
		:Parameters:
			json
				JSONable version of a Word
			
		:Return:
			Revision
		"""
		word = Word()
		word.__content            = json['content']
		word.__revision_id        = json['revision']['id']
		word.__revision_user      = json['revision']['user']
		word.__revision_timestamp = json['revision']['timestamp']
		word.__visible            = json['visible']
		
		return word
	
	def getContent(self): return self.__content
	def setContent(self, content): self.__content = content
	def getRevisionId(self): return self.__revision_id
	def setRevisionId(self, revision_id): self.__revision_id = revision_id
	def getRevisionUsername(self): return self.__revision_user
	def setRevisionUsername(self, username): self.__revision_user = username
	def getRevisionTimestamp(self): return self.__revision_timestamp
	def setRevisionTimestamp(self, timestamp): self.revision_timestamp = timestamp
	def getVisible(self): return self.__visible
	def setVisible(self, visible): self.__visible = visible
	
	def increment(self):
		"""
		Increments the internal PWR counter of the word.
		
		Note: This is probably not the best way to update the PWR of a
		word since it is hard to extend for PWV.  Refactoring this 
		function is likely.
		"""
		self.__visible += 1
	
	def __str__(self):
		return str(self.toJSON())
	
	def __hash__(self):
		return id(self)
	
	def __eq__(self, other):
		try:
			if (
				self.getContent()           == other.getContent() and
				self.getRevisionId()        == other.getRevisionId() and
				self.getRevisionUsername()  == other.getRevisionUsername() and
				self.getRevisionTimestamp() == other.getRevisionTimestamp() and
				self.getVisible()           == other.getVisible()
				):
				return True
			else:
				return False
			
		except AttributeError:
			return False
	
	def __ne__(self, other):
		return not self == other
	
	
