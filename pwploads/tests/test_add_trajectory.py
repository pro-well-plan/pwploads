from unittest import TestCase
import well_profile as wp
import pwploads


def default_casing_with_trajectory():
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
    trajectory = wp.get(2000, profile='J', build_angle=20, kop=800, eob=1300)
    casing.add_trajectory(trajectory)

    return casing, pipe


class TestCasing(TestCase):
    def test_add_trajectory(self):

        casing, pipe = default_casing_with_trajectory()

        self.assertTrue(casing.trajectory.md[-1] <= pipe['shoeDepth'])
