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

"""abydos.tests.distance.test_distance_dennis.

This module contains unit tests for abydos.distance.Dennis
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import Dennis


class DennisTestCases(unittest.TestCase):
    """Test Dennis functions.

    abydos.distance.Dennis
    """

    cmp = Dennis()

    def test_dennis_sim(self):
        """Test abydos.distance.Dennis.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), float('nan'))
        self.assertEqual(self.cmp.sim('a', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'a'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', ''), float('nan'))
        self.assertEqual(self.cmp.sim('', 'abc'), float('nan'))
        self.assertEqual(self.cmp.sim('abc', 'abc'), 27.92884359526058)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), -0.17857142857142858)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 13.8128832374)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 13.8128832374)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 13.8128832374)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 13.8128832374)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 18.3981958336
        )


if __name__ == '__main__':
    unittest.main()
