from xml_iterator import XMLIterator
from ..util import wp2Timestamp

def cleanTag(prefix, raw):
	return raw[len(prefix):]
	

class Iterator:
	"""
	WikiFile dump processor.  This class constructs with a filepointer to a 
	Wikipedia XML dump file.
	
	"""
	
	def __init__(self, fp):
		"""
		Constructor
		
		:Parameters:
			fp : file pointer
				a file pointer to the xml file to process.
		"""
		
		self.fp = fp           #:The file pointer passed to the constructor
		self.namespaces = {}   #:A map of possible namespaces
		self.siteName  = None  #:The name of the site
		self.base      = None  #:Base of the xml file
		self.generator = None  #:Generator of the dump
		self.case      = None  #:The default title case
		
		self.mediawikiElement = XMLIterator(fp)
		self.ns = self.mediawikiElement.tag[:-len('mediawiki')]
		
		pageCount = 0
		done = False
		for element in self.mediawikiElement:
			tag = cleanTag(self.ns, element.tag)
			if tag == "siteinfo":
				self.loadSiteInfo(element)
				element.clear()
				break
				
				
		
	def loadSiteInfo(self, siteInfoElement):
		for element in siteInfoElement:
			tag = cleanTag(self.ns, element.tag)

			if tag == 'sitename':
				self.siteName = element.text
			elif tag == 'base':
				self.base = element.text
			elif tag == 'generator':
				self.generator = element.text
			elif tag == 'case':
				self.case = element.text
			elif tag == 'namespaces':
				self.loadNamespaces(element)
				element.clear()
			
			
	
	def loadNamespaces(self, namespacesElement):
		for element in namespacesElement:
			tag = cleanTag(self.ns, element.tag)
			
			if tag == "namespace":
				namespace = Namespace(element)
				self.namespaces[namespace.getName()] = namespace.getId()
			else:
				assert False, "This should never happen"
				
		
	def readPages(self):
		for element in self.mediawikiElement:
			tag = cleanTag(self.ns, element.tag)
			if tag == "page":
				yield Page(self.ns, element)
			
		
	

class Namespace:
	
	def __init__(self, nsElement):
		self.setId(nsElement.get('key'))
		self.setName(nsElement.text)
	
	def setId(self, id): self.id = int(id)
	def getId(self): return self.id
	
	def setName(self, name): 
		if name == None:
			self.name = None
		else:
			self.name = unicode(name)
	def getName(self): return self.name
	
	def __repr__(self):
		return "%s(%r, %r)" % (
			self.__class__.__name__,
			self.getId(),
			self.getName()
		)
	
	def __eq__(self, other):
		try:
			return (
				self.getId() == other.getId() and
				self.getName() == other.getName()
			)
		except AttributeError:
			return False

class Page:
	
	def __init__(self, ns, pageElement):
		self.id = None
		self.title = None
		self.namespace = None
		self.pageElement = pageElement
		self.ns = ns
		for element in pageElement:
			tag = cleanTag(ns, element.tag)
			if tag == "id":
				self.setId(element.text)
			elif tag == "title":
				self.setTitle(element.text)
			elif tag == "ns":
				self.setNamespace(element.text)
			
			if self.id != None and self.title != None:
				break
		
	def readRevisions(self):
		for element in self.pageElement:
			tag = cleanTag(self.ns, element.tag)
			if tag == "revision":
				yield Revision(self.ns, element)
				#element.clear()
			
			
	
	def setId(self, id): self.id = int(id)
	def getId(self): return self.id
	
	def setTitle(self, title): self.title = unicode(title)
	def getTitle(self): return self.title

	def setNamespace(self, ns): self.namespace = int(ns)
	def getNamespace(self): return self.namespace
		
	

class Revision:
	
	TAG_MAP = {
		'id':          lambda s,e:s.setId(e.text),
		'timestamp':   lambda s,e:s.setTimestamp(e.text),
		'contributor': lambda s,e:s.setContributor(e),
		'minor':       lambda s,e:s.setMinor(True),
		'comment':     lambda s,e:s.setComment(e.text),
		'text':        lambda s,e:s.setText(e.text),
		'sha1':	       lambda s,e:s.setSha1(e.text),
		'parentid':    lambda s,e:s.setParentId(e.text),
		'model':       lambda s,e:s.setModel(e.text),
		'format':      lambda s,e:s.setFormat(e.text)
	}
	
	def __init__(self, ns, revisionElement):
		self.ns = ns
		self.id          = None
		self.timestamp   = None
		self.contributor = None
		self.minor       = False #No tag means minor edit
		self.comment     = None
		self.text        = None
		self.sha1        = None
		self.parentId    = None
		self.model       = None
		self.format      = None
		for element in revisionElement:
			tag = cleanTag(ns, element.tag)
			self.TAG_MAP[tag](self, element)
	
	def setId(self, id): self.id = int(id)
	def getId(self): return self.id
	
	def setTimestamp(self, timestamp):
		try: self.timestamp = int(timestamp)
		except ValueError: self.timestamp = wp2Timestamp(timestamp)
	def getTimestamp(self): return self.timestamp
	
	def setContributor(self, element): 
		if element.get("deleted", None) == "deleted":
			self.contributor = None
		else:
			self.contributor = Contributor(self.ns, element)
		
	def getContributor(self): return self.contributor
	
	def setMinor(self, minor): self.minor = minor == True
	def getMinor(self): return self.minor
	
	def setComment(self, comment): self.comment = unicode(comment)
	def getComment(self): return self.comment
	
	def setText(self, text): 
		if text == None: self.text = u''
		else: self.text = unicode(text)
	def getText(self): return self.text

	def setSha1(self, value): self.sha1 = value
	def getSha1(self): return self.sha1

	def setParentId(self, id): self.parentId = int(id)
	def getParentId(self): return self.parentId

	def setModel(self, value): self.model = value
	def getModel(self): return self.model

	def setFormat(self, value): self.format = value
	def getFormat(self): return self.format

class Contributor:
	
	TAG_MAP = {
		'id':       lambda s,e:s.setId(e.text),
		'username': lambda s,e:s.setUsername(e.text),
		'ip':       lambda s,e:s.setUsername(e.text)
	}
	
	def __init__(self, ns, contributorElement):
		self.id = None
		for element in contributorElement:
			tag = cleanTag(ns, element.tag)
			self.TAG_MAP[tag](self, element)
	
	def setId(self, id): self.id = int(id)
	def getId(self): return self.id
	
	def setUsername(self, username): self.username = unicode(username)
	def getUsername(self): return self.username
	

		
