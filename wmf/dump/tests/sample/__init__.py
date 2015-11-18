import os, subprocess

def extractFile(fileName):
	decompressCall = "lzma -c -q -d %s" % fileName
	process = subprocess.Popen(
		decompressCall,
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE,
		shell=True
	)
	return process.stdout
	
def getSmallXMLFilePath():
	pwd = os.path.dirname(os.path.realpath(__file__))
	return os.path.join(pwd, "small.xml.lzma")


def getLargeXMLFilePath():
	pwd = os.path.dirname(os.path.realpath(__file__))
	return os.path.join(pwd, "large.xml.lzma")


def getSmallXMLFilePointer():
	return extractFile(getSmallXMLFilePath())
	
def getLargeXMLFilePointer():
	return extractFile(getLargeXMLFilePath())
	