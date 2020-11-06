from unittest import TestCase
import well_profile as wp
from test_create_casing import default_casing


def default_casing_with_trajectory():
    casing = default_casing()
    trajectory = wp.get(2000, profile='J', build_angle=20, kop=800, eob=1300)
    casing.add_trajectory(trajectory)

    return casing


class TestCasing(TestCase):
    def test_add_trajectory(self):

        casing = default_casing_with_trajectory()

        self.assertIsInstance(casing.trajectory.cells_no, int, 'cells_no is not an integer')
        self.assertEqual(len(casing.trajectory.md), casing.trajectory.cells_no,
                         'md has a different number of points')
        self.assertEqual(len(casing.trajectory.tvd), casing.trajectory.cells_no,
                         'tvd has a different number of points')
        self.assertEqual(len(casing.trajectory.inclination), casing.trajectory.cells_no,
                         'incl has different number of points')
