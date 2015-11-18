#!/usr/bin/python
import unittest
from .. import WordList, Word, Revision
import re
from difflib import SequenceMatcher

def suite():
	suite = unittest.TestSuite(
		[
			unittest.TestLoader().loadTestsFromTestCase(WordListTestCase)
		]
	)
	
	return suite


##
# Word List Test Case
#
class WordListTestCase(unittest.TestCase):
	
	def splitText(self, text):
		return re.findall(
			r"[\w]+|\[\[|\]\]|\{\{|\}\}|\n+| +|&\w+;|'''|''|=+|\{\||\|\}|\|\-|.",
			text
		)
	
	
	def diffContents(self, oldContents, newContents):
		return {"sm": SequenceMatcher(None, oldContents, newContents), "contents": newContents}
	
	
	def testSimpleConstructor(self):
		rev = {
			"revid": 336293237,
			"pageid": 15661504,
			"parentid": 333114931,
			"user": "PiperNigrum",
			"timestamp": "2010-01-06T23:11:33Z",
			"size": 3116,
			"comment": "Change GroupLens from external link to wikilink",
			"*": "Hello!  My name is Aaron Halfaker and I am a researcher in the [[GroupLens Research]] lab at the [[University of Minnesota]] specializing in online communities and mass collaboration.  The majority of my work in Wikipedia involves the development and maintenance of user scripts that enable communication or otherwise provide insight into the editing process.  See my [[User:EpochFail\/Research_protocol|research protocol]] for more information.  I also like to edit articles relating to computer science, mycology, psychology and philosophy.\n\n== WikiProject Membership ==\n<div style=\"float:left;padding:10px;\">{{User WikiProject User scripts}}<\/div>\n<div style=\"float:left;padding:10px;\">{{User_WikiProject_Fungi}}<\/div>\n<br style=\"clear:both;\" \/>\n\n== User Interaction Work==\n=== [[User:EpochFail\/NICE|NICE]] interface modification ===\n<div style=\"float:right;\">{{:User:EpochFail\/Userboxes\/NICE}}<\/div>\nI'm currently running a study of the [[User:EpochFail\/NICE|NICE]] user interface modification.  If you are interested in giving the interface modification a try, see the [[User:EpochFail\/NICE|documentation page]] for more information.\n<br style=\"clear:both\"\/>\n\n=== [[User:EpochFail\/HAPPI|HAPPI]] edit pane modification ===\n<div style=\"float:right;padding:5px;\">{{:User:EpochFail\/Userboxes\/HAPPI}}<\/div>\nI am also studying a new interface modification that is designed to help editors understand how words have persisted through the history of an article.  This UI modificiation adds highlighting to the normal edit window in order to make salient several features about the content of an article and how that content has survived through the revision history.  If you are interested in giving it a try, see the [[User:EpochFail\/HAPPI|documentation page]] for more information.\n<br style=\"clear:both\"\/>\n\n=== [[User:SuggestBot|SuggestBot]] wikiwork recommendations ===\nI've done minor maintenance to help get [[User:SuggestBot|SuggestBot]] back up and running.\n\n=== [[User:EpochFail\/NOOB|NOOB]] experience visualizer ===\nIn my spare time, I'm working on [[User:EpochFail\/NOOB|NOOB]], a simple user script that modifies the revision history interface to show how long editors have been around and how many revisions they have accrued.  This script is a work in progress and there is currently no study associated with it.\n\n== Peer Reviewed Work ==\n*Panciera, K., Halfaker, A., and Terveen, L. [http:\/\/www.grouplens.org\/node\/415 Wikipedians are born, not made: A study of power editors on Wikipedia], 2009. GROUP. ACM, 51-60.\n*Halfaker, A., Kittur, N., Kraut, R., and Riedl, J. [http:\/\/www.grouplens.org\/node\/416 A Jury of Your Peers: Quality, Experience and Ownership in Wikipedia], 2009. WikiSym. ACM, In Submission.\n\n== Other accounts ==\nI own and use [[User:PermaNoob]] for testing user scripts.  I only use the account to perform test edits or to test new interface modifications.  All of my real content edits come from this account. \n\n== Fish ==\n[[File:Rainbow trout.png|100x100px|center]]\n\n== Contact Information ==\n* [[User_talk:EpochFail|My talk page]] (preferred)\n* [[Special:EmailUser\/EpochFail|Email me]]"
		}
		r = Revision(rev)
		contents = self.splitText(rev['*'])
		wl = WordList(contents, r)
		
		words = wl.getWords()
		for i in range(0, len(words)):
			word = words[i]
			content = contents[i]
			self.failUnlessEqual(
				word.getContent(),
				content
			)
		
		
	
	def testDiff(self):
		rev = {
			"revid": 336293237,
			"pageid": 15661504,
			"parentid": 333114931,
			"user": "PiperNigrum",
			"timestamp": "2010-01-06T23:11:33Z",
			"size": 3116,
			"comment": "Change GroupLens from external link to wikilink",
			"*": "Hello!  My name is Aaron Halfaker"
		}
		r1 = Revision.fromWPAPI(rev)
		r1Contents = self.splitText(rev['*'])
		wl1 = WordList(r1Contents, r1)
		
		rev = {
			"revid": 336293238,
			"pageid": 15661504,
			"parentid": 333114931,
			"user": "EpochFail",
			"timestamp": "2010-01-06T23:11:33Z",
			"size": 3116,
			"comment": "No need to say hello.",
			"*": "My name is Aaron Halfaker"
		}
		r2 = Revision.fromWPAPI(rev)
		r2Contents = self.splitText(rev['*'])
		
		diff = self.diffContents(r1Contents, r2Contents)
		(wl2, wordsAdded, wordsRemoved) = wl1.applyDiff(diff, r2)
		
		self.failUnlessEqual(len(wordsAdded), 0)
		self.failUnlessEqual(wordsRemoved[0].getContent(), "Hello")
		self.failUnlessEqual(wordsRemoved[1].getContent(), "!")
		self.failUnlessEqual(wordsRemoved[2].getContent(), "  ")
		self.failUnlessEqual(
			wl2.getWords(), wl1.getWords()[3:]
		)
		
		
	
	def testDeflateInflate(self):
		rev = {
			"revid": 336293237,
			"pageid": 15661504,
			"parentid": 333114931,
			"user": "PiperNigrum",
			"timestamp": "2010-01-06T23:11:33Z",
			"size": 3116,
			"comment": "Change GroupLens from external link to wikilink",
			"*": "Hello!  My name is Aaron Halfaker and I am a researcher in the [[GroupLens Research]] lab at the [[University of Minnesota]] specializing in online communities and mass collaboration.  The majority of my work in Wikipedia involves the development and maintenance of user scripts that enable communication or otherwise provide insight into the editing process.  See my [[User:EpochFail\/Research_protocol|research protocol]] for more information.  I also like to edit articles relating to computer science, mycology, psychology and philosophy.\n\n== WikiProject Membership ==\n<div style=\"float:left;padding:10px;\">{{User WikiProject User scripts}}<\/div>\n<div style=\"float:left;padding:10px;\">{{User_WikiProject_Fungi}}<\/div>\n<br style=\"clear:both;\" \/>\n\n== User Interaction Work==\n=== [[User:EpochFail\/NICE|NICE]] interface modification ===\n<div style=\"float:right;\">{{:User:EpochFail\/Userboxes\/NICE}}<\/div>\nI'm currently running a study of the [[User:EpochFail\/NICE|NICE]] user interface modification.  If you are interested in giving the interface modification a try, see the [[User:EpochFail\/NICE|documentation page]] for more information.\n<br style=\"clear:both\"\/>\n\n=== [[User:EpochFail\/HAPPI|HAPPI]] edit pane modification ===\n<div style=\"float:right;padding:5px;\">{{:User:EpochFail\/Userboxes\/HAPPI}}<\/div>\nI am also studying a new interface modification that is designed to help editors understand how words have persisted through the history of an article.  This UI modificiation adds highlighting to the normal edit window in order to make salient several features about the content of an article and how that content has survived through the revision history.  If you are interested in giving it a try, see the [[User:EpochFail\/HAPPI|documentation page]] for more information.\n<br style=\"clear:both\"\/>\n\n=== [[User:SuggestBot|SuggestBot]] wikiwork recommendations ===\nI've done minor maintenance to help get [[User:SuggestBot|SuggestBot]] back up and running.\n\n=== [[User:EpochFail\/NOOB|NOOB]] experience visualizer ===\nIn my spare time, I'm working on [[User:EpochFail\/NOOB|NOOB]], a simple user script that modifies the revision history interface to show how long editors have been around and how many revisions they have accrued.  This script is a work in progress and there is currently no study associated with it.\n\n== Peer Reviewed Work ==\n*Panciera, K., Halfaker, A., and Terveen, L. [http:\/\/www.grouplens.org\/node\/415 Wikipedians are born, not made: A study of power editors on Wikipedia], 2009. GROUP. ACM, 51-60.\n*Halfaker, A., Kittur, N., Kraut, R., and Riedl, J. [http:\/\/www.grouplens.org\/node\/416 A Jury of Your Peers: Quality, Experience and Ownership in Wikipedia], 2009. WikiSym. ACM, In Submission.\n\n== Other accounts ==\nI own and use [[User:PermaNoob]] for testing user scripts.  I only use the account to perform test edits or to test new interface modifications.  All of my real content edits come from this account. \n\n== Fish ==\n[[File:Rainbow trout.png|100x100px|center]]\n\n== Contact Information ==\n* [[User_talk:EpochFail|My talk page]] (preferred)\n* [[Special:EmailUser\/EpochFail|Email me]]"
		}
		r1 = Revision(rev)
		r1Contents = self.splitText(rev['*'])
		wl1 = WordList(r1Contents, r1)
		
		wordToIndexMap = {}
		indexToWordMap = {}
		words = wl1.getWords()
		for index in range(0, len(words)):
			word = words[index]
			wordToIndexMap[word] = index
			indexToWordMap[index] = word
		
		json = wl1.deflate(wordToIndexMap)
		
		wl2 = WordList.inflate(json,indexToWordMap)
		
		self.failUnlessEqual(wl1, wl2)
	

if __name__ == "__main__":
	suite = suite()
	unittest.TextTestRunner(verbosity=2).run(suite)
