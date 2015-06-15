#!/usr/bin/python
# -*- coding: utf-8 -*-
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
        self.freq = []
        self.deleted = []
        self.internal_id = 0
        self.used = []


    def __repr__(self):
        return str(id(self))


    def to_dict(self):
        word = {}
        word.update({str(self.revision) : self.value})

        return word
