from unittest import TestCase
import well_profile as wp
import pwploads


def default_casing_with_trajectory():
    csg_od = 8
    csg_id = 7
    length = 1500

    casing = pwploads.Casing(csg_od, csg_id, length,
                             nominal_weight=100,
                             yield_s=80000,
                             df_burst=1.1,
                             df_collapse=1.1,
                             df_tension=1.3,
                             df_compression=1.3,
                             df_vme=1.25)
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
