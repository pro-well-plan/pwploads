from unittest import TestCase
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
    casing.add_trajectory(r'https://github.com/pro-well-plan/pwploads/raw/master/pwploads/tests/TrajectorySample.xlsx')

    return casing, pipe


class TestCasing(TestCase):
    def test_add_trajectory(self):

        casing, pipe = default_casing_with_trajectory()

        self.assertTrue(casing.trajectory.md[-1] <= pipe['shoeDepth'])
