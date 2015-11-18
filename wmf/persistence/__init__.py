from .persistence_state import PersistenceState
#from .persistent_word_state import PersistentWordState
from .revision import Revision
from .word import Word
from .token import Token
from .word_list import WordList
from .token_list import TokenList

__docformat__ = "restructuredtext en"

"""
A package with utilities for managing the persistent word analysis across text
versions of a document.  `PersistenceState` is the highest level of the 
interface and the part of the system that's most interesting externally.  `Word`s
are also very important.  The current implementation of `Word` only accounts for
how the number of revisions in which a Word is visible.  If persistent word 
views (or something similar) is intended to be kept, refactoring will be 
necessary.
"""

def splitter(self, text):
	return re.findall(
		r"[\w]+|\[\[|\]\]|\{\{|\}\}|\n+| +|&\w+;|'''|''|=+|\{\||\|\}|\|\-|.",
		text
	)
	

def differ(self, oldContents, newContents):
	return {"sm": SequenceMatcher(None, oldContents, newContents), "contents": newContents}

			


