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

"""abydos.distance._euclidean.

Euclidean distance & similarity
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from deprecation import deprecated

from ._minkowski import Minkowski
from .. import __version__

__all__ = ['Euclidean', 'dist_euclidean', 'euclidean', 'sim_euclidean']


class Euclidean(Minkowski):
    """Euclidean distance.

    Euclidean distance is the straigh-line or as-the-crow-flies distance,
    equivalent to Minkowski distance in :math:`L^2`-space.

    .. versionadded:: 0.3.6
    """

    def dist_abs(
        self,
        src,
        tar,
        normalized=False,
        alphabet=None,
        tokenizer=None,
        *args,
        **kwargs
    ):
        """Return the Euclidean distance between two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison
        qval : int
            The length of each q-gram; 0 for non-q-gram version
        normalized : bool
            Normalizes to [0, 1] if True
        alphabet : collection or int
            The values or size of the alphabet

        Returns
        -------
        float
            The Euclidean distance

        Examples
        --------
        >>> cmp = Euclidean()
        >>> cmp.dist_abs('cat', 'hat')
        2.0
        >>> round(cmp.dist_abs('Niall', 'Neil'), 12)
        2.645751311065
        >>> cmp.dist_abs('Colin', 'Cuilen')
        3.0
        >>> round(cmp.dist_abs('ATCG', 'TAGC'), 12)
        3.162277660168

        .. versionadded:: 0.3.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        return super(self.__class__, self).dist_abs(
            src,
            tar,
            pval=2,
            normalized=normalized,
            alphabet=alphabet,
            tokenizer=tokenizer,
            args=args,
            kwargs=kwargs,
        )

    def dist(self, src, tar, alphabet=None, tokenizer=None, *args, **kwargs):
        """Return the normalized Euclidean distance between two strings.

        The normalized Euclidean distance is a distance
        metric in :math:`L^2`-space, normalized to [0, 1].

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison
        qval : int
            The length of each q-gram; 0 for non-q-gram version
        alphabet : collection or int
            The values or size of the alphabet

        Returns
        -------
        float
            The normalized Euclidean distance

        Examples
        --------
        >>> cmp = Euclidean()
        >>> round(cmp.dist('cat', 'hat'), 12)
        0.57735026919
        >>> round(cmp.dist('Niall', 'Neil'), 12)
        0.683130051064
        >>> round(cmp.dist('Colin', 'Cuilen'), 12)
        0.727606875109
        >>> cmp.dist('ATCG', 'TAGC')
        1.0

        .. versionadded:: 0.3.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        return self.dist_abs(
            src,
            tar,
            normalized=True,
            alphabet=alphabet,
            tokenizer=None,
            args=args,
            kwargs=kwargs,
        )


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the Euclidean.dist_abs method instead.',
)
def euclidean(
    src, tar, normalized=False, alphabet=None, tokenizer=None, *args, **kwargs
):
    """Return the Euclidean distance between two strings.

    This is a wrapper for :py:meth:`Euclidean.dist_abs`.

    Parameters
    ----------
    src : str
        Source string (or QGrams/Counter objects) for comparison
    tar : str
        Target string (or QGrams/Counter objects) for comparison
    qval : int
        The length of each q-gram; 0 for non-q-gram version
    normalized : bool
        Normalizes to [0, 1] if True
    alphabet : collection or int
        The values or size of the alphabet

    Returns
    -------
    float: The Euclidean distance

    Examples
    --------
    >>> euclidean('cat', 'hat')
    2.0
    >>> round(euclidean('Niall', 'Neil'), 12)
    2.645751311065
    >>> euclidean('Colin', 'Cuilen')
    3.0
    >>> round(euclidean('ATCG', 'TAGC'), 12)
    3.162277660168

    .. versionadded:: 0.3.0

    """
    return Euclidean().dist_abs(
        src,
        tar,
        normalized=normalized,
        alphabet=alphabet,
        tokenizer=None,
        args=args,
        kwargs=kwargs,
    )


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the Euclidean.dist method instead.',
)
def dist_euclidean(src, tar, alphabet=None, tokenizer=None, *args, **kwargs):
    """Return the normalized Euclidean distance between two strings.

    This is a wrapper for :py:meth:`Euclidean.dist`.

    Parameters
    ----------
    src : str
        Source string (or QGrams/Counter objects) for comparison
    tar : str
        Target string (or QGrams/Counter objects) for comparison
    qval : int
        The length of each q-gram; 0 for non-q-gram version
    alphabet : collection or int
        The values or size of the alphabet

    Returns
    -------
    float
        The normalized Euclidean distance

    Examples
    --------
    >>> round(dist_euclidean('cat', 'hat'), 12)
    0.57735026919
    >>> round(dist_euclidean('Niall', 'Neil'), 12)
    0.683130051064
    >>> round(dist_euclidean('Colin', 'Cuilen'), 12)
    0.727606875109
    >>> dist_euclidean('ATCG', 'TAGC')
    1.0

    .. versionadded:: 0.3.0

    """
    return Euclidean().dist(
        src, tar, alphabet=alphabet, tokenizer=None, args=args, kwargs=kwargs
    )


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the Euclidean.sim method instead.',
)
def sim_euclidean(src, tar, alphabet=None, tokenizer=None, *args, **kwargs):
    """Return the normalized Euclidean similarity of two strings.

    This is a wrapper for :py:meth:`Euclidean.sim`.

    Parameters
    ----------
    src : str
        Source string (or QGrams/Counter objects) for comparison
    tar : str
        Target string (or QGrams/Counter objects) for comparison
    qval : int
        The length of each q-gram; 0 for non-q-gram version
    alphabet : collection or int
        The values or size of the alphabet

    Returns
    -------
    float
        The normalized Euclidean similarity

    Examples
    --------
    >>> round(sim_euclidean('cat', 'hat'), 12)
    0.42264973081
    >>> round(sim_euclidean('Niall', 'Neil'), 12)
    0.316869948936
    >>> round(sim_euclidean('Colin', 'Cuilen'), 12)
    0.272393124891
    >>> sim_euclidean('ATCG', 'TAGC')
    0.0

    .. versionadded:: 0.3.0

    """
    return Euclidean().sim(
        src, tar, alphabet=alphabet, tokenizer=None, args=args, kwargs=kwargs
    )


if __name__ == '__main__':
    import doctest

    doctest.testmod()
