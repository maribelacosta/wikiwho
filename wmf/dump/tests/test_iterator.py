import sys, logging
import hashlib
from nose.tools import eq_
from . import sample
from ..iterator import Iterator, Namespace
import wmf

logging.basicConfig(level=logging.INFO)

def test_small():
	fp = sample.getSmallXMLFilePointer()
	wf = Iterator(fp)
	for key in [
		 -2, -1, 0,  1,  2,  3,  4,  5,  6,
		  7,  8, 9, 10, 11, 12, 13, 14, 15,
		100,101,108,109
	]:
		assert key in wf.namespaces.values(), "Key %s not found in %s" % (key, wf.namespaces)
	
	for page in wf.readPages():
		eq_(
			page.getTitle(),
			u'Talk:Pilsbury Block'
		)
		for revision in page.readRevisions():
			sh = hashlib.sha1()
			eq_(
				revision.getId(),
				213377884
			)
			eq_(
				revision.getTimestamp(),
				wmf.wp2Timestamp("2008-05-19T01:41:53Z")
			)
			eq_(
				revision.getContributor().getId(),
				905763
			)
			eq_(
				revision.getContributor().getUsername(),
				u"Swampyank"
			)
			eq_(
				revision.getMinor(),
				False
			)
			eq_(
				revision.getComment(),
				u"[[WP:AES|\u2190]]Created page with '{{WikiProject National Register of Historic Places|class=Stub}} {{WikiProject Maine|class=Stub|importance=Low}} {{reqphoto|in=Maine}}'"
			)
			
			eq_(
				revision.getText(),
				u"{{WikiProject National Register of Historic Places|class=Stub}}\n" + 
				u"{{WikiProject Maine|class=Stub|importance=Low}}\n" + 
				u"{{reqphoto|in=Maine}}"
			)

			if revision.getSha1() != None:
				sh.update(u"{{WikiProject National Register of Historic Places|class=Stub}}\n")
				sh.update(u"{{WikiProject Maine|class=Stub|importance=Low}}\n")
				sh.update(u"{{reqphoto|in=Maine}}")
				eq_(
					revision.getSha1(),
					sh.hexdigest()
				)
		
	

def test_large():
	fp = sample.getLargeXMLFilePointer()
	wf = Iterator(fp)
	pageCounter = 0
	revisionCounter = 0
	for page in wf.readPages():
		pageCounter += 1
		for revision in page.readRevisions():
			assert revision.getId() != None
			assert revision.getTimestamp() != None
			__ = revision.getContributor()
			__ = revision.getComment()
			assert revision.getMinor() != None
			assert revision.getText() != None
			#sys.stderr.write(".")
			revisionCounter += 1
			if revisionCounter >= 100: break
		
	
	eq_(pageCounter, 1)
	#eq_(revisionCounter, 15180)
	eq_(revisionCounter, 100)

