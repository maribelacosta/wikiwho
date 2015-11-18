#!/usr/bin/python
import unittest
import sys
from .. import WordList, Word, Revision, PersistenceState
import re
from difflib import SequenceMatcher

def suite():
	suite = unittest.TestSuite(
		[
			unittest.TestLoader().loadTestsFromTestCase(PersistenceStateTestCase)
		]
	)
	
	return suite


##
# PersistenceState Case
#
class PersistenceStateTestCase(unittest.TestCase):
	
	def splitter(self, text):
		return re.findall(
			r"[\w]+|\[\[|\]\]|\{\{|\}\}|\n+| +|&\w+;|'''|''|=+|\{\||\|\}|\|\-|.",
			text
		)
	
	
	def differ(self, oldContents, newContents):
		return {"sm": SequenceMatcher(None, oldContents, newContents), "contents": newContents}
	
	
	def testSimpleConstructor(self):
		state = PersistenceState(self.splitter, self.differ, 15)
		
	
	def testRun1(self):
		revs = [
			{"revid":190055192,"pageid":15661504,"user":"EpochFail","timestamp":"2008-02-08T22:36:02Z","comment":"[[WP:AES|\u2190]]Created page with '[[User:EpochFail]] is a researcher at the University of Minnesota specializing in online communities and mass collaboration.'","*":"[[User:EpochFail]] is a researcher at the University of Minnesota"},
			{"revid":276121340,"pageid":15661504,"parentid":190055192,"user":"EpochFail","timestamp":"2009-03-09T21:48:03Z","comment":"wooooo","*":"[[User:EpochFail]] is a researcher at the University of Minnesota"},
			{"revid":276121389,"pageid":15661504,"parentid":276121340,"user":"EpochFail","timestamp":"2009-03-09T21:48:18Z","comment":"[[WP:UNDO|Undid]] revision 276121340 by [[Special:Contributions\/EpochFail|EpochFail]] ([[User talk:EpochFail|talk]])","*":"[[User:EpochFail]] is a researcher at the University of Minnesota"},
			{"revid":276122260,"pageid":15661504,"parentid":276121389,"user":"EpochFail","timestamp":"2009-03-09T21:52:00Z","comment":"[[WP:UNDO|Undid]] revision 276121389 by [[Special:Contributions\/EpochFail|EpochFail]] ([[User talk:EpochFail|talk]]) Just testing","*":"[[User:EpochFail]] is a researcher at the University of Minnesota"},
			{"revid":276122556,"pageid":15661504,"parentid":276122260,"user":"EpochFail","timestamp":"2009-03-09T21:53:17Z","comment":"[[WP:UNDO|Undid]] revision 276122260 by [[Special:Contributions\/EpochFail|EpochFail]] ([[User talk:EpochFail|talk]]) still just testing","*":"[[User:EpochFail]] is a researcher at the University of Minnesota"},
			{"revid":276124685,"pageid":15661504,"parentid":276122556,"user":"EpochFail","timestamp":"2009-03-09T22:01:43Z","comment":"[[WP:UNDO|Undid]] revision 276122556 by [[Special:Contributions\/EpochFail|EpochFail]] ([[User talk:EpochFail|talk]]) still testing.  Please don't ban me.  :D  I'm making fun things for WP","*":"[[User:EpochFail]] is a researcher at the University of Minnesota"},
			{"revid":276320463,"pageid":15661504,"parentid":276124685,"user":"EpochFail","timestamp":"2009-03-10T18:05:35Z","comment":"[[WP:UNDO|Undid]] revision 276124685 by [[Special:Contributions\/EpochFail|EpochFail]] ([[User talk:EpochFail|talk]])  more test reverting","*":"[[User:EpochFail]] is a researcher at the University of Minnesota"},
			{"revid":276322808,"pageid":15661504,"parentid":276320463,"user":"EpochFail","timestamp":"2009-03-10T18:16:07Z","comment":"[[WP:UNDO|Undid]] revision 276320463 by [[Special:Contributions\/EpochFail|EpochFail]] ([[User talk:EpochFail|talk]])  plz work","*":"[[User:EpochFail]] is a researcher at the University of Minnesota"},
			{"revid":276341997,"pageid":15661504,"parentid":276322808,"user":"EpochFail","timestamp":"2009-03-10T19:38:19Z","comment":"[[WP:UNDO|Undid]] revision 276322808 by [[Special:Contributions\/EpochFail|EpochFail]] ([[User talk:EpochFail|talk]]) askjbkasbdkas","*":"[[User:EpochFail]] is a researcher at the University of Minnesota"},
			{"revid":277049022,"pageid":15661504,"parentid":276341997,"user":"EpochFail","timestamp":"2009-03-13T21:06:15Z","comment":"[[WP:UNDO|Undid]] revision 276341997 by [[Special:Contributions\/EpochFail|EpochFail]] ([[User talk:EpochFail|talk]])","*":"[[User:EpochFail]] is a researcher at the University of Minnesota"}
		]
		state = PersistenceState(self.splitter, self.differ, 15)
		for rev in revs:
			revision = Revision.fromWPAPI(rev)
			(wordsAdded, wordsRemoved) = state.update(revision, rev.get('*', ''))
		
		self.failUnlessEqual(
			revision.getWordList().getWords()[0].getVisible(), 
			len(revs)
		)
	
	def testDeflateInflate(self):
		revs = [
			{"revid":190055192,"pageid":15661504,"user":"EpochFail","timestamp":"2008-02-08T22:36:02Z","comment":"[[WP:AES|\u2190]]Created page with '[[User:EpochFail]] is a researcher at the University of Minnesota specializing in online communities and mass collaboration.'","*":"[[User:EpochFail]] is a researcher at the University of Minnesota"},
			{"revid":276121340,"pageid":15661504,"parentid":190055192,"user":"EpochFail","timestamp":"2009-03-09T21:48:03Z","comment":"wooooo","*":"[[User:EpochFail]] is a researcher at the University of Minnesota"},
			{"revid":276121389,"pageid":15661504,"parentid":276121340,"user":"EpochFail","timestamp":"2009-03-09T21:48:18Z","comment":"[[WP:UNDO|Undid]] revision 276121340 by [[Special:Contributions\/EpochFail|EpochFail]] ([[User talk:EpochFail|talk]])","*":"[[User:EpochFail]] is a researcher at the University of Minnesota"},
			{"revid":276122260,"pageid":15661504,"parentid":276121389,"user":"EpochFail","timestamp":"2009-03-09T21:52:00Z","comment":"[[WP:UNDO|Undid]] revision 276121389 by [[Special:Contributions\/EpochFail|EpochFail]] ([[User talk:EpochFail|talk]]) Just testing","*":"[[User:EpochFail]] is a researcher at the University of Minnesota"},
			{"revid":276122556,"pageid":15661504,"parentid":276122260,"user":"EpochFail","timestamp":"2009-03-09T21:53:17Z","comment":"[[WP:UNDO|Undid]] revision 276122260 by [[Special:Contributions\/EpochFail|EpochFail]] ([[User talk:EpochFail|talk]]) still just testing","*":"[[User:EpochFail]] is a researcher at the University of Minnesota"},
			{"revid":276124685,"pageid":15661504,"parentid":276122556,"user":"EpochFail","timestamp":"2009-03-09T22:01:43Z","comment":"[[WP:UNDO|Undid]] revision 276122556 by [[Special:Contributions\/EpochFail|EpochFail]] ([[User talk:EpochFail|talk]]) still testing.  Please don't ban me.  :D  I'm making fun things for WP","*":"[[User:EpochFail]] is a researcher at the University of Minnesota"},
			{"revid":276320463,"pageid":15661504,"parentid":276124685,"user":"EpochFail","timestamp":"2009-03-10T18:05:35Z","comment":"[[WP:UNDO|Undid]] revision 276124685 by [[Special:Contributions\/EpochFail|EpochFail]] ([[User talk:EpochFail|talk]])  more test reverting","*":"[[User:EpochFail]] is a researcher at the University of Minnesota"},
			{"revid":276322808,"pageid":15661504,"parentid":276320463,"user":"EpochFail","timestamp":"2009-03-10T18:16:07Z","comment":"[[WP:UNDO|Undid]] revision 276320463 by [[Special:Contributions\/EpochFail|EpochFail]] ([[User talk:EpochFail|talk]])  plz work","*":"[[User:EpochFail]] is a researcher at the University of Minnesota"},
			{"revid":276341997,"pageid":15661504,"parentid":276322808,"user":"EpochFail","timestamp":"2009-03-10T19:38:19Z","comment":"[[WP:UNDO|Undid]] revision 276322808 by [[Special:Contributions\/EpochFail|EpochFail]] ([[User talk:EpochFail|talk]]) askjbkasbdkas","*":"[[User:EpochFail]] is a researcher at the University of Minnesota"},
			{"revid":277049022,"pageid":15661504,"parentid":276341997,"user":"EpochFail","timestamp":"2009-03-13T21:06:15Z","comment":"[[WP:UNDO|Undid]] revision 276341997 by [[Special:Contributions\/EpochFail|EpochFail]] ([[User talk:EpochFail|talk]])","*":"[[User:EpochFail]] is a researcher at the University of Minnesota"}
		]
		state1 = PersistenceState(self.splitter, self.differ, 15)
		for rev in revs:
			revision = Revision.fromWPAPI(rev)
			(wordsAdded, wordsRemoved) = state1.update(revision, rev.get('*', ''))
		
		json = state1.deflate()
		
		state2 = PersistenceState.inflate(json, self.splitter, self.differ)
		
		self.failUnlessEqual(
			state1,
			state2
		)
	
	def testDeflateInflateState(self):
		revs = [
			{"revid":190055192,"pageid":15661504,"user":"EpochFail","timestamp":"2008-02-08T22:36:02Z","comment":"[[WP:AES|\u2190]]Created page with '[[User:EpochFail]] is a researcher at the University of Minnesota specializing in online communities and mass collaboration.'","*":"[[User:EpochFail]] is a researcher at the University of Minnesota"},
			{"revid":276121340,"pageid":15661504,"parentid":190055192,"user":"EpochFail","timestamp":"2009-03-09T21:48:03Z","comment":"wooooo","*":"[[User:EpochFail]] is a researcher at the University of Minnesota"},
			{"revid":276121389,"pageid":15661504,"parentid":276121340,"user":"EpochFail","timestamp":"2009-03-09T21:48:18Z","comment":"[[WP:UNDO|Undid]] revision 276121340 by [[Special:Contributions\/EpochFail|EpochFail]] ([[User talk:EpochFail|talk]])","*":"[[User:EpochFail]] is a researcher at the University of Minnesota"},
			{"revid":276122260,"pageid":15661504,"parentid":276121389,"user":"EpochFail","timestamp":"2009-03-09T21:52:00Z","comment":"[[WP:UNDO|Undid]] revision 276121389 by [[Special:Contributions\/EpochFail|EpochFail]] ([[User talk:EpochFail|talk]]) Just testing","*":"[[User:EpochFail]] is a researcher at the University of Minnesota"},
			{"revid":276122556,"pageid":15661504,"parentid":276122260,"user":"EpochFail","timestamp":"2009-03-09T21:53:17Z","comment":"[[WP:UNDO|Undid]] revision 276122260 by [[Special:Contributions\/EpochFail|EpochFail]] ([[User talk:EpochFail|talk]]) still just testing","*":"[[User:EpochFail]] is a researcher at the University of Minnesota"},
			{"revid":276124685,"pageid":15661504,"parentid":276122556,"user":"EpochFail","timestamp":"2009-03-09T22:01:43Z","comment":"[[WP:UNDO|Undid]] revision 276122556 by [[Special:Contributions\/EpochFail|EpochFail]] ([[User talk:EpochFail|talk]]) still testing.  Please don't ban me.  :D  I'm making fun things for WP","*":"[[User:EpochFail]] is a researcher at the University of Minnesota"},
			{"revid":276320463,"pageid":15661504,"parentid":276124685,"user":"EpochFail","timestamp":"2009-03-10T18:05:35Z","comment":"[[WP:UNDO|Undid]] revision 276124685 by [[Special:Contributions\/EpochFail|EpochFail]] ([[User talk:EpochFail|talk]])  more test reverting","*":"[[User:EpochFail]] is a researcher at the University of Minnesota"},
			{"revid":276322808,"pageid":15661504,"parentid":276320463,"user":"EpochFail","timestamp":"2009-03-10T18:16:07Z","comment":"[[WP:UNDO|Undid]] revision 276320463 by [[Special:Contributions\/EpochFail|EpochFail]] ([[User talk:EpochFail|talk]])  plz work","*":"[[User:EpochFail]] is a researcher at the University of Minnesota"},
			{"revid":276341997,"pageid":15661504,"parentid":276322808,"user":"EpochFail","timestamp":"2009-03-10T19:38:19Z","comment":"[[WP:UNDO|Undid]] revision 276322808 by [[Special:Contributions\/EpochFail|EpochFail]] ([[User talk:EpochFail|talk]]) askjbkasbdkas","*":"[[User:EpochFail]] is a researcher at the University of Minnesota"},
			{"revid":277049022,"pageid":15661504,"parentid":276341997,"user":"EpochFail","timestamp":"2009-03-13T21:06:15Z","comment":"[[WP:UNDO|Undid]] revision 276341997 by [[Special:Contributions\/EpochFail|EpochFail]] ([[User talk:EpochFail|talk]])","*":"[[User:EpochFail]] is a researcher at the University of Minnesota"}
		]
		state1 = PersistenceState(self.splitter, self.differ, 15)
		for rev in revs:
			revision = Revision.fromWPAPI(rev)
			(wordsAdded, wordsRemoved) = state1.update(revision, rev.get('*', ''))
		
		
		state2 = PersistenceState(self.splitter, self.differ, 15)
		for rev in revs[:5]:
			revision = Revision.fromWPAPI(rev)
			(wordsAdded, wordsRemoved) = state2.update(revision, rev.get('*', ''))
		
		json = state2.deflate()
		state2 = PersistenceState.inflate(json, self.splitter, self.differ)
		for rev in revs[5:]:
			revision = Revision.fromWPAPI(rev)
			(wordsAdded, wordsRemoved) = state2.update(revision, rev.get('*', ''))
		
		self.failUnlessEqual(
			state1,
			state2
		)
	
	def testWordListAccuracy(self):
		revs = [
			{"revid":190055192,"pageid":15661504,"user":"EpochFail","timestamp":"2008-02-08T22:36:02Z","comment":"","*":"Apples are fruit"},#Apples[7] are[7] fruit[10]
			{"revid":276121340,"pageid":15661504,"user":"EpochFail","timestamp":"2009-03-09T21:48:03Z","comment":"","*":"Apples are not fruit"},
			{"revid":276121389,"pageid":15661504,"user":"EpochFail","timestamp":"2009-03-09T21:48:18Z","comment":"","*":"Apples are fruit"},
			{"revid":276122260,"pageid":15661504,"user":"EpochFail","timestamp":"2009-03-09T21:52:00Z","comment":"","*":"Apples are red fruit"},
			{"revid":276122556,"pageid":15661504,"user":"EpochFail","timestamp":"2009-03-09T21:53:17Z","comment":"","*":"Apples are not red fruit"},
			{"revid":276124685,"pageid":15661504,"user":"EpochFail","timestamp":"2009-03-09T22:01:43Z","comment":"","*":"Apples are red fruit"},
			{"revid":276320463,"pageid":15661504,"user":"EpochFail","timestamp":"2009-03-10T18:05:35Z","comment":"","*":"Apple is a red fruit that contains seeds"},
			{"revid":276322808,"pageid":15661504,"user":"EpochFail","timestamp":"2009-03-10T18:16:07Z","comment":"","*":"Apple is a red fruit that contains seeds with cyanide."},
			{"revid":276341997,"pageid":15661504,"user":"EpochFail","timestamp":"2009-03-10T19:38:19Z","comment":"","*":"Apples are red fruit"},
			{"revid":277049022,"pageid":15661504,"user":"EpochFail","timestamp":"2009-03-13T21:06:15Z","comment":"","*":"Apple is a red fruit that contains seeds"}
		]
		state = PersistenceState(lambda x: x.split(" "), self.differ, 15)
		revision1 = Revision.fromWPAPI(revs[0])
		(wordsAdded1, _) = state.update(revision1, revs[0]['*'])
		
		for rev in revs[1:3]:
			revision = Revision.fromWPAPI(rev)
			(_, _) = state.update(revision, rev['*'])
		
		revision2 = Revision.fromWPAPI(revs[3])
		(wordsAdded2, _) = state.update(revision2, revs[3]['*'])
		
		revision3 = Revision.fromWPAPI(revs[4])
		(wordsAdded3, _) = state.update(revision3, revs[4]['*'])
		
		for rev in revs[5:]:
			revision = Revision.fromWPAPI(rev)
			(_, _) = state.update(revision, rev['*'])
		
		self.failUnlessEqual(wordsAdded1[0].getContent(),"Apples")
		self.failUnlessEqual(wordsAdded1[0].getVisible(),7)
		self.failUnlessEqual(wordsAdded1[1].getContent(),"are")
		self.failUnlessEqual(wordsAdded1[1].getVisible(),7)
		self.failUnlessEqual(wordsAdded1[2].getVisible(),10)
		
		self.failUnlessEqual(len(wordsAdded2), 1)
		self.failUnlessEqual(wordsAdded2[0].getContent(), "red")
		self.failUnlessEqual(wordsAdded2[0].getVisible(), 7)
		
		self.failUnlessEqual(len(wordsAdded3), 1)
		self.failUnlessEqual(wordsAdded3[0].getContent(), "not")
		self.failUnlessEqual(wordsAdded3[0].getVisible(), 1)
		
	

if __name__ == "__main__":
	suite = suite()
	unittest.TextTestRunner(verbosity=2).run(suite)
