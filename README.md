wikiwho
=======
An algorithm to identify authorship and editor interactions in Wiki revisioned content.

Installation Requirements
========================
WikiWho has been tested on Mac OS X and Debian GNU/Linux, running on Python 2.7. 
(A python3 version can be found in this branch: https://github.com/maribelacosta/wikiwho/tree/python3 It has however not  been extensively tested yet - stick to the master for now if you want reliability)

WikiWho utilizes the Wikimedia Utilities library to process the revisioned content extracted from Wikipedia. 
These functions can be downloaded from the official Wikimedia Utilities repository (under the MIT license) at the
following link:
* https://bitbucket.org/halfak/wikimedia-utilities

Running WikiwhoRelationships.py  
===============
(Note: WikiWho.py is the original script, giving just provenance information. WikiwhoRelationships.py can provide the exact same authorship/provenance data, plus interactions, but might run slower due to the overhead of interaction calculation. We didn't test that yet.)

How to run:

python WikiwhoRelationships.py 

parameters: 

-i \[source_file_name.xml\] (complete history dump XML of one article)

-o [a | r] --> what type of output to produce --> a=authorship for all tokens of a revision | r= interactions for every revision with each other revision in the past. I.e., this will list you all revisions and for each type of interaction we defined (delete, undelete, reintro, ..) the revisions that were target of that interaction and the number of tokens that interaction included. We will soon provide code that will spit put a more aggregated version of this as an editor-editor network. Yet, from the output available right now, you can already construct such a network yourself by summing up the positive and/or negative interactions between two editors over the whole revision history or a part of it.

-r [\<revid\> | all] --> what revision to show. revID or "all" for -o a, revID only for -o r 


example A:

python WikiwhoRelationships.py -i Randomarticle.xml -o a -r 5

gives authorship for all tokens of revision 5 (has to be an actual revision id) of Randomarticle

example B:

python WikiwhoRelationships.py -i Randomarticle.xml -o r -r 5

gives the edit interactions produced at every revision to other revisions, up to revision number 5 (has to be an actual revision id) of Randomarticle




Contact
=======
* Fabian Floeck: fabian.floeck[.]gesis.org
* Maribel Acosta: maribel.acosta[.]kit.edu

License
=======
This work is licensed under the MIT license.
