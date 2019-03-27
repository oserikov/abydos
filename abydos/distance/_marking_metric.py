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

"""abydos.distance._marking_metric.

Ehrenfeucht & Haussler's marking metric
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from math import log

from ._marking import Marking

__all__ = ['MarkingMetric']


class MarkingMetric(Marking):
    r"""Ehrenfeucht & Haussler's marking metric.

    This metric :cite:`Ehrenfeucht:1988` is the base 2 logarithm of the product
    of the marking distances between each term plus 1 computed in both orders.
    For strings x and y, this is:

        .. math::

            dist_{MarkingMetric}(x, y) =
            log_2((diff(x, y)+1)(diff(y, x)+1))

    The function diff is Ehrenfeucht & Haussler's marking distance
    :class:`Marking`.

    .. versionadded:: 0.4.0
    """

    def __init__(self, **kwargs):
        """Initialize MarkingMetric instance.

        Parameters
        ----------
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.0

        """
        super(MarkingMetric, self).__init__(**kwargs)

    def dist_abs(self, src, tar):
        """Return the marking distance of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        int
            marking distance

        Examples
        --------
        >>> cmp = MarkingMetric()
        >>> cmp.dist_abs('cat', 'hat')
        0
        >>> cmp.dist_abs('Niall', 'Neil')
        0
        >>> cmp.dist_abs('aluminum', 'Catalan')
        0
        >>> cmp.dist_abs('ATCG', 'TAGC')
        0
        >>> cmp.dist_abs('cbaabdcb', 'abcba')
        2


        .. versionadded:: 0.4.0

        """
        diff1 = super(MarkingMetric, self).dist_abs(src, tar)
        diff2 = super(MarkingMetric, self).dist_abs(tar, src)
        return log((diff1 + 1) * (diff2 + 1), 2)

    def dist(self, src, tar):
        """Return the normalized marking distance of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            marking distance

        Examples
        --------
        >>> cmp = Marking()
        >>> cmp.dist_abs('cat', 'hat')
        0.0
        >>> cmp.dist_abs('Niall', 'Neil')
        0.0
        >>> cmp.dist_abs('aluminum', 'Catalan')
        0.0
        >>> cmp.dist_abs('ATCG', 'TAGC')
        0.0
        >>> cmp.dist_abs('cbaabdcb', 'abcba')
        0.25


        .. versionadded:: 0.4.0

        """
        score = self.dist_abs(src, tar)
        if score:
            return score / log((len(src) + 1) * (len(tar) + 1), 2)
        return 0.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
