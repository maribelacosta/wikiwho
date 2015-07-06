#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Feb 20, 2013
@author: Maribel Acosta
@author: Fabian Floeck
'''

from difflib import Differ
from mw.xml_dump import Iterator as mwIterator
from mw.xml_dump.functions import open_file
from time import time

from structures import Text
from structures.Paragraph import Paragraph
from structures.Revision import Revision
from structures.Sentence import Sentence
from structures.Word import Word

from etc.Relation import Relation

from sys import argv,exit
import getopt

from copy import deepcopy, copy

# Container of revisions.
revisions = {}
revision_order = []

# Hash tables.
paragraphs_ht = {}
sentences_ht = {}
spam = []

# SPAM detection variables.
CHANGE_PERCENTAGE = -0.40
PREVIOUS_LENGTH = 1000
CURR_LENGTH = 1000
FLAG = "move"
UNMATCHED_PARAGRAPH = 0.0
WORD_DENSITY = 10

def analyseArticle(file_name):
    # Container of relationships.
    relations = {}

    # Revisions to compare.
    revision_curr = Revision()
    revision_prev = Revision()
    text_curr = None

    # Access the file.
    dumpIterator = mwIterator.from_file(open_file(file_name))

    # Iterate over the pages.
    for page in dumpIterator:
        i = 0

        # Iterate over revisions of the article.
        for revision in page:
            vandalism = False

            # Update the information about the previous revision.
            revision_prev = revision_curr

            if (revision.sha1 == None):
                revision.sha1 = Text.calculateHash(revision.text)

            if (revision.sha1 in spam):
                vandalism = True

            #TODO: SPAM detection: DELETION
            if (revision.comment!= None and revision.comment.find(FLAG) > 0):
                pass
            else:
                if (revision_prev.length > PREVIOUS_LENGTH) and (len(revision.text) < CURR_LENGTH) and (((len(revision.text)-revision_prev.length)/float(revision_prev.length)) <= CHANGE_PERCENTAGE):
                    vandalism = True
                    revision_curr = revision_prev

            if (not vandalism):
                # Information about the current revision.
                revision_curr = Revision()
                revision_curr.id = i
                revision_curr.wikipedia_id = int(revision.id)
                revision_curr.length = len(revision.text)
                revision_curr.timestamp = revision.timestamp

                # Relation of the current relation.
                relation = Relation()
                relation.revision = int(revision.id)
                relation.length = len(revision.text)

                # Some revisions don't have contributor.
                if (revision.contributor != None):
                    revision_curr.contributor_id = revision.contributor.id
                    revision_curr.contributor_name = revision.contributor.user_text
                    relation.author = revision.contributor.user_text
                else:
                    revision_curr.contributor_id = 'Not Available ' + revision.id
                    revision_curr.contribur_name = 'Not Available ' + revision.id
                    relation.author = 'Not Available ' + revision.id

                # Content within the revision.
                text_curr = revision.text.lower()

                # Perform comparison.
                vandalism = determineAuthorship(revision_curr, revision_prev, text_curr, relation)


                if (not vandalism):
                    # Add the current revision with all the information.
                    revisions.update({revision_curr.wikipedia_id : revision_curr})
                    relations.update({revision_curr.wikipedia_id : relation})
                    revision_order.append((revision_curr.wikipedia_id, False))
                    # Update the fake revision id.
                    i = i+1

                    # Calculate the number of tokens in the revision.
                    total = 0
                    for p in revision_curr.ordered_paragraphs:
                        for paragraph_curr in revision_curr.paragraphs[p]:
                            for hash_sentence_curr in paragraph_curr.sentences.keys():
                                for sentence_curr in paragraph_curr.sentences[hash_sentence_curr]:
                                    total = total + len(sentence_curr.words)
                    revision_curr.total_tokens = total
                    relation.total_tokens = total

                else:
                    revision_order.append((revision_curr.wikipedia_id, True))
                    revision_curr = revision_prev
                    spam.append(revision.sha1)

    return (revisions, revision_order, relations)

def determineAuthorship(revision_curr, revision_prev, text_curr, relation):

    # Containers for unmatched paragraphs and sentences in both revisions.
    unmatched_sentences_curr = []
    unmatched_sentences_prev = []
    matched_sentences_prev = []
    matched_words_prev = []
    possible_vandalism = False
    vandalism = False

    # Analysis of the paragraphs in the current revision.
    (unmatched_paragraphs_curr, unmatched_paragraphs_prev, matched_paragraphs_prev) = analyseParagraphsInRevision(revision_curr, revision_prev, text_curr, relation)

    # Analysis of the sentences in the unmatched paragraphs of the current revision.
    if (len(unmatched_paragraphs_curr)>0):
        (unmatched_sentences_curr, unmatched_sentences_prev, matched_sentences_prev, _) = analyseSentencesInParagraphs(unmatched_paragraphs_curr, unmatched_paragraphs_prev, revision_curr, revision_prev, relation)

        #TODO: SPAM detection
        if (len(unmatched_paragraphs_curr)/float(len(revision_curr.ordered_paragraphs)) > UNMATCHED_PARAGRAPH):
            possible_vandalism = True

        # Analysis of words in unmatched sentences (diff of both texts).
        if (len(unmatched_sentences_curr)>0):
            (matched_words_prev, vandalism) = analyseWordsInSentences(unmatched_sentences_curr, unmatched_sentences_prev, revision_curr, possible_vandalism, relation)

    if (len(unmatched_paragraphs_curr) == 0):
        for paragraph in unmatched_paragraphs_prev:
            for sentence_key in paragraph.sentences.keys():
                for sentence in paragraph.sentences[sentence_key]:
                    if not(sentence.matched):
                        unmatched_sentences_prev.append(sentence)

    # Add the information of 'deletion' to words
    for unmatched_sentence in unmatched_sentences_prev:
        for word_prev in unmatched_sentence.words:
            if not(word_prev.matched):
                for elem in word_prev.deleted:
                    if (elem != revision_curr.wikipedia_id) and (elem in revisions.keys()):
                        if (revisions[elem].contributor_id != revision_curr.contributor_id):
                            if (elem in relation.redeleted.keys()):
                                relation.redeleted.update({elem : relation.redeleted[elem] + 1})
                            else:
                                relation.redeleted.update({elem : 1})
                        else:
                            if (elem in relation.self_redeleted.keys()):
                                relation.self_redeleted.update({elem : relation.self_redeleted[elem] + 1})
                            else:
                                relation.self_redeleted.update({elem : 1})

                # Revert: deleting something that somebody else reintroduced.
                for elem in word_prev.freq:
                    if (elem != revision_curr.wikipedia_id) and (elem in revisions.keys()):
                        if (revisions[elem].contributor_id != revision_curr.contributor_id):
                            if (elem in relation.revert.keys()):
                                relation.revert.update({elem: relation.revert[elem] +1})
                            else:
                                relation.revert.update({elem: 1})
                        else:
                            if (elem in relation.self_revert.keys()):
                                relation.self_revert.update({elem: relation.self_revert[elem] +1})
                            else:
                                relation.self_revert.update({elem: 1})

                word_prev.deleted.append(revision_curr.wikipedia_id)
                if (revisions[word_prev.revision].contributor_id != revision_curr.contributor_id):
                    if (word_prev.revision in relation.deleted.keys()):
                        relation.deleted.update({word_prev.revision : relation.deleted[word_prev.revision] + 1 })
                    else:
                        relation.deleted.update({word_prev.revision : 1 })
                else:
                    if (word_prev.revision in relation.self_deleted.keys()):
                        relation.self_deleted.update({word_prev.revision : relation.self_deleted[word_prev.revision] + 1 })
                    else:
                        relation.self_deleted.update({word_prev.revision : 1 })



    # Reset matched structures from old revisions.
    for matched_paragraph in matched_paragraphs_prev:
        matched_paragraph.matched = False
        for sentence_hash in matched_paragraph.sentences.keys():
            for sentence in matched_paragraph.sentences[sentence_hash]:
                sentence.matched = False
                for word in sentence.words:
                    word.matched = False

    for matched_sentence in matched_sentences_prev:
        matched_sentence.matched = False
        for word in matched_sentence.words:
            word.matched = False

    for matched_word in matched_words_prev:
        matched_word.matched = False


    if (not vandalism):
        # Add the new paragraphs to hash table of paragraphs.
        for unmatched_paragraph in unmatched_paragraphs_curr:
            if (unmatched_paragraph.hash_value in paragraphs_ht.keys()):
                paragraphs_ht[unmatched_paragraph.hash_value].append(unmatched_paragraph)
            else:
                paragraphs_ht.update({unmatched_paragraph.hash_value : [unmatched_paragraph]})

            # Add the new sentences to hash table of sentences.
        for unmatched_sentence in unmatched_sentences_curr:
            if (unmatched_sentence.hash_value in sentences_ht.keys()):
                sentences_ht[unmatched_sentence.hash_value].append(unmatched_sentence)
            else:
                sentences_ht.update({unmatched_sentence.hash_value : [unmatched_sentence]})


    return vandalism

def analyseParagraphsInRevision(revision_curr, revision_prev, text_curr, relation):

    # Containers for unmatched and matched paragraphs.
    unmatched_paragraphs_curr = []
    unmatched_paragraphs_prev = []
    matched_paragraphs_prev = []

    # Split the text of the current into paragraphs.
    paragraphs = Text.splitIntoParagraphs(text_curr)

    # Iterate over the paragraphs of the current version.
    for paragraph in paragraphs:

        # Build Paragraph structure and calculate hash value.
        paragraph = paragraph.strip()
        hash_curr = Text.calculateHash(paragraph)
        matched_curr = False

        # If the paragraph is in the previous revision,
        # update the authorship information and mark both paragraphs as matched (also in HT).
        if (hash_curr in revision_prev.ordered_paragraphs):

            for paragraph_prev in revision_prev.paragraphs[hash_curr]:
                if (not paragraph_prev.matched):
                    matched_curr = True
                    paragraph_prev.matched = True
                    matched_paragraphs_prev.append(paragraph_prev)

                    # TODO: added this (CHECK).
                    for hash_sentence_prev in paragraph_prev.sentences.keys():
                        for sentence_prev in paragraph_prev.sentences[hash_sentence_prev]:
                            sentence_prev.matched = True
                            for word_prev in sentence_prev.words:
                                word_prev.matched = True
                                word_prev.used.append(revision_curr.wikipedia_id)

                    addParagraphs(revision_curr, revision_prev, hash_curr, paragraph_prev)
                    break


        # If the paragraph is not in the previous revision, but it is in an older revision
        # update the authorship information and mark both paragraphs as matched.
        if ((not matched_curr) and (hash_curr in paragraphs_ht)):
            for paragraph_prev in paragraphs_ht[hash_curr]:
                if (not paragraph_prev.matched):
                    matched_curr = True
                    paragraph_prev.matched = True
                    matched_paragraphs_prev.append(paragraph_prev)

                    # TODO: added this (CHECK).
                    for hash_sentence_prev in paragraph_prev.sentences.keys():
                        for sentence_prev in paragraph_prev.sentences[hash_sentence_prev]:
                            sentence_prev.matched = True
                            for word_prev in sentence_prev.words:
                                word_prev.matched = True
                                word_prev.used.append(revision_curr.wikipedia_id)

                                if (revision_prev.wikipedia_id not in word_prev.used):
                                    word_prev.freq.append(revision_curr.wikipedia_id)

                                # Revert: reintroducing something that somebody else deleted,
                                # (and was not used in the previous revision)
                                if (revision_prev.wikipedia_id not in word_prev.used):

                                    for elem in word_prev.deleted:
                                        if (elem in revisions.keys()):
                                            if (revisions[elem].contributor_id != revision_curr.contributor_id):
                                                if (elem in relation.revert.keys()):
                                                    relation.revert.update({elem : relation.revert[elem] + 1})
                                                else:
                                                    relation.revert.update({elem : 1})
                                            else:
                                                if (elem in relation.self_revert.keys()):
                                                    relation.self_revert.update({elem : relation.self_revert[elem] + 1})
                                                else:
                                                    relation.self_revert.update({elem : 1})


                                if (revision_prev.wikipedia_id not in word_prev.used):
                                    if (elem in revisions.keys()):
                                        if (revisions[word_prev.revision].contributor_id != revision_curr.contributor_id):
                                            if (word_prev.revision in relation.reintroduced.keys()):
                                                relation.reintroduced.update({word_prev.revision : relation.reintroduced[word_prev.revision] + 1 })
                                            else:
                                                relation.reintroduced.update({word_prev.revision : 1 })
                                        else:
                                            if (word_prev.revision in relation.self_reintroduced.keys()):
                                                relation.self_reintroduced.update({word_prev.revision : relation.self_reintroduced[word_prev.revision] + 1})
                                            else:
                                                relation.self_reintroduced.update({word_prev.revision : 1})

                    addParagraphs(revision_curr, revision_prev, hash_curr, paragraph_prev)
                    break

        # If the paragraph did not match with previous revisions,
        # add to container of unmatched paragraphs for further analysis.
        if (not matched_curr):
            paragraph_curr = Paragraph()
            paragraph_curr.hash_value = Text.calculateHash(paragraph)
            paragraph_curr.value = paragraph

            revision_curr.ordered_paragraphs.append(paragraph_curr.hash_value)

            if (paragraph_curr.hash_value in revision_curr.paragraphs.keys()):
                revision_curr.paragraphs[paragraph_curr.hash_value].append(paragraph_curr)
            else:
                revision_curr.paragraphs.update({paragraph_curr.hash_value : [paragraph_curr]})

            unmatched_paragraphs_curr.append(paragraph_curr)


    # Identify unmatched paragraphs in previous revision for further analysis.
    for paragraph_prev_hash in revision_prev.ordered_paragraphs:
        for paragraph_prev in revision_prev.paragraphs[paragraph_prev_hash]:
            if (not paragraph_prev.matched):
                unmatched_paragraphs_prev.append(paragraph_prev)

    return (unmatched_paragraphs_curr, unmatched_paragraphs_prev, matched_paragraphs_prev)

def addParagraphs(revision_curr, revision_prev, hash_curr, paragraph_prev):
    # Add paragraph to current revision.
    if (hash_curr in revision_curr.paragraphs.keys()):
        revision_curr.paragraphs[paragraph_prev.hash_value].append(paragraph_prev)
        revision_curr.ordered_paragraphs.append(paragraph_prev.hash_value)
    else:
        revision_curr.paragraphs.update({paragraph_prev.hash_value : [paragraph_prev]})
        revision_curr.ordered_paragraphs.append(paragraph_prev.hash_value)

def analyseSentencesInParagraphs(unmatched_paragraphs_curr, unmatched_paragraphs_prev, revision_curr, revision_prev, relation):

    # Containers for unmatched and matched sentences.
    unmatched_sentences_curr = []
    unmatched_sentences_prev = []
    matched_sentences_prev = []
    total_sentences = 0


    # Iterate over the unmatched paragraphs of the current revision.
    for paragraph_curr in unmatched_paragraphs_curr:

        # Split the current paragraph into sentences.
        sentences = Text.splitIntoSentences(paragraph_curr.value)

        # Iterate over the sentences of the current paragraph
        for sentence in sentences:

            # Create the Sentence structure.
            sentence = sentence.strip()
            sentence = ' '.join(Text.splitIntoWords(sentence))
            hash_curr = Text.calculateHash(sentence)
            matched_curr = False
            total_sentences = total_sentences + 1


            # Iterate over the unmatched paragraphs from the previous revision.
            for paragraph_prev in unmatched_paragraphs_prev:
                if (hash_curr in paragraph_prev.sentences.keys()):
                    for sentence_prev in paragraph_prev.sentences[hash_curr]:

                        if (not sentence_prev.matched):

                            matched_one = False
                            matched_all = True
                            for word_prev in sentence_prev.words:

                                if (word_prev.matched):
                                    matched_one = True
                                else:
                                    matched_all = False

                            if not(matched_one):
                                sentence_prev.matched = True
                                matched_curr = True
                                matched_sentences_prev.append(sentence_prev)

                                # TODO: CHECK this
                                for word_prev in sentence_prev.words:
                                    word_prev.matched = True
                                    word_prev.used.append(revision_curr.wikipedia_id)


                                # Add the sentence information to the paragraph.
                                if (hash_curr in paragraph_curr.sentences.keys()):
                                    paragraph_curr.sentences[hash_curr].append(sentence_prev)
                                    paragraph_curr.ordered_sentences.append(sentence_prev.hash_value)
                                else:
                                    paragraph_curr.sentences.update({sentence_prev.hash_value : [sentence_prev]})
                                    paragraph_curr.ordered_sentences.append(sentence_prev.hash_value)
                                break
                            elif (matched_all):

                                sentence_prev.matched = True
                                matched_sentences_prev.append(sentence_prev)

                    if (matched_curr):
                        break


            # Iterate over the hash table of sentences from old revisions.
            if ((not matched_curr) and (hash_curr in sentences_ht.keys())):
                for sentence_prev in sentences_ht[hash_curr]:
                    if (not sentence_prev.matched):
                        matched_one = False
                        matched_all = True
                        for word_prev in sentence_prev.words:
                            if (word_prev.matched):
                                matched_one = True
                            else:
                                matched_all = False

                        if not(matched_one):

                            sentence_prev.matched = True
                            matched_curr = True
                            matched_sentences_prev.append(sentence_prev)

                            # TODO: CHECK this
                            for word_prev in sentence_prev.words:
                                word_prev.matched = True
                                word_prev.used.append(revision_curr.wikipedia_id)

                                if (revision_prev.wikipedia_id not in word_prev.used):
                                    word_prev.freq.append(revision_curr.wikipedia_id)

                                # Revert: reintroducing something that somebody else deleted
                                if (revision_prev.wikipedia_id not in word_prev.used):
                                    for elem in word_prev.deleted:

                                        if (elem in revisions.keys()):
                                            if (revisions[elem].contributor_id != revision_curr.contributor_id):
                                                if (elem in relation.revert.keys()):
                                                    relation.revert.update({elem : relation.revert[elem] + 1})
                                                else:
                                                    relation.revert.update({elem : 1})
                                            else:
                                                if (elem in relation.self_revert.keys()):
                                                    relation.self_revert.update({elem : relation.self_revert[elem] + 1})
                                                else:
                                                    relation.self_revert.update({elem : 1})

                                if (revision_prev.wikipedia_id not in word_prev.used):
                                    if (elem in revisions.keys()):
                                        if (revisions[word_prev.revision].contributor_id != revision_curr.contributor_id):
                                            if (word_prev.revision in relation.reintroduced.keys()):
                                                relation.reintroduced.update({word_prev.revision : relation.reintroduced[word_prev.revision] + 1 })
                                            else:
                                                relation.reintroduced.update({word_prev.revision : 1 })
                                        else:
                                            if (word_prev.revision in relation.self_reintroduced.keys()):
                                                relation.self_reintroduced.update({word_prev.revision : relation.self_reintroduced[word_prev.revision] + 1})
                                            else:
                                                relation.self_reintroduced.update({word_prev.revision : 1})



                            # Add the sentence information to the paragraph.
                            if (hash_curr in paragraph_curr.sentences.keys()):
                                paragraph_curr.sentences[hash_curr].append(sentence_prev)
                                paragraph_curr.ordered_sentences.append(sentence_prev.hash_value)
                            else:
                                paragraph_curr.sentences.update({sentence_prev.hash_value : [sentence_prev]})
                                paragraph_curr.ordered_sentences.append(sentence_prev.hash_value)
                            break
                        elif (matched_all):
                            sentence_prev.matched = True
                            matched_sentences_prev.append(sentence_prev)


            # If the sentence did not match, then include in the container of unmatched sentences for further analysis.
            if (not matched_curr):
                sentence_curr = Sentence()
                sentence_curr.value = sentence
                sentence_curr.hash_value = hash_curr

                paragraph_curr.ordered_sentences.append(sentence_curr.hash_value)
                if (sentence_curr.hash_value in paragraph_curr.sentences.keys()):
                    paragraph_curr.sentences[sentence_curr.hash_value].append(sentence_curr)
                else:
                    paragraph_curr.sentences.update({sentence_curr.hash_value : [sentence_curr]})

                unmatched_sentences_curr.append(sentence_curr)


    # Identify the unmatched sentences in the previous paragraph revision.
    for paragraph_prev in unmatched_paragraphs_prev:
        for sentence_prev_hash in paragraph_prev.ordered_sentences:
            for sentence_prev in paragraph_prev.sentences[sentence_prev_hash]:
                if (not sentence_prev.matched):
                    unmatched_sentences_prev.append(sentence_prev)
                    sentence_prev.matched = True
                    matched_sentences_prev.append(sentence_prev)


    return (unmatched_sentences_curr, unmatched_sentences_prev, matched_sentences_prev, total_sentences)


def analyseWordsInSentences(unmatched_sentences_curr, unmatched_sentences_prev, revision_curr, possible_vandalism, relation):

    matched_words_prev = []
    unmatched_words_prev = []

    # Split sentences into words.
    text_prev = []
    for sentence_prev in unmatched_sentences_prev:
        for word_prev in sentence_prev.words:
            if (not word_prev.matched):
                text_prev.append(word_prev.value)
                unmatched_words_prev.append(word_prev)

    text_curr = []
    for sentence_curr in unmatched_sentences_curr:
        splitted = Text.splitIntoWords(sentence_curr.value)
        text_curr.extend(splitted)
        sentence_curr.splitted.extend(splitted)

    # Edit consists of removing sentences, not adding new content.
    if (len(text_curr) == 0):
        return (matched_words_prev, False)

    # SPAM detection.
    if (possible_vandalism):

        density = Text.computeAvgWordFreq(text_curr, revision_curr.wikipedia_id)

        if (density > WORD_DENSITY):
            return (matched_words_prev, possible_vandalism)
        else:
            possible_vandalism = False

    if (len(text_prev) == 0):
        for sentence_curr in unmatched_sentences_curr:
            for word in sentence_curr.splitted:
                word_curr = Word()
                word_curr.author_id = revision_curr.contributor_id
                word_curr.author_name = revision_curr.contributor_name
                word_curr.revision = revision_curr.wikipedia_id
                word_curr.value = word
                sentence_curr.words.append(word_curr)
                word_curr.used.append(revision_curr.wikipedia_id)
                relation.added = relation.added + 1

        return (matched_words_prev, possible_vandalism)

    d = Differ()
    diff = list(d.compare(text_prev, text_curr))


    for sentence_curr in unmatched_sentences_curr:

        for word in sentence_curr.splitted:
            curr_matched = False
            pos = 0

            while (pos < len(diff)):

                word_diff = diff[pos]

                if (word == word_diff[2:]):

                    if (word_diff[0] == ' '):
                        for word_prev in unmatched_words_prev:
                            if ((not word_prev.matched) and (word_prev.value == word)):
                                word_prev.used.append(revision_curr.wikipedia_id)
                                word_prev.matched = True
                                curr_matched = True
                                sentence_curr.words.append(word_prev)
                                matched_words_prev.append(word_prev)
                                diff[pos] = ''
                                pos = len(diff)+1

                                break

                    elif (word_diff[0] == '-'):
                        for word_prev in unmatched_words_prev:
                            if ((not word_prev.matched) and (word_prev.value == word)):
                                word_prev.matched = True
                                matched_words_prev.append(word_prev)
                                diff[pos] = ''
                                word_prev.deleted.append(revision_curr.wikipedia_id)
                                if (revisions[word_prev.revision].contributor_id != revision_curr.contributor_id):
                                    if (word_prev.revision in relation.deleted.keys()):
                                        relation.deleted.update({word_prev.revision : relation.deleted[word_prev.revision] + 1 })
                                    else:
                                        relation.deleted.update({word_prev.revision : 1 })
                                else:
                                    if (word_prev.revision in relation.self_deleted.keys()):
                                        relation.self_deleted.update({word_prev.revision : relation.self_deleted[word_prev.revision] + 1 })
                                    else:
                                        relation.self_deleted.update({word_prev.revision : 1 })
                                break

                    elif (word_diff[0] == '+'):
                        curr_matched = True
                        word_curr = Word()
                        word_curr.value = word
                        word_curr.author_id = revision_curr.contributor_id
                        word_curr.author_name = revision_curr.contributor_name
                        word_curr.revision = revision_curr.wikipedia_id
                        word_curr.used.append(revision_curr.wikipedia_id)
                        sentence_curr.words.append(word_curr)
                        relation.added = relation.added + 1

                        diff[pos] = ''
                        pos = len(diff)+1

                pos = pos + 1

            if not(curr_matched):
                word_curr = Word()
                word_curr.value = word
                word_curr.author_id = revision_curr.contributor_id
                word_curr.author_name = revision_curr.contributor_name
                word_curr.revision = revision_curr.wikipedia_id
                word_curr.used.append(revision_curr.wikipedia_id)
                sentence_curr.words.append(word_curr)
                relation.added = relation.added + 1

    return (matched_words_prev, possible_vandalism)


def printAllRevisions(order, revisions):

    for (revision, vandalism) in order:
        if not(vandalism):
            printRevision(revisions[revision])


def printRevision(revision):

    print("Printing authorhship for revision: ", revision.wikipedia_id)
    text = []
    authors = []
    for hash_paragraph in revision.ordered_paragraphs:
        para = revision.paragraphs[hash_paragraph]
        paragraph = para[-1]

        for hash_sentence in paragraph.ordered_sentences:
            sentence = paragraph.sentences[hash_sentence][-1]

            for word in sentence.words:
                text.append(word.value)
                authors.append(word.revision)
    print(text)
    print(authors)

def printRevisionTrackAppearance(revision):

    print("Printing authorship for revision: ", revision.wikipedia_id)
    text = []
    authors = []
    for hash_paragraph in revision.ordered_paragraphs:

        p_copy = deepcopy(revision.paragraphs[hash_paragraph])
        paragraph = p_copy.pop(0)

        for hash_sentence in paragraph.ordered_sentences:
            sentence = paragraph.sentences[hash_sentence].pop(0)

            for word in sentence.words:
                appeared = copy(word.used)
                disappeared = copy(word.deleted)

                changes = []
                changes.append("+(" + str(appeared.pop(0))+")")


                while len(disappeared) > 0:

                    d = disappeared.pop(0)

                    if (d > revision.wikipedia_id):
                        break

                    changes.append("-(" + str(d)+")")

                    while len(appeared) > 0:
                        a = appeared.pop(0)
                        if (a > d):
                            changes.append("+(" + str(a)+")")
                            break

                print(word.value + "@@" + str(word.revision)  + "@@" + str(changes))
                text.append(word.value)
                authors.append(word.revision)

def printRelationships(relations, order):

    print("Printing relationships")

    header = ["revision", "author", "deleted(-)", "revert(-)", "reintroduced(+)", "redeleted(+)", "added", "total", "self-deleted", "self-revert", "self-reintroduced", "self-redeleted"]
    print("\t".join(header))

    for (revision, vandalism) in order:
        if (vandalism):
            continue
        relation = relations[revision]
        print(str(relation.revision) + "\t" + (relation.author) + "\t" + str(relation.deleted) + "\t" + str(relation.revert) + "\t" + str(relation.reintroduced)  + "\t" + str(relation.redeleted) + "\t" + str(relation.added)  + "\t"  +  str(relation.total_tokens) + "\t" + str(relation.self_deleted) + "\t" + str(relation.self_revert) + "\t" + str(relation.self_reintroduced) + "\t" + str(relation.self_redeleted))

def printJSON(relations, order):

    deleted_values = {}
    revert_values = {}
    reintroduced_values = {}
    redeleted_values = {}

    for (revision, vandalism) in order:
        if (vandalism):
            continue
        relation = relations[revision]
        print(str(relation.revision) + "\t" + str(relation.author) + "\t" + str(relation.deleted) + "\t" + str(relation.revert) + "\t" + str(relation.reintroduced) + "\t" + str(relation.redeleted) + "\t" + str(relation.added)  + "\t" +  str(relation.total_tokens))



def main(my_argv):
    inputfile = ''
    revision = None
    output = ''

    if (len(my_argv) <= 3):
        try:
            opts, _ = getopt.getopt(my_argv,"i:",["ifile="])
        except getopt.GetoptError:
            print('Usage: Wikiwho.py -i <inputfile> -o <output> [-rev <revision_id>]')
            exit(2)
    else:
        try:
            opts, _ = getopt.getopt(my_argv,"i:o:r:",["ifile=","revision=", "output="])
        except getopt.GetoptError:
            print('Usage: Wikiwho.py -i <inputfile> -o output [-rev <revision_id>]')
            exit(2)

    for opt, arg in opts:
        if opt in ('-h', "--help"):
            print("WikiWho: An algorithm for detecting attribution of authorship in revisioned content")
            print()
            print('Usage: Wikiwho.py -i <inputfile> [-rev <revision_id>]')
            print("-i --ifile File to analyze")
            print("-o --type of output: <a> for authorship, <r> for relations")
            print("-r --revision Revision to analyse. If not specified, the last revision is printed.")
            print("-h --help This help.")
            exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-r", "--revision"):
            revision = arg
        elif opt in ("-o", "--output"):
            output = arg

    return (inputfile,revision,output)

if __name__ == '__main__':

    (file_name, revision, output) = main(argv[1:])

    time1 = time()
    (revisions, order, relations) = analyseArticle(file_name)
    time2 = time()

    if (output == 'r'):
        printRelationships(relations, order)

    if (output == 'a'):
        print("revision", revision)
        if (revision == 'all'):
            printAllRevisions(order, revisions)
        else:
            printRevision(revisions[int(revision)])
