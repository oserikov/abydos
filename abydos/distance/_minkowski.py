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

"""abydos.distance.minkowski.

The distance.minkowski module implements Minkowski token-based distances:

    - Minkowski distance & similarity
    - Manhattan distance & similarity
    - Euclidean distance & similarity
    - Chebyshev distance
"""

from __future__ import division, unicode_literals

from numbers import Number

from ._distance import Distance
from ._util import _get_qgrams

__all__ = [
    'Chebyshev',
    'Euclidean',
    'Manhattan',
    'Minkowski',
    'chebyshev',
    'dist_euclidean',
    'dist_manhattan',
    'dist_minkowski',
    'euclidean',
    'manhattan',
    'minkowski',
    'sim_euclidean',
    'sim_manhattan',
    'sim_minkowski',
]


class Minkowski(Distance):
    """Minkowski distance.

    The Minkowski distance :cite:`Minkowski:1910` is a distance metric in
    :math:`L^p-space`.
    """

    def dist_abs(
        self, src, tar, qval=2, pval=1, normalized=False, alphabet=None
    ):
        """Return the Minkowski distance (:math:`L^p-norm`) of two strings.

        :param str src: source string (or QGrams/Counter objects) for
            comparison
        :param str tar: target string (or QGrams/Counter objects) for
            comparison
        :param int qval: the length of each q-gram; 0 for non-q-gram version
        :param int or float pval: the :math:`p`-value of the :math:`L^p`-space.
        :param bool normalized: normalizes to [0, 1] if True
        :param collection or int alphabet: the values or size of the alphabet
        :returns: the Minkowski distance
        :rtype: float

        >>> cmp = Minkowski()
        >>> cmp.dist_abs('cat', 'hat')
        4.0
        >>> cmp.dist_abs('Niall', 'Neil')
        7.0
        >>> cmp.dist_abs('Colin', 'Cuilen')
        9.0
        >>> cmp.dist_abs('ATCG', 'TAGC')
        10.0
        """
        q_src, q_tar = _get_qgrams(src, tar, qval)
        diffs = ((q_src - q_tar) + (q_tar - q_src)).values()

        normalizer = 1
        if normalized:
            totals = (q_src + q_tar).values()
            if alphabet is not None:
                # noinspection PyTypeChecker
                normalizer = (
                    alphabet if isinstance(alphabet, Number) else len(alphabet)
                )
            elif pval == 0:
                normalizer = len(totals)
            else:
                normalizer = sum(_ ** pval for _ in totals) ** (1 / pval)

        if len(diffs) == 0:
            return 0.0
        if pval == float('inf'):
            # Chebyshev distance
            return max(diffs) / normalizer
        if pval == 0:
            # This is the l_0 "norm" as developed by David Donoho
            return len(diffs) / normalizer
        return sum(_ ** pval for _ in diffs) ** (1 / pval) / normalizer

    def dist(self, src, tar, qval=2, pval=1, alphabet=None):
        """Return normalized Minkowski distance of two strings.

        The normalized Minkowski distance :cite:`Minkowski:1910` is a distance
        metric in :math:`L^p-space`, normalized to [0, 1].

        :param str src: source string (or QGrams/Counter objects) for
            comparison
        :param str tar: target string (or QGrams/Counter objects) for
            comparison
        :param int qval: the length of each q-gram; 0 for non-q-gram version
        :param int or float pval: the :math:`p`-value of the :math:`L^p`-space.
        :param collection or int alphabet: the values or size of the alphabet
        :returns: the normalized Minkowski distance
        :rtype: float

        >>> cmp = Minkowski()
        >>> cmp.dist('cat', 'hat')
        0.5
        >>> round(cmp.dist('Niall', 'Neil'), 12)
        0.636363636364
        >>> round(cmp.dist('Colin', 'Cuilen'), 12)
        0.692307692308
        >>> cmp.dist('ATCG', 'TAGC')
        1.0
        """
        return self.dist_abs(src, tar, qval, pval, True, alphabet)


def minkowski(src, tar, qval=2, pval=1, normalized=False, alphabet=None):
    """Return the Minkowski distance (:math:`L^p-norm`) of two strings.

    This is a wrapper for :py:meth:`Minkowski.dist_abs`.

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram version
    :param int or float pval: the :math:`p`-value of the :math:`L^p`-space.
    :param bool normalized: normalizes to [0, 1] if True
    :param collection or int alphabet: the values or size of the alphabet
    :returns: the Minkowski distance
    :rtype: float

    >>> minkowski('cat', 'hat')
    4.0
    >>> minkowski('Niall', 'Neil')
    7.0
    >>> minkowski('Colin', 'Cuilen')
    9.0
    >>> minkowski('ATCG', 'TAGC')
    10.0
    """
    return Minkowski().dist_abs(src, tar, qval, pval, normalized, alphabet)


def dist_minkowski(src, tar, qval=2, pval=1, alphabet=None):
    """Return normalized Minkowski distance of two strings.

    This is a wrapper for :py:meth:`Minkowski.dist`.

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram version
    :param int or float pval: the :math:`p`-value of the :math:`L^p`-space.
    :param collection or int alphabet: the values or size of the alphabet
    :returns: the normalized Minkowski distance
    :rtype: float

    >>> dist_minkowski('cat', 'hat')
    0.5
    >>> round(dist_minkowski('Niall', 'Neil'), 12)
    0.636363636364
    >>> round(dist_minkowski('Colin', 'Cuilen'), 12)
    0.692307692308
    >>> dist_minkowski('ATCG', 'TAGC')
    1.0
    """
    return Minkowski().dist(src, tar, qval, pval, alphabet)


def sim_minkowski(src, tar, qval=2, pval=1, alphabet=None):
    """Return normalized Minkowski similarity of two strings.

    This is a wrapper for :py:meth:`Minkowski.sim`.

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram version
    :param int or float pval: the :math:`p`-value of the :math:`L^p`-space.
    :param collection or int alphabet: the values or size of the alphabet
    :returns: the normalized Minkowski similarity
    :rtype: float

    >>> sim_minkowski('cat', 'hat')
    0.5
    >>> round(sim_minkowski('Niall', 'Neil'), 12)
    0.363636363636
    >>> round(sim_minkowski('Colin', 'Cuilen'), 12)
    0.307692307692
    >>> sim_minkowski('ATCG', 'TAGC')
    0.0
    """
    return Minkowski().sim(src, tar, qval, pval, alphabet)


class Manhattan(Minkowski):
    """Manhattan distance.

    Manhattan distance is the city-block or taxi-cab distance, equivalent
    to Minkowski distance in :math:`L^1`-space.
    """

    def dist_abs(self, src, tar, qval=2, normalized=False, alphabet=None):
        """Return the Manhattan distance between two strings.

        :param str src: source string (or QGrams/Counter objects) for
            comparison
        :param str tar: target string (or QGrams/Counter objects) for
            comparison
        :param int qval: the length of each q-gram; 0 for non-q-gram version
        :param normalized: normalizes to [0, 1] if True
        :param collection or int alphabet: the values or size of the alphabet
        :returns: the Manhattan distance
        :rtype: float

        >>> cmp = Manhattan()
        >>> cmp.dist_abs('cat', 'hat')
        4.0
        >>> cmp.dist_abs('Niall', 'Neil')
        7.0
        >>> cmp.dist_abs('Colin', 'Cuilen')
        9.0
        >>> cmp.dist_abs('ATCG', 'TAGC')
        10.0
        """
        return super(self.__class__, self).dist_abs(
            src, tar, qval, 1, normalized, alphabet
        )

    def dist(self, src, tar, qval=2, alphabet=None):
        """Return the normalized Manhattan distance between two strings.

        The normalized Manhattan distance is a distance metric in
        :math:`L^1-space`, normalized to [0, 1].

        This is identical to Canberra distance.

        :param str src: source string (or QGrams/Counter objects) for
            comparison
        :param str tar: target string (or QGrams/Counter objects) for
            comparison
        :param int qval: the length of each q-gram; 0 for non-q-gram version
        :param collection or int alphabet: the values or size of the alphabet
        :returns: the normalized Manhattan distance
        :rtype: float

        >>> cmp = Manhattan()
        >>> cmp.dist('cat', 'hat')
        0.5
        >>> round(cmp.dist('Niall', 'Neil'), 12)
        0.636363636364
        >>> round(cmp.dist('Colin', 'Cuilen'), 12)
        0.692307692308
        >>> cmp.dist('ATCG', 'TAGC')
        1.0
        """
        return self.dist_abs(src, tar, qval, True, alphabet)


def manhattan(src, tar, qval=2, normalized=False, alphabet=None):
    """Return the Manhattan distance between two strings.

    This is a wrapper for :py:meth:`Manhattan.dist_abs`.

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram version
    :param normalized: normalizes to [0, 1] if True
    :param collection or int alphabet: the values or size of the alphabet
    :returns: the Manhattan distance
    :rtype: float

    >>> manhattan('cat', 'hat')
    4.0
    >>> manhattan('Niall', 'Neil')
    7.0
    >>> manhattan('Colin', 'Cuilen')
    9.0
    >>> manhattan('ATCG', 'TAGC')
    10.0
    """
    return Manhattan().dist_abs(src, tar, qval, normalized, alphabet)


def dist_manhattan(src, tar, qval=2, alphabet=None):
    """Return the normalized Manhattan distance between two strings.

    This is a wrapper for :py:meth:`Manhattan.dist`.

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram version
    :param collection or int alphabet: the values or size of the alphabet
    :returns: the normalized Manhattan distance
    :rtype: float

    >>> dist_manhattan('cat', 'hat')
    0.5
    >>> round(dist_manhattan('Niall', 'Neil'), 12)
    0.636363636364
    >>> round(dist_manhattan('Colin', 'Cuilen'), 12)
    0.692307692308
    >>> dist_manhattan('ATCG', 'TAGC')
    1.0
    """
    return Manhattan().dist(src, tar, qval, alphabet)


def sim_manhattan(src, tar, qval=2, alphabet=None):
    """Return the normalized Manhattan similarity of two strings.

    This is a wrapper for :py:meth:`Manhattan.sim`.

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram version
    :param collection or int alphabet: the values or size of the alphabet
    :returns: the normalized Manhattan similarity
    :rtype: float

    >>> sim_manhattan('cat', 'hat')
    0.5
    >>> round(sim_manhattan('Niall', 'Neil'), 12)
    0.363636363636
    >>> round(sim_manhattan('Colin', 'Cuilen'), 12)
    0.307692307692
    >>> sim_manhattan('ATCG', 'TAGC')
    0.0
    """
    return Manhattan().sim(src, tar, qval, alphabet)


class Euclidean(Minkowski):
    """Euclidean distance.

    Euclidean distance is the straigh-line or as-the-crow-flies distance,
    equivalent to Minkowski distance in :math:`L^2`-space.
    """

    def dist_abs(self, src, tar, qval=2, normalized=False, alphabet=None):
        """Return the Euclidean distance between two strings.

        :param str src: source string (or QGrams/Counter objects) for
            comparison
        :param str tar: target string (or QGrams/Counter objects) for
            comparison
        :param int qval: the length of each q-gram; 0 for non-q-gram version
        :param normalized: normalizes to [0, 1] if True
        :param collection or int alphabet: the values or size of the alphabet
        :returns: the Euclidean distance
        :rtype: float

        >>> cmp = Euclidean()
        >>> cmp.dist_abs('cat', 'hat')
        2.0
        >>> round(cmp.dist_abs('Niall', 'Neil'), 12)
        2.645751311065
        >>> cmp.dist_abs('Colin', 'Cuilen')
        3.0
        >>> round(cmp.dist_abs('ATCG', 'TAGC'), 12)
        3.162277660168
        """
        return super(self.__class__, self).dist_abs(
            src, tar, qval, 2, normalized, alphabet
        )

    def dist(self, src, tar, qval=2, alphabet=None):
        """Return the normalized Euclidean distance between two strings.

        The normalized Euclidean distance is a distance
        metric in :math:`L^2-space`, normalized to [0, 1].

        :param str src: source string (or QGrams/Counter objects) for
            comparison
        :param str tar: target string (or QGrams/Counter objects) for
            comparison
        :param int qval: the length of each q-gram; 0 for non-q-gram version
        :param collection or int alphabet: the values or size of the alphabet
        :returns: the normalized Euclidean distance
        :rtype: float

        >>> cmp = Euclidean()
        >>> round(cmp.dist('cat', 'hat'), 12)
        0.57735026919
        >>> round(cmp.dist('Niall', 'Neil'), 12)
        0.683130051064
        >>> round(cmp.dist('Colin', 'Cuilen'), 12)
        0.727606875109
        >>> cmp.dist('ATCG', 'TAGC')
        1.0
        """
        return self.dist_abs(src, tar, qval, True, alphabet)


def euclidean(src, tar, qval=2, normalized=False, alphabet=None):
    """Return the Euclidean distance between two strings.

    This is a wrapper for :py:meth:`Euclidean.dist_abs`.

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram version
    :param normalized: normalizes to [0, 1] if True
    :param collection or int alphabet: the values or size of the alphabet
    :returns: the Euclidean distance
    :rtype: float

    >>> euclidean('cat', 'hat')
    2.0
    >>> round(euclidean('Niall', 'Neil'), 12)
    2.645751311065
    >>> euclidean('Colin', 'Cuilen')
    3.0
    >>> round(euclidean('ATCG', 'TAGC'), 12)
    3.162277660168
    """
    return Euclidean().dist_abs(src, tar, qval, normalized, alphabet)


def dist_euclidean(src, tar, qval=2, alphabet=None):
    """Return the normalized Euclidean distance between two strings.

    This is a wrapper for :py:meth:`Euclidean.dist`.

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram version
    :param collection or int alphabet: the values or size of the alphabet
    :returns: the normalized Euclidean distance
    :rtype: float

    >>> round(dist_euclidean('cat', 'hat'), 12)
    0.57735026919
    >>> round(dist_euclidean('Niall', 'Neil'), 12)
    0.683130051064
    >>> round(dist_euclidean('Colin', 'Cuilen'), 12)
    0.727606875109
    >>> dist_euclidean('ATCG', 'TAGC')
    1.0
    """
    return Euclidean().dist(src, tar, qval, alphabet)


def sim_euclidean(src, tar, qval=2, alphabet=None):
    """Return the normalized Euclidean similarity of two strings.

    This is a wrapper for :py:meth:`Euclidean.sim`.

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram version
    :param collection or int alphabet: the values or size of the alphabet
    :returns: the normalized Euclidean similarity
    :rtype: float

    >>> round(sim_euclidean('cat', 'hat'), 12)
    0.42264973081
    >>> round(sim_euclidean('Niall', 'Neil'), 12)
    0.316869948936
    >>> round(sim_euclidean('Colin', 'Cuilen'), 12)
    0.272393124891
    >>> sim_euclidean('ATCG', 'TAGC')
    0.0
    """
    return Euclidean().sim(src, tar, qval, alphabet)


class Chebyshev(Minkowski):
    r"""Chebyshev distance.

    Euclidean distance is the chessboard distance,
    equivalent to Minkowski distance in :math:`L^\infty-space`.
    """

    def dist_abs(self, src, tar, qval=2, normalized=False, alphabet=None):
        r"""Return the Chebyshev distance between two strings.

        :param str src: source string (or QGrams/Counter objects) for
            comparison
        :param str tar: target string (or QGrams/Counter objects) for
            comparison
        :param int qval: the length of each q-gram; 0 for non-q-gram version
        :param normalized: normalizes to [0, 1] if True
        :param collection or int alphabet: the values or size of the alphabet
        :returns: the Chebyshev distance
        :rtype: float

        >>> cmp = Chebyshev()
        >>> cmp.dist_abs('cat', 'hat')
        1.0
        >>> cmp.dist_abs('Niall', 'Neil')
        1.0
        >>> cmp.dist_abs('Colin', 'Cuilen')
        1.0
        >>> cmp.dist_abs('ATCG', 'TAGC')
        1.0
        >>> cmp.dist_abs('ATCG', 'TAGC', qval=1)
        0.0
        >>> cmp.dist_abs('ATCGATTCGGAATTTC', 'TAGCATAATCGCCG', qval=1)
        3.0
        """
        return super(self.__class__, self).dist_abs(
            src, tar, qval, float('inf'), normalized, alphabet
        )

    def sim(self):
        raise Exception('Method disabled for Chebyshev distance.')

    def dist(self):
        raise Exception('Method disabled for Chebyshev distance.')


def chebyshev(src, tar, qval=2, normalized=False, alphabet=None):
    r"""Return the Chebyshev distance between two strings.

    This is a wrapper for the :py:meth:`Chebyshev.dist_abs`.

    :param str src: source string (or QGrams/Counter objects) for comparison
    :param str tar: target string (or QGrams/Counter objects) for comparison
    :param int qval: the length of each q-gram; 0 for non-q-gram version
    :param normalized: normalizes to [0, 1] if True
    :param collection or int alphabet: the values or size of the alphabet
    :returns: the Chebyshev distance
    :rtype: float

    >>> chebyshev('cat', 'hat')
    1.0
    >>> chebyshev('Niall', 'Neil')
    1.0
    >>> chebyshev('Colin', 'Cuilen')
    1.0
    >>> chebyshev('ATCG', 'TAGC')
    1.0
    >>> chebyshev('ATCG', 'TAGC', qval=1)
    0.0
    >>> chebyshev('ATCGATTCGGAATTTC', 'TAGCATAATCGCCG', qval=1)
    3.0
    """
    return Chebyshev().dist_abs(src, tar, qval, normalized, alphabet)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
