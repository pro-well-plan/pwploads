from unittest import TestCase
import pwploads
import well_profile as wp

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

casing.green_cement(tvd_fluid_int=[300],    # fluid of 1.2 sg before reaching 300 m depth
                    rho_fluid_int=[1.2, 1.5],
                    rho_cement=1.8,
                    p_test=4472.65,
                    f_pre=0)


class TestCasing(TestCase):
    def test_green_cement(self):

        self.assertTrue('Green Cement' == casing.csg_loads[0][0], 'Load: Green cement was not included')
        self.assertEqual(len(casing.csg_loads[0][1]), casing.trajectory.cells_no, 'number of points are not equal')