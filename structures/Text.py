#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Feb 20, 2013

@author: maribelacosta
'''

import hashlib
from codecs import encode

def calculateHash(text):
    encodedText = encode(text)
    return hashlib.md5(encodedText).hexdigest()


def splitIntoParagraphs(text):
    paragraphs = text.split("\n\n")

    return paragraphs


def splitIntoSentences(text):
    p = text

    p = p.replace('.', '.@@@@')
    p = p.replace('\n', '\n@@@@')
    p = p.replace(';', ';@@@@')
    p = p.replace('?', '?@@@@')
    p = p.replace('!', '!@@@@')
    #p = p.replace('.{', '.||{')
    #p = p.replace('!{', '!||{')
    #p = p.replace('?{', '?||{')
    p = p.replace('>{', '>@@@@{')
    p = p.replace('}<', '}@@@@<')
    #p = p.replace('.[', '.||[')
    #p = p.replace('.]]', '.]]||')
    #p = p.replace('![', '!||[')
    #p = p.replace('?[', '?||[')
    p = p.replace('<ref', '@@@@<ref')
    p = p.replace('/ref>', '/ref>@@@@')


    while '@@@@@@@@' in p :
        p = p.replace('@@@@@@@@', '@@@@')

    sentences = p.split('@@@@')

    return sentences


def splitIntoWords(text):
    p = text
    p = p.replace('|', '||@||')

    p = p.replace('<', '||<').replace('>', '>||')
    p = p.replace('?', '?||').replace('!', '!||').replace('.[[', '.||[[').replace('\n', '||')

    p = p.replace('.', '||.||').replace(',', '||,||').replace(';', '||;||').replace(':', '||:||').replace('?', '||?||').replace('!', '||!||')
    p = p.replace('-', '||-||').replace('/', '||/||').replace('\\', '||\\||').replace('\'\'\'', '||\'\'\'||')
    p = p.replace('(', '||(||').replace(')', '||)||')
    p = p.replace('[', '||[||').replace(']', '||]||')
    p = p.replace('{', '||{||').replace('}', '||}||')
    p = p.replace('*', '||*||').replace('#', '||#||').replace('@', '||@||').replace('&', '||&||')
    p = p.replace('=', '||=||').replace('+', '||+||').replace('_', '||_||').replace('%', '||%||')
    p = p.replace('~', '||~||')
    p = p.replace('$', '||$||')
    p = p.replace('^', '||^||')

    p = p.replace('<', '||<||').replace('>', '||>||')
    p = p.replace('[||||[', '[[').replace(']||||]', ']]')
    p = p.replace('{||||{', '{{').replace('}||||}', '}}')
    p = p.replace('||.||||.||||.||', '...').replace('/||||>', '/>').replace('<||||/', '</')
    p = p.replace('-||||-', '--')

    p = p.replace('<||||!||||--||', '||<!--||').replace('||--||||>', '||-->||')
    p = p.replace(' ', '||')

    while '||||' in p :
        p = p.replace('||||', '||')

    words = filter(lambda a : a != '', p.split('||'))
    words = ['|' if w == '@' else w for w in words]

    return words


def computeAvgWordFreq(text_list, revision_id=0):

    d = {}

    for elem in text_list:
        if not elem in d:
            d.update({elem : text_list.count(elem)})

    if ('<' in d):
        del d['<']

    if ('>' in d):
        del d['>']

    if ('tr' in d):
        del d['tr']

    if ('td' in d):
        del d['td']

#    if ('(' in d):
#        del d['(']
#
#    if (')' in d):
#        del d[')']

    if ('[' in d):
        del d['[']

    if (']' in d):
        del d[']']

    if ('"' in d):
        del d['"']

#    if ('|' in d):
#        del d['|']

    if ('*' in d):
        del d['*']

    if ('==' in d):
        del d['==']


    if (len(d) > 0):
        return sum(d.values())/float(len(d))
    else:
        return 0
