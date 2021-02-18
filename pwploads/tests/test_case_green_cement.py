from unittest import TestCase
import pwploads
import well_profile as wp

csg_od = 8
csg_id = 7
length = 1500

pipe = {'od': 8,
        'id': 7.2,
        'shoeDepth': 1500,
        'tocMd': 1000,
        'weight': 100,
        'yield': 80000,
        'e': 29e6}
df = {'pipe': {'tension': 1.1, 'compression': 1.1, 'burst': 1.1, 'collapse': 1.1, 'triaxial': 1.25},
      'connection': {'tension': 1.0, 'compression': 1.0}}

casing = pwploads.Casing(pipe, factors=df)
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
