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

"""abydos.distance._fuzzy_tversky.

Fuzzy Tversky index
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._fuzzy_token_distance import _FuzzyTokenDistance

__all__ = ['FuzzyTversky']


class FuzzyTversky(_FuzzyTokenDistance):
    r"""Fuzzy Tversky index.

    The Fuzzy Tversky index, by analogy with :cite:`Wang:2014`,
    for two sets X and Y is:
    :math:`sim_{Fuzzy Tversky}(X, Y) = \frac{|X \widetilde\cap_\delta Y|}
    {|X \widetilde\cap_\delta Y| + \alpha|X - Y| + \beta|Y - X|}`,
    where :math:`|X \widetilde\cap_\delta Y|` is the fuzzy overlap or fuzzy
    intersection. This fuzzy intersection is sum of similarities of all tokens
    in the two sets that are greater than equal to some threshold value
    (:math:`\delta`).

    Unequal α and β will tend to emphasize one or the other set's
    contributions:

        - :math:`\alpha > \beta` emphasizes the contributions of X over Y
        - :math:`\alpha < \beta` emphasizes the contributions of Y over X)

    Parameter values' relation to 1 emphasizes different types of
    contributions:

        - :math:`\alpha` and :math:`\beta > 1` emphsize unique contributions over the
          intersection
        - :math:`\alpha` and :math:`\beta < 1` emphsize the intersection over unique
          contributions

    The symmetric variant is developed by analogy to :cite:`Jiminez:2013`. This
    is activated by specifying a bias parameter.

    The lower bound of Fuzzy Tversky similarity, and the value when
    :math:`\delta = 1.0`, is the Tversky similarity. Tokens shorter than
    :math:`\frac{\delta}{1-\delta}`, 4 in the case of the default threshold
    :math:`\delta = 0.8`, must match exactly to contribute to similarity.

    .. versionadded:: 0.4.0
    """

    def __init__(
        self, alpha=1.0, beta=1.0, bias=None, tokenizer=None, threshold=0.8, metric=None, **kwargs
    ):
        """Initialize FuzzyTversky instance.

        Parameters
        ----------
        alpha : float
            Tversky index parameter as described above
        beta : float
            Tversky index parameter as described above
        bias : float
            The symmetric Tversky index bias parameter
        tokenizer : _Tokenizer
            A tokenizer instance from the abydos.tokenizer package, defaulting
            to the QGrams tokenizer with q=4
        threshold : float
            The minimum similarity for a pair of tokens to contribute to
            similarity
        metric : _Distance
            A distance instance from the abydos.distance package, defaulting
            to normalized Levenshtein similarity
        **kwargs
            Arbitrary keyword arguments

        Other Parameters
        ----------------
        qval : int
            The length of each q-gram. Using this parameter and tokenizer=None
            will cause the instance to use the QGram tokenizer with this
            q value.

        .. versionadded:: 0.4.0

        """
        super(FuzzyTversky, self).__init__(tokenizer=tokenizer, threshold=threshold, metric=metric, **kwargs)
        self.set_params(alpha=alpha, beta=beta, bias=bias)

    def sim(self, src, tar):
        """Return the Fuzzy Tversky index of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Fuzzy Tversky similarity

        Raises
        ------
        ValueError
            Unsupported weight assignment; alpha and beta must be greater than
            or equal to 0.

        Examples
        --------
        >>> cmp = FuzzyTversky()
        >>> cmp.sim('cat', 'hat')
        0.3333333333333333
        >>> cmp.sim('Niall', 'Neil')
        0.2222222222222222
        >>> cmp.sim('aluminum', 'Catalan')
        0.0625
        >>> cmp.sim('ATCG', 'TAGC')
        0.0

        .. versionadded:: 0.4.0

        """
        if self.params['alpha'] < 0 or self.params['beta'] < 0:
            raise ValueError(
                'Unsupported weight assignment; alpha and beta '
                + 'must be greater than or equal to 0.'
            )

        if src == tar:
            return 1.0
        elif not src or not tar:
            return 0.0

        self.tokenize(src, tar)

        q_src_mag = sum(self._src_tokens.values())
        q_tar_mag = sum(self._tar_tokens.values())
        q_intersection_mag = self.fuzzy_intersection()

        if not self._src_tokens or not self._tar_tokens:
            return 0.0

        if self.params['bias'] is None:
            return q_intersection_mag / (
                q_intersection_mag
                + self.params['alpha'] * (q_src_mag - q_intersection_mag)
                + self.params['beta'] * (q_tar_mag - q_intersection_mag)
            )

        a_val = min(
            q_src_mag - q_intersection_mag, q_tar_mag - q_intersection_mag
        )
        b_val = max(
            q_src_mag - q_intersection_mag, q_tar_mag - q_intersection_mag
        )
        c_val = q_intersection_mag + self.params['bias']
        return c_val / (
            self.params['beta']
            * (
                self.params['alpha'] * a_val
                + (1 - self.params['alpha']) * b_val
            )
            + c_val
        )


if __name__ == '__main__':
    import doctest

    doctest.testmod()
