from .word import Word
from gl.containers import AutoVivifyingDict

__docformat__ = "restructuredtext en"

class WordList:
	"""
	Represents the content of a revision as an ordered list of `Word` and 
	allows certain functionality like applying a diff to create a new 
	`WordList`.
	"""
	
	__slots__=(
		"__words"
	)
	
	def __init__(self, contents=[], revision=NotImplemented):
		"""
		Constructor
		
		:Parameters:
			contents : list of strings
				The of Words to prime with
			revision : `revision.Revision`
				The revision from which the contents 
		"""
		self.__words = []
		if revision != NotImplemented:
			for content in contents:
				self.__words.append(Word(content, revision))
			
	
	@staticmethod
	def fromWords(words):
		"""
		Creates a `WordList` from a list of `Word`
		"""
		wordList = WordList()
		wordList.__words = words
		return wordList
		
	
	def deflate(self, word2Index):
		"""
		Produces a JSONable version of the instance based on a word 
		index that can be provided by PersistentState.
		
		:Parameters:
			word2Index : dict
				A word->index map.
		
		:Return:
			A JSONable dictionary
		"""
		json = []
		for word in self.__words:
			json.append(word2Index[word])
		
		return json
	
	@staticmethod
	def inflate(json, index2Word):
		"""
		Creates a WordList identical to the one whose deflate() call 
		produced json assuming index2Word reflects the same map 
		used by deflate().
		
		:Parameters:
			json
				JSONable version of a Word
			index2Word : dict
				an index->Word map
			
		:Return:
			WordList
		"""
		wordList = WordList()
		for index in json:
			wordList.__words.append(index2Word[index])
		
		return wordList
	
	
	def getWords(self): return self.__words
	def getContents(self):
		return [word.getContent() for word in self.__words]
	
	def increment(self):
		"""
		Increments the each words internal counter.  
		
		Note: This is probably not the best way to update the PWR of a
		word since it is hard to extend for PWV.  Refactoring this 
		function is likely. 
		"""
		for word in self.__words:
			word.increment()
	
	def applyDiff(self, diff, revision):
		"""
		Creates a new `WordList` by applying the result of a diff.  This
		method is useful for create a new `WordList` to represent the
		word persistence of a new revision.
		
		:Parameters:
			diff : dict
				A dictionary of sm (a SequenceMatcher) and contents (a list of word cotents)
			revision : `Revision`
				The revision whose changes the diff represents
			
		:Return:
			A tuple of (NewWordList, wordsAdded, wordRemoved)
		"""
		newList = []
		wordsAdded = []
		wordsRemoved = []
		for (code, a_start, a_end, b_start, b_end) in diff['sm'].get_opcodes():
			if code   == "insert":
				for content in diff['contents'][b_start:b_end]: 
					newWord = Word(content, revision)
					newList.append(newWord)
					wordsAdded.append(newWord)
			elif code == "replace":
				for content in diff['contents'][b_start:b_end]:
					newWord = Word(content, revision)
					newList.append(newWord)
					wordsAdded.append(newWord)
				
				wordsRemoved.extend(self.__words[a_start:a_end])
					
			elif code == "equal":
				newList.extend(self.__words[a_start:a_end])
			elif code == "delete":
				wordsRemoved.extend(self.__words[a_start:a_end])
					
		
		return (WordList.fromWords(newList), wordsAdded, wordsRemoved)
	
	def __eq__(self, other):
		try:
			s = self.getWords()
			o = other.getWords()
			if len(s) != len(o):
				return False
			else:
				for i in range(0, len(s)):
					sWord = s[i]
					oWord = o[i]
					if sWord != oWord:
						print "%s!=%s" % (sWord, oWord)
						return False
					
				return True
			
		
		except AttributeError:
			return False
		
	def __ne__(self, other):
		return not self == other
