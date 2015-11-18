from __future__ import with_statement, absolute_import
import re, types
import time, calendar, datetime
import hashlib
import urllib

__docformat__ = "restructuredtext en"

"""
This module contains utility functions for interacting with Wikipedia.
"""

LONG_WP_TIME_STRING = '%Y-%m-%dT%H:%M:%SZ'
"""
The longhand version of Wikipedia timestamps.
"""

SHORT_WP_TIME_STRING = '%Y%m%d%H%M%S'
"""
The shorthand version of Wikipedia timestamps
"""

WPAPI_URL = "http://%s.wikipedia.org/w/api.php"
"""
The wikipedia API URL.  A positional format token is included to so that the 
language specific prefix can be formatted in. See `wpAPIURL()`.
"""


VLOOSE_RE = re.compile(r'''
	  (^revert\ to.+using)
	| (^reverted\ edits\ by.+using)
	| (^reverted\ edits\ by.+to\ last\ version\ by)
	| (^bot\ -\ rv.+to\ last\ version\ by)
	| (-assisted\ reversion)
	| (^(revert(ed)?|rv).+to\ last)
	| (^undo\ revision.+by)
	''', re.IGNORECASE | re.DOTALL | re.VERBOSE)

VSTRICT_RE = re.compile(r'''
	  (\brvv)
	| (\brv[/ ]v)
	| (WP:HG)
	| (User:ClueBot)
	| (vandal(?!proof|bot))
	| (\b(rv|rev(ert)?|rm)\b.*(blank|spam|nonsense|porn|mass\sdelet|vand))
	''', re.IGNORECASE | re.DOTALL | re.VERBOSE)

NAMESPACES = {
	'en': set([
		'Media',
		'Special',
		'Talk',
		'User talk',
		'Wikipedia talk',
		'Image talk',
		'MediaWiki talk',
		'Template talk',
		'Help talk',
		'Category talk',
		'Portal talk',
		'File talk',
		'User',
		'Wikipedia',
		'Image',
		'MediaWiki',
		'Template',
		'Help',
		'Category',
		'Portal',
		'File'
	])
}

NAMESPACE_RE = re.compile(r'^((?:%s)):' % ')|(?:'.join(NAMESPACES['en']),
						  re.IGNORECASE)

def wpAPIURL(prefix="en"):
	"""
	Creates a the URL for the wikipedia API based on a language prefix. 
	
	:Parameters:
		prefix : string
			the prefix to be formatted into the url
		
	:Return:
		the Wikipedia API url for a given language prefix
	"""
	return WPAPI_URL % prefix


def wp2Timestamp(wpTime):
	"""
	Converts a Wikipedia timestamp to a Unix Epoch-based timestamp (seconds 
	since Jan. 1st 1970 GMT).  This function will handle both long 
	(see `LONG_WP_TIME_STRING`) and short (see `SHORT_WP_TIME_STRING`) 
	time formats.
	
	:Parameters:
		wpTime : string
			Wikipedia timestamp to be converted
		
	:Return:
		integer Unix Epoch-based timestamp (seconds since Jan. 1st 1970 
		GMT) version of the provided wpTime.
	"""
	try:
		myTime = time.strptime(wpTime, LONG_WP_TIME_STRING)
	except ValueError as e:
		try:
			myTime = time.strptime(wpTime, SHORT_WP_TIME_STRING)
		except ValueError as e:
			raise ValueError("'%s' is not a valid Wikipedia date format" % wpTime)
		
	return int(calendar.timegm(myTime))

def timestamp2WP(timestamp):
	"""
	Converts a Unix Epoch-based timestamp (seconds 	since Jan. 1st 1970 GMT)
	timestamp to one acceptable by Wikipedia. 
	
	:Parameters:
		timestamp : int
			Unix timestamp to be converted
		
	:Return:
		string Wikipedia style timestamp
	"""
	
	return datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y%m%d%H%M%S')

def digest(content):
	return hashlib.md5(content.encode("utf-8")).hexdigest()
	

def normalize(name):
	"""
	Normalizes text from a Wikipedia title/segment by capitalizing the
	first letter, replacing underscores with spaces, and collapsing all
	spaces to one space.
	
	:Parameters:
		name : string
			Namespace or title portion of a Wikipedia page name.
		
	:Return:
		string Normalized text
	"""
	
	return name.capitalize().replace("_", " ").strip()
	
def normalizeTitle(title, namespaces=NAMESPACES['en']):
	"""
	Normalizes a Wikipedia page title and splits the title into
	namespace and title pieces.
	
	:Parameters:
		title : string
			The title of a Wikipedia page.
		namespaces : set
			A set of namespaces to look for in the title.
		
	:Return:
		The namespace, title tuple
	"""

	if type(title) == types.UnicodeType:
		title = title.encode('utf-8')
	
	title = title.strip()
	parts = title.split(":", 1)
	if len(parts) == 1:
		namespace = None
		title = normalize(parts[0])
	elif parts[1] == '':
		namespace = None
		title = normalize(title)
	else:
		nsPart = normalize(parts[0])
		if nsPart in namespaces:
			namespace = nsPart
			title = normalize(parts[1])
		else:
			namespace = None
			title = normalize(title)
	
	return (namespace, title)
	
def normalizeURLTitle(title, namespaces=NAMESPACES['en']):
	"""
	Normalizes a Wikipedia page title obtained from a URL and splits
	the title into namespace and title pieces.
	
	:Parameters:
		title : string
			The title of a Wikipedia page.
		namespaces : set
			A set of namespaces to look for in the title.
		
	:Return:
		The namespace, title tuple
	"""

	if type(title) == types.UnicodeType:
		title = title.encode('utf-8')
	title = urllib.unquote(title).split('#')[0]
	ns = NAMESPACE_RE.match(title)
	if not ns:
		namespace = ""
		title = normalize(title)
	else:
		nsPart = ns.group(1).capitalize()
		if nsPart in namespaces:
			namespace = nsPart
			title = normalize(title[ns.end():])
	return (namespace, title)

def isVandalismByComment(editComment, testLoose=True, testStrict=True):
	'''
	Check the given edit comment against the VLOOSE and VSTRICT regexes
	as configured, and returns a boolean defining if it matches or not.

	@param editComment: The edit comment to test.
	@type editComment: str

	@param testLoose: If the edit comment matches VLOOSE_RE, True is returned
	@type testLoose: bool

	@param testStrict: If the edit comment matches VSTRICT_RE, True is returned
	@type testStrict: bool
	'''
	if editComment == None:
		return False
	if testLoose and VLOOSE_RE.search(editComment):
		return True;
	if testStrict and VSTRICT_RE.search(editComment):
		return True;

	return False;
