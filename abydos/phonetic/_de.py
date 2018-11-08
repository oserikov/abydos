# -*- coding: utf-8 -*-

# Copyright 2014-2018 by Christopher C. Little.
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

"""abydos.phonetic._de.

The phonetic._de module implements the Kölner Phonetik and related
algorithms for German:

    - Kölner Phonetik
    - Phonem
    - Haase Phonetik
    - Reth-Schek Phonetik
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from itertools import product
from unicodedata import normalize as unicode_normalize

from six import text_type
from six.moves import range

from ._phonetic import Phonetic

__all__ = [
    'Haase',
    'Koelner',
    'Phonem',
    'RethSchek',
    'haase_phonetik',
    'koelner_phonetik',
    'koelner_phonetik_alpha',
    'koelner_phonetik_num_to_alpha',
    'phonem',
    'reth_schek_phonetik',
]


class Koelner(Phonetic):
    """Kölner Phonetik.

    Based on the algorithm defined by :cite:`Postel:1969`.
    """

    _uc_v_set = set('AEIOUJY')

    _num_trans = dict(zip((ord(_) for _ in '012345678'), 'APTFKLNRS'))
    _num_set = set('012345678')

    def encode(self, word):
        """Return the Kölner Phonetik (numeric output) code for a word.

        While the output code is numeric, it is still a str because 0s can lead
        the code.

        Args:
            word (str): The word to transform

        Returns:
            str: The Kölner Phonetik value as a numeric string

        Example:
            >>> pe = Koelner()
            >>> pe.encode('Christopher')
            '478237'
            >>> pe.encode('Niall')
            '65'
            >>> pe.encode('Smith')
            '862'
            >>> pe.encode('Schmidt')
            '862'
            >>> pe.encode('Müller')
            '657'
            >>> pe.encode('Zimmermann')
            '86766'

        """

        def _after(word, pos, letters):
            """Return True if word[pos] follows one of the supplied letters.

            Args:
                word (str): The word to check
                pos (int): Position within word to check
                letters (str): Letters to confirm precede word[pos]

            Returns:
                bool: True if word[pos] follows a value in letters

            """
            return pos > 0 and word[pos - 1] in letters

        def _before(word, pos, letters):
            """Return True if word[pos] precedes one of the supplied letters.

            Args:
                word (str): The word to check
                pos (int): Position within word to check
                letters (str): Letters to confirm follow word[pos]

            Returns:
                bool: True if word[pos] precedes a value in letters

            """
            return pos + 1 < len(word) and word[pos + 1] in letters

        sdx = ''

        word = unicode_normalize('NFKD', text_type(word.upper()))
        word = word.replace('ß', 'SS')

        word = word.replace('Ä', 'AE')
        word = word.replace('Ö', 'OE')
        word = word.replace('Ü', 'UE')
        word = ''.join(c for c in word if c in self._uc_set)

        # Nothing to convert, return base case
        if not word:
            return sdx

        for i in range(len(word)):
            if word[i] in self._uc_v_set:
                sdx += '0'
            elif word[i] == 'B':
                sdx += '1'
            elif word[i] == 'P':
                if _before(word, i, {'H'}):
                    sdx += '3'
                else:
                    sdx += '1'
            elif word[i] in {'D', 'T'}:
                if _before(word, i, {'C', 'S', 'Z'}):
                    sdx += '8'
                else:
                    sdx += '2'
            elif word[i] in {'F', 'V', 'W'}:
                sdx += '3'
            elif word[i] in {'G', 'K', 'Q'}:
                sdx += '4'
            elif word[i] == 'C':
                if _after(word, i, {'S', 'Z'}):
                    sdx += '8'
                elif i == 0:
                    if _before(
                        word, i, {'A', 'H', 'K', 'L', 'O', 'Q', 'R', 'U', 'X'}
                    ):
                        sdx += '4'
                    else:
                        sdx += '8'
                elif _before(word, i, {'A', 'H', 'K', 'O', 'Q', 'U', 'X'}):
                    sdx += '4'
                else:
                    sdx += '8'
            elif word[i] == 'X':
                if _after(word, i, {'C', 'K', 'Q'}):
                    sdx += '8'
                else:
                    sdx += '48'
            elif word[i] == 'L':
                sdx += '5'
            elif word[i] in {'M', 'N'}:
                sdx += '6'
            elif word[i] == 'R':
                sdx += '7'
            elif word[i] in {'S', 'Z'}:
                sdx += '8'

        sdx = self._delete_consecutive_repeats(sdx)

        if sdx:
            sdx = sdx[:1] + sdx[1:].replace('0', '')

        return sdx

    def _to_alpha(self, num):
        """Convert a Kölner Phonetik code from numeric to alphabetic.

        Args:
            num (str or int): A numeric Kölner Phonetik representation

        Returns:
            str: An alphabetic representation of the same word

        Examples:
            >>> pe = Koelner()
            >>> pe._to_alpha('862')
            'SNT'
            >>> pe._to_alpha('657')
            'NLR'
            >>> pe._to_alpha('86766')
            'SNRNN'

        """
        num = ''.join(c for c in text_type(num) if c in self._num_set)
        return num.translate(self._num_trans)

    def encode_alpha(self, word):
        """Return the Kölner Phonetik (alphabetic output) code for a word.

        Args:
            word (str): The word to transform

        Returns:
            str: The Kölner Phonetik value as an alphabetic string

        Examples:
            >>> pe = Koelner()
            >>> pe.encode_alpha('Smith')
            'SNT'
            >>> pe.encode_alpha('Schmidt')
            'SNT'
            >>> pe.encode_alpha('Müller')
            'NLR'
            >>> pe.encode_alpha('Zimmermann')
            'SNRNN'

        """
        return koelner_phonetik_num_to_alpha(koelner_phonetik(word))


def koelner_phonetik(word):
    """Return the Kölner Phonetik (numeric output) code for a word.

    This is a wrapper for :py:meth:`Koelner.encode`.

    Args:
        word (str): The word to transform

    Returns:
        str: The Kölner Phonetik value as a numeric string

    Example:
        >>> koelner_phonetik('Christopher')
        '478237'
        >>> koelner_phonetik('Niall')
        '65'
        >>> koelner_phonetik('Smith')
        '862'
        >>> koelner_phonetik('Schmidt')
        '862'
        >>> koelner_phonetik('Müller')
        '657'
        >>> koelner_phonetik('Zimmermann')
        '86766'

    """
    return Koelner().encode(word)


def koelner_phonetik_num_to_alpha(num):
    """Convert a Kölner Phonetik code from numeric to alphabetic.

    This is a wrapper for :py:meth:`Koelner._to_alpha`.

    Args:
        num (str or int): A numeric Kölner Phonetik representation

    Returns:
        str: An alphabetic representation of the same word

    Examples:
        >>> koelner_phonetik_num_to_alpha('862')
        'SNT'
        >>> koelner_phonetik_num_to_alpha('657')
        'NLR'
        >>> koelner_phonetik_num_to_alpha('86766')
        'SNRNN'

    """
    return Koelner()._to_alpha(num)


def koelner_phonetik_alpha(word):
    """Return the Kölner Phonetik (alphabetic output) code for a word.

    This is a wrapper for :py:meth:`Koelner.encode_alpha`.

    Args:
        word (str): The word to transform

    Returns:
        str: The Kölner Phonetik value as an alphabetic string

    Examples:
        >>> koelner_phonetik_alpha('Smith')
        'SNT'
        >>> koelner_phonetik_alpha('Schmidt')
        'SNT'
        >>> koelner_phonetik_alpha('Müller')
        'NLR'
        >>> koelner_phonetik_alpha('Zimmermann')
        'SNRNN'

    """
    return Koelner().encode_alpha(word)


class Phonem(Phonetic):
    """Phonem.

    Phonem is defined in :cite:`Wilde:1988`.

    This version is based on the Perl implementation documented at
    :cite:`Wilz:2005`.
    It includes some enhancements presented in the Java port at
    :cite:`dcm4che:2011`.

    Phonem is intended chiefly for German names/words.
    """

    _substitutions = (
        ('SC', 'C'),
        ('SZ', 'C'),
        ('CZ', 'C'),
        ('TZ', 'C'),
        ('TS', 'C'),
        ('KS', 'X'),
        ('PF', 'V'),
        ('QU', 'KW'),
        ('PH', 'V'),
        ('UE', 'Y'),
        ('AE', 'E'),
        ('OE', 'Ö'),
        ('EI', 'AY'),
        ('EY', 'AY'),
        ('EU', 'OY'),
        ('AU', 'A§'),
        ('OU', '§'),
    )

    _trans = dict(
        zip(
            (ord(_) for _ in 'ZKGQÇÑßFWPTÁÀÂÃÅÄÆÉÈÊËIJÌÍÎÏÜÝ§ÚÙÛÔÒÓÕØ'),
            'CCCCCNSVVBDAAAAAEEEEEEYYYYYYYYUUUUOOOOÖ',
        )
    )

    _uc_set = set('ABCDLMNORSUVWXYÖ')

    def encode(self, word):
        """Return the Phonem code for a word.

        Args:
            word (str): The word to transform

        Returns:
            str: The Phonem value

        Examples:
            >>> pe = Phonem()
            >>> pe.encode('Christopher')
            'CRYSDOVR'
            >>> pe.encode('Niall')
            'NYAL'
            >>> pe.encode('Smith')
            'SMYD'
            >>> pe.encode('Schmidt')
            'CMYD'

        """
        word = unicode_normalize('NFC', text_type(word.upper()))
        for i, j in self._substitutions:
            word = word.replace(i, j)
        word = word.translate(self._trans)

        return ''.join(
            c
            for c in self._delete_consecutive_repeats(word)
            if c in self._uc_set
        )


def phonem(word):
    """Return the Phonem code for a word.

    This is a wrapper for :py:meth:`Phonem.encode`.

    Args:
        word (str): The word to transform

    Returns:
        str: The Phonem value

    Examples:
        >>> phonem('Christopher')
        'CRYSDOVR'
        >>> phonem('Niall')
        'NYAL'
        >>> phonem('Smith')
        'SMYD'
        >>> phonem('Schmidt')
        'CMYD'

    """
    return Phonem().encode(word)


class Haase(Phonetic):
    """Haase Phonetik.

    Based on the algorithm described at :cite:`Prante:2015`.

    Based on the original :cite:`Haase:2000`.
    """

    _uc_v_set = set('AEIJOUY')

    def encode(self, word, primary_only=False):
        """Return the Haase Phonetik (numeric output) code for a word.

        While the output code is numeric, it is nevertheless a str.

        Args:
            word (str): The word to transform
            primary_only (bool): If True, only the primary code is returned

        Returns:
            tuple: The Haase Phonetik value as a numeric string

        Examples:
            >>> pe = Haase()
            >>> pe.encode('Joachim')
            ('9496',)
            >>> pe.encode('Christoph')
            ('4798293', '8798293')
            >>> pe.encode('Jörg')
            ('974',)
            >>> pe.encode('Smith')
            ('8692',)
            >>> pe.encode('Schmidt')
            ('8692', '4692')

        """

        def _after(word, pos, letters):
            """Return True if word[pos] follows one of the supplied letters.

            Args:
                word (str): Word to modify
                pos (int): Position to examine
                letters (set): Letters to check for

            Returns:
                bool: True if word[pos] follows one of letters

            """
            if pos > 0 and word[pos - 1] in letters:
                return True
            return False

        def _before(word, pos, letters):
            """Return True if word[pos] precedes one of the supplied letters.

            Args:
                word (str): Word to modify
                pos (int): Position to examine
                letters (set): Letters to check for

            Returns:
                bool: True if word[pos] precedes one of letters

            """
            if pos + 1 < len(word) and word[pos + 1] in letters:
                return True
            return False

        word = unicode_normalize('NFKD', text_type(word.upper()))
        word = word.replace('ß', 'SS')

        word = word.replace('Ä', 'AE')
        word = word.replace('Ö', 'OE')
        word = word.replace('Ü', 'UE')
        word = ''.join(c for c in word if c in self._uc_set)

        variants = []
        if primary_only:
            variants = [word]
        else:
            pos = 0
            if word[:2] == 'CH':
                variants.append(('CH', 'SCH'))
                pos += 2
            len_3_vars = {
                'OWN': 'AUN',
                'WSK': 'RSK',
                'SCH': 'CH',
                'GLI': 'LI',
                'AUX': 'O',
                'EUX': 'O',
            }
            while pos < len(word):
                if word[pos : pos + 4] == 'ILLE':
                    variants.append(('ILLE', 'I'))
                    pos += 4
                elif word[pos : pos + 3] in len_3_vars:
                    variants.append(
                        (word[pos : pos + 3], len_3_vars[word[pos : pos + 3]])
                    )
                    pos += 3
                elif word[pos : pos + 2] == 'RB':
                    variants.append(('RB', 'RW'))
                    pos += 2
                elif len(word[pos:]) == 3 and word[pos:] == 'EAU':
                    variants.append(('EAU', 'O'))
                    pos += 3
                elif len(word[pos:]) == 1 and word[pos:] in {'A', 'O'}:
                    if word[pos:] == 'O':
                        variants.append(('O', 'OW'))
                    else:
                        variants.append(('A', 'AR'))
                    pos += 1
                else:
                    variants.append((word[pos],))
                    pos += 1

            variants = [''.join(letters) for letters in product(*variants)]

        def _haase_code(word):
            sdx = ''
            for i in range(len(word)):
                if word[i] in self._uc_v_set:
                    sdx += '9'
                elif word[i] == 'B':
                    sdx += '1'
                elif word[i] == 'P':
                    if _before(word, i, {'H'}):
                        sdx += '3'
                    else:
                        sdx += '1'
                elif word[i] in {'D', 'T'}:
                    if _before(word, i, {'C', 'S', 'Z'}):
                        sdx += '8'
                    else:
                        sdx += '2'
                elif word[i] in {'F', 'V', 'W'}:
                    sdx += '3'
                elif word[i] in {'G', 'K', 'Q'}:
                    sdx += '4'
                elif word[i] == 'C':
                    if _after(word, i, {'S', 'Z'}):
                        sdx += '8'
                    elif i == 0:
                        if _before(
                            word,
                            i,
                            {'A', 'H', 'K', 'L', 'O', 'Q', 'R', 'U', 'X'},
                        ):
                            sdx += '4'
                        else:
                            sdx += '8'
                    elif _before(word, i, {'A', 'H', 'K', 'O', 'Q', 'U', 'X'}):
                        sdx += '4'
                    else:
                        sdx += '8'
                elif word[i] == 'X':
                    if _after(word, i, {'C', 'K', 'Q'}):
                        sdx += '8'
                    else:
                        sdx += '48'
                elif word[i] == 'L':
                    sdx += '5'
                elif word[i] in {'M', 'N'}:
                    sdx += '6'
                elif word[i] == 'R':
                    sdx += '7'
                elif word[i] in {'S', 'Z'}:
                    sdx += '8'

            sdx = self._delete_consecutive_repeats(sdx)

            return sdx

        encoded = tuple(_haase_code(word) for word in variants)
        if len(encoded) > 1:
            encoded_set = set()
            encoded_single = []
            for code in encoded:
                if code not in encoded_set:
                    encoded_set.add(code)
                    encoded_single.append(code)
            return tuple(encoded_single)

        return encoded


def haase_phonetik(word, primary_only=False):
    """Return the Haase Phonetik (numeric output) code for a word.

    This is a wrapper for :py:meth:`Haase.encode`.

    Args:
        word (str): The word to transform
        primary_only (bool): If True, only the primary code is returned

    Returns:
        tuple: The Haase Phonetik value as a numeric string

    Examples:
        >>> haase_phonetik('Joachim')
        ('9496',)
        >>> haase_phonetik('Christoph')
        ('4798293', '8798293')
        >>> haase_phonetik('Jörg')
        ('974',)
        >>> haase_phonetik('Smith')
        ('8692',)
        >>> haase_phonetik('Schmidt')
        ('8692', '4692')

    """
    return Haase().encode(word, primary_only)


class RethSchek(Phonetic):
    """Reth-Schek Phonetik.

    This algorithm is proposed in :cite:`Reth:1977`.

    Since I couldn't secure a copy of that document (maybe I'll look for it
    next time I'm in Germany), this implementation is based on what I could
    glean from the implementations published by German Record Linkage
    Center (www.record-linkage.de):

    - Privacy-preserving Record Linkage (PPRL) (in R) :cite:`Rukasz:2018`
    - Merge ToolBox (in Java) :cite:`Schnell:2004`

    Rules that are unclear:

    - Should 'C' become 'G' or 'Z'? (PPRL has both, 'Z' rule blocked)
    - Should 'CC' become 'G'? (PPRL has blocked 'CK' that may be typo)
    - Should 'TUI' -> 'ZUI' rule exist? (PPRL has rule, but I can't
      think of a German word with '-tui-' in it.)
    - Should we really change 'SCH' -> 'CH' and then 'CH' -> 'SCH'?
    """

    _replacements = {
        3: {
            'AEH': 'E',
            'IEH': 'I',
            'OEH': 'OE',
            'UEH': 'UE',
            'SCH': 'CH',
            'ZIO': 'TIO',
            'TIU': 'TIO',
            'ZIU': 'TIO',
            'CHS': 'X',
            'CKS': 'X',
            'AEU': 'OI',
        },
        2: {
            'LL': 'L',
            'AA': 'A',
            'AH': 'A',
            'BB': 'B',
            'PP': 'B',
            'BP': 'B',
            'PB': 'B',
            'DD': 'D',
            'DT': 'D',
            'TT': 'D',
            'TH': 'D',
            'EE': 'E',
            'EH': 'E',
            'AE': 'E',
            'FF': 'F',
            'PH': 'F',
            'KK': 'K',
            'GG': 'G',
            'GK': 'G',
            'KG': 'G',
            'CK': 'G',
            'CC': 'C',
            'IE': 'I',
            'IH': 'I',
            'MM': 'M',
            'NN': 'N',
            'OO': 'O',
            'OH': 'O',
            'SZ': 'S',
            'UH': 'U',
            'GS': 'X',
            'KS': 'X',
            'TZ': 'Z',
            'AY': 'AI',
            'EI': 'AI',
            'EY': 'AI',
            'EU': 'OI',
            'RR': 'R',
            'SS': 'S',
            'KW': 'QU',
        },
        1: {
            'P': 'B',
            'T': 'D',
            'V': 'F',
            'W': 'F',
            'C': 'G',
            'K': 'G',
            'Y': 'I',
        },
    }

    def encode(self, word):
        """Return Reth-Schek Phonetik code for a word.

        Args:
            word (str): The word to transform

        Returns:
            str: The Reth-Schek Phonetik code

        Examples:
            >>> reth_schek_phonetik('Joachim')
            'JOAGHIM'
            >>> reth_schek_phonetik('Christoph')
            'GHRISDOF'
            >>> reth_schek_phonetik('Jörg')
            'JOERG'
            >>> reth_schek_phonetik('Smith')
            'SMID'
            >>> reth_schek_phonetik('Schmidt')
            'SCHMID'

        """
        # Uppercase
        word = word.upper()

        # Replace umlauts/eszett
        word = word.replace('Ä', 'AE')
        word = word.replace('Ö', 'OE')
        word = word.replace('Ü', 'UE')
        word = word.replace('ß', 'SS')

        # Main loop, using above replacements table
        pos = 0
        while pos < len(word):
            for num in range(3, 0, -1):
                if word[pos : pos + num] in self._replacements[num]:
                    word = (
                        word[:pos]
                        + self._replacements[num][word[pos : pos + num]]
                        + word[pos + num :]
                    )
                    pos += 1
                    break
            else:
                pos += 1  # Advance if nothing is recognized

        # Change 'CH' back(?) to 'SCH'
        word = word.replace('CH', 'SCH')

        # Replace final sequences
        if word[-2:] == 'ER':
            word = word[:-2] + 'R'
        elif word[-2:] == 'EL':
            word = word[:-2] + 'L'
        elif word[-1:] == 'H':
            word = word[:-1]

        return word


def reth_schek_phonetik(word):
    """Return Reth-Schek Phonetik code for a word.

    This is a wrapper for :py:meth:`RethSchek.encode`.

    Args:
        word (str): The word to transform

    Returns:
        str: The Reth-Schek Phonetik code

    Examples:
        >>> reth_schek_phonetik('Joachim')
        'JOAGHIM'
        >>> reth_schek_phonetik('Christoph')
        'GHRISDOF'
        >>> reth_schek_phonetik('Jörg')
        'JOERG'
        >>> reth_schek_phonetik('Smith')
        'SMID'
        >>> reth_schek_phonetik('Schmidt')
        'SCHMID'

    """
    return RethSchek().encode(word)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
