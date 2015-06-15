#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Feb 20, 2013

@author: maribelacosta
'''

class Revision(object):
    '''
    classdocs
    '''


    def __init__(self):
        self.id = 0                  # Fake sequential id. Starts in 0.
        self.wikipedia_id = 0        # Wikipedia revision id.
        self.contributor_id = 0;     # Id of the contributor who performed the revision.
        self.contributor_name = ''   # Name of the contributor who performed the revision.
        self.contributor_ip = ''     # Name of the contributor who performed the revision.
        self.paragraphs = {}         # Dictionary of paragraphs. It is of the form {paragraph_hash : [Paragraph]}.
        self.ordered_paragraphs = [] # Ordered paragraph hash.
        self.length = 0              # Content length (bytes).
        self.total_tokens = 0        # Number of tokens in the revision.
        self.timestamp = 0

    def __repr__(self):
        return str(id(self))

    def to_dict(self):
        revision = {}
        revision.update({'obj' : []})
        for paragraph_hash in self.ordered_paragraphs:
            p = []
            for paragraph in self.paragraphs[paragraph_hash]:
                p.append(repr(paragraph))
            revision['obj'].append(p)

        return revision
