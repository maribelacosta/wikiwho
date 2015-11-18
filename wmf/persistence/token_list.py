from .token import Token
from gl.containers import AutoVivifyingDict

__docformat__ = "restructuredtext en"

class TokenList:
	"""
	Represents the content of a revision as an ordered list of `Token` and 
	allows certain functionality like applying a diff to create a new 
	`TokenList`.
	"""
	
	__slots__=(
		"__tokens"
	)
	
	def __init__(self, contents=[], revision=NotImplemented):
		"""
		Constructor
		
		:Parameters:
			contents : list of strings
				The of Tokens to prime with
			revision : `revision.Revision`
				The revision from which the contents 
		"""
		self.__tokens = []
		if revision != NotImplemented:
			for content in contents:
				self.__tokens.append(Token(content, revision))
			
	
	@staticmethod
	def fromTokens(tokens):
		"""
		Creates a `TokenList` from a list of `Token`
		"""
		tokenList = TokenList()
		tokenList.__tokens = tokens
		return tokenList
		
	
	def deflate(self, token2Index):
		"""
		Produces a JSONable version of the instance based on a token 
		index that can be provided by PersistentState.
		
		:Parameters:
			token2Index : dict
				A token->index map.
		
		:Return:
			A JSONable dictionary
		"""
		json = []
		for token in self.__tokens:
			json.append(token2Index[token])
		
		return json
	
	@staticmethod
	def inflate(json, index2Token):
		"""
		Creates a TokenList identical to the one whose deflate() call 
		produced json assuming index2Token reflects the same map 
		used by deflate().
		
		:Parameters:
			json
				JSONable version of a Token
			index2Token : dict
				an index->Token map
			
		:Return:
			TokenList
		"""
		tokenList = TokenList()
		for index in json:
			tokenList.__tokens.append(index2Token[index])
		
		return tokenList
	
	
	def getTokens(self): return self.__tokens
	def getContents(self):
		return [token.getContent() for token in self.__tokens]
	
	def increment(self, revision):
		"""
		Increments the each tokens internal counter.  
		
		Note: This is probably not the best way to update the PWR of a
		token since it is hard to extend for PWV.  Refactoring this 
		function is likely. 
		"""
		for token in self.__tokens:
			token.increment(revision)
	
	def applyDiff(self, diff, revision):
		"""
		Creates a new `TokenList` by applying the result of a diff.  This
		method is useful for create a new `TokenList` to represent the
		token persistence of a new revision.
		
		:Parameters:
			diff : dict
				A dictionary of sm (a SequenceMatcher) and contents (a list of token cotents)
			revision : `Revision`
				The revision whose changes the diff represents
			
		:Return:
			A tuple of (NewTokenList, tokensAdded, tokenRemoved)
		"""
		newList = []
		tokensAdded = []
		tokensRemoved = []
		for (code, a_start, a_end, b_start, b_end) in diff['sm'].get_opcodes():
			if code   == "insert":
				for content in diff['contents'][b_start:b_end]: 
					newToken = Token(content, revision)
					newList.append(newToken)
					tokensAdded.append(newToken)
			elif code == "replace":
				for content in diff['contents'][b_start:b_end]:
					newToken = Token(content, revision)
					newList.append(newToken)
					tokensAdded.append(newToken)
				
				tokensRemoved.extend(self.__tokens[a_start:a_end])
					
			elif code == "equal":
				newList.extend(self.__tokens[a_start:a_end])
			elif code == "delete":
				tokensRemoved.extend(self.__tokens[a_start:a_end])
					
		
		return (TokenList.fromTokens(newList), tokensAdded, tokensRemoved)
	
	def __eq__(self, other):
		try:
			s = self.getTokens()
			o = other.getTokens()
			if len(s) != len(o):
				return False
			else:
				for i in range(0, len(s)):
					sToken = s[i]
					oToken = o[i]
					if sToken != oToken:
						print "%s!=%s" % (sToken, oToken)
						return False
					
				return True
			
		
		except AttributeError:
			return False
		
	def __ne__(self, other):
		return not self == other
