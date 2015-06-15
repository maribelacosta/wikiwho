#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Jun 14, 2014

@author: maribelacosta
'''

class Relation(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.revision = ''     # Wikipedia revision id
        self.author = ''       # Author of the revision
        self.length = 0        # Total length of 'revision'
        self.total_tokens = 0

        self.added = 0         # Number of new tokens.

        self.deleted = {}      # Given a revision, the number of tokens deleted from that revision
        self.reintroduced = {} # Given a revision, the number of tokens reintroduced from that revision
        self.redeleted = {}    #
        self.revert = {}

        self.self_reintroduced = {}
        self.self_redeleted = {}
        self.self_deleted = {}
        self.self_revert = {}
