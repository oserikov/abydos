# -*- coding: utf-8 -*-

# Copyright 2019 by Christopher C. Little.
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

"""abydos.distance._phonetic_edit_distance.

Phonetic edit distance
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from numpy import float as np_float
from numpy import zeros as np_zeros

from six.moves import range

from ._distance import _Distance
from ..phones._phones import _FEATURE_MASK, cmp_features, ipa_to_features

__all__ = ['PhoneticEditDistance']


class PhoneticEditDistance(_Distance):
    """Phonetic edit distance.

    This is a variation on Levenshtein edit distance, intended for strings in
    IPA, that compares individual phones based on their featural similarity.

    .. versionadded:: 0.4.1
    """

    def __init__(
        self,
        mode='lev',
        cost=(0.3, 0.3, 1, 0.1),
        normalizer=max,
        weights=None,
        **kwargs
    ):
        """Initialize PhoneticEditDistance instance.

        Parameters
        ----------
        mode : str
            Specifies a mode for computing the edit distance:

                - ``lev`` (default) computes the ordinary Levenshtein distance,
                  in which edits may include inserts, deletes, and
                  substitutions
                - ``osa`` computes the Optimal String Alignment distance, in
                  which edits may include inserts, deletes, substitutions, and
                  transpositions but substrings may only be edited once

        cost : tuple
            A 4-tuple representing the cost of the four possible edits:
            inserts, deletes, substitutions, and transpositions, respectively
            (by default: (1, 1, 1, 0.1)). Note that transpositions cost a
            relatively low 0.1. If this were 1.0, no phones would ever be
            transposed under the normal weighting, since even quite dissimilar
            phones such as [a] and [p] still agree in nearly 63% of their
            features.
        normalizer : function
            A function that takes an list and computes a normalization term
            by which the edit distance is divided (max by default). Another
            good option is the sum function.
        weights : None or list or tuple or dict
            If None, all features are of equal significance and a simple
            normalized hamming distance of the features is calculated. If a
            list or tuple of numeric values is supplied, the values are
            inferred as the weights for each feature, in order of the features
            listed in abydos.phones._phones._FEATURE_MASK. If a dict is
            supplied, its key values should match keys in
            abydos.phones._phones._FEATURE_MASK to which each weight (value)
            should be assigned. Missing values in all cases are assigned a
            weight of 0 and will be omitted from the comparison.
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.1

        """
        super(PhoneticEditDistance, self).__init__(**kwargs)
        self._mode = mode
        self._cost = cost
        self._normalizer = normalizer

        if weights:
            if isinstance(weights, dict):
                weights = [
                    weights[feature] if feature in weights else 0
                    for feature in sorted(
                        _FEATURE_MASK, key=_FEATURE_MASK.get, reverse=True
                    )
                ]
            elif isinstance(weights, (list, tuple)):
                weights = list(weights) + [0] * (
                    len(_FEATURE_MASK) - len(weights)
                )
        self._weights = weights

    def _alignment_matrix(self, src, tar):
        """Return the phonetic edit distance alignment matrix.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        numpy.ndarray
            The alignment matrix


        .. versionadded:: 0.4.1

        """
        ins_cost, del_cost, sub_cost, trans_cost = self._cost

        src_len = len(src)
        tar_len = len(tar)

        src = ipa_to_features(src)
        tar = ipa_to_features(tar)

        d_mat = np_zeros((src_len + 1, tar_len + 1), dtype=np_float)
        for i in range(src_len + 1):
            d_mat[i, 0] = i * del_cost
        for j in range(tar_len + 1):
            d_mat[0, j] = j * ins_cost

        for i in range(src_len):
            for j in range(tar_len):
                d_mat[i + 1, j + 1] = min(
                    d_mat[i + 1, j] + ins_cost,  # ins
                    d_mat[i, j + 1] + del_cost,  # del
                    d_mat[i, j]
                    + (
                        sub_cost
                        * (1.0 - cmp_features(src[i], tar[i], self._weights))
                        if src[i] != tar[j]
                        else 0
                    ),  # sub/==
                )

                if self._mode == 'osa':
                    if (
                        i + 1 > 1
                        and j + 1 > 1
                        and src[i] == tar[j - 1]
                        and src[i - 1] == tar[j]
                    ):
                        # transposition
                        d_mat[i + 1, j + 1] = min(
                            d_mat[i + 1, j + 1],
                            d_mat[i - 1, j - 1] + trans_cost,
                        )

        return d_mat

    def alignment(self, src, tar):
        """Return the phonetic edit distance alignment of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        tuple
            A tuple containing the phonetic edit distance and the two strings,
            aligned.

        Examples
        --------
        >>> cmp = PhoneticEditDistance()
        >>> cmp.alignment('cat', 'hat')
        (1.0, 'cat', 'hat')
        >>> cmp.alignment('Niall', 'Neil')
        (3.0, 'Niall', 'Neil-')
        >>> cmp.alignment('aluminum', 'Catalan')
        (7.0, '-aluminum', 'Catalan--')
        >>> cmp.alignment('ATCG', 'TAGC')
        (3.0, 'ATCG-', '-TAGC')

        >>> cmp = PhoneticEditDistance(mode='osa')
        >>> cmp.alignment('ATCG', 'TAGC')
        (2.0, 'ATCG', 'TAGC')
        >>> cmp.alignment('ACTG', 'TAGC')
        (4.0, 'ACTG', 'TAGC')


        .. versionadded:: 0.4.1

        """
        d_mat = self._alignment_matrix(src, tar)

        src_aligned = []
        tar_aligned = []

        src_pos = len(src)
        tar_pos = len(tar)

        distance = d_mat[src_pos, tar_pos]

        while src_pos and tar_pos:
            up = d_mat[src_pos, tar_pos - 1]
            left = d_mat[src_pos - 1, tar_pos]
            diag = d_mat[src_pos - 1, tar_pos - 1]
            print(up, left, diag)
            if diag <= min(up, left):
                src_pos -= 1
                tar_pos -= 1
                src_aligned.append(src[src_pos])
                tar_aligned.append(tar[tar_pos])
            elif up <= left:
                tar_pos -= 1
                src_aligned.append('-')
                tar_aligned.append(tar[tar_pos])
            else:
                src_pos -= 1
                src_aligned.append(src[src_pos])
                tar_aligned.append('-')
        while tar_pos:
            tar_pos -= 1
            tar_aligned.append(tar[tar_pos])
            src_aligned.append('-')
        while src_pos:
            src_pos -= 1
            src_aligned.append(src[src_pos])
            tar_aligned.append('-')

        return distance, ''.join(src_aligned[::-1]), ''.join(tar_aligned[::-1])

    def dist_abs(self, src, tar):
        """Return the phonetic edit distance between two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        int (may return a float if cost has float values)
            The phonetic edit distance between src & tar

        Examples
        --------
        >>> cmp = PhoneticEditDistance()
        >>> cmp.dist_abs('cat', 'hat')
        1
        >>> cmp.dist_abs('Niall', 'Neil')
        3
        >>> cmp.dist_abs('aluminum', 'Catalan')
        7
        >>> cmp.dist_abs('ATCG', 'TAGC')
        3

        >>> cmp = PhoneticEditDistance(mode='osa')
        >>> cmp.dist_abs('ATCG', 'TAGC')
        2
        >>> cmp.dist_abs('ACTG', 'TAGC')
        4


        .. versionadded:: 0.4.1

        """
        ins_cost, del_cost, sub_cost, trans_cost = self._cost

        src_len = len(src)
        tar_len = len(tar)

        if src == tar:
            return 0
        if not src:
            return ins_cost * tar_len
        if not tar:
            return del_cost * src_len

        d_mat = self._alignment_matrix(src, tar)

        if int(d_mat[src_len, tar_len]) == d_mat[src_len, tar_len]:
            return int(d_mat[src_len, tar_len])
        else:
            return d_mat[src_len, tar_len]

    def dist(self, src, tar):
        """Return the normalized phonetic edit distance between two strings.

        The edit distance is normalized by dividing the edit distance
        (calculated by either of the two supported methods) by the
        greater of the number of characters in src times the cost of a delete
        and the number of characters in tar times the cost of an insert.
        For the case in which all operations have :math:`cost = 1`, this is
        equivalent to the greater of the length of the two strings src & tar.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            The normalized Levenshtein distance between src & tar

        Examples
        --------
        >>> cmp = PhoneticEditDistance()
        >>> round(cmp.dist('cat', 'hat'), 12)
        0.333333333333
        >>> round(cmp.dist('Niall', 'Neil'), 12)
        0.6
        >>> cmp.dist('aluminum', 'Catalan')
        0.875
        >>> cmp.dist('ATCG', 'TAGC')
        0.75


        .. versionadded:: 0.4.1

        """
        if src == tar:
            return 0.0
        ins_cost, del_cost = self._cost[:2]

        src_len = len(src)
        tar_len = len(tar)

        normalize_term = self._normalizer(
            [src_len * del_cost, tar_len * ins_cost]
        )

        return self.dist_abs(src, tar) / normalize_term


if __name__ == '__main__':
    import doctest

    doctest.testmod()
