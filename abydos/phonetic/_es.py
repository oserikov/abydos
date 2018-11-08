# -*- coding: utf-8 -*-

# Copyright 2018 by Christopher C. Little.
# This file is part of Abydos.
#
# Abydos is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Abydos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Abydos. If not, see <http://www.gnu.org/licenses/>.

"""abydos.phonetic._es.

The phonetic._es module implements phonetic algorithms intended for Spanish,
including:

    - Phonetic Spanish
    - Spanish Metaphone
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from unicodedata import normalize as unicode_normalize

from six import text_type

from ._phonetic import Phonetic

__all__ = [
    'PhoneticSpanish',
    'SpanishMetaphone',
    'phonetic_spanish',
    'spanish_metaphone',
]


class PhoneticSpanish(Phonetic):
    """PhoneticSpanish.

    This follows the coding described in :cite:`Amon:2012` and
    :cite:`delPilarAngeles:2015`.
    """

    _trans = dict(
        zip((ord(_) for _ in 'BCDFGHJKLMNPQRSTVXYZ'), '14328287566079431454')
    )

    _uc_set = set('BCDFGHJKLMNPQRSTVXYZ')

    def encode(self, word, max_length=-1):
        """Return the PhoneticSpanish coding of word.

        Args:
            word (str): The word to transform
            max_length (int): The length of the code returned (defaults to
                unlimited)

        Returns:
            str: The PhoneticSpanish code

        Examples:
            >>> pe = PhoneticSpanish()
            >>> pe.encode('Perez')
            '094'
            >>> pe.encode('Martinez')
            '69364'
            >>> pe.encode('Gutierrez')
            '83994'
            >>> pe.encode('Santiago')
            '4638'
            >>> pe.encode('Nicolás')
            '6454'

        """
        # uppercase, normalize, and decompose, filter to A-Z minus vowels & W
        word = unicode_normalize('NFKD', text_type(word.upper()))
        word = ''.join(c for c in word if c in self._uc_set)

        # merge repeated Ls & Rs
        word = word.replace('LL', 'L')
        word = word.replace('R', 'R')

        # apply the Soundex algorithm
        sdx = word.translate(self._trans)

        if max_length > 0:
            sdx = (sdx + ('0' * max_length))[:max_length]

        return sdx


def phonetic_spanish(word, max_length=-1):
    """Return the PhoneticSpanish coding of word.

    This is a wrapper for :py:meth:`PhoneticSpanish.encode`.

    Args:
        word (str): The word to transform
        max_length (int): The length of the code returned (defaults to
            unlimited)

    Returns:
        str: The PhoneticSpanish code

    Examples:
        >>> phonetic_spanish('Perez')
        '094'
        >>> phonetic_spanish('Martinez')
        '69364'
        >>> phonetic_spanish('Gutierrez')
        '83994'
        >>> phonetic_spanish('Santiago')
        '4638'
        >>> phonetic_spanish('Nicolás')
        '6454'

    """
    return PhoneticSpanish().encode(word, max_length)


class SpanishMetaphone(Phonetic):
    """Spanish Metaphone.

    This is a quick rewrite of the Spanish Metaphone Algorithm, as presented at
    https://github.com/amsqr/Spanish-Metaphone and discussed in
    :cite:`Mosquera:2012`.

    Modified version based on :cite:`delPilarAngeles:2016`.
    """

    def encode(self, word, max_length=6, modified=False):
        """Return the Spanish Metaphone of a word.

        Args:
            word (str): The word to transform
            max_length (int): The length of the code returned (defaults to 6)
            modified (bool): Set to True to use del Pilar Angeles &
                Bailón-Miguel's modified version of the algorithm

        Returns:
            str: The Spanish Metaphone code

        Examples:
            >>> pe = SpanishMetaphone()
            >>> pe.encode('Perez')
            'PRZ'
            >>> pe.encode('Martinez')
            'MRTNZ'
            >>> pe.encode('Gutierrez')
            'GTRRZ'
            >>> pe.encode('Santiago')
            'SNTG'
            >>> pe.encode('Nicolás')
            'NKLS'

        """

        def _is_vowel(pos):
            """Return True if the character at word[pos] is a vowel.

            Args:
                pos (int): Position to check for a vowel

            Returns:
                bool: True if word[pos] is a vowel

            """
            return pos < len(word) and word[pos] in {'A', 'E', 'I', 'O', 'U'}

        word = unicode_normalize('NFC', text_type(word.upper()))

        meta_key = ''
        pos = 0

        # do some replacements for the modified version
        if modified:
            word = word.replace('MB', 'NB')
            word = word.replace('MP', 'NP')
            word = word.replace('BS', 'S')
            if word[:2] == 'PS':
                word = word[1:]

        # simple replacements
        word = word.replace('Á', 'A')
        word = word.replace('CH', 'X')
        word = word.replace('Ç', 'S')
        word = word.replace('É', 'E')
        word = word.replace('Í', 'I')
        word = word.replace('Ó', 'O')
        word = word.replace('Ú', 'U')
        word = word.replace('Ñ', 'NY')
        word = word.replace('GÜ', 'W')
        word = word.replace('Ü', 'U')
        word = word.replace('B', 'V')
        word = word.replace('LL', 'Y')

        while len(meta_key) < max_length:
            if pos >= len(word):
                break

            # get the next character
            current_char = word[pos]

            # if a vowel in pos 0, add to key
            if _is_vowel(pos) and pos == 0:
                meta_key += current_char
                pos += 1
            # otherwise, do consonant rules
            else:
                # simple consonants (unmutated)
                if current_char in {
                    'D',
                    'F',
                    'J',
                    'K',
                    'M',
                    'N',
                    'P',
                    'T',
                    'V',
                    'L',
                    'Y',
                }:
                    meta_key += current_char
                    # skip doubled consonants
                    if word[pos + 1 : pos + 2] == current_char:
                        pos += 2
                    else:
                        pos += 1
                else:
                    if current_char == 'C':
                        # special case 'acción', 'reacción',etc.
                        if word[pos + 1 : pos + 2] == 'C':
                            meta_key += 'X'
                            pos += 2
                        # special case 'cesar', 'cien', 'cid', 'conciencia'
                        elif word[pos + 1 : pos + 2] in {'E', 'I'}:
                            meta_key += 'Z'
                            pos += 2
                        # base case
                        else:
                            meta_key += 'K'
                            pos += 1
                    elif current_char == 'G':
                        # special case 'gente', 'ecologia',etc
                        if word[pos + 1 : pos + 2] in {'E', 'I'}:
                            meta_key += 'J'
                            pos += 2
                        # base case
                        else:
                            meta_key += 'G'
                            pos += 1
                    elif current_char == 'H':
                        # since the letter 'H' is silent in Spanish,
                        # set the meta key to the vowel after the letter 'H'
                        if _is_vowel(pos + 1):
                            meta_key += word[pos + 1]
                            pos += 2
                        else:
                            meta_key += 'H'
                            pos += 1
                    elif current_char == 'Q':
                        if word[pos + 1 : pos + 2] == 'U':
                            pos += 2
                        else:
                            pos += 1
                        meta_key += 'K'
                    elif current_char == 'W':
                        meta_key += 'U'
                        pos += 1
                    elif current_char == 'R':
                        meta_key += 'R'
                        pos += 1
                    elif current_char == 'S':
                        if not _is_vowel(pos + 1) and pos == 0:
                            meta_key += 'ES'
                            pos += 1
                        else:
                            meta_key += 'S'
                            pos += 1
                    elif current_char == 'Z':
                        meta_key += 'Z'
                        pos += 1
                    elif current_char == 'X':
                        if (
                            len(word) > 1
                            and pos == 0
                            and not _is_vowel(pos + 1)
                        ):
                            meta_key += 'EX'
                            pos += 1
                        else:
                            meta_key += 'X'
                            pos += 1
                    else:
                        pos += 1

        # Final change from S to Z in modified version
        if modified:
            meta_key = meta_key.replace('S', 'Z')

        return meta_key


def spanish_metaphone(word, max_length=6, modified=False):
    """Return the Spanish Metaphone of a word.

    This is a wrapper for :py:meth:`SpanishMetaphone.encode`.

    Args:
        word (str): The word to transform
        max_length (int): The length of the code returned (defaults to 6)
        modified (bool): Set to True to use del Pilar Angeles &
            Bailón-Miguel's modified version of the algorithm

    Returns:
        str: The Spanish Metaphone code

    Examples:
        >>> spanish_metaphone('Perez')
        'PRZ'
        >>> spanish_metaphone('Martinez')
        'MRTNZ'
        >>> spanish_metaphone('Gutierrez')
        'GTRRZ'
        >>> spanish_metaphone('Santiago')
        'SNTG'
        >>> spanish_metaphone('Nicolás')
        'NKLS'

    """
    return SpanishMetaphone().encode(word, max_length, modified)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
