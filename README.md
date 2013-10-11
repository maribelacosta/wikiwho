wikiwho
=======
An algorithm to identify authorship in Wiki revisioned content.

Installation Requirements
========================
WikiWho has been tested on Mac OS X and Debian GNU/Linux, running on Python 2.7. 

WikiWho utilizes the Wikimedia Utilities library to process the revisioned content extracted from Wikipedia. 
These functions can be downloaded from the official Wikimedia Utilities repository (under the MIT license) at the
following link:
* https://bitbucket.org/halfak/wikimedia-utilities

Running WikiWho
===============

python Wikiwho.py -i inputfile [-rev revision_id]

Example:
python Wikiwho.py -i "../example/Bioglass.xml" 

Output
------
After running the provided example, the output of WikiWho looks like this:

Calculating authorship for: /Users/maribelacosta/Desktop/dataset2/Bioglass.xml
Printing authorhship for revision:  537791102
['{{', 'disputed', '|', 'date', '=', 'february', '2012', '}}', (...)]
[474609306, 474609306, 474612283, 474612283, 474612283, 474612283, 474612283, 474609306, (...)]
Execution time: 0.855736017227

The first array "token" corresponds to the analyzed tokens. The second array associates the tokens to their
respective origin, e.g. origin[i] is the original label of token[i].

Contact
=======
* Fabian Floeck: fabian.floeck[.]kit.edu
* Maribel Acosta: maribel.acosta[.]kit.edu

License
=======
This work is licensed under GNU/GPL v2.
