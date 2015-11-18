import requests, json, hashlib

class MediaWikiAPIError(Exception): pass

class MediaWikiAPI:
	
	def __init__(self, uri, headers={}, cookies={}):
		self.uri = uri
		self.headers = headers
		self.cookies = cookies
		self.session = requests.session(headers=headers, cookies=cookies)
	
	
	def __process(self, requester, data):
		data.update({'format': 'json'})
		response = requester(self.uri, data)
	
		if response.status_code == requests.codes.ok:
			#print(response.text)
			js = json.loads(response.text)
			if 'error' in js: 
				raise MediaWikiAPIError("%s: %s" % (js['error'].get('code'), js['error'].get('info')))
			else:
				return js
			
		else:
			response.raise_for_status()
		
		
	def post(self, data):return self.__process(self.session.post, data)
	def get(self, data):return self.__process(self.session.get, data)
	
	def reload(self):
		self.session = requests.session(headers=headers, cookies=cookies)
	
	def headers(self, headers=None):
		if headers == None: return self.headers
		else: self.headers = headers
	
	def cookies(self, cookies=None):
		if cookies == None: return self.cookies
		else: self.cookies = cookies
	
	

class Revisions(MediaWikiAPI):
	
	def reverted(self, revId, pageId=None, pageTitle=None):
		if (pageId, pageTitle) == (None, None):
			raise TypeError("Either pageId or pageTitle must be set.")
		
		data = {
			'action':    "query",
			'prop':      "revisions",
			'rvprop':    "|".join(['ids', 'content', 'comment']),
			'rvstartid': revId-1,
			'rvlimit':   15
		}
		
		if pageId != None:
			data.update({'pageids': pageId})
		else:
			data.update({'titles': pageTitle})
		
		js = self.post(data)
		
		oldRevs = {}
		for revision in reversed(js['query']['pages'].values()[0]['revisions']):
			revision['checksum'] = hashlib.md5(revision.get('*', "")).hexdigest()
			if '*' in revision: del revision['*']
			
			oldRevs[revision['checksum']] = revision
			
		data.update({
			'rvdir': "newer",
			'rvstartid': revId, 
			'rvlimit': 16 #Note: getting 16 since I want to get the current rev too
		}) 
		
		js = self.post(data)
		
		currentRev = js['query']['pages'].values()[0].get('revisions', []).pop(0)
		if currentRev['revid'] != revId: 
			raise ValueError("Can't find rev_id %s in %s(%s)." % (revId, js['query']['pages'].values()[0]['title'], js['query']['pages'].values()[0]['pageid']))
		currentRev['checksum'] = hashlib.md5(currentRev.get('*', "")).hexdigest()
		if '*' in revision: del revision['*']
		
		for revision in js['query']['pages'].values()[0]['revisions']:
			revision['checksum'] = hashlib.md5(revision.get('*', "")).hexdigest()
			if '*' in revision: del revision['*']
			
			if revision['checksum'] == currentRev['checksum']: continue #reverted back to
			elif revision['checksum'] in oldRevs: #revert found!
				return (revision, oldRevs[revision['checksum']])
			
		
		return None
		
	
	def meta(self, revIds, props=None, **kwargs):
		if not hasattr(revIds, "__iter__"): revIds = [revIds] #If not iterable, create a singleton list
		props = set() if props == None else set(props)
		
		
		props = props | set([
			'ids',
			'sha1'
		])
		
		data = {
			'action': "query",
			'prop':   "revisions",
			'revids': "|".join(str(id) for id in revIds),
			'rvprop': "|".join(str(p) for p in props)
		}
		data.update(kwargs)
		
		js = self.post(data)
		
		for page in js['query']['pages'].values():
			for revision in page['revisions']:
				yield revision
			
		
	


