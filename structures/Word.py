'''
Created on Feb 20, 2013

@author: maribelacosta
'''

class Word(object):
    '''
    Implementation of the structure "Word", which includes the authorship information.
    '''


    def __init__(self):
        self.author_id = 0    # Identificator of the author of the word.
        self.author_name = '' # Username of the author of the word.
        self.revision = 0     # Revision where the word was included.
        self.value = ''       # The word (simple text).
        self.matched = False  #
        self.length = 0
        
    
    def __repr__(self):
        return str(id(self))
    
    
    def to_dict(self):
        word = {}
        #word.update({'author' : {'id': self.author_id, 'username': self.author_name}})
        word.update({str(self.revision) : self.value})
    
        return word
    
