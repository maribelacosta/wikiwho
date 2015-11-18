from .word_list import WordList
import time, calendar
import hashlib
from gl import wp

__docformat__ = "restructuredtext en"

class Revision:
	__slots__ = (
		"__id",
		"__pageId",
		"__username",
		"__timestamp",
		"__comment",
		"__checksum",
		"__wordList"
	)
	
	def __init__(self, revId=None, pageId=None, username=None, 
		timestamp=None, comment=None, checksum=None):
		"""
		Constructor
		
		:Parameters:
			revId : int
				-
			pageId : int
				-
			username : unicode
				-
			timestamp : int
				-
			comment : unicode
				-
			checksum : string
				32 character hex MD5 checksum of content
			
		"""
		self.__id        = revId
		self.__pageId    = pageId
		self.__username  = username
		self.__timestamp = timestamp
		self.__comment   = comment
		self.__checksum  = checksum
		self.__wordList  = None
	
	
	@staticmethod
	def fromWPAPI(rev):
		"""
		Creates a revision from the rev dictionary returned by the 
		Wikipedia API (format=json)
		
		:Parameters:
			rev : dict
				"rev" dictionary from the WP API
		
		:Return:
			Revision
		"""
		return Revision(
			rev.get('revid'),
			rev.get('pageid'),
			rev.get('user'),
			wp.wp2Timestamp(rev['timestamp']),
			rev.get('comment', ''),
			wp.digest(rev.get('*', ''))
		)
	
	def deflate(self, word2Index):
		"""
		Creates a JSONable version of the instance based on a word 
		index that can be provided by PersistentState.
		
		:Parameters:
			word2Index : dict
				A word->index map.
			
		:Return:
			A JSONable dictionary
		"""
		json = {
			'id':        self.__id,
			'username':  self.__username,
			'timestamp': self.__timestamp,
			'comment':   self.__comment,
			'pageId':    self.__pageId,
			'checksum':  self.__checksum
		}
		if self.__wordList != None:
			json['wordList'] = self.__wordList.deflate(word2Index)
		
		return json
	
	@staticmethod
	def inflate(json, index2Word):
		"""
		Creates a Revision instance identical to the one whose deflate()
		call produced json assuming index2Word reflects the same map 
		used by deflate().
		
		:Parameters:
			json
				JSONable version of a Word instance
			index2Word : dict
				an index->Word map
			
		:Return:
			Revision
		
		"""
		revision = Revision()
		revision.__id        = json['id']
		revision.__username  = json['username']
		revision.__timestamp = json['timestamp']
		revision.__comment   = json['comment']
		revision.__pageId    = json['pageId']
		revision.__checksum  = json['checksum']
		if 'wordList' in json:
			revision.setWordList(
				WordList.inflate(
					json['wordList'], 
					index2Word
				)
			)
		return revision
		
	
	def getId(self):                 return self.__id
	def getUsername(self):           return self.__username
	def getTimestamp(self):          return self.__timestamp
	def getComment(self):            return self.__comment
	def getPageId(self):             return self.__pageId
	def getChecksum(self):           return self.__checksum
	def getWordList(self):           return self.__wordList
	def setWordList(self, wordList): self.__wordList = wordList
	def getContents(self):           return self.__wordList.getContents()
	
	def __eq__(self, other):
		try:
			if (
				self.getId()        == other.getId() and
				self.getUsername()  == other.getUsername() and
				self.getTimestamp() == other.getTimestamp() and
				self.getComment()   == other.getComment() and
				self.getPageId()    == other.getPageId() and
				self.getChecksum()  == other.getChecksum() and
				self.getWordList()  == other.getWordList()
				):
				return True
			else:
				return False
		
		except AttributeError:
			return False
	
	def __ne__(self, other):
		return not self == other
