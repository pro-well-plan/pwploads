from unittest import TestCase
from test_add_trajectory import default_casing_with_trajectory

casing = default_casing_with_trajectory()

casing.running(tvd_fluid=[300],     # fluid of 1.2 sg before reaching 300 m depth
               rho_fluid=[1.2, 1.5],
               v_avg=0.3,
               e=32e6,
               fric=0.24,
               a=1.5)


class TestCasing(TestCase):
    def test_green_cement(self):

        self.assertTrue('Running' == casing.csg_loads[0][0], 'Load: Running was not included')
        self.assertEqual(len(casing.csg_loads[0][1]), casing.trajectory.cells_no, 'number os points are not equal')
