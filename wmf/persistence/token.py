
__docformat__ = "restructuredtext en"

class Token:
	__slots__ = (
		'__content',
		'__revision_ids'
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
			self.__revision_ids       = [revision.getId()]
			print revision.getId()
		else:
			self.__content            = content
			self.__revision_ids       = []
	
	def deflate(self):
		"""
		Produces a JSONable version of the instance.
		
		:Return:
			A JSONable dictionary
		"""
		return {
			'content' : self.__content,
			'revision': self.__revision_ids
		}
	
	@staticmethod
	def inflate(json):
		"""
		Creates a Token identical to the one whose deflate() call 
		produced json.
		
		:Parameters:
			json
				JSONable version of a Token
			
		:Return:
			Token
		"""
		token = Token()
		
		token.__content      = json['content']
		token.__revision_ids = json['revision']
		
		return token
	
	def getContent(self): return self.__content
	def setContent(self, content): self.__content = content
	def getRevisionIds(self): return self.__revision_ids
	def setRevisionIds(self, revision_ids): self.__revision_ids = revision_ids
	
	#get number of revisions in which this token occurs
	def getVisible(self): return len(self.__revision_ids)
	
	#get revision in which this token was created
	def getAddedRevision(self):
		return self.__revision_ids[0]
		
	#get most recent revision in which this token appears
	def getMostRecentRevision(self):
		return self.__revision_ids[-1]
	
	def increment(self, revision):
		"""
		Increments the internal PWR counter of the word.
		
		Note: This is probably not the best way to update the PWR of a
		word since it is hard to extend for PWV.  Refactoring this 
		function is likely.
		"""
		self.__revision_ids.append(revision.getId())
	
	def __str__(self):
		return str(self.toJSON())
	
	def __hash__(self):
		return id(self)
	
	def __eq__(self, other):
		try:
			if (
				self.getContent()     == other.getContent() and
				self.getRevisionIds() == other.getRevisionIds()
				):
				return True
			else:
				return False
			
		except AttributeError:
			return False
	
	def __ne__(self, other):
		return not self == other
	
	
