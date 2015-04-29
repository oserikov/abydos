# -*- coding: utf-8 -*-
"""abydos.tests.test_corpus

This module contains unit tests for abydos.corpus

Copyright 2014 by Christopher C. Little.
This file is part of Abydos.

Abydos is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Abydos is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Abydos. If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import unicode_literals
import unittest
from abydos.corpus import Corpus

class CorpusTestCases(unittest.TestCase):
    """test cases for abydos.corpus
    """
    def test_corpus(self):
        """test abydos.corpus.Corpus
        """
        # base cases
        self.assertEqual(Corpus().corpus, [])
        self.assertEqual(Corpus('').corpus, [])
        self.assertEqual(Corpus(' ').corpus, [])
        self.assertEqual(Corpus('\n').corpus, [])
        self.assertEqual(Corpus(' \n').corpus, [])
        self.assertEqual(Corpus(' \n ').corpus, [])

        # one document/one sentence
        self.assertEqual(Corpus('a').corpus, [[['a']]])
        self.assertEqual(Corpus('ab ab').corpus, [[['ab', 'ab']]])
        self.assertEqual(Corpus('abc def ghi').corpus,
                         [[['abc', 'def', 'ghi']]])

        # multiple documents (one sentence each)
        self.assertEqual(Corpus('abc\n\ndef ghi').corpus,
                         [[['abc']], [['def', 'ghi']]])
        self.assertEqual(Corpus('abc\n\ndef ghi\n\n').corpus,
                         [[['abc']], [['def', 'ghi']]])
        self.assertEqual(Corpus('\n\nabc\r\n\ndef ghi\n\n').corpus,
                         [[['abc']], [['def', 'ghi']]])

        # one document (multiple sentences each)
        self.assertEqual(Corpus('abc\n def ghi').corpus,
                         [[['abc'], ['def', 'ghi']]])
        self.assertEqual(Corpus('abc\n def ghi\n').corpus,
                         [[['abc'], ['def', 'ghi']]])
        self.assertEqual(Corpus('\nabc\n def ghi\n').corpus,
                         [[['abc'], ['def', 'ghi']]])

        # multiple documents (multiple sentences each)
        self.assertEqual(Corpus('abc\n abc def\n\n\ndef ghi\n jkl\n').corpus,
                         [[['abc'], ['abc', 'def']],
                          [['def', 'ghi'], ['jkl']]])

        # sentence(s) with ignorables
        self.assertEqual(Corpus('abc\nd-ef ghi\n', filter_chars='.-').corpus,
                         [[['abc'], ['def', 'ghi']]])
        self.assertEqual(Corpus('abc\n\n\nd-ef ghi\n\n\n', filter_chars='.-').corpus,
                         [[['abc']], [['def', 'ghi']]])
        self.assertEqual(Corpus('\n\nabc\r\n\ndef ghi.\n\na b c d e f g.\n\n\n',
                                filter_chars='.-').corpus,
                         [[['abc']], [['def', 'ghi']],
                          [['a', 'b', 'c', 'd', 'e', 'f', 'g']]])

        # sentences with stopword removal
        self.assertEqual(Corpus('The quick brown fox jumped over the lazy dog',
                                stop_words=('The', 'the')).corpus,
                          [[['quick', 'brown', 'fox', 'jumped', 'over', 'lazy',
                             'dog']]])
        self.assertEqual(Corpus('a ab abc def',
                                stop_words=('A', 'a')).corpus,
                          [[['ab', 'abc', 'def']]])

        # alternate document divider
        self.assertEqual(Corpus('The quick brown@ fox jumped over@the lazy dog',
                                doc_split='@').corpus,
                          [[['The', 'quick', 'brown']],
                           [['fox', 'jumped', 'over']],
                           [['the', 'lazy', 'dog']]])

        # alternate sentence divider
        self.assertEqual(Corpus('The quick brown$ fox jumped over$the lazy dog',
                                sent_split='$').corpus,
                          [[['The', 'quick', 'brown'],
                            ['fox', 'jumped', 'over'],
                            ['the', 'lazy', 'dog']]])
        self.assertEqual(Corpus('The quick brown$ fox jumped over@the lazy dog',
                                doc_split='@', sent_split='$').corpus,
                          [[['The', 'quick', 'brown'],
                            ['fox', 'jumped', 'over']],
                           [['the', 'lazy', 'dog']]])
        self.assertEqual(Corpus('<BOS> The quick brown <EOS>'+
                                '<BOS> fox jumped over the lazy dog <EOS>',
                                sent_split='<BOS>',
                                stop_words=['<EOS>']).corpus,
                          [[['The', 'quick', 'brown'],
                            ['fox', 'jumped', 'over', 'the', 'lazy', 'dog']]])
        

if __name__ == '__main__':
    unittest.main()
