from unittest import TestCase
import pwploads
import well_profile as wp

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

casing.running(tvd_fluid=[300],     # fluid of 1.2 sg before reaching 300 m depth
               rho_fluid=[1.2, 1.5],
               v_avg=0.3,
               fric=0.24,
               a=1.5)


class TestCasing(TestCase):
    def test_running(self):

        self.assertTrue('Running' == casing.csg_loads[0][0], 'Load: Running was not included')
