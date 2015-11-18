#!/usr/bin/python
import unittest
from .. import Revision, WordList
import time
import calendar
import hashlib

def suite():
	suite = unittest.TestSuite(
		[
			unittest.TestLoader().loadTestsFromTestCase(RevisionTestCase)
		]
	)
	
	return suite


##
# Revision Test Case
#
class RevisionTestCase(unittest.TestCase):
		
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
		r = Revision.fromWPAPI(rev)
		
		self.failUnlessEqual(
			r.getId(),
			rev['revid']
		)
		self.failUnlessEqual(
			r.getPageId(),
			rev['pageid']
		)
		self.failUnlessEqual(
			r.getUsername(),
			rev['user']
		)
		self.failUnlessEqual(
			r.getTimestamp(),
			int(calendar.timegm(time.strptime(rev['timestamp'], '%Y-%m-%dT%H:%M:%SZ')))
		)
		self.failUnlessEqual(
			r.getComment(),
			rev['comment']
		)
		self.failUnlessEqual(
			r.getChecksum(),
			hashlib.md5(rev.get('*', '').encode('utf-8')).hexdigest()
		)
	
	def testLimitedConstruction(self):
		rev = {
			"revid": 336293237,
			"pageid": 15661504,
			"parentid": 333114931,
			"timestamp": "2010-01-06T23:11:33Z",
			"size": 3116
		}
		r = Revision.fromWPAPI(rev)
		
		self.failUnlessEqual(
			r.getId(),
			rev['revid']
		)
		self.failUnlessEqual(
			r.getPageId(),
			rev['pageid']
		)
		self.failUnlessEqual(
			r.getUsername(),
			None
		)
		self.failUnlessEqual(
			r.getTimestamp(),
			int(calendar.timegm(time.strptime(rev['timestamp'], '%Y-%m-%dT%H:%M:%SZ')))
		)
		self.failUnlessEqual(
			r.getComment(),
			''
		)
		self.failUnlessEqual(
			r.getChecksum(),
			hashlib.md5(''.encode('utf8')).hexdigest()
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
		r = Revision(rev)
		r.setWordList(WordList(rev.get('*', '').split(" "), r))
		
		wordToIndexMap = {}
		indexToWordMap = {}
		words = r.getWordList().getWords()
		for index in range(0, len(words)):
			word = words[index]
			wordToIndexMap[word] = index
			indexToWordMap[index] = word
		
		json = r.deflate(wordToIndexMap)
		
		r2 = Revision.inflate(json, indexToWordMap)
		
		self.failUnlessEqual(
			r,
			r2
		)

if __name__ == "__main__":
	suite = suite()
	unittest.TextTestRunner(verbosity=2).run(suite)
