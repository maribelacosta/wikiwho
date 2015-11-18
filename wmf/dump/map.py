"""
Dump Mapper

This script acts as a map/function over the pages in a set of MediaWiki 
database dump files.  This script allows the algorithm for processing a set of
pages to be spread across the available processor cores of a system for faster 
analysis. 

This script can also be imported as a module to expose the `map()` function
that returns an iterator over output rather than printing to stdout.

Examples:

dump_map revision_meta /dumps/enwiki-20110115-pages-meta-history* > ~/data/revision_meta.tsv
"""
import sys, logging, re, types, argparse, os, subprocess, importlib
from multiprocessing import Process, Queue, Lock, cpu_count, Value
from Queue import Empty

from .iterator import Iterator

class FileTypeError(Exception):pass

class Processor(Process):
	"""
	A processor for managing the reading of dump files from a queue and
	the application of a a function for each 'page'.
	"""
	
	def __init__(self, input, processPage, output, callback, logger, noop):
		"""
		Constructor
		
		:Parameters:
			input : `multiprocessing.Queue`
				a queue paths to dump files to process
			processPage : function
				a function to apply to each page of a dump file
			output : `multiprocessing.Queue`
				a queue to send processing output to
			callback : function
				a function to run upon completion
			logger : `logging.Logger`
				a logger object to send logging events to
		"""
		self.input       = input
		self.processPage = processPage
		self.output      = output
		self.callback    = callback
		self.logger      = logger
		self.noop        = noop
		Process.__init__(self)
	
	def run(self):
		try:
			while True:
				foo = self.input.qsize()
				fn = self.input.get(block=False)
				self.logger.info("Processing dump file %s." % fn)
				dump = Iterator(openDumpFile(fn))
				for page in dump.readPages():
					self.logger.debug("Processing page %s:%s." % (page.getId(), page.getTitle()))
					try:
						if self.noop: self.processPage(dump, page)
						else:
							for out in self.processPage(dump, page):
								self.output.put(out)
					except Exception as e:
						self.logger.error(
							"Failed to process page %s:%s - %s" % (
								page.getId(),
								page.getTitle(),
								e
							)
						)
					
				
			
			
		except Empty:
			self.logger.info("Nothing left to do.  Shutting down thread.")
		finally:
			self.callback()
		

def map(dumps, processPage, threads=cpu_count()-1, outputBuffer=100):
	"""
	Maps a function across all of the pages in a set of dump files and returns
	an (order not guaranteed) iterator over the output.  Increasing the 
	`outputBuffer` size will allow more mapplications to happen before the 
	output is read, but will consume memory to do so.  Big output buffers 
	are benefitial when the resulting iterator from this map will be read in
	bursts.
	
	The `processPage` function must return an iterable object (such as a 
	generator).  If your processPage function does not need to produce 
	output, make it return an empty iterable upon completion (like an empty
	list).
	
	:Parameters:
		dumps : list
			a list of paths to dump files to process
		processPage : function
			a function to run on every page of a set of dump files
		threads : int
			the number of individual processing threads to spool up
		outputBuffer : int
			the maximum number of output values to buffer. 
	"""
	input   = dumpFiles(dumps)
	output  = Queue(maxsize=outputBuffer)
	running = Value('i', 0)
	threads = max(1, min(int(threads), input.qsize()))
	
	def dec(): running.value -= 1
	
	for i in range(0, threads):
		running.value += 1
		Processor(
			input,
			processPage,
			output,
			dec,
			logging.getLogger("Process %s" % i),
			False
		).start()
	
	#output while processes are running
	while running.value > 0:
		try:          yield output.get(timeout=.25)
		except Empty: pass
	
	#finish yielding output buffer
	try:
		while True: yield output.get(block=False) 
	except Empty: 
		pass
		
	

	

EXTENSIONS = {
	'xml': "cat",
	'bz2': "bzcat",
	'7z':  "7zr e -so",
	'lzma':"lzcat"
}
"""
A map from file extension to the command to run to extract the data to standard out.
"""

EXT_RE = re.compile(r'\.([^\.]+)$')
"""
A regular expression for extracting the final extension of a file.
"""


def dumpFile(path):
	"""
	Verifies that a file exists at a given path and that the file has a 
	known extension type.
	
	:Parameters:
		path : `str`
			the path to a dump file
		
	"""
	path = os.path.expanduser(path)
	if not os.path.isfile(path):
		raise FileTypeError("Can't find file %s" % path)
	
	match = EXT_RE.search(path)
	if match == None:
		raise FileTypeError("No extension found for %s." % path)
	elif match.groups()[0] not in EXTENSIONS:
		raise FileTypeError("File type %r is not supported." % path)
	else:
		return path

def dumpFiles(paths):
	"""
	Produces a `multiprocessing.Queue` containing path for each value in
	`paths` to be used by the `Processor`s.
	
	:Parameters:
		paths : iterable
			the paths to add to the processing queue
	"""
	q = Queue()
	for path in paths: q.put(dumpFile(path))
	return q

def openDumpFile(path):
	"""
	Turns a path to a dump file into a file-like object of (decompressed)
	XML data.
	
	:Parameters:
		path : `str`
			the path to the dump file to read
	"""
	match = EXT_RE.search(path)
	ext = match.groups()[0]
	p = subprocess.Popen(
		"%s %s" % (EXTENSIONS[ext], path), 
		shell=True, 
		stdout=subprocess.PIPE,
		stderr=open(os.devnull, "w")
	)
	#sys.stderr.write("\n%s %s\n" % (EXTENSIONS[ext], path))
	#sys.stderr.write(p.stdout.read(1000))
	#return False
	return p.stdout


def encode(v):
	"""
	Encodes an output value as a string intended to be read by eval()
	"""
	if type(v) == types.FloatType:
		return str(int(v))
	elif v == None:
		return "\\N"
	else:
		return repr(v)



def main():
	parser = argparse.ArgumentParser(
		description='Maps a function across pages of MediaWiki dump files'
	)
	parser.add_argument(
		'-o', '--out',
		metavar="<path>",
		type=lambda path:open(path, "w"), 
		help='the path to an output file to write putput to (defaults to stdout)',
		default=sys.stdout
	)
	parser.add_argument(
		'-t', '--threads',
		metavar="",
		type=int, 
		help='the number of threads to start (defaults to # of cores -1)',
		default=cpu_count()-1
	)
	parser.add_argument(
		'processor',
		type=lambda path: importlib.import_module(path, path), 
		help='the class path to the module that contains the process() function be passed each page'
	)
	parser.add_argument(
		'dump',
		type=dumpFile, 
		help='the XML dump file(s) to process',
		nargs="+"
	)
	parser.add_argument(
		'--debug',
		action="store_true",
		default=False
	)
	args = parser.parse_args()
	
	LOGGING_STREAM = sys.stderr
	if args.debug: level = logging.DEBUG
	else:          level = logging.INFO
	logging.basicConfig(
		level=level,
		stream=LOGGING_STREAM,
		format='%(name)s: %(asctime)s %(levelname)-8s %(message)s',
		datefmt='%b-%d %H:%M:%S'
	)
	logging.info("Starting dump processor with %s threads." % min(args.threads, len(args.dump)))
	for row in map(args.dump, args.processor.process, threads=args.threads):
		print('\t'.join(encode(v) for v in row))

if __name__ == "__main__":
	main()
