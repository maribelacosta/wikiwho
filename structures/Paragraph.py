#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Feb 20, 2013

@author: maribelacosta
'''

class Paragraph(object):
    '''
    classdocs
    '''


    def __init__(self):
        self.hash_value = '' # The hash value of the paragraph.
        self.value = ''      # The text of the paragraph.
        self.sentences = {}  # Dictionary of sentences in the paragraph. It is a dictionary of the form {sentence_hash : Sentence}
        self.ordered_sentences = [] # List with the hash of the sentences, ordered by hash appeareances.
        self.matched = False # Flag.

    def __repr__(self):
        return str(id(self))

    def to_dict(self):
        paragraph = {}
        paragraph.update({'hash' : self.hash_value})

        obj_sentences = []
        for sentence_hash in self.ordered_sentences:
            s = []
            for sentence in self.sentences[sentence_hash]:
                s.append(repr(sentence))
            obj_sentences.append(s)

        paragraph.update({'obj' : obj_sentences})

        return paragraph
