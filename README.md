wikiwho
=======
An algorithm to identify authorship and editor interactions in Wiki revisioned content.

Installation Requirements
========================
WikiWho has been tested on Mac OS X and Debian GNU/Linux, running on Python 2.7. 

WikiWho utilizes the Wikimedia Utilities library to process the revisioned content extracted from Wikipedia. 
These functions can be downloaded from the official Wikimedia Utilities repository (under the MIT license) at the
following link:
* https://bitbucket.org/halfak/wikimedia-utilities

Running wikiwho(Relationships)
===============

python WikiwhoRelationships.py 

parameters: 

-i \[source_file_name.xml\] (complete history dump XML of one article)

-o [a | r] --> what type of output to produce --> a=authorship for all tokens of a revision | r= editor relations for a revision, built on a all edit interactions in the past

-r [\<revid\> | all] --> what revision to show. revID or "all" for -o a, revID only for -o r 


example A:

python WikiwhoRelationships.py -i Randomarticle.xml -o a -r 5

gives authorship for all tokens of revision 5 (has to be an actual revision id) of Randomarticle

example B:

python WikiwhoRelationships.py -i Randomarticle.xml -o r -r 5

gives the edit interactions produced at every revision to other revisions, up to revision number 5 (has to be an actual revision id) of Randomarticle




Contact
=======
* Fabian Floeck: fabian.floeck[.]kit.edu
* Maribel Acosta: maribel.acosta[.]kit.edu

License
=======
This work is licensed under GNU/GPL v2.
