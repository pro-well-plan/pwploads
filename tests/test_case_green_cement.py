from unittest import TestCase
from test_add_trajectory import default_casing_with_trajectory

casing = default_casing_with_trajectory()

casing.green_cement(tvd_fluid_int=[300],    # fluid of 1.2 sg before reaching 300 m depth
                    rho_fluid_int=[1.2, 1.5],
                    rho_cement=1.8,
                    p_test=4472.65,
                    f_pre=0)


class TestCasing(TestCase):
    def test_green_cement(self):

        self.assertTrue('Green Cement' == casing.csg_loads[0][0], 'Load: Green cement was not included')
        self.assertEqual(len(casing.csg_loads[0][1]), casing.trajectory.cells_no, 'number os points are not equal')
