from gl.containers import LimitedDictLists
from .word import Word
from .revision import Revision
from .word_list import WordList

__docformat__ = "restructuredtext en"

class PersistenceState:
	"""
	Represents the state of word persistence in an article.  When Revisions
	and their content are given to a PersistenceState (via `update()`), 
	PersistenceState keeps track of how words persist as new revisions are 
	made.
	"""
	__slots__ = (
		'__splitter',
		'__differ',
		'__revertLimit',
		'__lastRevision',
		'__revisions',
		'__recentPersistence'
	)
	def __init__(self, splitter, differ, revertLimit=15):
		"""
		Constructor
		
		:Parameters:
			splitter : function
				Function to use when splitting revision content into words
			differ : function
				Function to use when generating the difference between two list of words
			revertLimit : int
				The maximum amount of steps backwards a revert can take.
		"""
		self.__splitter          = splitter
		self.__differ            = differ 
		
		self.__revertLimit       = revertLimit
		self.__lastRevision      = None
		self.__revisions         = 0
		self.__recentPersistence = LimitedDictLists(maxsize=revertLimit)
	
	def deflate(self):
		"""
		Creates a JSONable version of the instance.  This includes a 
		carefully constructed index of Words as they represent the 
		history of revisions.
		
		:Return:
			A JSONable dictionary
		"""
		#create an index of all of the Words we care about.  This is 
		#important since we want all of the words to be referenced 
		#correctly.
		index = 0
		words = set()
		word2Index = {}
		index2WordJSON = {}
		for (checksum, revision) in self.__recentPersistence.getQueue():
			for word in revision.getWordList().getWords():
				if word not in word2Index:
					word2Index[word] = index
					index2WordJSON[index] = word.deflate()
					index += 1
			
		#Create a list of revisions that can be used to reload the 
		#recentPersistence.
		queue = []
		for (checksum, revision) in self.__recentPersistence.getQueue():
			#Ignore checksum.  It is in Revision. 
			queue.append(revision.deflate(word2Index))
			
		
		json = {
			'revertLimit':        self.__revertLimit,
			'revisions':          self.__revisions,
			'index2WordJSON':     index2WordJSON,
			'recentPersistence':  queue
		}
		return json
	
	@staticmethod
	def inflate(json, splitter, differ):
		"""
		Creates an instance of PersistentState that is identical to the
		one whose deflate() method was called to produce the json.
		
		:Parameters:
			json : dict
				a JSONable version of a PersistenceState
			splitter : function
				Function to use when splitting revision content
				into words
			differ : function
				Function to use when generating the difference
				between two list of words
			
		:Return:
			PersistentState
		"""
		#Create a state and populate fields
		state = PersistenceState(splitter, differ, json['revertLimit'])
		state.__revisions = json['revisions']
		
		#Create the word map
		index2Word = {}
		for index in json['index2WordJSON']:
			index2Word[index] = Word.inflate(json['index2WordJSON'][index])
		
		#For each thing in the history of persistence, create it using 
		#the index2Word we just made and insert it in the right 
		#order.
		for revisionJSON in json['recentPersistence']:
			r = Revision.inflate(revisionJSON, index2Word)
			state.__recentPersistence.insert(
				r.getChecksum(),
				r
			)
			state.__lastRevision = r
		
		return state
		
	def getLastRevision(self): return self.__lastRevision
	def getRevisions(self):	return self.__revisions
	
	def update(self, revision, content):
		"""
		Modifies the internal state based a new revision and content.
		
		:Parameters:
			revision : Revision
				The new revision to apply
			content : string
				The content for the new revision
			
		:Return:
			(wordsAdded, wordsRemoved) that resulted from applying
			the revision and content to the previous state.
		"""
		#Check for previous revisions that are identical
		if revision.getChecksum() in self.__recentPersistence:
			#we found a revert or a noop
			wordsAdded = []
			wordsRemoved = []
			revision.setWordList(self.__recentPersistence[revision.getChecksum()].getWordList())
		else:
			
			#actual change took place
			contents = self.__splitter(content)
			if self.__lastRevision == None:
				#First revision
				wordsRemoved = []
				revision.setWordList(WordList(contents, revision))
				wordsAdded = revision.getWordList().getWords()
			else:
				diff = self.__differ(
					self.__lastRevision.getContents(), 
					contents
				)
				(wl, wordsAdded, wordsRemoved) = self.__lastRevision.getWordList().applyDiff(diff, revision)
				
				revision.setWordList(wl)
		
		revision.getWordList().increment()
		self.__lastRevision = revision
		self.__recentPersistence.insert(revision.getChecksum(), revision)
		self.__revisions += 1
		
		return (wordsAdded, wordsRemoved)
	
	def __eq__(self, other):
		if (
			isinstance(other, self.__class__) and 
			self.getLastRevision() == other.getLastRevision() and
			self.getRevisions()    == other.getRevisions()
		):
			
			selfQueue = self.__recentPersistence.getQueue()
			otherQueue = other.__recentPersistence.getQueue()
			if len(selfQueue) == len(otherQueue):
				for i in range(0, len(selfQueue)):
					selfRevision = selfQueue[i]
					otherRevision = otherQueue[i]
					
					if selfRevision != otherRevision:
						return False
					
				return True
			else:
				return False
		else:
			return False
		
	def __ne__(self, other):
		return not self == other
