import sys, logging
from nose.tools import eq_
from . import sample
from ..map import map
from ..processors import reverts


def test_simple_map():
	dumps = [sample.getSmallXMLFilePath(), sample.getLargeXMLFilePath()]
	
	def processPage(dump, page):
		assert hasattr(dump, "namespaces")
		assert hasattr(page, "readRevisions")
		
		count = 0
		for rev in page.readRevisions():
			count += 1
			if count >= 100: break
		
		yield (page.getId(), count)
	
	output = dict(map(dumps, processPage))
	
	eq_(output[17500012], 1)
	eq_(output[12], 100)


def test_revert_map():
	dumps = [sample.getSmallXMLFilePath(), sample.getLargeXMLFilePath()]
	
	output = list(map(dumps, reverts.process))
