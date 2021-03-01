from unittest import TestCase
import pwploads


def default_casing(grade):
    pipe = {'od': 8,
            'id': 7.2,
            'shoeDepth': 1500,
            'tocMd': 1000,
            'weight': 100,
            'grade': grade,
            'e': 29e6,
            'top': 500}
    df = {'pipe': {'tension': 1, 'compression': 1, 'burst': 1, 'collapse': 1, 'triaxial': 1},
          'connection': {'tension': 1.0, 'compression': 1.0}}

    casing = pwploads.Casing(pipe, factors=df)

    return casing


class TestCasing(TestCase):
    def test_different_yield(self):
        for yield_s in ['X-45', 'X-50', 'X-60', 'X-80', 'X-100', 'X-120']:
            pipe = default_casing(yield_s)
            fig = pipe.plot()
            # fig.show()
