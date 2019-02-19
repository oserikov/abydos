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

"""abydos.tests.distance.test_distance_kuhns_i.

This module contains unit tests for abydos.distance.KuhnsI
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import KuhnsI


class KuhnsITestCases(unittest.TestCase):
    """Test KuhnsI functions.

    abydos.distance.KuhnsI
    """

    cmp = KuhnsI()

    def test_kuhns_i_sim(self):
        """Test abydos.distance.KuhnsI.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 0.0)
        self.assertEqual(self.cmp.sim('a', ''), -6.507705122865472e-06)
        self.assertEqual(self.cmp.sim('', 'a'), -6.507705122865472e-06)
        self.assertEqual(self.cmp.sim('abc', ''), -1.3015410245730944e-05)
        self.assertEqual(self.cmp.sim('', 'abc'), -1.3015410245730944e-05)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 0.010126517045015332)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), -3.2538525614327364e-05)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.0075851391)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.0075851391)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.0075851391)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.0075851391)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.0176319882
        )


if __name__ == '__main__':
    unittest.main()
