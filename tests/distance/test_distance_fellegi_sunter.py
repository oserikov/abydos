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

"""abydos.tests.distance.test_distance_fellegi_sunter.

This module contains unit tests for abydos.distance.FellegiSunter
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import FellegiSunter


class FellegiSunterTestCases(unittest.TestCase):
    """Test FellegiSunter functions.

    abydos.distance.FellegiSunter
    """

    cmp = FellegiSunter()

    def test_fellegi_sunter_dist_abs(self):
        """Test abydos.distance.FellegiSunter.dist_abs."""
        # Base cases
        self.assertEqual(self.cmp.dist_abs('', ''), 0.0)
        self.assertEqual(self.cmp.dist_abs('a', ''), 0.0)
        self.assertEqual(self.cmp.dist_abs('', 'a'), 0.0)
        self.assertEqual(self.cmp.dist_abs('abc', ''), 0.0)
        self.assertEqual(self.cmp.dist_abs('', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist_abs('abc', 'abc'), 1.760686675602297)
        self.assertEqual(self.cmp.dist_abs('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(
            self.cmp.dist_abs('Nigel', 'Niall'), 1.3515915598
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Niall', 'Nigel'), 1.3515915598
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Colin', 'Coiln'), 1.3515915598
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Coiln', 'Colin'), 1.3515915598
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('ATCAACGAGT', 'AACGATTAG'), 2.8141447562
        )


if __name__ == '__main__':
    unittest.main()