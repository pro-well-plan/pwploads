from unittest import TestCase
import pwploads


def default_casing(yield_s):
    pipe = {'od': 8,
            'id': 7.2,
            'shoeDepth': 1500,
            'tocMd': 1000,
            'weight': 100,
            'yield': yield_s,
            'e': 29e6,
            'top': 500}
    df = {'pipe': {'tension': 1, 'compression': 1, 'burst': 1, 'collapse': 1, 'triaxial': 1},
          'connection': {'tension': 1.0, 'compression': 1.0}}

    casing = pwploads.Casing(pipe, factors=df)

    return casing


class TestCasing(TestCase):
    def test_add_trajectory(self):
        for yield_s in [45000, 50000, 60000, 80000, 100000, 120000]:
            pipe = default_casing(yield_s)
            fig = pipe.plot()
            # fig.show()

