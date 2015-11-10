wikiwho
=======
An algorithm to identify authorship and editor interactions in Wiki revisioned content.

(also check out our API: http://f-squared.org/wikiwho/#api ) 

Installation Requirements
========================
WikiWho has been tested on Mac OS X and Debian GNU/Linux, running on Python 2.7. 
(A python3 version can be found in this branch: https://github.com/maribelacosta/wikiwho/tree/python3 It has however not  been extensively tested yet - stick to the master for now if you want reliability)

WikiWho utilizes the Wikimedia Utilities library to process the revisioned content extracted from Wikipedia. 
These functions can be downloaded from the Wikimedia Utilities repository (under the MIT license) at the
following link:
* https://bitbucket.org/halfak/wikimedia-utilities  (note: this is a legacy version of mw-utilities, the new one is python 3 and will not run with the p2.7 version of wikiwho!) 

Running WikiwhoRelationships.py  
===============
(Note: WikiWho.py is the original script, giving just provenance information. WikiwhoRelationships.py can provide the exact same authorship/provenance data, plus interactions, but might run slower due to the overhead of interaction calculation. We didn't test that yet.)

Expected data: 
- the full revision history of one or a given set of wiki articles (basically everything that wikimedia utilities can process). It is here expected to be .xml, could also be .json, etc. if you parse it correctly. 

- you can get xml for single articles [here](https://en.wikipedia.org/w/index.php?title=Special:Export&history), although this is only recommended for testing purposes. Or (more reliable, but only 50 revisions at a time) at the official API: [example call](https://en.wikipedia.org//w/api.php?rvcontinue=20150501221233%7C660323497&rvdir=newer&titles=Darmstadt&continue=&rvlimit=max&format=json&action=query&rvprop=content%7Cids%7Ctimestamp%7Csha1%7Ccomment%7Cflags%7Cuser%7Cuserid&prop=revisions) (note that you will have to use rvcontinue to get all revisions). Finally, the full history dump can be downloaded at the [WM dumps page](http://dumps.wikimedia.org/backup-index-bydb.html). Note that the dump is quite big for enwiki, i.e. not recommended just for testing. Use wm utilities to read the compressed files.    


How to run:

python WikiwhoRelationships.py 

parameters: 

**-i** \[source_file_name.xml\] (complete history dump XML of one article)

**-o [a | r]** --> what type of output to produce --> **a** = authorship for all tokens of a revision | **r** = interactions for every revision with each other revision in the past. I.e., this will list you all revisions and for each type of interaction we defined (delete, undelete, reintro, ..) the revisions that were target of that interaction and the number of tokens that interaction included. We will soon provide code that will spit put a more aggregated version of this as an editor-editor network. Yet, from the output available right now, you can already construct such a network yourself by summing up the positive and/or negative interactions between two editors over the whole revision history or a part of it.

**-r [\<revid\> | all]** --> what revision to show. revID or "all" for -o a, revID only for -o r 

Examples
===============

- example A:

```python WikiwhoRelationships.py -i Randomarticle.xml -o a -r 5```

gives authorship for all tokens of revision 5 (has to be an actual revision id) of Randomarticle
 
- example B:

```python WikiwhoRelationships.py -i Randomarticle.xml -o r -r 5```


gives the edit interactions produced at every revision to other revisions, up to revision number 5 (has to be an actual revision id) of Randomarticle

- "Finger_Lakes3" dummy article example:

run 

    python WikiwhoRelationships.py -i Finger_Lakes3_dummy.xml -o a -r 27  

the xml file can be found in the "example files" folder. 27 is the last revision, you can also run it for all others. 
check the Finger_Lakes3_explained.xlsx in the same folder to get an explanation of the results. 
you can also try the -o r argument, the results are also displayed in the xlsx 



Contact
=======
* Fabian Floeck: fabian.floeck[.]gesis.org
* Maribel Acosta: maribel.acosta[.]kit.edu

License
=======
This work is licensed under the MIT license.
