import unittest
from ..limited_dict_lists import LimitedDictLists


##
# Limited Dict Test Case
#
class LimitedDictListsTestCase(unittest.TestCase):
		
	def testSimpleConstructor(self):
		d = LimitedDictLists(maxsize=3)
		self.failUnless(len(d) == 0, "Dictionary should be empty, but thinks it has %s pairs" % len(d))
		
	def testInsert1(self):
		d = LimitedDictLists(maxsize=3)
		expectorate = d.insert("1", 1)
		self.failUnless(len(d) == 1, "List should contain one values, has %s" % len(d))
		expectorate = d.insert("2", 2)
		self.failUnless(len(d) == 2, "List should contain two values, has %s" % len(d))
		expectorate = d.insert("3", 3)
		self.failUnless(len(d) == 3, "List should contain three values, has %s" % len(d))
		expectorate = d.insert("4", 4)
		self.failUnless(len(d) == 3, "List should contain three values, has %s" % len(d))
		
	def testInsert2(self):
		d = LimitedDictLists(maxsize=1)
		expectorate = d.insert("1", 1)
		expectorate = d.insert("2", 2)
		self.failUnless("1" not in d, "List should not contain keys for elements that have been spat out.")
		
	def testGet1(self):
		d = LimitedDictLists(maxsize=2)
		d.insert("frack", "bum")
		d.insert("fum", "grap")
		self.failUnless(d.getByIndex(-1) == "grap", "getByIndex() fails on negative indexes.  Expected %r, got %r." % ("grap", d.getByIndex(0)))
		self.failUnless(d.getByIndex(0) == "bum", "getByIndex() fails on positive indexes.  Expected %r, got %r." % ("bum", d.getByIndex(0)))
		expectorate = d.insert("frum", "hurr")
		self.failUnless(d.getByIndex(0) == "grap", "getByIndex() fails on positive indexes.  Expected %r, got %r." % ("grap", d.getByIndex(0)))
		self.failUnless(d.getByIndex(1) == "hurr", "getByIndex() fails on positive indexes.  Expected %r, got %r." % ("hurr", d.getByIndex(1)))
		
	def testGet2(self):
		d = LimitedDictLists(maxsize=10)
		d.insert("1", "bum")
		d.insert("2", "grap")
		d.insert("3", "derr")
		d.insert("4", "foo")
		d.insert("5", "ham")
		d.insert("6", "tram")
		d.insert("7", "spam")
		d.insert("8", "lam")
		d.insert("9", "bar")
		d.insert("10", "ten")
		self.failUnless(d.getByIndex(-1) == "ten", "getByIndex() fails on negative indexes.  Expected %r, got %r." % ("ten", d.getByIndex(-1)))
		d.insert("11", "eleven")
		d.insert("12", "twelve")
		d.insert("13", "thirteen")
		self.failUnless(d.getByIndex(-1) == "thirteen", "getByIndex() fails on negative indexes.  Expected %r, got %r." % ("thirteen", d.getByIndex(-1)))
	
	def testIterator(self):
		d = LimitedDictLists(maxsize=3)
		d.insert("frack", "bum")
		d.insert("frack", "grap")
		d.insert("frum", "grap1")
		
		for key in d:
			if key[0] == "frack":
				self.failUnless(
					d[key[0]] == "grap", 
					"Iterator returns crazy things. Expected %r, got %r" % ("grap", d[key[0]])
				)
			else:
				self.failUnless(
					d[key[0]] == "grap1", 
					"Iterator returns crazy things. Expected %r, got %r" % ("grap1", d[key[0]])
				)
				
	
	def testDelItem(self):
		d = LimitedDictLists(maxsize=3)
		d.insert("frack", "bum")
		d.insert("frack", "grap")
		d.insert("frum", "grap1")
		del d['frack']
		expectorate = d.insert("frack", "foo")
		self.failUnless(
			expectorate == None, 
			"Something got spit out when it wasn't supposed to.   Expected None, got %r." % expectorate
		)
		expectorate = d.insert("frack", "foo1")
		self.failUnless(
			expectorate == None, 
			"Something got spit out when it wasn't supposed to.   Expected None, got %r." % expectorate
		)
		expectorate = d.insert("dum", "bum")
		self.failUnless(
			expectorate != None, 
			"Nothing got spit out, but something was supposed to be.   Expected something, got None."
		)

if __name__ == "__main__":
	suite = suite()
	unittest.TextTestRunner(verbosity=2).run(suite)
