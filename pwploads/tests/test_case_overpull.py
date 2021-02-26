from unittest import TestCase
import pwploads

pipe = {'od': 8,
        'id': 7.2,
        'shoeDepth': 1500,
        'tocMd': 1000,
        'weight': 100,
        'yield': 80000,
        'e': 29e6,
        'top': 500}
df = {'pipe': {'tension': 1.1, 'compression': 1.1, 'burst': 1.1, 'collapse': 1.1, 'triaxial': 1.25},
      'connection': {'tension': 1.0, 'compression': 1.0}}

casing = pwploads.Casing(pipe, factors=df)
casing.add_trajectory('TrajectorySample.xlsx')

casing.overpull(tvd_fluid=[300],    # fluid of 1.2 sg before reaching 300 m depth
                rho_fluid=[1.2, 1.5],
                v_avg=0.3,
                fric=0.24,
                a=1.5,
                f_ov=0)


class TestCasing(TestCase):
    def test_overpull(self):

        self.assertTrue('Overpull' in [load['description'] for load in casing.loads],
                        'Load: Overpull was not included')
